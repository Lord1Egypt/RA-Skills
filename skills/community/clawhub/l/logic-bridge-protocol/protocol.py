"""
Role: Logic Bridge Protocol — requirement closure check + JSON tasks for agents.
Input: dict with key raw_text; optional runtime: Python 3.10+, pydantic v2.
Output: logic_bridge_protocol() → JSON dict (ok | error).
Links: —
Note: Published alongside skills/logic-bridge-protocol/SKILL.md for ClawHub.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Literal

from pydantic import BaseModel, Field


class SkillInput(BaseModel):
    """Input payload for `logic_bridge_protocol`."""

    raw_text: str = Field(..., min_length=1, description="Vague requirement or user story text")


class FileEditorTask(BaseModel):
    """Minimal task description for a file-editing agent."""

    intent: Literal["write", "patch", "review"] = "write"
    target_path: str = Field(..., description="Suggested file path to write or modify")
    instructions: str = Field(..., description="Natural-language instructions for the editor agent")


class SkillSuccess(BaseModel):
    status: Literal["ok"] = "ok"
    message: str
    file_editor_tasks: list[FileEditorTask]


class SkillFailure(BaseModel):
    status: Literal["error"] = "error"
    message: str
    follow_up_questions: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _is_chinese(text: str) -> bool:
    """Return True if the text contains a meaningful amount of Chinese characters."""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return chinese_chars >= 2


def _five_principles_check(text: str) -> tuple[bool, list[str]]:
    """
    Checks: actor (who), scenario, problem/goal, and actionable path.
    Returns gaps in the same language as the input (Chinese or English).
    """
    t = _normalize(text)
    zh = _is_chinese(t)
    gaps: list[str] = []

    if len(t) < 12:
        gaps.append(
            "描述太短了，请补充：谁在用、在什么情况下、希望发生什么变化。"
            if zh else
            "The description is too short. Add who is involved, in what situation, and what should change."
        )

    who_ok = bool(
        re.search(
            r"(用户|运营|管理员|我|我们|他|她|他们|作为|persona|user|admin|operator|customer|we|I|you|they|someone|as a)",
            t,
            re.I,
        )
    )
    if not who_ok:
        gaps.append(
            '缺少「谁」：请说明是哪类用户或角色在使用，例如"作为运营同学……"。'
            if zh else
            'Who is missing: name the primary user or role (e.g. "as a support agent..." / "运营同学").'
        )

    scenario_ok = bool(
        re.search(
            r"(场景|当|如果|在.+时|页面|流程|screen|page|flow|when|if|while|on the|in the app)",
            t,
            re.I,
        )
    )
    if not scenario_ok:
        gaps.append(
            '缺少「场景」：请说明在哪个页面或什么情况下触发，例如"在订单列表页..."。'
            if zh else
            "Scenario is unclear: say where or when this happens (page, flow, trigger, or context)."
        )

    goal_ok = bool(
        re.search(
            r"(问题|痛点|希望|目标|需要|想要|problem|goal|want|need|so that|in order to|issue|pain)",
            t,
            re.I,
        )
    )
    if not goal_ok:
        gaps.append(
            '缺少「目标」：请说明想解决什么问题，或者希望达到什么效果。'
            if zh else
            "Problem or goal is missing: what pain exists and what success looks like."
        )

    path_ok = bool(
        re.search(
            r"(先|然后|再|最后|点击|步骤|路径|first|then|next|finally|click|step|navigate|after)",
            t,
            re.I,
        )
    )
    if not path_ok:
        gaps.append(
            '缺少「操作路径」：请描述具体步骤，例如"先点 X，然后选 Y，最后看到 Z"。'
            if zh else
            'Path is not actionable: describe the flow (e.g. "click X, then Y, then see Z").'
        )

    return len(gaps) == 0, gaps


def _stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def logic_bridge_protocol(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Entry point: validate input; return failure with follow-ups, or success with FileEditor tasks.
    Never raises — always returns a JSON-serialisable dict.
    """
    from pydantic import ValidationError as _VE

    try:
        data = SkillInput.model_validate(payload)
    except _VE as exc:
        raw = payload.get("raw_text", "") if isinstance(payload, dict) else ""
        zh = _is_chinese(str(raw)) if raw else False
        failure = SkillFailure(
            message="输入内容有误，请检查后重试。" if zh else "Invalid input payload.",
            follow_up_questions=[
                "输入不能为空，请描述你的需求。" if zh else err["msg"]
                for err in exc.errors()
            ],
        )
        return json.loads(failure.model_dump_json())
    text = data.raw_text
    ok, gaps = _five_principles_check(text)
    if not ok:
        zh = _is_chinese(text)
        failure = SkillFailure(
            message="需求还未闭环，请补充以下信息：" if zh else "Requirements are not closed-loop yet. Please fill the gaps below.",
            follow_up_questions=gaps,
        )
        return json.loads(failure.model_dump_json())

    digest = _stable_hash(text)
    zh = _is_chinese(text)
    success = SkillSuccess(
        message="需求已闭环，可以生成任务文档。" if zh else "Checks passed. You can materialize the task document and downstream edits.",
        file_editor_tasks=[
            FileEditorTask(
                intent="write",
                target_path="docs/logic_bridge_task.md",
                instructions=(
                    "Produce a Logic Bridge task brief in Markdown with: "
                    "First Principle goal, pyramid-style breakdown, AI todo list, boundary conditions; "
                    f"append a stable digest line at the end: sha256={digest}."
                ),
            )
        ],
    )
    return json.loads(success.model_dump_json())


if __name__ == "__main__":
    demo = {"raw_text": "button"}
    print(json.dumps(logic_bridge_protocol(demo), ensure_ascii=False, indent=2))
