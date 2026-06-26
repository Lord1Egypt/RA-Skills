from __future__ import annotations

from pathlib import Path

from ..core.deps import require_bin
from ..core.exec import run_cmd
from pypdf import PdfReader, PdfWriter


_PRESET_MAP = {
    "screen": "/screen",
    "ebook": "/ebook",
    "printer": "/printer",
    "prepress": "/prepress",
}


def compress_pdf(
    input_path: Path,
    output_path: Path,
    preset: str = "screen",
    remove_metadata: bool = False,
) -> None:
    gs = require_bin("gs", "Install Ghostscript to enable compression")
    setting = _PRESET_MAP.get(preset.lower())
    if not setting:
        raise ValueError(f"Invalid preset: {preset}. Use one of {', '.join(_PRESET_MAP)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        f"-dPDFSETTINGS={setting}",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]
    run_cmd(cmd)

    if remove_metadata:
        _strip_metadata(output_path)


def _strip_metadata(path: Path) -> None:
    reader = PdfReader(str(path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    with path.open("wb") as f:
        writer.write(f)
