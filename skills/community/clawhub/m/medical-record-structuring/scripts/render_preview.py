"""Render a structured extraction result as a Markdown preview."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def render(payload: dict) -> str:
    bundle = payload.get("fhir_bundle", payload)
    report = payload.get("extraction_report", {})
    lines = ["# Medical Record Structuring Preview", ""]
    lines.append(f"- Record type: **{report.get('record_type', 'unknown')}**")
    lines.append(f"- Sections found: {', '.join(report.get('sections_found', []))}")
    counts = report.get("entities_count", {})
    if counts:
        lines.append(f"- Entities: " + ", ".join(f"{k}×{v}" for k, v in counts.items()))
    lines.append("")
    lines.append("## FHIR Resources")
    lines.append("")
    for e in bundle.get("entry", []):
        r = e.get("resource", {})
        lines.append(f"- **{r.get('resourceType')}** — {json.dumps({k:v for k,v in r.items() if k!='resourceType'}, ensure_ascii=False)[:120]}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_preview.py <extracted.json>", file=sys.stderr)
        sys.exit(2)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(render(data))
