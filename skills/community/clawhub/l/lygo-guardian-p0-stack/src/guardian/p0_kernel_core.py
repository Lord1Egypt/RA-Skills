"""P0.4 + P0.5 + harmony — portable; not a substitute for repo byte Φ-gate."""

from .p0_4_gate import p0_4_validate
from .p0_5_understanding import understanding_pass
from .harmony_check import harmony_pass


def validate_with_understanding(content: str, context: dict) -> dict:
    gate = p0_4_validate(content, context)
    understand = understanding_pass(content)
    harmony = harmony_pass(content, context)
    risk = max(gate.get("score", 0.0), 1.0 - harmony.get("harmony_score", 1.0))
    if not gate.get("deterministic_result", True):
        action = "isolate"
    elif risk >= 0.7:
        action = "flag"
    else:
        action = "allow"
    return {
        "allow": action == "allow",
        "action": action,
        "risk": float(risk),
        "reasons": [gate.get("pattern_name", "none"), harmony.get("mode", "unknown")],
        "understanding": understand.get("understanding"),
        "healing_suggestion": understand.get("healing_suggestion"),
        "compassionate_response": understand.get("compassionate_response", False),
    }