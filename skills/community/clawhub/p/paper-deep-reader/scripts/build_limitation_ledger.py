#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _common import parse_frontmatter, save_json, sectionized_lines, split_sentences, strip_markdown, write_text

ACK_CUES = [
    "limitation", "limitations", "future work", "we do not", "we only", "restricted to", "assume", "assumes",
    "under the assumption", "may fail", "does not address", "leave for future work", "out of scope", "narrow"
]
INFERRED_RULES = [
    ("No explicit ablation section detected; mechanism-level attribution may be weak.", ["ablation", "sensitivity", "component analysis"]),
    ("No obvious robustness section detected; stability across settings may be under-tested.", ["robustness", "stress test", "sensitivity analysis"]),
    ("No explicit limitations or discussion section detected; caveats may be underspecified.", ["limitations", "discussion"]),
    ("No clear appendix or supplement references detected in the text; hidden implementation or proof detail may be missing from the current extract.", ["appendix", "supplement"]),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a limitation ledger from paper markdown or text.")
    p.add_argument("input", help="Input markdown or text file")
    p.add_argument("--output", default="", help="Markdown output path")
    p.add_argument("--json-output", default="", help="Optional JSON output path")
    return p.parse_args()


def extract_acknowledged(md: str) -> list[str]:
    rows = []
    for title, body in sectionized_lines(md):
        joined = strip_markdown(body)
        for sent in split_sentences(joined):
            low = sent.lower()
            if any(cue in low for cue in ACK_CUES):
                item = f"[{title}] {sent}"
                if item not in rows:
                    rows.append(item)
    return rows[:15]


def infer_limitations(md: str) -> list[str]:
    low = md.lower()
    inferred = []
    for message, cues in INFERRED_RULES:
        if not any(cue in low for cue in cues):
            inferred.append(message)
    # Add a gentle generic inference if the paper appears purely synthetic.
    if not any(x in low for x in ["real data", "dataset", "experiment", "empirical", "benchmark", "sample"]):
        inferred.append("Evidence may be narrow or synthetic-only; check whether external validity is limited.")
    return inferred[:10]


def render_md(ack: list[str], inferred: list[str]) -> str:
    lines = ["### Limitations explicitly acknowledged by the paper"]
    if ack:
        for item in ack:
            lines.append(f"- {item}")
    else:
        lines.append("- None extracted automatically. Review discussion / conclusion / appendix manually.")
    lines.append("")
    lines.append("### Limitations inferred by a careful reader")
    if inferred:
        for item in inferred:
            lines.append(f"- {item}")
    else:
        lines.append("- None inferred automatically.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    md = Path(args.input).read_text(encoding="utf-8")
    _, md = parse_frontmatter(md)
    ack = extract_acknowledged(md)
    inferred = infer_limitations(md)
    out_md = render_md(ack, inferred)

    if args.output:
        write_text(args.output, out_md)
    else:
        print(out_md)

    if args.json_output:
        save_json(args.json_output, {"acknowledged_limitations": ack, "inferred_limitations": inferred})


if __name__ == "__main__":
    main()
