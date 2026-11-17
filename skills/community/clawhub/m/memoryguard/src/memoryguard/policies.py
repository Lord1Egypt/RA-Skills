"""Pro 策略接口预留。

Community 版使用基础实现（auto_organizer.py 内置），
Pro 版后续替换为高级实现（Rust 闭源模块）。

设计原则：
- 接口先行，实现后置
- Community 版不 import 这个文件，Pro 版注入
- 所有方法返回结构化数据，不直接操作 store

这个文件是 Pro 扩展点：Community 版的 auto_organizer.py 不依赖它，
Pro 版通过 PolicyRegistry 注入高级策略实现替换默认行为。
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from .auto_organizer import SECRET_PATTERNS


# ===========================================================================
# 策略接口基类
# ===========================================================================


class OrganizerPolicy:
    """自动整理策略接口。

    Community 版由 auto_organizer.py 内置启发式逻辑实现；
    Pro 版替换为基于 embedding + LLM 的高级分类/去重/冲突检测。
    """

    policy_name: str = "organizer"

    def classify(self, content: str, metadata: dict) -> str:
        """分类策略：返回 MemoryKind 值。

        返回值：preference / fact / project / procedure / episode / correction

        Pro 版：使用 embedding + 上下文感知分类，支持多语言和隐式意图识别。
        """
        raise NotImplementedError

    def should_supersede(self, new_content: str, old_record: dict) -> bool:
        """是否覆盖旧记录。

        Pro 版：基于语义等价性 + 置信度对比 + 锁定策略综合判断，
        支持部分覆盖和版本链追溯。
        """
        raise NotImplementedError

    def should_merge(self, new_content: str, existing_records: list[dict]) -> bool:
        """是否合并 provenance（同义重复）。

        Pro 版：跨语言改写检测 + 语义归一化 + 自动去重合并策略。
        """
        raise NotImplementedError

    def should_conflict(self, new_content: str, existing_records: list[dict]) -> bool:
        """是否进入冲突组（互斥内容）。

        Pro 版：基于立场检测 + 领域知识图谱判断互斥性，
        支持细粒度冲突分类（事实冲突/偏好冲突/时序冲突）。
        """
        raise NotImplementedError


class DecayPolicy:
    """衰减策略接口。

    Community 版提供基础时间衰减（高阈值，极少归档）；
    Pro 版实现基于时间衰减 + 访问频率 + 纠正次数的动态归档。
    """

    policy_name: str = "decay"

    def compute_decay_score(self, record: dict, factors: dict) -> float:
        """计算衰减分数 [0.0, 1.0]，越高越接近归档。

        Pro 版：多因子加权模型（age/access_count/correction_count/recency/visibility），
        支持 custom decay curve 和 kind-aware 权重。
        """
        raise NotImplementedError

    def should_archive(self, record: dict, score: float) -> bool:
        """是否归档（score 超过阈值且非锁定）。

        Pro 版：分阶段归档（cold -> frozen -> archived），
        支持 kind-aware 阈值和人工审批触发。
        """
        raise NotImplementedError

    def decay_factors(self, record: dict) -> dict:
        """提取衰减因子。

        返回 dict 含：age_days / access_count / correction_count / last_accessed_at

        Pro 版：从访问日志和纠正历史中提取完整因子集，
        包括引用次数、下游影响、关联记忆活跃度等。
        """
        raise NotImplementedError


class SupersedePolicy:
    """覆盖策略接口。

    Community 版由 auto_organizer.py 内置纠错检测 + locked 判断；
    Pro 版增加置信度阈值 + 版本链完整性 + 回滚风险评估。
    """

    policy_name: str = "supersede"

    def should_auto_supersede(self, new_record: dict, old_record: dict) -> tuple[bool, str]:
        """返回 (是否覆盖, 原因)。

        Pro 版：语义等价性 + 置信度差值 + 锁定状态 + 人工审批阈值，
        支持部分覆盖和条件覆盖。
        """
        raise NotImplementedError

    def is_locked(self, record: dict) -> bool:
        """是否锁定（禁止自动覆盖）。

        Pro 版：支持分级锁定（soft/hard/permanent）和条件锁定期。
        """
        raise NotImplementedError

    def confidence_threshold(self, record: dict) -> float:
        """覆盖所需的置信度阈值。

        Pro 版：按 kind 和 provenance 强度动态调整阈值，
        支持来源可信度和时间衰减加权。
        """
        raise NotImplementedError


class QuarantinePolicy:
    """隔离策略接口。

    Community 版由 auto_organizer.py 内置正则检测 secret/token；
    Pro 版增加 entropy 分析 + 上下文感知 + PII 检测。
    """

    policy_name: str = "quarantine"

    def detect_secrets(self, content: str) -> list[dict]:
        """检测敏感信息，返回匹配列表。

        每个元素：{"pattern": str, "match": str, "start": int, "end": int}

        Pro 版：entropy 分析 + 环境变量泄漏检测 + 自定义规则引擎 + PII 识别。
        """
        raise NotImplementedError

    def should_quarantine(self, record: dict) -> tuple[bool, str]:
        """返回 (是否隔离, 原因)。

        Pro 版：综合 secret/PII/toxic content/合规策略，
        支持分级隔离和自动脱敏建议。
        """
        raise NotImplementedError

    def release_criteria(self, quarantine_entry: dict) -> bool:
        """释放条件（脱敏后可释放）。

        Pro 版：脱敏验证 + 人工审批 + 审计日志 + 释放后监控。
        """
        raise NotImplementedError


class ReportGenerator:
    """治理报告生成器接口。

    Community 版提供基础 JSON 聚合；
    Pro 版支持 HTML/PDF 渲染 + 趋势分析 + 可视化。
    """

    policy_name: str = "report"

    def generate_weekly_report(self, store_data: dict) -> dict:
        """生成周报：写入/覆盖/冲突/隔离统计。

        Pro 版：趋势对比 + 异常检测 + 治理建议 + Agent 活跃度分析。
        """
        raise NotImplementedError

    def generate_health_report(self, store_data: dict) -> dict:
        """生成健康报告：覆盖率/冲突率/隔离率/置信度分布。

        Pro 版：健康评分模型 + 风险预警 + 记忆质量评估 + 改进建议。
        """
        raise NotImplementedError

    def format_report(self, data: dict, format: str) -> str:
        """格式化报告。

        format 支持：json（Community）/ html、pdf（Pro）

        Pro 版：HTML 模板渲染 + PDF 导出 + 自定义主题。
        """
        raise NotImplementedError


# ===========================================================================
# CommunityPolicy：Community 版默认实现
# ===========================================================================


# 分类关键词（镜像 auto_organizer._classify，保持行为一致）
_CLASSIFY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("preference", ["偏好", "喜欢", "prefer", "like", "习惯"]),
    ("procedure", ["步骤", "流程", "procedure", "step", "how to"]),
    ("project", ["项目", "project", "仓库", "repo"]),
    ("episode", ["事件", "episode", "发生", "happened"]),
    ("correction", ["纠正", "更正", "correction", "actually", "不对", "错误", "应该是"]),
]

# 纠错关键词（镜像 auto_organizer._is_correction）
_CORRECTION_KEYWORDS: list[str] = [
    "纠正", "更正", "correction", "actually",
    "不对", "错误", "应该是", "update", "更新",
]

# 偏好关键词（镜像 auto_organizer._is_conflict）
_PREFERENCE_KEYWORDS: list[str] = ["偏好", "喜欢", "prefer"]


def _tokenize(text: str) -> set[str]:
    """中英文混合分词（与 auto_organizer._tokenize 一致）。"""
    return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[\u4e00-\u9fff]", text.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard 相似度（与 auto_organizer._jaccard 一致）。"""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class CommunityPolicy(
    OrganizerPolicy,
    DecayPolicy,
    SupersedePolicy,
    QuarantinePolicy,
    ReportGenerator,
):
    """Community 版默认策略实现。

    复用 auto_organizer.py 的启发式逻辑，通过 PolicyRegistry 注册为默认实现。
    Pro 版可通过 PolicyRegistry.register() 替换为高级实现。

    所有方法均为纯函数风格（不依赖 store 实例），
    输入 dict / str，输出 dict / tuple / str / bool。
    """

    policy_name: str = "community"

    # ------------------------------------------------------------------
    # OrganizerPolicy
    # ------------------------------------------------------------------

    def classify(self, content: str, metadata: dict) -> str:
        """启发式分类（镜像 auto_organizer._classify）。"""
        text = content.lower()
        for kind, keywords in _CLASSIFY_KEYWORDS:
            if any(k in text for k in keywords):
                return kind
        return "fact"

    def should_supersede(self, new_content: str, old_record: dict) -> bool:
        """纠错内容且旧记录未锁定时覆盖（镜像 auto_organizer organize 流程 3a）。"""
        if old_record.get("locked", False):
            return False
        text = new_content.lower()
        return any(k in text for k in _CORRECTION_KEYWORDS)

    def should_merge(self, new_content: str, existing_records: list[dict]) -> bool:
        """高相似度且非纠错时合并 provenance（镜像 auto_organizer organize 流程 3c）。"""
        text = new_content.lower()
        if any(k in text for k in _CORRECTION_KEYWORDS):
            return False
        content_tokens = _tokenize(new_content)
        if not content_tokens:
            return False
        for rec in existing_records:
            rec_tokens = _tokenize(rec.get("body", ""))
            if _jaccard(content_tokens, rec_tokens) >= 0.85:
                return True
        return False

    def should_conflict(self, new_content: str, existing_records: list[dict]) -> bool:
        """同主题不同结论时进入冲突组（镜像 auto_organizer._is_conflict）。"""
        text = new_content.lower()
        if not any(k in text for k in _PREFERENCE_KEYWORDS):
            return False
        for rec in existing_records:
            rec_text = rec.get("body", "").lower()
            if any(k in rec_text for k in _PREFERENCE_KEYWORDS) and text != rec_text:
                return True
        return False

    # ------------------------------------------------------------------
    # DecayPolicy
    # ------------------------------------------------------------------

    def decay_factors(self, record: dict) -> dict:
        """提取基础衰减因子。"""
        factors: dict[str, Any] = {
            "age_days": 0,
            "access_count": record.get("access_count", 0),
            "correction_count": len(record.get("supersedes", [])),
            "last_accessed_at": record.get("updated_at", ""),
        }
        created_at = record.get("created_at", "")
        if created_at:
            try:
                created = datetime.fromisoformat(created_at)
                now = datetime.now(timezone.utc)
                factors["age_days"] = max(0, (now - created).days)
            except (ValueError, TypeError):
                pass
        return factors

    def compute_decay_score(self, record: dict, factors: dict) -> float:
        """基础衰减分数：年龄权重 + 低置信度加权。

        Community 版使用高阈值，极少触发归档。
        """
        age_days = factors.get("age_days", 0)
        confidence = record.get("confidence", 0.5)
        age_score = min(0.6, age_days / 365.0 * 0.3)
        confidence_penalty = (1.0 - confidence) * 0.2
        return round(min(1.0, age_score + confidence_penalty), 4)

    def should_archive(self, record: dict, score: float) -> bool:
        """Community 版高阈值归档（score > 0.85 且未锁定）。"""
        if record.get("locked", False):
            return False
        return score > 0.85

    # ------------------------------------------------------------------
    # SupersedePolicy
    # ------------------------------------------------------------------

    def should_auto_supersede(
        self, new_record: dict, old_record: dict
    ) -> tuple[bool, str]:
        """纠错检测 + 锁定检查（镜像 auto_organizer organize 流程 3a）。"""
        if old_record.get("locked", False):
            return (False, "old record is locked")
        body = new_record.get("body", "")
        text = body.lower()
        if any(k in text for k in _CORRECTION_KEYWORDS):
            return (True, "correction keywords detected")
        metadata = new_record.get("metadata", {})
        if isinstance(metadata, dict) and metadata.get("type") == "correction":
            return (True, "metadata marked as correction")
        return (False, "not a correction")

    def is_locked(self, record: dict) -> bool:
        """检查 locked 字段。"""
        return bool(record.get("locked", False))

    def confidence_threshold(self, record: dict) -> float:
        """Community 版统一阈值 0.45（与 auto_organizer LOW_CONFIDENCE 阈值一致）。"""
        return 0.45

    # ------------------------------------------------------------------
    # QuarantinePolicy
    # ------------------------------------------------------------------

    def detect_secrets(self, content: str) -> list[dict]:
        """正则检测敏感信息（复用 auto_organizer.SECRET_PATTERNS）。"""
        matches: list[dict[str, Any]] = []
        for pattern in SECRET_PATTERNS:
            m = pattern.search(content)
            if m:
                matches.append({
                    "pattern": pattern.pattern[:80],
                    "match": m.group()[:80],
                    "start": m.start(),
                    "end": m.end(),
                })
        return matches

    def should_quarantine(self, record: dict) -> tuple[bool, str]:
        """检测 body 中的敏感信息。"""
        body = record.get("body", "")
        hits = self.detect_secrets(body)
        if hits:
            reason = f"detected {len(hits)} secret pattern(s): {hits[0]['pattern']}"
            return (True, reason)
        return (False, "")

    def release_criteria(self, quarantine_entry: dict) -> bool:
        """Community 版：released 标记为 True 即可释放。"""
        return bool(quarantine_entry.get("released", False))

    # ------------------------------------------------------------------
    # ReportGenerator
    # ------------------------------------------------------------------

    def generate_weekly_report(self, store_data: dict) -> dict:
        """基础周报：记录/事件/决策/冲突/隔离计数。"""
        return {
            "report_type": "weekly",
            "share_group_id": store_data.get("share_group_id", ""),
            "summary": {
                "total_records": store_data.get("total_records", 0),
                "active": store_data.get("active", 0),
                "shadowed": store_data.get("shadowed", 0),
                "conflicted": store_data.get("conflicted", 0),
                "quarantined": store_data.get("quarantined", 0),
                "deleted": store_data.get("deleted", 0),
            },
            "activity": {
                "total_events": store_data.get("total_events", 0),
                "total_decisions": store_data.get("total_decisions", 0),
                "total_conflicts": store_data.get("total_conflicts", 0),
                "total_quarantine": store_data.get("total_quarantine", 0),
            },
            "active_version": store_data.get("active_version"),
        }

    def generate_health_report(self, store_data: dict) -> dict:
        """基础健康报告：覆盖率/冲突率/隔离率。"""
        total = store_data.get("total_records", 0)
        active = store_data.get("active", 0)
        conflicted = store_data.get("conflicted", 0)
        quarantined = store_data.get("quarantined", 0)
        return {
            "report_type": "health",
            "share_group_id": store_data.get("share_group_id", ""),
            "metrics": {
                "active_rate": round(active / total, 4) if total else 0.0,
                "conflict_rate": round(conflicted / total, 4) if total else 0.0,
                "quarantine_rate": round(quarantined / total, 4) if total else 0.0,
                "total_records": total,
            },
            "status": "healthy" if conflicted == 0 and quarantined == 0 else "attention",
        }

    def format_report(self, data: dict, format: str) -> str:
        """Community 版仅支持 JSON 格式。"""
        if format.lower() == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError(
            f"Community 版不支持 {format} 格式，仅支持 json；"
            f"Pro 版支持 html/pdf"
        )


# ===========================================================================
# PolicyRegistry：策略注册表
# ===========================================================================


# 策略类型 -> 对应基类
_POLICY_TYPES: dict[str, type] = {
    "organizer": OrganizerPolicy,
    "decay": DecayPolicy,
    "supersede": SupersedePolicy,
    "quarantine": QuarantinePolicy,
    "report": ReportGenerator,
}


class PolicyRegistry:
    """策略注册表。

    Community 版默认注册 CommunityPolicy 到所有策略类型。
    Pro 版通过 register() 替换特定策略为高级实现。

    用法：
        registry = PolicyRegistry()
        organizer = registry.get("organizer")
        # Pro 版注入：
        registry.register("organizer", ProOrganizerPolicy())
    """

    def __init__(self) -> None:
        self._registry: dict[str, Any] = {}
        default = CommunityPolicy()
        for policy_type in _POLICY_TYPES:
            self._registry[policy_type] = default

    def register(self, policy_type: str, impl: Any) -> None:
        """注册策略实现。

        Args:
            policy_type: 策略类型（organizer/decay/supersede/quarantine/report）
            impl: 策略实现实例（鸭子类型，实现对应基类的方法即可）
        """
        if policy_type not in _POLICY_TYPES:
            raise ValueError(
                f"未知策略类型: {policy_type}；"
                f"支持: {list(_POLICY_TYPES.keys())}"
            )
        self._registry[policy_type] = impl

    def get(self, policy_type: str) -> Any:
        """获取策略实现。

        Args:
            policy_type: 策略类型

        Returns:
            策略实现实例（默认为 CommunityPolicy）
        """
        if policy_type not in self._registry:
            raise ValueError(
                f"未知策略类型: {policy_type}；"
                f"支持: {list(_POLICY_TYPES.keys())}"
            )
        return self._registry[policy_type]
