"""Prompt compilation for evidence-backed continuity-ledger extraction."""

from __future__ import annotations

from pathlib import Path


def compile_ledger_extraction_prompt_text(draft: str, existing_ledger: str = "") -> str:
    draft = draft.strip()
    if not draft:
        raise ValueError("Ledger extraction requires a non-empty draft.")
    blocks = [
        "# Continuity Ledger Extraction",
        "",
        "Extract a reviewable candidate ledger from the supplied manuscript. Do not continue, rewrite, "
        "or improve the prose. Treat only direct textual evidence as confirmed canon. Preserve an "
        "existing ledger unless the new text explicitly changes it.",
        "",
        "## Extraction Rules",
        "",
        "- Record each claim with a short quoted evidence fragment and its chapter or local location.",
        "- Label every entry `observed`, `inferred`, `conflicted`, or `unknown`. Never silently convert an inference into canon.",
        "- Record changes as transitions: before state -> on-page trigger -> after state. Do not infer off-page movement, possession, injuries, promises, or knowledge.",
        "- Keep unresolved facts separate from contradictions. An unmentioned detail is not automatically changed.",
        "- Do not invent character traits, motives, exact locations, relationship labels, or world rules merely to make the ledger complete.",
        "",
        "## Required Candidate Ledger",
        "",
        "Return compact Markdown with these sections: Fixed Facts; Character State And Carried Objects; "
        "Obligations, Promises, Debts And Open Questions; Injuries, Capabilities And Resource Use; "
        "Spatial Layout, Occupancy And Reach; Relationship And Information Boundaries; Conflicts Or "
        "Unknowns; Proposed Ledger Changes Requiring Human Confirmation. Every non-empty row needs evidence.",
    ]
    if existing_ledger.strip():
        blocks.extend(["", "# Existing Ledger Authority", "", existing_ledger.strip()])
    blocks.extend(["", "# Manuscript Evidence", "", draft])
    return "\n".join(blocks) + "\n"


def compile_ledger_extraction_prompt(draft_path: str, existing_ledger_path: str | None = None) -> str:
    draft = Path(draft_path).read_text(encoding="utf-8")
    existing = Path(existing_ledger_path).read_text(encoding="utf-8") if existing_ledger_path else ""
    return compile_ledger_extraction_prompt_text(draft, existing)
