"""Reusable, interruptible, and resumable SOP pipeline for novel creation."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union

from .blueprint import validate_blueprint, BlueprintError
from .context import build_context, ContextError
from .io import file_lock, read_json, safe_id, sha256_file, write_json_atomic
from .review import apply_review, ReviewError
from .settlement import apply_settlement, SettlementError
from .state import (
    STATES,
    InvalidTransition,
    init_project,
    read_chapter_state,
    transition_chapter,
)
from .wiki import rebuild_wiki


STAGE_BY_STATE = {
    "PLANNED": "BLUEPRINT",
    "BLUEPRINT_VALID": "CONTEXT",
    "CONTEXT_LOCKED": "DRAFT",
    "DRAFTED": "TEXT_REVIEW",
    "TEXT_PASS": "ENGINE_REVIEW",
    "ENGINE_PASS": "SETTLEMENT",
    "SETTLED": "DELIVERY",
    "DELIVERABLE": "COMPLETED",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_project_root(path: Optional[Union[str, Path]] = None) -> Path:
    start = Path(path).resolve() if path else Path.cwd().resolve()
    if (start / ".novelforge" / "state" / "project.json").is_file():
        return start
    for parent in start.parents:
        if (parent / ".novelforge" / "state" / "project.json").is_file():
            return parent
    return start


def _pipeline_checkpoint_path(root: Path) -> Path:
    return root / ".novelforge" / "state" / "pipeline.json"


def _get_blueprint_file(root: Path, chapter: str) -> Path:
    candidates = (
        root / "blueprints" / f"{chapter}.md",
        root / "blueprints" / f"{chapter}.json",
        root / "wiki" / "blueprints" / f"{chapter}.md",
        root / "wiki" / "blueprints" / f"{chapter}.json",
    )
    for c in candidates:
        if c.is_file():
            return c
    return root / "blueprints" / f"{chapter}.md"


def _get_chapter_file(root: Path, chapter: str) -> Path:
    candidates = (
        root / "chapters" / f"{chapter}.md",
        root / "chapters" / f"{chapter}.txt",
        root / "wiki" / "chapters" / f"{chapter}.md",
        root / "wiki" / "chapters" / f"{chapter}.txt",
    )
    for c in candidates:
        if c.is_file():
            return c
    return root / "chapters" / f"{chapter}.md"


def _build_io_contract(root: Path, target_chapter: str, current_status: str) -> Dict[str, Any]:
    advance_cmd = f"python3 scripts/novelforgectl.py pipeline advance {root} {target_chapter}"
    bp_file = _get_blueprint_file(root, target_chapter)
    txt_file = _get_chapter_file(root, target_chapter)

    if current_status == "PLANNED":
        inputs = [{"role": "project_profile", "path": str(root / ".novelforge" / "state" / "project.json"), "description": "项目题材与引擎规则"}]
        settlements_dir = root / ".novelforge" / "settlements"
        if settlements_dir.is_dir():
            prev_settlements = sorted(settlements_dir.glob("*.json"))
            if prev_settlements:
                inputs.append({
                    "role": "previous_settlement",
                    "path": str(prev_settlements[-1]),
                    "description": f"前序章节事实结算 ({prev_settlements[-1].stem})",
                })
        return {
            "inputs": inputs,
            "output": {
                "role": "blueprint",
                "path": str(bp_file),
                "format": "markdown" if bp_file.suffix == ".md" else "json",
                "template": {
                    "id": target_chapter,
                    "phase": "scene",
                    "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []},
                    "scene_types": [],
                    "state": {},
                    "settlement": {"changes": [], "next_question": ""},
                },
                "description": "章节蓝图：设定因果目标、场景、依赖项与下一问",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "BLUEPRINT_VALID":
        return {
            "inputs": [{"role": "blueprint", "path": str(bp_file), "description": "已通过结构校验的章节蓝图"}],
            "output": {
                "role": "context_ticket",
                "path": str(root / ".novelforge" / "context" / f"{target_chapter}.json"),
                "format": "json",
                "description": "锁定依赖哈希与引擎快照的上下文工单（由脚本自动编译）",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "CONTEXT_LOCKED":
        return {
            "inputs": [
                {"role": "context_ticket", "path": str(root / ".novelforge" / "context" / f"{target_chapter}.json"), "description": "锁定的显式事实与叙事引擎快照"},
                {"role": "blueprint", "path": str(bp_file), "description": "章节蓝图场景结构"},
            ],
            "output": {
                "role": "chapter_text",
                "path": str(txt_file),
                "format": "markdown" if txt_file.suffix == ".md" else "text/plain",
                "description": "章节正文初稿",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "DRAFTED":
        return {
            "inputs": [
                {"role": "chapter_text", "path": str(txt_file), "description": "已起草的正文内容"},
                {"role": "project_profile", "path": str(root / ".novelforge" / "state" / "project.json"), "description": "项目画像与质检规则"},
            ],
            "output": {
                "role": "text_review",
                "path": str(root / ".novelforge" / "reviews" / f"{target_chapter}-text.json"),
                "format": "json",
                "template": {
                    "chapter": target_chapter,
                    "kind": "text",
                    "source_hash": "<sha256 of chapter_text>",
                    "result": "PASS",
                    "checks": [],
                },
                "description": "文本质量与风格诊断报告",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "TEXT_PASS":
        return {
            "inputs": [
                {"role": "chapter_text", "path": str(txt_file), "description": "通过文本质检的正文内容"},
                {"role": "context_ticket", "path": str(root / ".novelforge" / "context" / f"{target_chapter}.json"), "description": "锁定的长线伏笔与人物知识边界"},
            ],
            "output": {
                "role": "engine_review",
                "path": str(root / ".novelforge" / "reviews" / f"{target_chapter}-engine.json"),
                "format": "json",
                "template": {
                    "chapter": target_chapter,
                    "kind": "engine",
                    "source_hash": "<sha256 of chapter_text>",
                    "result": "PASS",
                    "checks": [],
                },
                "description": "故事连续性与引擎方法卡审查报告",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "ENGINE_PASS":
        return {
            "inputs": [
                {"role": "chapter_text", "path": str(txt_file), "description": "通过双重审查的章节正文"},
                {"role": "text_review", "path": str(root / ".novelforge" / "reviews" / f"{target_chapter}-text.json")},
                {"role": "engine_review", "path": str(root / ".novelforge" / "reviews" / f"{target_chapter}-engine.json")},
            ],
            "output": {
                "role": "settlement",
                "path": str(root / "settlements" / f"{target_chapter}.json"),
                "format": "json",
                "template": {
                    "schema": 1,
                    "chapter": target_chapter,
                    "source_hash": "<sha256 of chapter_text>",
                    "facts": [],
                },
                "description": "章节事实结算（实体属性、关系变化、伏笔推进）",
            },
            "advance_command": advance_cmd,
        }

    elif current_status == "SETTLED":
        return {
            "inputs": [
                {"role": "settlement", "path": str(root / ".novelforge" / "settlements" / f"{target_chapter}.json"), "description": "已应用的事实结算"}
            ],
            "output": {
                "role": "wiki_index",
                "path": str(root / "index.md"),
                "description": "故事索引网络",
            },
            "advance_command": advance_cmd,
        }

    return {
        "inputs": [],
        "output": None,
        "advance_command": None,
    }



def _resolve_chapter(root: Path, chapter: Optional[str] = None) -> str:
    if chapter and safe_id(chapter):
        return chapter
    checkpoint_file = _pipeline_checkpoint_path(root)
    if checkpoint_file.is_file():
        try:
            data = read_json(checkpoint_file)
            active = data.get("active_chapter")
            if active and safe_id(active):
                return active
        except (OSError, ValueError, TypeError):
            pass
    chapters_dir = root / ".novelforge" / "state" / "chapters"
    if chapters_dir.is_dir():
        states = sorted(chapters_dir.glob("*.json"))
        if states:
            for state_path in reversed(states):
                try:
                    chapter_state = read_json(state_path)
                    if chapter_state.get("status") != "DELIVERABLE":
                        return state_path.stem
                except (OSError, ValueError, TypeError):
                    continue
            return states[-1].stem
    return "v01-c01"


def get_pipeline_status(root_input: Optional[Union[str, Path]] = None, chapter: Optional[str] = None) -> Dict[str, Any]:
    root = find_project_root(root_input)
    project_file = root / ".novelforge" / "state" / "project.json"
    if not project_file.is_file():
        return {
            "status": "UNINITIALIZED",
            "message": "Project is not initialized. Run pipeline advance or project init.",
            "can_advance": True,
            "next_action": "INIT_PROJECT",
        }

    target_chapter = _resolve_chapter(root, chapter)
    state_file = root / ".novelforge" / "state" / "chapters" / f"{target_chapter}.json"
    if not state_file.is_file():
        chapter_state = {"status": "PLANNED", "chapter": target_chapter, "version": 0}
    else:
        chapter_state = read_chapter_state(root, target_chapter)

    current_status = chapter_state.get("status", "PLANNED")
    current_stage = STAGE_BY_STATE.get(current_status, "UNKNOWN")

    bp_file = _get_blueprint_file(root, target_chapter)
    txt_file = _get_chapter_file(root, target_chapter)
    ctx_file = root / ".novelforge" / "context" / f"{target_chapter}.json"
    tr_file = root / ".novelforge" / "reviews" / f"{target_chapter}-text.json"
    er_file = root / ".novelforge" / "reviews" / f"{target_chapter}-engine.json"
    st_file = root / ".novelforge" / "settlements" / f"{target_chapter}.json"
    st_proposal = root / "settlements" / f"{target_chapter}.json"

    checkpoint_file = _pipeline_checkpoint_path(root)
    checkpoint = read_json(checkpoint_file) if checkpoint_file.is_file() else {}

    artifacts = {
        "blueprint": bp_file.is_file(),
        "context_ticket": ctx_file.is_file(),
        "chapter_text": txt_file.is_file() and len(txt_file.read_text(encoding="utf-8").strip()) > 0,
        "text_review": tr_file.is_file(),
        "engine_review": er_file.is_file(),
        "settlement": st_proposal.is_file() or st_file.is_file(),
    }

    can_advance = False
    next_action = "NONE"
    blocked_reason = None

    if current_status == "PLANNED":
        if artifacts["blueprint"]:
            can_advance = True
            next_action = "VALIDATE_BLUEPRINT"
        else:
            blocked_reason = f"Missing blueprint: {bp_file.relative_to(root)}"
            next_action = "WRITE_BLUEPRINT"
    elif current_status == "BLUEPRINT_VALID":
        can_advance = True
        next_action = "BUILD_CONTEXT"
    elif current_status == "CONTEXT_LOCKED":
        if artifacts["chapter_text"]:
            can_advance = True
            next_action = "ADVANCE_TO_DRAFTED"
        else:
            blocked_reason = f"Draft {txt_file.relative_to(root)} is missing or empty"
            next_action = "WRITE_DRAFT"
    elif current_status == "DRAFTED":
        if artifacts["text_review"]:
            can_advance = True
            next_action = "APPLY_TEXT_REVIEW"
        else:
            blocked_reason = f"Missing text review: .novelforge/reviews/{target_chapter}-text.json"
            next_action = "PERFORM_TEXT_REVIEW"
    elif current_status == "TEXT_PASS":
        if artifacts["engine_review"]:
            can_advance = True
            next_action = "APPLY_ENGINE_REVIEW"
        else:
            blocked_reason = f"Missing engine review: .novelforge/reviews/{target_chapter}-engine.json"
            next_action = "PERFORM_ENGINE_REVIEW"
    elif current_status == "ENGINE_PASS":
        if artifacts["settlement"]:
            can_advance = True
            next_action = "APPLY_SETTLEMENT"
        else:
            blocked_reason = f"Missing settlement: .novelforge/settlements/{target_chapter}.json"
            next_action = "WRITE_SETTLEMENT"
    elif current_status == "SETTLED":
        can_advance = True
        next_action = "DELIVER_CHAPTER"
    elif current_status == "DELIVERABLE":
        can_advance = False
        next_action = "COMPLETED"

    status_code = "COMPLETED" if current_status == "DELIVERABLE" else ("READY" if can_advance else "PAUSED")
    if checkpoint.get("interrupted") and not can_advance:
        status_code = "INTERRUPTED"

    return {
        "status": status_code,
        "chapter": target_chapter,
        "state": current_status,
        "stage": current_stage,
        "can_advance": can_advance,
        "next_action": next_action,
        "blocked_reason": blocked_reason,
        "interrupted": checkpoint.get("interrupted", False),
        "interruption_reason": checkpoint.get("reason"),
        "artifacts": artifacts,
        "io_contract": _build_io_contract(root, target_chapter, current_status),
    }


def record_pipeline_checkpoint(
    root: Path,
    chapter: str,
    stage: str,
    state: str,
    interrupted: bool = False,
    reason: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    checkpoint_file = _pipeline_checkpoint_path(root)
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "active_chapter": chapter,
        "stage": stage,
        "state": state,
        "interrupted": interrupted,
        "reason": reason,
        "details": details or {},
        "updated_at": _now_iso(),
    }
    write_json_atomic(checkpoint_file, payload)


def interrupt_pipeline(
    root_input: Optional[Union[str, Path]] = None,
    chapter: str = "",
    reason: str = "",
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    root = find_project_root(root_input)
    if not safe_id(chapter):
        raise ValueError("chapter id must be path-safe")
    status = get_pipeline_status(root, chapter)
    record_pipeline_checkpoint(
        root,
        chapter,
        stage=status.get("stage", "UNKNOWN"),
        state=status.get("state", "UNKNOWN"),
        interrupted=True,
        reason=reason,
        details=details,
    )
    status["status"] = "INTERRUPTED"
    status["interrupted"] = True
    status["interruption_reason"] = reason
    return status


def advance_pipeline(
    root_input: Optional[Union[str, Path]] = None,
    chapter: Optional[str] = None,
    stop_at: Optional[str] = None,
) -> Dict[str, Any]:
    root = find_project_root(root_input)
    project_file = root / ".novelforge" / "state" / "project.json"
    if not project_file.is_file():
        init_project(root)

    target_chapter = _resolve_chapter(root, chapter)
    if not safe_id(target_chapter):
        raise ValueError(f"chapter id is not path-safe: {target_chapter}")

    step_log = []

    while True:
        state_file = root / ".novelforge" / "state" / "chapters" / f"{target_chapter}.json"
        current_state = read_chapter_state(root, target_chapter)["status"] if state_file.is_file() else "PLANNED"

        if stop_at and (current_state == stop_at or STAGE_BY_STATE.get(current_state) == stop_at):
            record_pipeline_checkpoint(
                root,
                target_chapter,
                stage=STAGE_BY_STATE.get(current_state, "UNKNOWN"),
                state=current_state,
                interrupted=True,
                reason=f"Reached requested stop point: {stop_at}",
            )
            step_log.append(f"Paused at requested stop point: {stop_at}")
            break

        if current_state == "DELIVERABLE":
            record_pipeline_checkpoint(
                root,
                target_chapter,
                stage="COMPLETED",
                state="DELIVERABLE",
                interrupted=False,
                reason=None,
            )
            break

        if current_state == "PLANNED":
            bp_file = _get_blueprint_file(root, target_chapter)
            if not bp_file.is_file():
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="BLUEPRINT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Blueprint missing: {bp_file.relative_to(root)}",
                )
                step_log.append("Waiting for blueprint to be drafted")
                break
            try:
                validate_blueprint(root, target_chapter)
                step_log.append("Blueprint validated successfully (PLANNED -> BLUEPRINT_VALID)")
            except (BlueprintError, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="BLUEPRINT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Blueprint validation failed: {exc}",
                )
                step_log.append(f"Blueprint validation error: {exc}")
                break

        elif current_state == "BLUEPRINT_VALID":
            try:
                build_context(root, target_chapter)
                step_log.append("Context compiled and locked (BLUEPRINT_VALID -> CONTEXT_LOCKED)")
            except (ContextError, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="CONTEXT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Context build failed: {exc}",
                )
                step_log.append(f"Context compilation error: {exc}")
                break

        elif current_state == "CONTEXT_LOCKED":
            txt_file = _get_chapter_file(root, target_chapter)
            if not txt_file.is_file() or len(txt_file.read_text(encoding="utf-8").strip()) == 0:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="DRAFT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Chapter draft {txt_file.relative_to(root)} is missing or empty",
                )
                step_log.append("Waiting for chapter draft text")
                break
            try:
                transition_chapter(root, target_chapter, "DRAFTED")
                step_log.append("Chapter text registered (CONTEXT_LOCKED -> DRAFTED)")
            except (InvalidTransition, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="DRAFT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Draft transition failed: {exc}",
                )
                step_log.append(f"Draft transition error: {exc}")
                break

        elif current_state == "DRAFTED":
            tr_file = root / ".novelforge" / "reviews" / f"{target_chapter}-text.json"
            if not tr_file.is_file():
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="TEXT_REVIEW",
                    state=current_state,
                    interrupted=True,
                    reason=f"Text review artifact missing: .novelforge/reviews/{target_chapter}-text.json",
                )
                step_log.append("Waiting for text review")
                break
            try:
                tr_artifact = read_json(tr_file)
                if tr_artifact.get("result") != "PASS":
                    record_pipeline_checkpoint(
                        root,
                        target_chapter,
                        stage="TEXT_REVIEW",
                        state=current_state,
                        interrupted=True,
                        reason="Text review failed; repair patch required",
                        details={"checks": tr_artifact.get("checks", [])},
                    )
                    step_log.append("Text review did not pass; waiting for patch")
                    break
                apply_review(root, tr_artifact)
                step_log.append("Text review applied successfully (DRAFTED -> TEXT_PASS)")
            except (ReviewError, InvalidTransition, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="TEXT_REVIEW",
                    state=current_state,
                    interrupted=True,
                    reason=f"Applying text review failed: {exc}",
                )
                step_log.append(f"Text review application error: {exc}")
                break

        elif current_state == "TEXT_PASS":
            er_file = root / ".novelforge" / "reviews" / f"{target_chapter}-engine.json"
            if not er_file.is_file():
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="ENGINE_REVIEW",
                    state=current_state,
                    interrupted=True,
                    reason=f"Engine review artifact missing: .novelforge/reviews/{target_chapter}-engine.json",
                )
                step_log.append("Waiting for engine review")
                break
            try:
                er_artifact = read_json(er_file)
                if er_artifact.get("result") != "PASS":
                    record_pipeline_checkpoint(
                        root,
                        target_chapter,
                        stage="ENGINE_REVIEW",
                        state=current_state,
                        interrupted=True,
                        reason="Engine review failed; repair patch required",
                        details={"checks": er_artifact.get("checks", [])},
                    )
                    step_log.append("Engine review did not pass; waiting for patch")
                    break
                apply_review(root, er_artifact)
                step_log.append("Engine review applied successfully (TEXT_PASS -> ENGINE_PASS)")
            except (ReviewError, InvalidTransition, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="ENGINE_REVIEW",
                    state=current_state,
                    interrupted=True,
                    reason=f"Applying engine review failed: {exc}",
                )
                step_log.append(f"Engine review application error: {exc}")
                break

        elif current_state == "ENGINE_PASS":
            proposal_file = root / "settlements" / f"{target_chapter}.json"
            target_st = root / ".novelforge" / "settlements" / f"{target_chapter}.json"
            st_artifact = None
            if proposal_file.is_file():
                st_artifact = read_json(proposal_file)
            elif target_st.is_file():
                raw = read_json(target_st)
                if raw.get("status") == "APPLIED" and raw.get("applied") is True:
                    try:
                        transition_chapter(root, target_chapter, "SETTLED")
                        step_log.append("Settlement already applied (ENGINE_PASS -> SETTLED)")
                        continue
                    except (InvalidTransition, OSError) as exc:
                        record_pipeline_checkpoint(
                            root, target_chapter, stage="SETTLEMENT", state=current_state,
                            interrupted=True, reason=f"Settlement transition failed: {exc}",
                        )
                        break
                else:
                    st_artifact = raw
                    target_st.unlink()
            else:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="SETTLEMENT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Settlement artifact missing: settlements/{target_chapter}.json",
                )
                step_log.append("Waiting for settlement artifact")
                break
            try:
                apply_settlement(root, st_artifact)
                step_log.append("Settlement applied successfully (ENGINE_PASS -> SETTLED)")
            except (SettlementError, InvalidTransition, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="SETTLEMENT",
                    state=current_state,
                    interrupted=True,
                    reason=f"Applying settlement failed: {exc}",
                )
                step_log.append(f"Settlement application error: {exc}")
                break

        elif current_state == "SETTLED":
            try:
                rebuild_wiki(root)
                transition_chapter(root, target_chapter, "DELIVERABLE")
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="COMPLETED",
                    state="DELIVERABLE",
                    interrupted=False,
                    reason=None,
                )
                step_log.append("Wiki rebuilt and chapter marked deliverable (SETTLED -> DELIVERABLE)")
                break
            except (InvalidTransition, OSError, ValueError) as exc:
                record_pipeline_checkpoint(
                    root,
                    target_chapter,
                    stage="DELIVERY",
                    state=current_state,
                    interrupted=True,
                    reason=f"Delivery transition failed: {exc}",
                )
                step_log.append(f"Delivery transition error: {exc}")
                break

    final_status = get_pipeline_status(root, target_chapter)
    final_status["steps_executed"] = step_log
    return final_status


def resume_pipeline(
    root_input: Optional[Union[str, Path]] = None,
    chapter: Optional[str] = None,
    stop_at: Optional[str] = None,
) -> Dict[str, Any]:
    root = find_project_root(root_input)
    target_chapter = _resolve_chapter(root, chapter)
    checkpoint_file = _pipeline_checkpoint_path(root)
    if checkpoint_file.is_file():
        try:
            cp = read_json(checkpoint_file)
            if cp.get("interrupted"):
                cp["interrupted"] = False
                cp["resumed_at"] = _now_iso()
                write_json_atomic(checkpoint_file, cp)
        except (OSError, ValueError, TypeError):
            pass
    return advance_pipeline(root, target_chapter, stop_at=stop_at)
