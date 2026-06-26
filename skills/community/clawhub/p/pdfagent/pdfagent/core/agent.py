from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class AgentStep:
    tool: str
    params: dict[str, Any]


_SPLIT_RE = re.compile(r"\bpages?\s+([0-9,\- ]+)", re.IGNORECASE)
_EVERY_RE = re.compile(r"\bevery\s+(\d+)", re.IGNORECASE)
_ROTATE_RE = re.compile(r"\b(\d{2,3})\s*(deg|degree|degrees)\b", re.IGNORECASE)
_EVEN_RE = re.compile(r"\beven\s+pages?\b", re.IGNORECASE)
_ODD_RE = re.compile(r"\bodd\s+pages?\b", re.IGNORECASE)
_EVERY_OTHER_RE = re.compile(r"\bevery\s+other\s+page\b", re.IGNORECASE)


def parse_agent_text(text: str) -> list[AgentStep]:
    steps: list[AgentStep] = []
    for raw in re.split(r"\bthen\b|->|;", text, flags=re.IGNORECASE):
        step = raw.strip()
        if not step:
            continue
        lower = step.lower()
        if "merge" in lower or "combine" in lower:
            steps.append(AgentStep("merge", {}))
            continue
        if "split" in lower or "extract" in lower:
            params: dict[str, Any] = {}
            every = _EVERY_RE.search(step)
            if every:
                params["every"] = int(every.group(1))
            else:
                ranges = _SPLIT_RE.search(step)
                if ranges:
                    params["ranges"] = ranges.group(1).replace(" ", "")
            steps.append(AgentStep("split", params))
            continue
        if "rotate" in lower:
            params = {}
            rotate = _ROTATE_RE.search(step)
            if rotate:
                params["degrees"] = int(rotate.group(1))
            if _EVEN_RE.search(step) or _EVERY_OTHER_RE.search(step):
                params["pages"] = "even"
            elif _ODD_RE.search(step):
                params["pages"] = "odd"
            steps.append(AgentStep("rotate", params))
            continue

        # Unsupported tool in v0.1
        steps.append(AgentStep("unknown", {"raw": step}))

    if not steps:
        raise ValueError("No actionable steps found in agent text")

    return steps
