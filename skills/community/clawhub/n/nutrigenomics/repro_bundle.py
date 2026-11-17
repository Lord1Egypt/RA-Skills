"""
repro_bundle.py — Creates reproducibility artefacts for Nutrigenomics
Outputs: README_reproducibility.txt, environment.yml, checksums.txt, provenance.json

Privacy note
------------
This module deliberately avoids storing any information that could identify the
person whose genetic data was analysed:

  - The input file path and name are NOT written to any artefact.
  - The input file is NOT checksummed (a SHA-256 hash of a genetic file is a
    stable fingerprint that could be used to re-identify a specific dataset).
  - Only the SNP panel and the generated output report are checksummed, so users
    can verify that the panel definition and report have not been altered.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from path_safety import safe_write_text


CONDA_ENV = """name: nutrigenomics
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pandas>=2.2,<3.0
  - numpy>=1.26,<3.0
  - matplotlib>=3.8,<4.0
  - seaborn>=0.13,<1.0
"""


def _skill_version() -> str:
    """Read the skill version from openclaw.json so artefacts cannot drift from
    the release. Returns "unknown" rather than raising if the file is absent."""
    try:
        meta = json.loads((Path(__file__).parent / "openclaw.json").read_text(encoding="utf-8"))
        version = meta.get("version")
        return version if isinstance(version, str) and version else "unknown"
    except Exception:
        return "unknown"


def sha256_file(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file, or a sentinel if not found."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return "FILE_NOT_FOUND"


def create_reproducibility_bundle(
    input_file: str,
    output_dir: str,
    panel_path: str,
    args: dict,
) -> None:
    """
    Write reproducibility artefacts to output_dir.

    Artefacts written:
      README_reproducibility.txt  — step-by-step instructions to reproduce
      environment.yml             — pinned conda environment
      checksums.txt               — SHA-256 of panel + output report only
      provenance.json             — version, timestamp, and format args

    The input file is intentionally excluded from all artefacts to avoid
    persisting any identifier or fingerprint of the user's genetic data.
    """
    output_dir = Path(output_dir).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ── Allowlist of non-identifying arguments ────────────────────────────────
    # NEVER echo the raw argument namespace into an artefact. It carries --input,
    # --output and --panel, whose paths can identify a person or a machine. Both
    # artefacts below previously did exactly that while claiming the opposite.
    SAFE_ARG_KEYS = ("format", "no_figures")
    safe_args = {k: args[k] for k in SAFE_ARG_KEYS if k in args}
    safe_args["custom_panel"] = bool(args.get("panel"))

    # ── README_reproducibility.txt ────────────────────────────────────────────
    cmd_args = " ".join(
        f"--{k.replace('_', '-')}" if isinstance(v, bool) else f"--{k.replace('_', '-')} {v}"
        for k, v in safe_args.items()
        if v and k != "custom_panel"
    )
    instructions = f"""Nutrigenomics reproducibility notes
Generated: {timestamp}
Version: {_skill_version()}

This skill does not generate executable scripts. To reproduce the analysis manually:
1. Install the conda environment:
       conda env create -f environment.yml
       conda activate nutrigenomics
2. Run the analysis on your original input file:
       python nutrigenomics.py --input <your_genetic_file> {cmd_args}
3. Verify the output report and SNP panel with checksums.txt:
       sha256sum -c checksums.txt

Privacy note:
- The input file name and path are NOT stored in any artefact.
- The input file is NOT checksummed to avoid creating a persistent fingerprint
  of the user's genetic data.
- Only the SNP panel definition and the generated report are checksummed.
- Output files in this directory persist until manually deleted.
"""
    safe_write_text(output_dir / "README_reproducibility.txt", instructions)

    # ── environment.yml ───────────────────────────────────────────────────────
    safe_write_text(output_dir / "environment.yml", CONDA_ENV)

    # ── checksums.txt — output files only, no input fingerprint ──────────────
    # Intentionally excludes the input file to avoid storing a hash that could
    # serve as a stable identifier of the user's genetic dataset.
    files_to_checksum = [
        (panel_path, "snp_panel.json (reference)"),
        (str(output_dir / "nutrigenomics_report.md"), "nutrigenomics_report.md"),
    ]
    checksum_lines = [
        f"# Nutrigenomics output checksums — {timestamp}",
        "# Note: the input genetic file is intentionally not checksummed.",
    ]
    for fp, label in files_to_checksum:
        chk = sha256_file(fp)
        checksum_lines.append(f"{chk}  {label}")

    safe_write_text(output_dir / "checksums.txt", "\n".join(checksum_lines) + "\n")

    # ── provenance.json — no input filename or path ───────────────────────────
    # Only an explicit allowlist of non-identifying arguments is recorded. This
    # used to pass vars(args) straight through, which wrote the absolute path of
    # the user's genetic data file into the artefact while the privacy_note below
    # claimed the opposite. Never widen this to the full argument namespace: the
    # paths in it (--input, --output, --panel) can identify a person or a machine.
    provenance = {
        "tool": "Nutrigenomics",
        "version": _skill_version(),
        "timestamp": timestamp,
        "format_args": safe_args,
        "privacy_note": (
            "Input file name and path are not recorded. "
            "Only output files are checksummed."
        ),
    }
    safe_write_text(output_dir / "provenance.json", json.dumps(provenance, indent=2))
