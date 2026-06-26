from __future__ import annotations

from pathlib import Path

from ..core.deps import require_bin
from ..core.exec import run_cmd


def unlock_pdf(input_path: Path, output_path: Path, password: str) -> None:
    qpdf = require_bin("qpdf", "Install qpdf to enable unlock")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [qpdf, f"--password={password}", "--decrypt", str(input_path), str(output_path)]
    run_cmd(cmd)


def protect_pdf(
    input_path: Path,
    output_path: Path,
    user_password: str,
    owner_password: str | None = None,
    allow_print: bool = False,
    allow_copy: bool = False,
    allow_modify: bool = False,
) -> None:
    qpdf = require_bin("qpdf", "Install qpdf to enable protect")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    owner = owner_password or user_password
    perms = []
    if allow_print:
        perms.append("--print=full")
    else:
        perms.append("--print=none")
    if allow_copy:
        perms.append("--extract=y")
    else:
        perms.append("--extract=n")
    if allow_modify:
        perms.append("--modify=all")
    else:
        perms.append("--modify=none")

    cmd = [
        qpdf,
        "--encrypt",
        user_password,
        owner,
        "256",
        *perms,
        "--",
        str(input_path),
        str(output_path),
    ]
    run_cmd(cmd)
