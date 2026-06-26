#!/usr/bin/env python3
"""
Cross-Reference Audit Script for Multi-Agent LaTeX Reports.

When multiple agents write chapters in parallel, duplicate labels,
undefined references, and inconsistent cross-references are inevitable.
This script catches them all before compilation.

Usage:
    python cross_ref_audit.py path/to/report/
    python cross_ref_audit.py path/to/report/ --fix-prefix
    python cross_ref_audit.py path/to/report/ --verbose
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class AuditResult:
    duplicate_labels: dict[str, list[str]] = field(default_factory=dict)
    undefined_refs: dict[str, list[str]] = field(default_factory=dict)
    undefined_cites: dict[str, list[str]] = field(default_factory=dict)
    orphaned_labels: list[str] = field(default_factory=list)
    bib_duplicates: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(
            self.duplicate_labels
            or self.undefined_refs
            or self.undefined_cites
            or self.bib_duplicates
        )

    @property
    def error_count(self) -> int:
        return (
            len(self.duplicate_labels)
            + len(self.undefined_refs)
            + len(self.undefined_cites)
            + len(self.bib_duplicates)
        )


def find_tex_files(directory: Path) -> list[Path]:
    """Find all .tex files recursively."""
    return sorted(directory.rglob("*.tex"))


def find_bib_files(directory: Path) -> list[Path]:
    """Find all .bib files recursively."""
    return sorted(directory.rglob("*.bib"))


def extract_labels(filepath: Path) -> list[tuple[str, int]]:
    """Extract all \\label{} definitions with line numbers."""
    labels = []
    label_pattern = re.compile(r"\\label\{([^}]+)\}")
    content = filepath.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("%"):
            continue
        for match in label_pattern.finditer(line):
            labels.append((match.group(1), i))
    return labels


def extract_refs(filepath: Path) -> list[tuple[str, int]]:
    """Extract all \\ref{}, \\cref{}, \\Cref{}, \\autoref{} references."""
    refs = []
    ref_pattern = re.compile(
        r"\\(?:c?ref|C?ref|autoref|eqref|pageref)\{([^}]+)\}"
    )
    content = filepath.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("%"):
            continue
        for match in ref_pattern.finditer(line):
            # Handle comma-separated refs like \cref{fig:a,fig:b}
            for ref in match.group(1).split(","):
                refs.append((ref.strip(), i))
    return refs


def extract_cites(filepath: Path) -> list[tuple[str, int]]:
    """Extract all \\cite{}, \\citep{}, \\citet{} etc."""
    cites = []
    cite_pattern = re.compile(
        r"\\(?:cite[tp]?|citealp|citeauthor|citeyear)\{([^}]+)\}"
    )
    content = filepath.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith("%"):
            continue
        for match in cite_pattern.finditer(line):
            for key in match.group(1).split(","):
                cites.append((key.strip(), i))
    return cites


def extract_bib_keys(filepath: Path) -> list[tuple[str, int]]:
    """Extract all BibTeX entry keys."""
    keys = []
    entry_pattern = re.compile(r"@\w+\{([^,\s]+)")
    content = filepath.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(content.splitlines(), 1):
        for match in entry_pattern.finditer(line):
            keys.append((match.group(1), i))
    return keys


def audit(directory: Path, verbose: bool = False) -> AuditResult:
    """Run full cross-reference audit on a LaTeX project directory."""
    result = AuditResult()

    tex_files = find_tex_files(directory)
    bib_files = find_bib_files(directory)

    if not tex_files:
        result.warnings.append(f"No .tex files found in {directory}")
        return result

    if verbose:
        print(f"Scanning {len(tex_files)} .tex files, {len(bib_files)} .bib files")

    # Collect all labels, refs, cites
    all_labels: dict[str, list[str]] = defaultdict(list)
    all_refs: dict[str, list[str]] = defaultdict(list)
    all_cites: dict[str, list[str]] = defaultdict(list)
    all_bib_keys: dict[str, list[str]] = defaultdict(list)

    for f in tex_files:
        relpath = str(f.relative_to(directory))

        for label, line in extract_labels(f):
            all_labels[label].append(f"{relpath}:{line}")

        for ref, line in extract_refs(f):
            all_refs[ref].append(f"{relpath}:{line}")

        for cite, line in extract_cites(f):
            all_cites[cite].append(f"{relpath}:{line}")

    for f in bib_files:
        relpath = str(f.relative_to(directory))
        for key, line in extract_bib_keys(f):
            all_bib_keys[key].append(f"{relpath}:{line}")

    # Check 1: Duplicate labels
    for label, locations in all_labels.items():
        if len(locations) > 1:
            result.duplicate_labels[label] = locations

    # Check 2: Undefined references
    defined_labels = set(all_labels.keys())
    for ref, locations in all_refs.items():
        if ref not in defined_labels:
            result.undefined_refs[ref] = locations

    # Check 3: Undefined citations
    defined_bib_keys = set(all_bib_keys.keys())
    for cite, locations in all_cites.items():
        if cite not in defined_bib_keys:
            result.undefined_cites[cite] = locations

    # Check 4: Orphaned labels (defined but never referenced)
    referenced_labels = set(all_refs.keys())
    for label in defined_labels:
        if label not in referenced_labels:
            result.orphaned_labels.append(label)

    # Check 5: Duplicate BibTeX keys
    for key, locations in all_bib_keys.items():
        if len(locations) > 1:
            result.bib_duplicates.append(f"{key} defined at: {', '.join(locations)}")

    # Warnings: labels without chapter prefix
    for label in defined_labels:
        if ":" not in label:
            result.warnings.append(
                f"Label '{label}' has no prefix — consider using ch1:, fig:ch3:, etc."
            )

    return result


def print_report(result: AuditResult) -> None:
    """Print a formatted audit report."""
    print("\n" + "=" * 60)
    print("  CROSS-REFERENCE AUDIT REPORT")
    print("=" * 60)

    if not result.has_errors and not result.orphaned_labels and not result.warnings:
        print("\n  All clear — no issues found.\n")
        return

    # Errors
    if result.duplicate_labels:
        print(f"\n  DUPLICATE LABELS ({len(result.duplicate_labels)})")
        print("  " + "-" * 40)
        for label, locations in sorted(result.duplicate_labels.items()):
            print(f"  \\label{{{label}}}")
            for loc in locations:
                print(f"    -> {loc}")

    if result.undefined_refs:
        print(f"\n  UNDEFINED REFERENCES ({len(result.undefined_refs)})")
        print("  " + "-" * 40)
        for ref, locations in sorted(result.undefined_refs.items()):
            print(f"  \\ref{{{ref}}}")
            for loc in locations:
                print(f"    -> {loc}")

    if result.undefined_cites:
        print(f"\n  UNDEFINED CITATIONS ({len(result.undefined_cites)})")
        print("  " + "-" * 40)
        for cite, locations in sorted(result.undefined_cites.items()):
            print(f"  \\cite{{{cite}}}")
            for loc in locations:
                print(f"    -> {loc}")

    if result.bib_duplicates:
        print(f"\n  DUPLICATE BIB KEYS ({len(result.bib_duplicates)})")
        print("  " + "-" * 40)
        for dup in result.bib_duplicates:
            print(f"  {dup}")

    # Warnings
    if result.orphaned_labels:
        print(f"\n  ORPHANED LABELS ({len(result.orphaned_labels)})")
        print("  " + "-" * 40)
        for label in sorted(result.orphaned_labels):
            print(f"  \\label{{{label}}} — defined but never referenced")

    if result.warnings:
        print(f"\n  WARNINGS ({len(result.warnings)})")
        print("  " + "-" * 40)
        for warning in result.warnings[:20]:  # Limit output
            print(f"  {warning}")
        if len(result.warnings) > 20:
            print(f"  ... and {len(result.warnings) - 20} more")

    # Summary
    print("\n" + "=" * 60)
    if result.has_errors:
        print(f"  RESULT: {result.error_count} ERRORS found — fix before compiling")
    else:
        print("  RESULT: No errors (warnings only)")
    print("=" * 60 + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Audit LaTeX cross-references for multi-agent reports"
    )
    parser.add_argument("directory", help="Path to LaTeX project directory")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = audit(directory, verbose=args.verbose)

    if args.json:
        import json

        output = {
            "duplicate_labels": result.duplicate_labels,
            "undefined_refs": result.undefined_refs,
            "undefined_cites": result.undefined_cites,
            "orphaned_labels": result.orphaned_labels,
            "bib_duplicates": result.bib_duplicates,
            "warnings": result.warnings,
            "error_count": result.error_count,
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(result)

    sys.exit(1 if result.has_errors else 0)


if __name__ == "__main__":
    main()
