"""v3.2 §6 AutoOrganizer 自动整理器。

写入后自动执行：
- 分类：preference / fact / project / procedure / episode / correction
- 去重：同义或重复内容合并 provenance
- 覆盖：纠错或更新 supersede 旧记录
- 冲突：互斥内容进入 conflict group
- 隔离：secret/token/credential 进入 quarantine

覆盖不是删除：
  old_memory.status = shadowed
  new_memory.supersedes = [old_memory_id]
  DecisionEvent(action="auto_supersede")
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema_v3 import (
    MemoryEvent, MemoryKind,
    SharedMemoryRecord, SharedMemoryStatus,
    Provenance, DecisionEvent, stable_hash, _now_iso,
)
from .semantic_dedup import SemanticDedup
from .shared_memory_store import SharedMemoryStore


# Secret 检测正则
SECRET_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|pwd)\s*[=:]\s*\S+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),               # AWS Access Key
    re.compile(r"ghp_[A-Za-z0-9]{36}"),             # GitHub PAT
    re.compile(r"gho_[A-Za-z0-9]{36}"),             # GitHub OAuth
    re.compile(r"sk-[A-Za-z0-9]{20,}"),             # OpenAI API Key
    re.compile(r"xox[baprs]-[A-Za-z0-9-]+"),        # Slack Token
    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),  # Private Key
]


class AutoOrganizer:
    """写入后自动整理：分类/隔离/去重/覆盖/冲突。

    整理流程：
    1. 分类 -> 启发式推断 MemoryKind
    2. 隔离检查 -> secret/token/credential -> QUARANTINED
    3. 去重检查 -> TF-IDF 相似度
       3a. 纠错/更新 -> supersede 旧记录
       3b. 冲突 -> conflict group
       3c. 同义 -> 合并 provenance
    4. 新记忆 -> ACTIVE
    """

    def __init__(self, workspace: str | Path, share_group_id: str):
        self.store = SharedMemoryStore(workspace, share_group_id)
        self.semantic_dedup = SemanticDedup(workspace, share_group_id)
        # 接入 PolicyRegistry（局部导入避免循环依赖：policies.py 导入了 SECRET_PATTERNS）
        from .policies import PolicyRegistry
        self.registry = PolicyRegistry()

    def organize(self, event: MemoryEvent, kind_override: str = "",
                 write_policy: str = "auto_accept") -> tuple[SharedMemoryRecord, list[dict]]:
        """整理流程：分类 -> 隔离检查 -> 去重 -> 覆盖/冲突/合并 -> 新建。

        返回 (record, actions)。
        actions 是自动执行的动作列表，用于回填到 MemoryEvent.auto_actions。

        Args:
            event: 写入事件
            kind_override: 用户指定的 kind，非空时覆盖自动分类结果
            write_policy: 写入策略 (auto_accept / auto_quarantine_on_risk / propose_only)
        """
        actions: list[dict[str, Any]] = []
        propose_only = write_policy == "propose_only"

        # 1. 分类（通过 PolicyRegistry 统一入口）
        kind_str = self.registry.get('organizer').classify(
            event.raw_content, event.metadata)
        kind = MemoryKind(kind_str)
        confidence = self._confidence(event.raw_content, kind)
        actions.append({"action": "classify", "kind": kind.value, "confidence": confidence})

        # kind_override 优先于自动分类
        if kind_override:
            kind = MemoryKind(kind_override)
            actions.append({"action": "classify_override", "kind": kind.value,
                            "reason": "user specified kind"})
            decision = DecisionEvent(
                event_id=stable_hash("classify_override", event.event_id, _now_iso()),
                actor="user", action="classify_override",
                target_ids=[], reason="user specified kind",
                created_at=_now_iso(),
            )
            self.store.append_decision(decision)

        compressed_body = self._compress(event.raw_content)
        if compressed_body != event.raw_content:
            actions.append({"action": "compress", "original_length": len(event.raw_content),
                            "compressed_length": len(compressed_body)})

        derived = self._derive_repeated_memory(event.raw_content, kind)
        if derived:
            event.raw_content = derived["body"]
            kind = derived["kind"]
            confidence = max(confidence, 0.72)
            actions.append({"action": "derive", "kind": kind.value, "reason": derived["reason"]})
        elif compressed_body != event.raw_content:
            event.raw_content = compressed_body

        # 2. 隔离检查（secret/token/credential）
        secret_match = self._detect_secret(event.raw_content)
        if secret_match:
            if propose_only:
                # propose_only: 不隔离，只标记风险
                record = self._create_record(
                    event, kind, SharedMemoryStatus.LOW_CONFIDENCE, confidence=confidence,
                )
                self.store.append_record(record)
                actions.append({"action": "propose_only",
                                "reason": "write policy is propose_only"})
                actions.append({"action": "risk_flag",
                                "reason": f"检测到敏感信息（未隔离）: {secret_match}"})
                return record, actions
            record = self._create_record(
                event, kind, SharedMemoryStatus.QUARANTINED, confidence=confidence,
            )
            self.store.append_record(record)
            self.store.quarantine_memory(
                record.memory_id,
                reason=f"检测到敏感信息: {secret_match}",
                pattern=secret_match,
                original_content=event.raw_content,
            )
            actions.append({"action": "quarantine", "reason": secret_match})
            return record, actions

        # 3. 去重检查
        # 纠错内容用更低阈值查找相关记忆
        is_correction = self._is_correction(event, [])
        dedup_threshold = 0.50 if is_correction else 0.85
        duplicates = self._find_duplicates(event.raw_content, threshold=dedup_threshold)

        # 3-semantic. Jaccard 没找到时，尝试 semantic 检查（跨语言/改写）
        # 若 Jaccard 低但 semantic 高，以 semantic 为准
        semantic_matched = False
        if not duplicates:
            sem_dups = self.semantic_dedup.find_semantic_duplicates(
                event.raw_content, threshold=dedup_threshold,
            )
            if sem_dups:
                duplicates = [d["record"] for d in sem_dups]
                semantic_matched = True
                actions.append({
                    "action": "semantic_match",
                    "similarity": sem_dups[0]["similarity"],
                    "matched_ids": [d["memory_id"] for d in sem_dups],
                })

        if duplicates:
            # 3a. 纠错/更新 -> supersede
            if self._is_correction(event, duplicates):
                old = duplicates[0]
                if not old.locked:
                    if propose_only:
                        # propose_only: 不覆盖，创建 low_confidence
                        record = self._create_record(
                            event, kind, SharedMemoryStatus.LOW_CONFIDENCE,
                            confidence=confidence,
                        )
                        self.store.append_record(record)
                        actions.append({"action": "propose_only",
                                        "reason": "write policy is propose_only"})
                        return record, actions
                    if write_policy == "auto_quarantine_on_risk":
                        # 不覆盖，改为 conflicted + low_confidence
                        record = self._create_record(
                            event, kind, SharedMemoryStatus.LOW_CONFIDENCE,
                            confidence=confidence,
                        )
                        self.store.append_record(record)
                        member_ids = [old.memory_id, record.memory_id]
                        explanation = self._explain_conflict(
                            event.raw_content, [old])
                        group_id = self.store.conflict(member_ids, explanation)
                        actions.append({"action": "conflict",
                                        "group_id": group_id,
                                        "reason": explanation})
                        return record, actions
                    record = self._create_record(
                        event, kind, SharedMemoryStatus.ACTIVE,
                        supersedes=[old.memory_id], confidence=confidence,
                    )
                    self.store.append_record(record)
                    self.store.supersede(old.memory_id, record.memory_id,
                                          "auto_supersede: correction")
                    actions.append({"action": "supersede", "old_id": old.memory_id})
                    return record, actions
            # 3b. 冲突 -> conflict group
            elif self._is_conflict(event, duplicates) or (
                semantic_matched and self._has_kind_conflict(duplicates, kind)
            ):
                if propose_only:
                    # propose_only: 不创建冲突组，创建 low_confidence
                    record = self._create_record(
                        event, kind, SharedMemoryStatus.LOW_CONFIDENCE,
                        confidence=confidence,
                    )
                    self.store.append_record(record)
                    actions.append({"action": "propose_only",
                                    "reason": "write policy is propose_only"})
                    return record, actions
                record = self._create_record(
                    event, kind, SharedMemoryStatus.CONFLICTED, confidence=confidence,
                )
                self.store.append_record(record)
                member_ids = [old.memory_id for old in duplicates] + [record.memory_id]
                explanation = self._explain_conflict(event.raw_content, duplicates)
                group_id = self.store.conflict(member_ids, explanation)
                actions.append({"action": "conflict", "group_id": group_id, "reason": explanation})
                return record, actions
            # 3c. 同义 -> 合并 provenance（不创建新记录）
            else:
                if propose_only:
                    # propose_only: 不合并，创建 low_confidence
                    record = self._create_record(
                        event, kind, SharedMemoryStatus.LOW_CONFIDENCE,
                        confidence=confidence,
                    )
                    self.store.append_record(record)
                    actions.append({"action": "propose_only",
                                    "reason": "write policy is propose_only"})
                    return record, actions
                target = duplicates[0]
                self._merge_provenance(target, event)
                actions.append({"action": "merge_provenance",
                                "duplicate_ids": [d.memory_id for d in duplicates],
                                "target_id": target.memory_id})
                # 衍生检查（合并后 provenance 累积可能触发衍生）
                derive_action = self._check_derivation(event, target)
                if derive_action:
                    actions.append(derive_action)
                return target, actions

        # 4. 新记忆
        if propose_only:
            status = SharedMemoryStatus.LOW_CONFIDENCE
            actions.append({"action": "propose_only",
                            "reason": "write policy is propose_only"})
        else:
            status = SharedMemoryStatus.LOW_CONFIDENCE if confidence < 0.45 else SharedMemoryStatus.ACTIVE
        record = self._create_record(event, kind, status, confidence=confidence)
        self.store.append_record(record)
        actions.append({"action": "create_low_confidence" if status == SharedMemoryStatus.LOW_CONFIDENCE else "create_active"})

        # 5. 压缩检查
        compress_action = self._check_compression(event, record)
        if compress_action:
            actions.append(compress_action)

        # 6. 衍生检查
        derive_action = self._check_derivation(event, record)
        if derive_action:
            actions.append(derive_action)

        return record, actions

    # ------------------------------------------------------------------
    # 分类
    # ------------------------------------------------------------------

    def _classify(self, content: str) -> MemoryKind:
        """启发式分类。"""
        text = content.lower()
        if any(k in text for k in ["偏好", "喜欢", "prefer", "like", "习惯"]):
            return MemoryKind.PREFERENCE
        if any(k in text for k in ["步骤", "流程", "procedure", "step", "how to"]):
            return MemoryKind.PROCEDURE
        if any(k in text for k in ["项目", "project", "仓库", "repo"]):
            return MemoryKind.PROJECT
        if any(k in text for k in ["事件", "episode", "发生", "happened"]):
            return MemoryKind.EPISODE
        if any(k in text for k in ["纠正", "更正", "correction", "actually",
                                    "不对", "错误", "应该是"]):
            return MemoryKind.CORRECTION
        return MemoryKind.FACT

    def _confidence(self, content: str, kind: MemoryKind) -> float:
        text = content.strip()
        if not text:
            return 0.1
        score = 0.50
        if len(text) >= 12:
            score += 0.10
        if kind in (MemoryKind.PREFERENCE, MemoryKind.PROCEDURE, MemoryKind.PROJECT, MemoryKind.CORRECTION):
            score += 0.12
        if any(k in text.lower() for k in ["可能", "大概", "maybe", "probably", "不确定"]):
            score -= 0.20
        if len(self._tokenize(text)) < 4:
            score -= 0.18
        return max(0.1, min(0.95, score))

    def _compress(self, content: str) -> str:
        text = content.strip()
        if len(text) <= 1200:
            return text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        selected = []
        for line in lines:
            if any(k in line.lower() for k in ["偏好", "步骤", "流程", "项目", "事实", "必须", "不要", "prefer", "step", "project", "must"]):
                selected.append(line)
            if len("\n".join(selected)) >= 1000:
                break
        if not selected:
            selected = lines[:8]
        body = "\n".join(selected).strip()
        return body[:1200]

    def _derive_repeated_memory(self, content: str, kind: MemoryKind) -> dict[str, Any] | None:
        tokens = self._tokenize(content)
        if not tokens:
            return None
        active = self.store.list_records(status="active")
        related = [r for r in active if self._jaccard(tokens, self._tokenize(r.body)) >= 0.45]
        if len(related) < 2:
            return None
        text = content.lower()
        if kind == MemoryKind.PROCEDURE or any(k in text for k in ["步骤", "流程", "step", "procedure"]):
            return {"kind": MemoryKind.PROCEDURE, "body": f"反复出现的流程：{content.strip()[:900]}", "reason": "similar_procedure_repeated"}
        if kind == MemoryKind.PREFERENCE or any(k in text for k in ["偏好", "喜欢", "prefer", "like"]):
            return {"kind": MemoryKind.PREFERENCE, "body": f"反复出现的偏好：{content.strip()[:900]}", "reason": "similar_preference_repeated"}
        return None

    # ------------------------------------------------------------------
    # Secret 检测
    # ------------------------------------------------------------------

    def _detect_secret(self, content: str) -> str:
        """检测敏感信息，返回匹配的模式描述（空字符串表示无匹配）。"""
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                return pattern.pattern[:50]
        return ""

    # ------------------------------------------------------------------
    # 去重
    # ------------------------------------------------------------------

    def _find_duplicates(self, content: str,
                         threshold: float = 0.85) -> list[SharedMemoryRecord]:
        """查找与 content 相似的已有 active 记录。

        使用简单的 Jaccard 相似度（基于字符/词集合）。
        """
        active_records = self.store.list_records(status="active")
        if not active_records:
            return []
        content_tokens = self._tokenize(content)
        if not content_tokens:
            return []
        duplicates: list[tuple[float, SharedMemoryRecord]] = []
        for rec in active_records:
            rec_tokens = self._tokenize(rec.body)
            if not rec_tokens:
                continue
            sim = self._jaccard(content_tokens, rec_tokens)
            if sim >= threshold:
                duplicates.append((sim, rec))
        # 按相似度降序
        duplicates.sort(key=lambda x: -x[0])
        return [rec for _sim, rec in duplicates]

    def _tokenize(self, text: str) -> set[str]:
        """中英文混合分词：英文按 word，中文按单字。"""
        import re as _re
        tokens = _re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[\u4e00-\u9fff]", text.lower())
        return set(tokens)

    def _jaccard(self, a: set[str], b: set[str]) -> float:
        """Jaccard 相似度。"""
        if not a or not b:
            return 0.0
        intersection = a & b
        union = a | b
        return len(intersection) / len(union)

    # ------------------------------------------------------------------
    # 纠错/冲突判断
    # ------------------------------------------------------------------

    def _is_correction(self, event: MemoryEvent,
                       duplicates: list[SharedMemoryRecord]) -> bool:
        """判断是否是纠错/更新。

        启发式：
        - content 含纠错关键词（纠正/更正/actually/不对/应该是）
        - 或 metadata 中有 correction 标记
        """
        text = event.raw_content.lower()
        correction_keywords = ["纠正", "更正", "correction", "actually",
                               "不对", "错误", "应该是", "update", "更新"]
        if any(k in text for k in correction_keywords):
            return True
        if event.metadata.get("type") == "correction":
            return True
        return False

    def _is_conflict(self, event: MemoryEvent,
                     duplicates: list[SharedMemoryRecord]) -> bool:
        """判断是否是冲突。

        启发式：
        - content 和 duplicate 有相同主题但不同结论
        - 简单判断：都含"偏好"但不同选项
        """
        text = event.raw_content.lower()
        for dup in duplicates:
            dup_text = dup.body.lower()
            # 都含偏好关键词但内容不同
            if any(k in text for k in ["偏好", "喜欢", "prefer"]) and \
               any(k in dup_text for k in ["偏好", "喜欢", "prefer"]):
                if text != dup_text:
                    return True
        return False

    def _explain_conflict(self, content: str, duplicates: list[SharedMemoryRecord]) -> str:
        peers = [d.body[:80] for d in duplicates[:3]]
        return "auto_conflict: 可能互斥内容；new=" + content[:80] + "; existing=" + " | ".join(peers)

    def _has_kind_conflict(self, duplicates: list[SharedMemoryRecord],
                           new_kind: MemoryKind) -> bool:
        """semantic 场景下：语义相似但 kind 不同视为冲突。"""
        return any(dup.kind != new_kind for dup in duplicates)

    def _merge_provenance(self, target: SharedMemoryRecord, event: MemoryEvent) -> None:
        existing = {p.source_object_id for p in target.provenance}
        if event.event_id in existing:
            return
        target.provenance.append(Provenance(
            source_object_id=event.event_id,
            locator="event",
            excerpt_hash=stable_hash(event.raw_content),
            source_revision="",
        ))
        target.updated_at = _now_iso()
        self.store.update_record(target)

    # ------------------------------------------------------------------
    # 创建记录
    # ------------------------------------------------------------------

    def _create_record(self, event: MemoryEvent, kind: MemoryKind,
                       status: SharedMemoryStatus,
                       supersedes: list[str] | None = None,
                       confidence: float = 0.5) -> SharedMemoryRecord:
        """创建 SharedMemoryRecord。"""
        memory_id = stable_hash("mem", event.raw_content, event.agent_instance_id,
                                _now_iso())
        return SharedMemoryRecord(
            memory_id=memory_id,
            body=event.raw_content,
            kind=kind,
            status=status,
            confidence=confidence,
            provenance=[Provenance(
                source_object_id=event.event_id,
                locator="event",
                excerpt_hash=stable_hash(event.raw_content),
                source_revision="",
            )],
            supersedes=supersedes or [],
            locked=False,
            created_at=_now_iso(),
            updated_at=_now_iso(),
            agent_instance_id=event.agent_instance_id,
        )

    # ------------------------------------------------------------------
    # 衍生与压缩（v3.2 §4.3）
    # ------------------------------------------------------------------

    def _check_compression(self, event: MemoryEvent,
                           record: SharedMemoryRecord) -> dict[str, Any] | None:
        """压缩长 body：提取关键句，生成 compressed_body。

        不修改原始 body，压缩版本记录在 action 中供检索优先使用。
        - body > 500 字符：选最长 1 句，截断到 200 字符 + "..."
        - body > 1000 字符：选最长 3 句，截断到 200 字符 + "..."
        """
        body = record.body
        if len(body) <= 500:
            return None

        # 按句号/换行分割，选最长的关键句
        sentences = re.split(r"[。\n！？.!?]", body)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(body) > 1000:
            # 更激进压缩：选最长的 3 句
            key_sentences = sorted(sentences, key=len, reverse=True)[:3]
        else:
            # 普通压缩：选最长的 1 句
            key_sentences = sorted(sentences, key=len, reverse=True)[:1]

        if not key_sentences:
            compressed = body[:200] + "..."
        else:
            compressed = "。".join(key_sentences)[:200] + "..."

        return {
            "action": "compress",
            "memory_id": record.memory_id,
            "original_length": len(body),
            "compressed_length": len(compressed),
            "compressed_body": compressed,
        }

    def _check_derivation(self, event: MemoryEvent,
                          record: SharedMemoryRecord) -> dict[str, Any] | None:
        """从重复的 episode 记忆中衍生 procedure/preference。

        查找最近 30 天内同一 share_group 中相似的 active 记录，
        按 content 前 20 字聚类。如果找到 3+ 条相似 episode（按 provenance 计数），
        生成一条 LOW_CONFIDENCE 的 procedure 或 preference。
        """
        content_prefix = event.raw_content[:20]

        # 查找最近 30 天内的 active 记录
        now = datetime.now(timezone.utc)
        active_records = self.store.list_records(status="active")
        recent_records: list[SharedMemoryRecord] = []
        for r in active_records:
            try:
                dt = datetime.fromisoformat(r.created_at)
                if (now - dt).days <= 30:
                    recent_records.append(r)
            except (ValueError, TypeError):
                recent_records.append(r)

        # 按前 20 字聚类
        similar = [r for r in recent_records if r.body[:20] == content_prefix]

        # 计算 provenance 总数（每条 provenance = 一次 episode 交互）
        total_episodes = sum(len(r.provenance) for r in similar)

        # 需要 3+ 条相似 episode
        if total_episodes < 3:
            return None

        # 判断衍生类型
        text = event.raw_content.lower()
        source_ids = [r.memory_id for r in similar]

        if any(k in text for k in ["不要", "always", "never", "必须", "禁止", "勿"]):
            derived_kind = MemoryKind.PREFERENCE
        elif any(k in text for k in ["步骤", "流程", "先", "再", "step", "procedure"]):
            derived_kind = MemoryKind.PROCEDURE
        else:
            derived_kind = MemoryKind.PREFERENCE  # 通用偏好

        # 生成衍生记忆
        summary = event.raw_content.strip()[:200]
        derived_body = f"Based on {total_episodes} similar interactions: {summary}"

        derived_record = SharedMemoryRecord(
            memory_id=stable_hash("derive", record.memory_id, _now_iso()),
            body=derived_body,
            kind=derived_kind,
            status=SharedMemoryStatus.LOW_CONFIDENCE,
            confidence=0.4,
            provenance=[Provenance(
                source_object_id=sid,
                locator="derived_from",
                excerpt_hash=stable_hash(derived_body),
                source_revision="",
            ) for sid in source_ids],
            supersedes=[],
            locked=False,
            created_at=_now_iso(),
            updated_at=_now_iso(),
            agent_instance_id=event.agent_instance_id,
        )
        self.store.append_record(derived_record)

        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("derive_dec", derived_record.memory_id, _now_iso()),
            actor="auto",
            action="derive",
            target_ids=[derived_record.memory_id] + source_ids,
            reason=f"derived from {total_episodes} similar episodes",
            created_at=_now_iso(),
        )
        self.store.append_decision(decision)

        return {
            "action": "derive",
            "derived_id": derived_record.memory_id,
            "kind": derived_kind.value,
            "source_ids": source_ids,
            "episode_count": total_episodes,
        }
