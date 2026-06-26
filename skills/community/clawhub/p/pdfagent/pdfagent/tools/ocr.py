from __future__ import annotations

from pathlib import Path

from ..core.deps import require_bin
from ..core.exec import run_cmd


def ocr_pdf(
    input_path: Path,
    output_path: Path,
    languages: str = "eng",
    deskew: bool = False,
    force: bool = False,
) -> None:
    ocrmypdf = require_bin("ocrmypdf", "Install ocrmypdf to enable OCR")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [ocrmypdf, "-l", languages]
    if deskew:
        cmd.append("--deskew")
    if force:
        cmd.append("--force-ocr")
    cmd.extend([str(input_path), str(output_path)])

    run_cmd(cmd)
