#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _common import parse_frontmatter, save_json, sectionized_lines, split_sentences, strip_markdown, write_text

CLAIM_CUES = [
    "show", "shows", "demonstrate", "demonstrates", "prove", "proves", "find", "finds", "derive", "derives",
    "establish", "establishes", "identify", "identifies", "achieve", "achieves", "improve", "improves",
    "outperform", "outperforms", "reduce", "reduces", "increase", "increases", "yield", "yields",
    "enable", "enables", "support", "supports", "consistent", "robust", "significant"
]
EVIDENCE_PATTERNS = [
    re.compile(r"\b(Figure|Fig\.|Table|Theorem|Lemma|Proposition|Corollary|Section|Appendix|Eq\.|Equation|Algorithm|Experiment)\s*[A-Za-z0-9().-]+", re.I),
    re.compile(r"\b\d+(?:\.\d+)?%\b"),
    re.compile(r"\bp\s*[<=>]\s*0?\.\d+\b", re.I),
]
WEAK_SECTIONS = {"abstract", "introduction", "conclusion"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a heuristic claim-evidence matrix from paper markdown or text.")
    p.add_argument("input", help="Input markdown or text file")
    p.add_argument("--output", default="", help="Markdown table output path")
    p.add_argument("--json-output", default="", help="Optional JSON output path")
    p.add_argument("--max-claims", type=int, default=20, help="Maximum number of claims to keep")
    p.add_argument(
        "--source-type",
        choices=["paper", "notes"],
        default="paper",
        help="paper => mark claims as authors' stated claims; notes => infer from wording",
    )
    return p.parse_args()


def is_claim_sentence(sentence: str) -> bool:
    s = sentence.lower()
    return any(cue in s for cue in CLAIM_CUES)


def extract_evidence_refs(text: str) -> list[str]:
    refs = []
    for pat in EVIDENCE_PATTERNS:
        refs.extend([m.group(0) for m in pat.finditer(text)])
    seen = []
    for ref in refs:
        if ref not in seen:
            seen.append(ref)
    return seen


def estimate_strength(section: str, refs: list[str], sentence: str) -> str:
    sec = section.strip().lower()
    if any(r.lower().startswith(("theorem", "lemma", "proposition", "corollary")) for r in refs):
        return "strong-formal"
    if any(r.lower().startswith(("table", "figure", "fig.", "experiment", "algorithm")) for r in refs):
        return "medium-to-strong"
    if sec in WEAK_SECTIONS:
        return "weak"
    if any(ch.isdigit() for ch in sentence):
        return "medium"
    return "weak-to-medium"


def stated_or_inference(sentence: str, source_type: str) -> str:
    if source_type == "paper":
        return "authors' stated claim"
    s = sentence.lower()
    if any(x in s for x in ["i think", "this suggests", "it seems", "likely"]):
        return "my inference"
    return "authors' stated claim"


def build_claims(md: str, max_claims: int, source_type: str) -> tuple[list[dict], str]:
    rows = []
    seen_claim_text = set()
    for section, body in sectionized_lines(md):
        clean = strip_markdown(body)
        sentences = split_sentences(clean)
        for i, sent in enumerate(sentences):
            if not is_claim_sentence(sent):
                continue
            claim = sent.strip()
            if len(claim.split()) < 5 or claim in seen_claim_text:
                continue
            neighborhood = " ".join(sentences[max(0, i - 1): min(len(sentences), i + 2)])
            refs = extract_evidence_refs(neighborhood + " " + body)
            row = {
                "claim": claim,
                "claim_type": stated_or_inference(claim, source_type),
                "evidence_source": ", ".join(refs[:5]) or section,
                "strength": estimate_strength(section, refs, claim),
                "caveat": "",
                "section": section,
            }
            rows.append(row)
            seen_claim_text.add(claim)
            if len(rows) >= max_claims:
                break
        if len(rows) >= max_claims:
            break

    md_lines = [
        "| Claim | Stated by authors or my inference? | Evidence source (section / figure / table / theorem) | Strength | Caveat |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['claim']} | {row['claim_type']} | {row['evidence_source']} | {row['strength']} | {row['caveat']} |"
        )
    return rows, "\n".join(md_lines) + "\n"


def main() -> None:
    args = parse_args()
    md = Path(args.input).read_text(encoding="utf-8")
    _, md = parse_frontmatter(md)
    rows, table_md = build_claims(md, args.max_claims, args.source_type)

    if args.output:
        write_text(args.output, table_md)
    else:
        print(table_md)

    if args.json_output:
        save_json(args.json_output, {"claim_rows": rows})


if __name__ == "__main__":
    main()
