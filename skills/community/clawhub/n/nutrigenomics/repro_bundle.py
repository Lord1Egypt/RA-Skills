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


CONDA_ENV = """name: nutrigenomics
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy>=1.26
  - pandas>=2.2
  - matplotlib>=3.8
  - seaborn>=0.13
  - pip
  - pip:
    - reportlab>=4.0
"""


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

    # ── README_reproducibility.txt ────────────────────────────────────────────
    cmd_args = " ".join(
        f"--{k.replace('_', '-')} {v}"
        for k, v in args.items()
        if v and k != "synthetic"
    )
    instructions = f"""Nutrigenomics reproducibility notes
Generated: {timestamp}
Version: 0.2.8

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
    (output_dir / "README_reproducibility.txt").write_text(instructions, encoding="utf-8")

    # ── environment.yml ───────────────────────────────────────────────────────
    (output_dir / "environment.yml").write_text(CONDA_ENV, encoding="utf-8")

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

    (output_dir / "checksums.txt").write_text(
        "\n".join(checksum_lines) + "\n", encoding="utf-8"
    )

    # ── provenance.json — no input filename or path ───────────────────────────
    # The input_file field is deliberately omitted. Storing the filename risks
    # persisting a personally identifiable label (e.g. "john_smith_genome.csv").
    provenance = {
        "tool": "Nutrigenomics",
        "version": "0.2.8",
        "timestamp": timestamp,
        "format_args": args,
        "privacy_note": (
            "Input file name and path are not recorded. "
            "Only output files are checksummed."
        ),
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )
