from __future__ import annotations

from typing import Any

PROTEIN_SPLIT_CHARS = [",", "/"]


def protein_family(recipe: dict[str, Any]) -> str:
    raw = (recipe.get("core_protein") or "").lower()
    if not raw:
        return "other"
    bits = [raw]
    for char in PROTEIN_SPLIT_CHARS:
        next_bits = []
        for bit in bits:
            next_bits.extend(part.strip() for part in bit.split(char))
        bits = next_bits
    families = [bit for bit in bits if bit]
    if any(bit in {"beef", "steak"} for bit in families):
        return "beef"
    if any(bit in {"chicken"} for bit in families):
        return "chicken"
    if any(bit in {"pork", "sausage", "tenderloin", "chops"} for bit in families):
        return "pork"
    if any(bit in {"shrimp"} for bit in families):
        return "shrimp"
    if any(bit in {"fish", "cod", "salmon"} for bit in families):
        return "fish"
    if any(bit in {"pasta", "tomato", "broccoli"} for bit in families):
        return "non-protein-base"
    return families[0]


def primary_structural_role(recipe: dict[str, Any]) -> str:
    roles = recipe.get("structural_role") or []
    return roles[0] if roles else "unknown"
