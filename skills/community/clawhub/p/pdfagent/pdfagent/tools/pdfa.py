from __future__ import annotations

from pathlib import Path
import shutil

from ..core.deps import require_bin
from ..core.exec import ExternalCommandError, run_cmd
from ..core.deps import which


def pdf_to_pdfa(
    input_path: Path,
    output_path: Path,
    level: int = 2,
    icc_profile: Path | None = None,
) -> None:
    gs = require_bin("gs", "Install Ghostscript to enable PDF/A conversion")
    if level not in {1, 2, 3}:
        raise ValueError("PDF/A level must be 1, 2, or 3")
    if icc_profile is None:
        raise ValueError("--icc is required for PDF/A conversion")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    icc_path = icc_profile
    if " " in str(icc_profile):
        tmp_icc = output_path.parent / "pdfa_icc.icc"
        try:
            shutil.copy2(icc_profile, tmp_icc)
            icc_path = tmp_icc
        except OSError:
            icc_path = icc_profile

    cmd = [
        gs,
        f"-dPDFA={level}",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=pdfwrite",
        "-sProcessColorModel=DeviceRGB",
        "-sColorConversionStrategy=RGB",
        "-sPDFACompatibilityPolicy=1",
        f"-sOutputFile={output_path}",
        f"-sOutputICCProfile={icc_path}",
        str(input_path),
    ]
    try:
        run_cmd(cmd)
        return
    except ExternalCommandError:
        fallback = _ghostscript_srgb_icc()
        if fallback and Path(fallback) != Path(icc_path):
            cmd = [
                gs,
                f"-dPDFA={level}",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=pdfwrite",
                "-sProcessColorModel=DeviceRGB",
                "-sColorConversionStrategy=RGB",
                "-sPDFACompatibilityPolicy=1",
                f"-sOutputFile={output_path}",
                f"-sOutputICCProfile={fallback}",
                str(input_path),
            ]
            try:
                run_cmd(cmd)
                return
            except ExternalCommandError:
                pass

        ocrmypdf = which("ocrmypdf")
        if ocrmypdf:
            run_cmd(
                [
                    ocrmypdf,
                    "--output-type",
                    f"pdfa-{level}",
                    "--skip-text",
                    str(input_path),
                    str(output_path),
                ]
            )
            return
        raise


def _ghostscript_srgb_icc() -> str | None:
    candidates = [
        "/usr/local/Cellar/ghostscript/10.06.0_1/share/ghostscript/iccprofiles/srgb.icc",
        "/usr/local/share/ghostscript/iccprofiles/srgb.icc",
        "/usr/local/share/ghostscript/iccprofiles/default_rgb.icc",
        "/usr/local/share/ghostscript/10.06.0/iccprofiles/srgb.icc",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None
