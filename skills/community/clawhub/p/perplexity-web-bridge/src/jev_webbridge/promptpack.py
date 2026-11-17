"""Prompt-quality pack: wrap a bare goal in community-validated answer rules.

Pure text crafting (no site automation knowledge): the wrapper keeps the goal
VERBATIM so the DONE keyword gate keeps working, and adds the answer-quality
rules validated by the Perplexity community (per-sentence citations,
unsupported-labeling, recency window, conflict exposure) plus per-recipe focus
hints. Recipes: default | finance | tech | research.
"""
from __future__ import annotations

CORE_RULES = (
    "Role: meticulous research analyst.\n"
    "Requirements:\n"
    "1. Place a citation after every factual sentence.\n"
    "2. If evidence is weak or a claim cannot be sourced, label it "
    '"unsupported" instead of guessing.\n'
    "3. Cite sources with URLs; official pages only for pricing.\n"
    "4. Prefer information from the last 12 months where recency matters.\n"
    "5. Highlight conflicting findings and explain how you resolved them."
)

RECIPES: dict[str, str] = {
    "default": "",
    "finance": (
        "Focus: Finance + Academic. Primary sources only: SEC filings, "
        "earnings transcripts, 10-K/10-Q, analyst reports. "
        "Label projections vs historical data with confidence."
    ),
    "tech": (
        "Prefer official docs and issue trackers; quote error messages verbatim; "
        "compare options as a trade-off table with benchmark sources."
    ),
    "research": (
        "Research mode. Source-first: list sources before writing. "
        "Aim for breadth (30+ sources); open with an executive summary; "
        "end with open questions."
    ),
}


def enhance(goal: str, recipe: str = "default") -> str:
    """Return the wrapped prompt; ``goal`` appears verbatim (keyword gate safe)."""
    if recipe not in RECIPES:
        raise ValueError(f"unknown recipe {recipe!r}; expected one of {sorted(RECIPES)}")
    parts = [f"Objective: {goal}", CORE_RULES]
    if RECIPES[recipe]:
        parts.append(RECIPES[recipe])
    return "\n".join(parts)
