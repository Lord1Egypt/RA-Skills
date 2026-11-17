"""Manual/offline local mode.

This mode keeps the workflow deterministic: it converts rule risks into the
common Agent output format. A human or a host agent can edit the JSON later.
"""

import copy

from .base import AgentAdapter, normalize_agent_output


class ManualAdapter(AgentAdapter):
    provider = "manual"

    def review(self, payload):
        risks = []
        for risk in payload.get("rule_risks", []):
            item = copy.deepcopy(risk)
            item.setdefault("action", "keep")
            item.setdefault("source", "rule")
            item.setdefault("confidence", 0.78)
            risks.append(item)

        return normalize_agent_output({
            "agent_runtime": "manual-rule-pass-through",
            "provider": self.provider,
            "model": "deterministic-rule-pass-through",
            "review_mode": payload.get("review_mode"),
            "risks": risks,
            "excluded": [],
            "notes": [
                "manual 本地模式未调用外部模型，仅将规则风险规范化为 agent_risks.json。"
            ],
        })
