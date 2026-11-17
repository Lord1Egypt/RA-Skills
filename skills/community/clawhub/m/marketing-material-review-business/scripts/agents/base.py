"""Shared Agent review protocol.

Adapters receive a normalized payload and return the same JSON shape:
{
  "agent_runtime": "...",
  "risks": [...],
  "excluded": [...],
  "notes": [...]
}
"""

import copy


REQUIRED_RISK_FIELDS = ("word", "level", "basis", "reason", "suggestion")


class AgentReviewError(RuntimeError):
    pass


def normalize_agent_output(output):
    if not isinstance(output, dict):
        raise AgentReviewError("Agent output must be a JSON object")
    risks = output.get("risks")
    if not isinstance(risks, list):
        raise AgentReviewError("Agent output must contain a risks list")
    agent_runtime = output.get("agent_runtime") or output.get("provider") or "unknown"

    normalized_risks = []
    for index, risk in enumerate(risks, 1):
        if not isinstance(risk, dict):
            raise AgentReviewError(f"Risk #{index} must be a JSON object")
        missing = [field for field in REQUIRED_RISK_FIELDS if field not in risk]
        if missing:
            raise AgentReviewError(f"Risk #{index} missing fields: {', '.join(missing)}")
        item = copy.deepcopy(risk)
        item["id"] = index
        item.setdefault("action", "keep")
        item.setdefault("source", agent_runtime)
        item.setdefault("confidence", 0.8)
        normalized_risks.append(item)

    return {
        "agent_runtime": agent_runtime,
        "provider": output.get("provider", agent_runtime),
        "model": output.get("model"),
        "review_mode": output.get("review_mode"),
        "risks": normalized_risks,
        "excluded": output.get("excluded", []),
        "notes": output.get("notes", []),
    }


class AgentAdapter:
    provider = "base"

    def review(self, payload):
        raise NotImplementedError
