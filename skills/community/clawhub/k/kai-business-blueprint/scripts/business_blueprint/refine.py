"""Refine command: AI generates a structured diff from user feedback.

This module is LLM-agnostic. The caller supplies a ``llm_call(prompt) -> str``
function. We provide:

- ``build_refine_prompt`` — assembles the prompt sent to the LLM
- ``parse_refine_response`` — robustly extracts the JSON diff from LLM output
- ``refine_blueprint`` — top-level orchestration: prompt → parse → apply → write

For the in-skill default, ``stdout_llm_caller`` writes the prompt to a file and
expects the caller to paste the LLM response back. This keeps the module usable
without binding to a specific API.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from diff_patcher import DiffPatchError, apply_diff
from model import load_json, new_revision_meta, write_json


REFINE_PROMPT_TEMPLATE = """You are refining an existing business blueprint based on user feedback.

EXISTING BLUEPRINT (JSON):
```json
{blueprint_json}
```

USER FEEDBACK:
{feedback}

PRIOR CLARIFICATIONS (from earlier turn, may be empty):
{clarifications}

OUTPUT a refine diff as JSON with EXACTLY this structure:

```json
{{
  "diffId": "diff-{timestamp}",
  "baseBlueprintRevisionId": "{base_revision}",
  "operations": [
    {{"op": "modify", "path": "library.knowledge.painPoints[0].name", "old": "...", "new": "..."}},
    {{"op": "add", "path": "library.knowledge.painPoints[]", "value": {{...full entity dict...}}}},
    {{"op": "delete", "path": "library.knowledge.pitfalls[2]"}}
  ],
  "rationale": "1-2 sentences explaining how these changes address the feedback"
}}
```

CONSTRAINTS:
- Each operation must be MINIMAL and FOCUSED. Do not bundle unrelated changes.
- Modifications preserve entity IDs (only change name/fields, never the id).
- Additions must include id (fresh sequential), name, entityType.
- Deletions remove the entire entity. Also delete relations referencing the deleted ID
  (emit additional delete operations for those relations).
- For new knowledge entities, run self-check (see references/knowledge-self-check.md)
  and populate ``_selfCheck`` with passed/questions arrays.
- Path syntax:
  - Use ``library.knowledge.painPoints[0].name`` for modify of a specific field.
  - Use ``library.knowledge.painPoints[]`` (empty brackets) to APPEND.
  - Use ``library.knowledge.pitfalls[2]`` (with index) to DELETE the third pitfall.
- Output ONLY the JSON diff, no commentary, no markdown fencing other than the
  triple-backtick block above (the parser handles either).

DOMAIN-KNOWLEDGE NAMING (apply ONLY when meta.blueprintType == "domain-knowledge"):
- ``strategy.name``: 4-10 字产品级名词短语（"统一归因模型"、"AIGC 素材工厂"、
  "智能调价机器人"）。不要写成动作（"优化素材"、"调价"），不要写成维度
  （"测款节奏"、"受众分层"）。如果只能想到动作或维度，把它包装成方案名
  （"7×24 智能竞价机器人" 而非 "动态出价"）。
- ``painPoint.audience``: 自由字符串字段，主要受影响的 persona
  （"品牌方/DTC"、"平台卖家"、"代运营/服务商"）。多个时用逗号分隔。
  不需要建立独立 persona 实体——audience 仅作为分组标签。
- ``strategy.audience``: 同上，标注主要受益 persona。
- ``metric.forecast`` (可选): 形如 ``{{"direction": "up"|"down"|"neutral",
  "magnitude": <数字>, "unit": "%"|"倍"}}``，用于对客户可承诺的提升收益。
  现状基准仍用 ``value`` / ``benchmarkContext``。两者并存表达
  "现状 X，可达 Y"。
- 这些字段是 v2 minimal-validation 政策下的 pass-through 字段——validator
  不强制，但渲染器和 pitch 流程会消费它们。
"""


def build_refine_prompt(
    blueprint: dict[str, Any],
    feedback: str,
) -> str:
    """Assemble the refine prompt sent to the LLM."""
    blueprint_json = json.dumps(blueprint, ensure_ascii=False, indent=2)
    clarifications = blueprint.get("context", {}).get("clarifications", [])
    clarifications_text = (
        json.dumps(clarifications, ensure_ascii=False, indent=2)
        if clarifications
        else "None"
    )
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    base_revision = blueprint.get("meta", {}).get("revisionId", "unknown")

    return REFINE_PROMPT_TEMPLATE.format(
        blueprint_json=blueprint_json,
        feedback=feedback,
        clarifications=clarifications_text,
        timestamp=timestamp,
        base_revision=base_revision,
    )


def parse_refine_response(response: str) -> dict[str, Any]:
    """Extract the JSON diff from the LLM response.

    Handles three forms:
    1. Pure JSON object string
    2. JSON inside a ```json``` fenced block
    3. JSON inside a generic ``` fenced block
    """
    text = response.strip()
    if not text:
        raise ValueError("Empty refine response")

    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip code fences
    fence_start = text.find("```")
    if fence_start >= 0:
        # Skip language tag if present
        newline = text.find("\n", fence_start)
        if newline > fence_start:
            text = text[newline + 1:]
        fence_end = text.rfind("```")
        if fence_end > 0:
            text = text[:fence_end]

    text = text.strip()
    return json.loads(text)


def stdout_llm_caller(prompt: str) -> str:  # pragma: no cover - interactive
    """Default LLM caller: write prompt to a temp file, expect human response.

    Used when no API is configured. The caller pastes the LLM response on stdin.
    """
    import sys
    sys.stderr.write("=== REFINE PROMPT ===\n")
    sys.stderr.write(prompt)
    sys.stderr.write("\n=== END PROMPT — paste LLM response then Ctrl-D ===\n")
    return sys.stdin.read()


def generate_diff(
    blueprint: dict[str, Any],
    feedback: str,
    llm_call: Callable[[str], str],
) -> dict[str, Any]:
    """Build prompt, call LLM, parse diff. Pure function modulo llm_call."""
    prompt = build_refine_prompt(blueprint, feedback)
    response = llm_call(prompt)
    return parse_refine_response(response)


def refine_blueprint(
    blueprint_path: Path,
    feedback: str,
    output_path: Path,
    llm_call: Callable[[str], str] = stdout_llm_caller,
    auto_apply: bool = True,
) -> dict[str, Any]:
    """End-to-end refine: read blueprint, gen diff, optionally apply, write outputs.

    Returns the diff dict.
    """
    blueprint = load_json(blueprint_path)
    diff = generate_diff(blueprint, feedback, llm_call)

    diff_path = output_path.with_suffix(".diff.json")
    write_json(diff_path, diff)

    if auto_apply:
        try:
            new_blueprint = apply_diff(blueprint, diff)
        except DiffPatchError as exc:
            raise DiffPatchError(
                f"Failed to apply diff to {blueprint_path.name}: {exc}"
            ) from exc

        existing_meta = new_blueprint.setdefault("meta", {})
        existing_revision = existing_meta.get("revisionId")
        revision_meta = new_revision_meta(
            parent_revision_id=existing_revision,
            modified_by="ai-refine",
        )
        existing_meta.update(revision_meta)
        write_json(output_path, new_blueprint)

    return diff
