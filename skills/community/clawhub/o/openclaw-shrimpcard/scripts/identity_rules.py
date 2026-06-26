#!/usr/bin/env python3
from __future__ import annotations


BRAND_TOKENS = {
    "openclaw": ["openclaw", "lobster", "shrimp", "crab", "claw", "龙虾", "虾", "蟹"],
    "hermes": ["hermes"],
    "codex": ["codex"],
}


def _iter_values(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from _iter_values(item)
        return
    if isinstance(value, list):
        for item in value:
            yield from _iter_values(item)
        return
    if isinstance(value, str):
        yield value


def collect_live_evidence_text(snapshot: dict) -> str:
    parts: list[str] = []
    if "evidence_window" in snapshot or "evidence_items" in snapshot:
        window = snapshot.get("evidence_window", {})
        parts.extend(_iter_values(window))
        for item in snapshot.get("evidence_items", []):
            parts.extend(_iter_values(item))
    else:
        parts.extend(_iter_values(snapshot))
    return "\n".join(parts).lower()


def detect_explicit_brand(snapshot: dict) -> str | None:
    text = collect_live_evidence_text(snapshot)
    for brand, tokens in BRAND_TOKENS.items():
        if any(token in text for token in tokens):
            return brand
    return None


def neutral_identity_rule() -> str:
    return (
        "- Do not derive the target identity from the skill name, repository name, package name, "
        "script path, config file, or interface label.\n"
        "- If live evidence does not explicitly name a branded agent family or mascot, keep the public identity neutral.\n"
        "- In neutral cases, prefer `character_style: agent-avatar` and generic role naming over mascot branding."
    )


def brand_guidance(snapshot: dict) -> str:
    brand = detect_explicit_brand(snapshot)
    if brand == "openclaw":
        return (
            neutral_identity_rule()
            + "\n- Live evidence explicitly contains claw/lobster/shrimp branding, so `character_style: lobster` is allowed only if the final copy stays faithful to that evidence."
        )
    if brand == "hermes":
        return (
            neutral_identity_rule()
            + "\n- Live evidence explicitly names Hermes, so that name may appear in the final identity only if the wording remains evidence-backed and specific."
        )
    if brand == "codex":
        return (
            neutral_identity_rule()
            + "\n- Live evidence explicitly names Codex, so code-delivery framing is acceptable if the final wording still reflects repeated observed behavior."
        )
    return neutral_identity_rule()
