#!/usr/bin/env python3
"""
Medical Record Structuring · End-to-end pipeline.

Reads a Chinese clinical narrative from stdin or --input, runs section
segmentation + rule-based + LLM-assisted entity extraction, normalizes
codes (ICD-10 / LOINC / drug names), and emits a FHIR R4 bundle plus
extraction report.

This script is intentionally dependency-light (stdlib only for the demo
pipeline) so it works out of the box. Heavier extraction is delegated to
helper modules in the same folder, which the host agent can extend.

Usage:
    python3 run_pipeline.py --input record.txt --record-type admission \
        --output bundle.json
    echo "$TEXT" | python3 run_pipeline.py --record-type discharge
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Local helpers — kept small for the published skill bundle.
from segment_sections import segment_sections
from rule_extract import rule_extract
from assemble_fhir import assemble_fhir
from validate_fhir import validate_fhir


SUPPORTED_TYPES = {"admission", "progress", "discharge", "outpatient", "lab"}


def read_input(path: str | None) -> str:
    if path and path != "-":
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def detect_record_type(text: str) -> str:
    """Cheap heuristic; overridden by --record-type when provided."""
    if "入院记录" in text:
        return "admission"
    if "出院记录" in text or "出院小结" in text:
        return "discharge"
    if "病程记录" in text:
        return "progress"
    if "门诊" in text:
        return "outpatient"
    if "检验报告" in text or "化验" in text:
        return "lab"
    return "outpatient"


def run(text: str, record_type: str, mask_pii: bool) -> Dict[str, Any]:
    sections = segment_sections(text)
    entities = rule_extract(text, sections, record_type)
    fhir_bundle = assemble_fhir(entities, record_type=record_type)
    validation = validate_fhir(fhir_bundle)

    if mask_pii:
        # Lightweight mask for preview output. Full values remain in the
        # returned bundle which the caller controls.
        for entry in fhir_bundle.get("entry", []):
            res = entry.get("resource", {})
            if res.get("resourceType") == "Patient":
                for name in res.get("name", []):
                    family = name.get("family", "")
                    if family and len(family) >= 1:
                        name["family"] = family[0] + "*" * max(0, len(family) - 1)

    return {
        "fhir_bundle": fhir_bundle,
        "extraction_report": {
            "record_type": record_type,
            "sections_found": sorted(sections.keys()),
            "entities_count": {k: len(v) for k, v in entities.items()},
            "validation": validation,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Structure a Chinese clinical record.")
    parser.add_argument("--input", "-i", default="-", help="Input file path or '-' for stdin")
    parser.add_argument(
        "--record-type",
        choices=sorted(SUPPORTED_TYPES) + ["auto"],
        default="auto",
        help="Record type, or 'auto' for heuristic detection",
    )
    parser.add_argument("--output", "-o", default="-", help="Output file path or '-' for stdout")
    parser.add_argument("--mask-pii", action="store_true", default=True, help="Mask PII in preview (default on)")
    parser.add_argument("--no-mask-pii", dest="mask_pii", action="store_false")
    parser.add_argument("--fhir-only", action="store_true", help="Output only the FHIR bundle")
    args = parser.parse_args()

    text = read_input(args.input)
    if not text.strip():
        print("ERROR: empty input.", file=sys.stderr)
        return 2

    record_type = detect_record_type(text) if args.record_type == "auto" else args.record_type
    result = run(text, record_type, args.mask_pii)
    payload = result["fhir_bundle"] if args.fhir_only else result

    out_text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(out_text)
    else:
        Path(args.output).write_text(out_text, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
