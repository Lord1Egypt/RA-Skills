#!/usr/bin/env python3
"""Create a local-only manifest for user-provided fingered score PDFs.

The manifest records source identity without copying score content.  Entries
start as diagnostic: they cannot affect published accuracy until a separately
saved comparison and visual audit make them eligible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


def parse_input(raw: str) -> tuple[str, Path]:
    identifier, separator, filename = raw.partition("=")
    if not separator or not identifier.strip() or not filename.strip():
        raise argparse.ArgumentTypeError("each --input must use ID=/absolute/or/relative/file.pdf")
    path = Path(filename).expanduser().resolve()
    if path.suffix.lower() != ".pdf":
        raise argparse.ArgumentTypeError(f"{path}: expected a PDF")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{path}: file not found")
    return identifier.strip(), path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def local_pdf_page_count(path: Path) -> int | None:
    """Read a page count only from an already-installed common PDF utility.

    Benchmark creation must remain local and dependency-free. ``pdfinfo`` is
    optional: a missing tool leaves the entry diagnostic rather than guessing
    a page count from PDF internals.
    """
    executable = shutil.which("pdfinfo")
    if not executable:
        return None
    try:
        result = subprocess.run(
            [executable, str(path)], capture_output=True, text=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode:
        return None
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, flags=re.MULTILINE)
    return int(match.group(1)) if match and int(match.group(1)) > 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", action="append", required=True, type=parse_input, metavar="ID=PDF",
        help="local reference score; repeated once per piece",
    )
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--grade-band", default="user-declared<=5")
    parser.add_argument(
        "--holdout", action="append", default=[], metavar="ID",
        help="freeze this input ID as a holdout piece; all other IDs become development pieces",
    )
    args = parser.parse_args()

    holdout_ids = {str(value).strip() for value in args.holdout if str(value).strip()}
    input_ids = {identifier for identifier, _ in args.input}
    unknown_holdouts = holdout_ids - input_ids
    if unknown_holdouts:
        raise ValueError(f"unknown --holdout IDs: {sorted(unknown_holdouts)}")
    if holdout_ids and holdout_ids == input_ids:
        raise ValueError("holdout split needs at least one development piece")

    seen: set[str] = set()
    pieces: list[dict[str, object]] = []
    for identifier, path in args.input:
        if identifier in seen:
            raise ValueError(f"duplicate piece ID: {identifier}")
        seen.add(identifier)
        page_count = local_pdf_page_count(path)
        source = {
            "type": "pdf",
            "path": str(path),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "page_count": page_count,
        }
        pieces.append({
            "id": identifier,
            "benchmark_role": (
                "holdout" if identifier in holdout_ids else
                "development" if holdout_ids else "unassigned"
            ),
            "grade_band": args.grade_band,
            "source": source,
            "source_page_count_status": "local-pdfinfo" if page_count else "needs-manual-confirmation",
            "reference_annotation": "editorial fingering visible on source; not yet transcribed",
            "fingering_status": "diagnostic",
            "visual_status": "diagnostic",
        })

    payload = {
        "manifest_kind": "private-local-fingering-benchmark",
        "handling": "local-only; do not publish, upload, or commit source PDFs",
        "eligibility_rule": "An entry remains diagnostic until a same-source editorial comparison and all required visual audits are attached.",
        "split_rule": (
            "Frozen development/holdout split; holdout answers must not guide rule changes."
            if holdout_ids else
            "No split declared; add --holdout before using this manifest for a completion claim."
        ),
        "pieces": pieces,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output} with {len(pieces)} diagnostic entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
