# pyright: reportMissingImports=false
from pathlib import Path

from constants import BIN_LIBREOFFICE, BIN_PANDOC
from utils import (
    ensure_output_dir,
    is_binary_available,
    require_file,
    resolve_path,
    run_command,
)


def convert_document(input_str: str, output_str: str) -> dict:
    """Convert a document between formats using pandoc or libreoffice."""
    input_path = resolve_path(input_str)
    err = require_file(input_path)
    if err:
        return {"error": err}

    output = resolve_path(output_str)
    err = ensure_output_dir(output)
    if err:
        return {"error": err}

    in_ext = input_path.suffix.lower()
    out_ext = output.suffix.lower()

    # Try pandoc first for text-based formats
    if is_binary_available(BIN_PANDOC):
        rc, _, stderr = run_command(
            [
                BIN_PANDOC,
                str(input_path),
                "-o",
                str(output),
            ]
        )
        if rc == 0:
            return {
                "input": str(input_path),
                "output": str(output),
                "converter": "pandoc",
            }
        # Pandoc failed — fall through to libreoffice
        pandoc_err = stderr.strip()
    else:
        pandoc_err = None

    # Try libreoffice
    if is_binary_available(BIN_LIBREOFFICE):
        rc, _, stderr = run_command(
            [
                BIN_LIBREOFFICE,
                "--headless",
                "--convert-to",
                out_ext.lstrip("."),
                "--outdir",
                str(output.parent),
                str(input_path),
            ],
            timeout=120,
        )
        if rc == 0:
            # libreoffice writes to input filename stem + out_ext in outdir
            lo_output = output.parent / (input_path.stem + out_ext)
            if lo_output.exists() and lo_output != output:
                lo_output.rename(output)
            return {
                "input": str(input_path),
                "output": str(output),
                "converter": "libreoffice",
            }
        lo_err = stderr.strip()
    else:
        lo_err = None

    # Both failed or unavailable
    if pandoc_err is None and lo_err is None:
        return {
            "error": (
                "No document converter found. Install one:\n"
                "  pandoc:      brew install pandoc  /  apt install pandoc\n"
                "  libreoffice: brew install --cask libreoffice  /  apt install libreoffice"
            )
        }

    msg_parts = []
    if pandoc_err is not None:
        msg_parts.append(f"pandoc: {pandoc_err or 'failed'}")
    if lo_err is not None:
        msg_parts.append(f"libreoffice: {lo_err or 'failed'}")
    return {"error": "Conversion failed.\n" + "\n".join(msg_parts)}
