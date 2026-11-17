"""Immutable, evidence-aware actions derived from already-decided planning data.

This module owns the action-ordering seam.  It accepts typed planning inputs,
turns them into a compact immutable plan, and never reads files or recalculates
school/pathway decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date as CalendarDate
from enum import Enum
import hashlib
import re
from typing import Any, Iterable, Mapping

if __package__:
    from .contracts import EvidenceStatus
    from .planning_profile import PlanningProfile
else:  # pragma: no cover - direct scripts-path compatibility
    from contracts import EvidenceStatus
    from planning_profile import PlanningProfile


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_REASON_CODE = re.compile(r"^[a-z][a-z0-9_-]{0,127}$")
_PHASES = ("现在", "本学期", "下一阶段", "报名前", "出分后")
_URGENCY = frozenset({"urgent", "high", "normal", "low"})
_VALUE = frozenset({"high", "medium", "low"})
_EFFORT = frozenset({"low", "medium", "high"})
_EFFORT_ORDER = {"low": 0, "medium": 1, "high": 2}
_STATUS_ORDER = (
    EvidenceStatus.CONFLICT,
    EvidenceStatus.MASKED,
    EvidenceStatus.PARTIAL,
    EvidenceStatus.MISSING,
    EvidenceStatus.INFERRED,
    EvidenceStatus.REFERENCE,
    EvidenceStatus.CORROBORATED,
    EvidenceStatus.OFFICIAL,
)
_ISO_DATE = re.compile(r"(?<![0-9])(20[0-9]{2}-[0-9]{2}-[0-9]{2})(?![0-9])")
_ACTIONABLE_DECISIONS = frozenset({"主攻", "重点准备", "备选", "观察"})
_MAX_SAFE_ID_LENGTH = 128
_LONG_ID_DIGEST_LENGTH = 32
_UNCERTAINTY_REDUCTION_REASONS = frozenset({
    "evidence_gap_review",
    "rank_context_review",
    "pathway_evidence_review",
    "pathway_scope_review",
})


def _text(value: Any, name: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{name} must be a non-empty trimmed string")
    if len(value) > 2048 or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{name} must be a bounded single-line string")
    return value


def _ids(value: Iterable[str], name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a collection of IDs")
    items = tuple(value)
    if any(not isinstance(item, str) or _SAFE_ID.fullmatch(item) is None for item in items):
        raise ValueError(f"{name} must contain safe IDs")
    if len(items) != len(set(items)):
        raise ValueError(f"{name} must be unique")
    return tuple(sorted(items))


def _criteria(value: Iterable[str]) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError("completion_criteria must be a collection")
    items = tuple(_text(item, "completion criterion") for item in value)
    if not items or len(items) != len(set(items)):
        raise ValueError("completion_criteria must be non-empty and unique")
    return items


def _status(value: Any) -> EvidenceStatus:
    if isinstance(value, EvidenceStatus):
        return value
    try:
        return EvidenceStatus(value)
    except (TypeError, ValueError) as error:
        raise ValueError("evidence_status must be an EvidenceStatus") from error


def _aggregate_status(values: Iterable[EvidenceStatus]) -> EvidenceStatus:
    present = set(values)
    for status in _STATUS_ORDER:
        if status in present:
            return status
    return EvidenceStatus.MISSING


@dataclass(frozen=True, init=False)
class ActionItem:
    """One factory-authenticated, JSON-safe next action."""

    action_id: str
    title: str
    completion_criteria: tuple[str, ...]
    phase: str
    deadline: str | None
    urgency: str
    strategic_value: str
    effort: str
    blocking: bool
    depends_on: tuple[str, ...]
    school_ids: tuple[str, ...]
    pathway_ids: tuple[str, ...]
    reason_code: str
    reason: str
    consequence: str
    evidence_status: EvidenceStatus
    source_ids: tuple[str, ...]

    def __init__(self) -> None:
        raise TypeError("ActionItem is factory-only")

    @classmethod
    def create(cls, **values: Any) -> "ActionItem":
        expected = {item.name for item in fields(cls)}
        if set(values) != expected:
            raise TypeError("ActionItem factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        for name in ("action_id", "title", "reason_code", "reason", "consequence"):
            value = _text(getattr(self, name), name)
            assert value is not None
            object.__setattr__(self, name, value)
        if _SAFE_ID.fullmatch(self.action_id) is None:
            raise ValueError("action_id must use safe-ID syntax")
        if _REASON_CODE.fullmatch(self.reason_code) is None:
            raise ValueError("reason_code must use safe-ID syntax")
        object.__setattr__(self, "completion_criteria", _criteria(self.completion_criteria))
        if self.phase not in _PHASES:
            raise ValueError("phase is unsupported")
        if self.deadline is not None:
            deadline = _text(self.deadline, "deadline")
            assert deadline is not None
            try:
                CalendarDate.fromisoformat(deadline)
            except ValueError as error:
                raise ValueError("deadline must be a concrete date") from error
            object.__setattr__(self, "deadline", deadline)
        if self.urgency not in _URGENCY:
            raise ValueError("urgency is unsupported")
        if self.strategic_value not in _VALUE:
            raise ValueError("strategic_value is unsupported")
        if self.effort not in _EFFORT:
            raise ValueError("effort is unsupported")
        if not isinstance(self.blocking, bool):
            raise TypeError("blocking must be boolean")
        object.__setattr__(self, "depends_on", _ids(self.depends_on, "depends_on"))
        object.__setattr__(self, "school_ids", _ids(self.school_ids, "school_ids"))
        object.__setattr__(self, "pathway_ids", _ids(self.pathway_ids, "pathway_ids"))
        object.__setattr__(self, "evidence_status", _status(self.evidence_status))
        object.__setattr__(self, "source_ids", _ids(self.source_ids, "source_ids"))

    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: (
                getattr(self, item.name).value
                if isinstance(getattr(self, item.name), Enum)
                else list(getattr(self, item.name))
                if isinstance(getattr(self, item.name), tuple)
                else getattr(self, item.name)
            )
            for item in fields(self)
        }


def _pathway_value(pathway: Any, name: str, default: Any) -> Any:
    if isinstance(pathway, Mapping):
        return pathway.get(name, default)
    return getattr(pathway, name, default)


def _candidate(**values: Any) -> ActionItem:
    return ActionItem.create(**values)


def _pathway_action_id(prefix: str, policy_id: str) -> str:
    """Keep short policy IDs readable and bound long IDs with a stable digest."""

    value = f"{prefix}:{policy_id}"
    if len(value) <= _MAX_SAFE_ID_LENGTH:
        return value
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:_LONG_ID_DIGEST_LENGTH]
    readable_length = (
        _MAX_SAFE_ID_LENGTH - len(prefix) - len(digest) - 2
    )
    if readable_length < 1:  # pragma: no cover - internal prefixes are bounded
        raise ValueError("action ID prefix leaves no room for a policy binding")
    return f"{prefix}:{policy_id[:readable_length]}:{digest}"


def _merge(items: Iterable[ActionItem]) -> tuple[ActionItem, ...]:
    merged: dict[str, ActionItem] = {}
    for item in items:
        current = merged.get(item.action_id)
        if current is None:
            merged[item.action_id] = item
            continue
        if (
            current.title != item.title
            or current.reason_code != item.reason_code
            or current.phase != item.phase
            or current.deadline != item.deadline
        ):
            raise ValueError("duplicate action identity has conflicting semantics")
        merged[item.action_id] = ActionItem.create(
            **{
                **current.to_dict(),
                "completion_criteria": list(dict.fromkeys((*current.completion_criteria, *item.completion_criteria))),
                "blocking": current.blocking or item.blocking,
                "depends_on": sorted(set(current.depends_on) | set(item.depends_on)),
                "school_ids": sorted(set(current.school_ids) | set(item.school_ids)),
                "pathway_ids": sorted(set(current.pathway_ids) | set(item.pathway_ids)),
                "source_ids": sorted(set(current.source_ids) | set(item.source_ids)),
                "evidence_status": _aggregate_status((current.evidence_status, item.evidence_status)),
            }
        )
    return tuple(merged[key] for key in sorted(merged))


def _priority(item: ActionItem) -> tuple[Any, ...]:
    phase = _PHASES.index(item.phase)
    if item.deadline is not None:
        concrete = CalendarDate.fromisoformat(item.deadline).isoformat()
        return (0, concrete, item.action_id)
    if item.blocking:
        category = 0
    elif (
        item.reason_code == "long_lead_readiness"
        and item.strategic_value == "high"
    ):
        category = 1
    elif item.reason_code in _UNCERTAINTY_REDUCTION_REASONS:
        category = 2
    else:
        category = 3
    return (
        1,
        category,
        phase,
        _EFFORT_ORDER[item.effort],
        item.action_id,
    )


def _deadline_from_timeline(timeline: tuple[str, ...]) -> str | None:
    """Return only a validated authenticated concrete date."""

    for item in timeline:
        match = _ISO_DATE.search(item)
        if match is not None:
            value = match.group(1)
            try:
                CalendarDate.fromisoformat(value)
            except ValueError:
                continue
            return value
    return None


def _readiness_details(profile: PlanningProfile | None) -> tuple[str, str, tuple[str, ...]]:
    """Use finite profile fields, never the meaning of a free-text concern."""

    if profile is None:
        return (
            "本学期",
            "路径给出了需要尽早启动的准备动作",
            ("完成一项与目标路径直接对应的准备材料或能力证明",),
        )
    phase = {"高一": "下一阶段", "高二": "本学期", "高三": "现在"}.get(
        profile.grade, "本学期"
    )
    has_existing_material = bool(profile.awards or profile.activities)
    concern_count = len(profile.concerns)
    if has_existing_material:
        criterion = "将已有准备材料与目标路径要求逐项核验并补齐缺口"
        material_state = "画像记录已有可核验准备材料"
    else:
        criterion = "完成一项与目标路径直接对应的准备材料或能力证明"
        material_state = "画像尚未记录可核验准备材料"
    concern_state = (
        "已记录关注项，需在本次核验中逐项确认" if concern_count else "未记录额外关注项"
    )
    return phase, f"{material_state}；{concern_state}", (criterion,)


def order_actions(items: Iterable[ActionItem]) -> tuple[ActionItem, ...]:
    """Fail closed on invalid dependencies; otherwise use stable Kahn ordering."""

    actions = tuple(items)
    if not all(isinstance(item, ActionItem) for item in actions):
        raise TypeError("actions must contain ActionItem values")
    by_id = {item.action_id: item for item in actions}
    if len(by_id) != len(actions):
        raise ValueError("action IDs must be unique")
    unresolved = {
        item.action_id: set(item.depends_on)
        for item in actions
    }
    unknown = set().union(*unresolved.values()).difference(by_id)
    if unknown:
        raise ValueError("action dependency is unknown")
    ordered: list[ActionItem] = []
    while unresolved:
        ready = tuple(
            (by_id[action_id] for action_id, dependencies in unresolved.items() if not dependencies),
        )
        if not ready:
            raise ValueError("action dependency cycle")
        item = min(ready, key=_priority)
        ordered.append(item)
        unresolved.pop(item.action_id)
        for dependencies in unresolved.values():
            dependencies.discard(item.action_id)
    return tuple(ordered)


def build_action_plan(
    profile: PlanningProfile | None,
    rank_scenario: Any,
    recommendations: Iterable[Any],
    pathways: Iterable[Any],
    evidence_status: EvidenceStatus,
) -> tuple[ActionItem, ...]:
    """Derive one deterministic action plan from authenticated decisions only."""

    if profile is not None and not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile or None")
    status = _status(evidence_status)
    accepted_statuses = {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
    ordinary_batch_dependencies = (
        () if status in accepted_statuses else ("evidence-gap-review",)
    )
    rank_status = _status(getattr(rank_scenario, "status", EvidenceStatus.MISSING))
    rank_dependencies = (
        ()
        if rank_status in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}
        else ("rank-context-review",)
    )
    recommendation_items = tuple(recommendations)
    pathway_items = tuple(pathways)
    recognized_pathways: list[Any] = []
    candidates: list[ActionItem] = []

    for pathway in pathway_items:
        policy_id = _pathway_value(pathway, "policy_id", None)
        if not isinstance(policy_id, str) or _SAFE_ID.fullmatch(policy_id) is None:
            raise ValueError("pathways must provide a safe policy_id")
        pathway_state = _pathway_value(pathway, "status", None)
        investment_decision = _pathway_value(pathway, "investment_decision", None)
        if pathway_state not in {"formal", "pending_verification"}:
            continue
        recognized_pathways.append(pathway)
        timeline = tuple(_pathway_value(pathway, "timeline", ()))
        preparation = tuple(_pathway_value(pathway, "preparation_actions", ()))
        missing = tuple(_pathway_value(pathway, "missing_constraints", ()))
        source_ids = _ids(_pathway_value(pathway, "source_ids", ()), "pathway source_ids")
        if not source_ids:
            source_ids = _ids(
                _pathway_value(pathway, "policy_source_ids", ()),
                "pathway policy_source_ids",
            )
        pathway_status = _status(_pathway_value(pathway, "evidence_status", status))
        if pathway_state == "formal" and missing:
            raise ValueError("formal pathways cannot carry missing constraints")
        if pathway_state == "pending_verification" and not missing:
            raise ValueError("pending pathways require an explicit constraint")
        unverified_observation = (
            pathway_state == "pending_verification"
            and policy_id.startswith("pathway-observation-")
            and _pathway_value(pathway, "target_year", None) is None
            and _pathway_value(pathway, "data_year", None) is None
            and _pathway_value(pathway, "year_basis", "unverified")
            == "unverified"
        )
        deadline = _deadline_from_timeline(timeline)
        pathway_evidence_id = None
        qualification_id = None
        pathway_dependencies: tuple[str, ...] = ()
        if pathway_state == "pending_verification":
            if pathway_status not in accepted_statuses:
                pathway_evidence_id = _pathway_action_id(
                    "pathway-evidence-review", policy_id
                )
                candidates.append(_candidate(
                    action_id=pathway_evidence_id, title="补齐并复核路径政策证据",
                    completion_criteria=("获得可复核路径政策来源并重新核验资格",),
                    phase="现在", deadline=None,
                    urgency="high", strategic_value="high", effort="low", blocking=True,
                    depends_on=(), school_ids=(), pathway_ids=(policy_id,),
                    reason_code="pathway_evidence_review",
                    reason="当前路径政策证据不足以支持资格或申报结论",
                    consequence="证据未补齐前只能保留待核验状态",
                    evidence_status=pathway_status, source_ids=source_ids,
                ))
            qualification_id = _pathway_action_id(
                "qualification-blocker", policy_id
            )
            candidates.append(_candidate(
                action_id=qualification_id, title="核验路径资格与待补约束",
                completion_criteria=("逐项确认待核验资格并留存可追溯依据",),
                phase="现在", deadline=None,
                urgency="high", strategic_value="high", effort="low", blocking=True,
                depends_on=((pathway_evidence_id,) if pathway_evidence_id else ()),
                school_ids=(), pathway_ids=(policy_id,),
                reason_code="qualification_blocker",
                reason="路径仍有待核验资格、约束或政策字段",
                consequence="资格未确认前不能将该路径作为可申报结论",
                evidence_status=pathway_status, source_ids=source_ids,
            ))
            pathway_dependencies = (qualification_id,)
        if investment_decision not in _ACTIONABLE_DECISIONS:
            continue
        if deadline is not None:
            candidates.append(_candidate(
                action_id=_pathway_action_id("deadline-window", policy_id), title="在报名窗口前完成路径政策复核",
                completion_criteria=("核对当年简章、资格与报名窗口",), phase="报名前", deadline=deadline,
                urgency="urgent", strategic_value="high", effort="medium", blocking=False, depends_on=pathway_dependencies,
                school_ids=(), pathway_ids=(policy_id,), reason_code="deadline_window",
                reason="路径时间线要求在报名窗口前完成复核", consequence="错过窗口后无法以当前路径提交申请",
                evidence_status=pathway_status, source_ids=source_ids,
            ))
        if not unverified_observation and (
            preparation or (profile is not None and profile.concerns)
        ):
            readiness_phase, readiness_reason, readiness_criteria = _readiness_details(profile)
            candidates.append(_candidate(
                action_id=_pathway_action_id("long-lead-readiness", policy_id), title="补齐长期路径准备缺口",
                completion_criteria=readiness_criteria, phase=readiness_phase, deadline=None,
                urgency="high", strategic_value="high", effort="high", blocking=False, depends_on=pathway_dependencies,
                school_ids=(), pathway_ids=(policy_id,), reason_code="long_lead_readiness",
                reason=readiness_reason,
                consequence="准备周期不足会降低后续资格或材料竞争力",
                evidence_status=pathway_status, source_ids=source_ids,
            ))

    if status not in accepted_statuses:
        candidates.append(_candidate(
            action_id="evidence-gap-review", title="补齐或复核关键证据缺口",
            completion_criteria=("获得可复核来源并重新运行规划计算",), phase="现在", deadline=None,
            urgency="high", strategic_value="high", effort="low", blocking=False, depends_on=(),
            school_ids=(), pathway_ids=(), reason_code="evidence_gap_review",
            reason="当前证据未提供可直接作为定论的完整覆盖", consequence="证据缺口会保留不确定性，不能扩大为确定结论",
            evidence_status=status, source_ids=(),
        ))
    if rank_status not in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
        rank_source_ids = ()
        if rank_status is not EvidenceStatus.MISSING:
            rank_source_ids = _ids(getattr(rank_scenario, "source_ids", ()), "rank source_ids")
        candidates.append(_candidate(
            action_id="rank-context-review", title="补充可核验的位次定位依据",
            completion_criteria=("提供可复核的成绩或位次材料并重新计算",), phase="现在", deadline=None,
            urgency="high", strategic_value="high", effort="low", blocking=False, depends_on=(),
            school_ids=(), pathway_ids=(), reason_code="rank_context_review",
            reason="当前未提供可直接校准的位次依据", consequence="普通批范围不能被扩大为精确录取判断",
            evidence_status=rank_status, source_ids=rank_source_ids,
        ))
    if recommendation_items:
        school_ids = tuple(f"school:{index}" for index, _ in enumerate(recommendation_items, 1))
        candidates.append(_candidate(
            action_id="school-group-review", title="复核目标院校专业组与选科要求",
            completion_criteria=("逐校确认当年章程、专业组和选科要求",), phase="下一阶段", deadline=None,
            urgency="normal", strategic_value="medium", effort="medium", blocking=False, depends_on=tuple((*ordinary_batch_dependencies, *rank_dependencies)),
            school_ids=school_ids, pathway_ids=(), reason_code="school_group_review",
            reason="普通批建议必须以当年学校公告复核", consequence="未复核可能使院校或专业组判断失效",
            evidence_status=status, source_ids=(),
        ))
    else:
        candidates.append(_candidate(
            action_id="school-scope-review", title="确认普通批院校范围与可用覆盖",
            completion_criteria=("确认是否已有可展示院校，或记录当前覆盖限制",), phase="下一阶段", deadline=None,
            urgency="normal", strategic_value="medium", effort="low", blocking=False, depends_on=tuple((*ordinary_batch_dependencies, *rank_dependencies)),
            school_ids=(), pathway_ids=(), reason_code="school_scope_review",
            reason="当前没有可展示的普通批代表院校", consequence="不能将空结果解读为没有符合院校",
            evidence_status=status, source_ids=(),
        ))
    if not recognized_pathways:
        candidates.append(_candidate(
            action_id="pathway-scope-review", title="确认多元路径政策覆盖范围",
            completion_criteria=("确认是否存在经认证的路径政策，或记录当前缺口",), phase="下一阶段", deadline=None,
            urgency="normal", strategic_value="medium", effort="low", blocking=False, depends_on=(),
            school_ids=(), pathway_ids=(), reason_code="pathway_scope_review",
            reason="当前没有可展开的多元路径政策结果", consequence="不能把缺少政策材料误写为不具备路径资格",
            evidence_status=EvidenceStatus.MISSING, source_ids=(),
        ))
    candidates.append(_candidate(
        action_id="final-official-review", title="在正式填报或申报前完成官方最终复核",
        completion_criteria=("以省教育考试院和高校当年正式发布确认最终选择",), phase="报名前", deadline=None,
        urgency="normal", strategic_value="high", effort="low", blocking=False, depends_on=(),
        school_ids=(), pathway_ids=(), reason_code="final_official_review",
        reason="报告只使用当前已认证材料，最终规则仍以当年正式发布为准", consequence="未最终复核不能据此作出录取或资格承诺",
        evidence_status=status, source_ids=(),
    ))
    return order_actions(_merge(candidates))


__all__ = ["ActionItem", "build_action_plan", "order_actions"]
