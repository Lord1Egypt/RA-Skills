"""Light Math harmony check (soft heuristic). Canonical Φ: lygo-protocol-stack P0."""

from typing import Dict


def harmony_pass(content: str, context: Dict) -> Dict:
    text = (content or "").lower()
    harsh = sum(text.count(w) for w in ["idiot", "stupid", "hate", "worthless"])
    soft = sum(text.count(w) for w in ["thank", "grateful", "appreciate", "together", "help"])
    if harsh == 0 and soft == 0:
        harmony_score = 0.8
    else:
        harmony_score = max(0.0, min(1.0, (soft + 1) / (soft + harsh + 1)))
    if "repair" in text or "heal" in text or "fix" in text:
        mode = "repair"
    elif "vision" in text or "future" in text or "dream" in text:
        mode = "vision"
    else:
        mode = "grounding"
    return {"harmony_score": float(harmony_score), "mode": mode}