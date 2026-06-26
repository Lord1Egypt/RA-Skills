from __future__ import annotations

from pathlib import Path

from ..core.deps import require_bin
from ..core.exec import run_cmd


def repair_pdf(input_path: Path, output_path: Path) -> None:
    gs = require_bin("gs", "Install Ghostscript to enable repair")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]
    run_cmd(cmd)
