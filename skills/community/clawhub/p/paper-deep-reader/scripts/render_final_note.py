#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    dump_frontmatter,
    load_json,
    parse_frontmatter,
    read_text,
    replace_section_content,
    save_json,
    write_text,
)

SECTION_ALIASES = {
    "citation": "Citation",
    "one_paragraph_summary": "One-paragraph summary",
    "paper_map": "Paper map",
    "why_this_paper_matters": "Why this paper matters",
    "problem_setup": "Problem setup",
    "main_idea": "Main idea",
    "notation_table": "Notation table",
    "core_equations_estimators_laws": "Core equations / estimators / laws",
    "step_by_step_mechanism": "Step-by-step mechanism",
    "theoretical_claims_proof_ideas": "Theoretical claims / proof ideas",
    "complexity_efficiency_scaling_identification": "Complexity / efficiency / scaling / identification",
    "claim_evidence_matrix": "Claim–evidence matrix",
    "experimental_empirical_observational_design": "Experimental / empirical / observational design",
    "main_results": "Main results",
    "ablations_robustness_stress_tests": "Ablations / robustness / stress tests",
    "baselines_and_fairness": "Baselines and fairness",
    "limitations_and_failure_modes": "Limitations and failure modes",
    "relationship_to_other_work": "Relationship to other work",
    "open_questions": "Open questions",
    "implementation_reproduction_notes": "Implementation / reproduction notes",
    "what_i_learned_from_this_paper": "What I learned from this paper",
    "verdict": "Verdict",
}


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    default_template = here.parent / "references" / "note-template-base.md"

    p = argparse.ArgumentParser(description="Fill a scaffolded note or base template with structured section content.")
    p.add_argument("--input", default=str(default_template), help="Input note scaffold or template")
    p.add_argument("--output", required=True, help="Rendered note output path")
    p.add_argument("--sections-json", default="", help="JSON file containing section content keyed by alias names")
    p.add_argument("--paper-map-md", default="", help="Markdown file to inject into 'Paper map'")
    p.add_argument("--notation-table-md", default="", help="Markdown file to inject into 'Notation table'")
    p.add_argument("--claim-matrix-md", default="", help="Markdown file to inject into 'Claim–evidence matrix'")
    p.add_argument("--limitation-ledger-md", default="", help="Markdown file to inject into 'Limitations and failure modes'")
    p.add_argument("--metadata-json", default="", help="Optional JSON file with frontmatter keys to merge")
    p.add_argument("--set", nargs="*", default=None, help="Inline metadata overrides like title='...' year=2024")
    return p.parse_args()


def parse_set_args(items: list[str] | None) -> dict:
    out = {}
    for item in items or []:
        if "=" not in item:
            continue
        key, val = item.split("=", 1)
        out[key.strip()] = val.strip().strip("'\"")
    return out


def merge_frontmatter(md: str, metadata: dict) -> str:
    fm, body = parse_frontmatter(md)
    fm.update({k: v for k, v in metadata.items() if v is not None})
    title = metadata.get("title")
    if title:
        body = body.replace("# Untitled Paper", f"# {title}", 1)
        body = body.replace("# {{title}}", f"# {title}", 1)
    return dump_frontmatter(fm) + "\n\n" + body.lstrip("\n")


def main() -> None:
    args = parse_args()
    md = read_text(args.input)

    metadata = {}
    if args.metadata_json:
        metadata.update(load_json(args.metadata_json))
    metadata.update(parse_set_args(args.set))
    if metadata:
        md = merge_frontmatter(md, metadata)

    _, body = parse_frontmatter(md)
    frontmatter, _ = parse_frontmatter(md)

    section_data = load_json(args.sections_json) if args.sections_json else {}
    for key, heading in SECTION_ALIASES.items():
        if key in section_data and section_data[key] is not None:
            body = replace_section_content(body, heading, str(section_data[key]).rstrip() + "\n")

    if args.paper_map_md:
        body = replace_section_content(body, "Paper map", read_text(args.paper_map_md))
    if args.notation_table_md:
        body = replace_section_content(body, "Notation table", read_text(args.notation_table_md))
    if args.claim_matrix_md:
        body = replace_section_content(body, "Claim–evidence matrix", read_text(args.claim_matrix_md))
    if args.limitation_ledger_md:
        body = replace_section_content(body, "Limitations and failure modes", read_text(args.limitation_ledger_md))

    final_md = dump_frontmatter(frontmatter) + "\n\n" + body.lstrip("\n")
    write_text(args.output, final_md)
    print(args.output)


if __name__ == "__main__":
    main()
