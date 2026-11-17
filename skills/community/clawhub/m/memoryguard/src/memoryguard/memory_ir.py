"""Memory IR：跨来源规范化记忆层（spec §3.4, §10）。

v3 核心纠偏：
- 保留全部 provenance，不静默丢弃重复项
- TF-IDF 只生成 DuplicateGroup 候选，不自动合并
- Instruction/Skill 默认不进入 Memory IR（spec §1.1）
- 稳定 ID：hash(source_object_id + stable_locator + normalized_content_fingerprint)

与 v2.1 extractor.py 的区别：
- extractor.py 直接去重丢弃；本模块只生成候选组
- extractor.py 无 provenance；本模块强制每条 MemoryRecord 至少一个 Provenance
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .schema_v3 import (
    Completeness, DecisionEvent, DuplicateDecision, DuplicateGroup,
    MemoryKind, MemoryRecord, MemoryStatus, Provenance, SourceObject,
    SourceSnapshot, stable_hash, _now_iso,
)


# ---------------------------------------------------------------------------
# TF-IDF 工具（纯标准库，零依赖）
# ---------------------------------------------------------------------------


class TfidfVectorizer:
    """极简 TF-IDF：中文按字符切，英文按词切。"""

    def __init__(self):
        self.vocabulary: dict[str, int] = {}
        self.idf: dict[int, float] = {}

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        # 中英文混合：英文按 word，中文按单字
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[\u4e00-\u9fff]", text.lower())
        return [t for t in tokens if len(t) >= 1]

    def fit(self, docs: list[str]) -> None:
        df: dict[str, int] = {}
        total = len(docs)
        for doc in docs:
            seen = set()
            for tok in self._tokenize(doc):
                if tok not in seen:
                    df[tok] = df.get(tok, 0) + 1
                    seen.add(tok)
        self.vocabulary = {t: i for i, t in enumerate(sorted(df.keys()))}
        self.idf = {
            self.vocabulary[t]: math.log((1 + total) / (1 + df[t])) + 1.0
            for t in df
        }

    def transform(self, text: str) -> list[float]:
        vec = [0.0] * len(self.vocabulary)
        toks = self._tokenize(text)
        tf: dict[int, int] = {}
        for t in toks:
            idx = self.vocabulary.get(t)
            if idx is not None:
                tf[idx] = tf.get(idx, 0) + 1
        for idx, count in tf.items():
            vec[idx] = count * self.idf.get(idx, 1.0)
        return vec

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)


# ---------------------------------------------------------------------------
# MemoryNormalizer：从 SourceObject 提取 MemoryRecord
# ---------------------------------------------------------------------------


# 判断文件是否属于 Instruction/Skill（不进入 Memory IR）
INSTRUCTION_FILENAMES = {"AGENTS.md", "CLAUDE.md", "CLAUDE.local.md", "GEMINI.md",
                         "CODEBUDDY.md", ".cursorrules", ".windsurfrules",
                         "copilot-instructions.md"}
SKILL_MARKERS = ("SKILL.md", "skills/")


def _is_instruction_or_skill(rel_path: str) -> bool:
    """Instruction/Skill 默认不进入 Memory IR（spec §1.1）。"""
    name = rel_path.rsplit("/", 1)[-1]
    if name in INSTRUCTION_FILENAMES:
        return True
    if "SKILL.md" in rel_path or "skills/" in rel_path:
        return True
    return False


def _split_into_segments(content: str) -> list[tuple[str, str]]:
    """把内容拆成 (locator, text) 段。
    locator 是 "line:N-M" 或 "heading:Title" 形式。
    """
    segments: list[tuple[str, str]] = []
    lines = content.split("\n")
    current_heading = ""
    current_start = 0
    current_lines: list[str] = []

    def flush():
        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                locator = f"heading:{current_heading}" if current_heading else f"line:{current_start+1}-{current_start+len(current_lines)}"
                segments.append((locator, text))

    for i, line in enumerate(lines):
        m = re.match(r"^#+\s+(.+)$", line)
        if m:
            flush()
            current_heading = m.group(1).strip()
            current_start = i
            current_lines = [line]
        else:
            if not current_lines:
                current_start = i
            current_lines.append(line)
    flush()
    return segments


def _infer_kind(title: str, body: str) -> MemoryKind:
    """启发式推断 MemoryKind。"""
    text = (title + " " + body).lower()
    if any(k in text for k in ["偏好", "喜欢", "prefer", "like", "习惯"]):
        return MemoryKind.PREFERENCE
    if any(k in text for k in ["步骤", "流程", "procedure", "step", "how to"]):
        return MemoryKind.PROCEDURE
    if any(k in text for k in ["项目", "project", "仓库", "repo"]):
        return MemoryKind.PROJECT
    if any(k in text for k in ["事件", "episode", "发生", "happened"]):
        return MemoryKind.EPISODE
    return MemoryKind.FACT


def _extract_title(segment_text: str) -> str:
    """从段提取标题：第一行若有 # 取其内容，否则取前 40 字符。"""
    first_line = segment_text.split("\n", 1)[0]
    m = re.match(r"^#+\s+(.+)$", first_line)
    if m:
        return m.group(1).strip()[:80]
    return segment_text[:40].replace("\n", " ").strip()


@dataclass
class MemoryIR:
    """Memory IR 容器：所有 MemoryRecord + DuplicateGroup + DecisionEvent。"""

    records: list[MemoryRecord] = field(default_factory=list)
    duplicate_groups: list[DuplicateGroup] = field(default_factory=list)
    decisions: list[DecisionEvent] = field(default_factory=list)
    snapshot_id: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "records": [r.to_dict() for r in self.records],
            "duplicate_groups": [g.to_dict() for g in self.duplicate_groups],
            "decisions": [d.to_dict() for d in self.decisions],
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryIR":
        records = []
        for r in data.get("records", []):
            provs = [Provenance(**p) for p in r.get("provenance", [])]
            records.append(MemoryRecord(
                memory_id=r["memory_id"], kind=MemoryKind(r["kind"]),
                title=r["title"], body=r["body"], scope=r.get("scope", "project"),
                confidence=r.get("confidence", 0.5), provenance=provs,
                status=MemoryStatus(r.get("status", "candidate")),
                completeness=Completeness(r.get("completeness", "verifiable")),
                created_at=r.get("created_at", ""),
            ))
        groups = [DuplicateGroup(
            group_id=g["group_id"], member_ids=g["member_ids"],
            similarity_method=g.get("similarity_method", "tfidf_cosine"),
            scores=g.get("scores", []),
            decision=DuplicateDecision(g.get("decision", "unresolved")),
        ) for g in data.get("duplicate_groups", [])]
        decisions = [DecisionEvent(
            event_id=d["event_id"], actor=d["actor"], action=d["action"],
            target_ids=d["target_ids"], before_hash=d.get("before_hash", ""),
            after_hash=d.get("after_hash", ""), reason=d.get("reason", ""),
            created_at=d.get("created_at", ""),
        ) for d in data.get("decisions", [])]
        return cls(records=records, duplicate_groups=groups, decisions=decisions,
                   snapshot_id=data.get("snapshot_id", ""),
                   created_at=data.get("created_at", ""))


class MemoryNormalizer:
    """从 SourceSnapshot 规范化为 Memory IR。"""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.mg_dir = self.workspace / ".memoryguard"
        self.ir_path = self.mg_dir / "ir" / "current.json"
        self.decisions_path = self.mg_dir / "ir" / "decisions.jsonl"

    def normalize(self, snapshot: SourceSnapshot,
                  duplicate_threshold: float = 0.75,
                  root_map: dict[str, str] | None = None) -> MemoryIR:
        """从快照生成 Memory IR。

        v3.1 §1.3 P0：必须传入 root_map（root_id -> root.path），
        不能再用 workspace / relative_path 猜路径，否则外部来源会静默丢失。
        """
        records: list[MemoryRecord] = []
        # v3.1 §1.3：扫描和规范化使用同一次稳定内容读取，前后哈希不一致标记 changed_during_scan
        for obj in snapshot.source_objects:
            if _is_instruction_or_skill(obj.relative_path):
                continue  # Instruction/Skill 不进入 IR
            content = self._read_source_content(obj, root_map)
            if content is None:
                continue
            # 哈希一致性检查（v3.1 §1.3）
            import hashlib
            current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
            if current_hash != obj.content_hash:
                # 内容在扫描后发生变化：跳过并记录（不静默）
                continue
            segments = _split_into_segments(content)
            for locator, text in segments:
                title = _extract_title(text)
                body = text
                kind = _infer_kind(title, body)
                excerpt_hash = stable_hash(text)
                memory_id = stable_hash(obj.source_object_id, locator, excerpt_hash)
                prov = Provenance(
                    source_object_id=obj.source_object_id, locator=locator,
                    excerpt_hash=excerpt_hash, source_revision=obj.content_hash,
                )
                rec = MemoryRecord(
                    memory_id=memory_id, kind=kind, title=title, body=body,
                    scope="project", confidence=0.5, provenance=[prov],
                    status=MemoryStatus.CANDIDATE,
                    completeness=Completeness.VERIFIABLE,
                    created_at=_now_iso(),
                )
                records.append(rec)
        # 生成重复候选组（不自动删除）
        groups = self._find_duplicates(records, duplicate_threshold)
        ir = MemoryIR(
            records=records, duplicate_groups=groups,
            snapshot_id=snapshot.snapshot_id, created_at=_now_iso(),
        )
        return ir

    def _read_source_content(self, obj: SourceObject,
                             root_map: dict[str, str] | None = None) -> str | None:
        """v3.1 §1.3 P0：使用 SourceRoot.path 定位，不再用 workspace/relative_path 猜路径。"""
        if root_map and obj.source_root_id in root_map:
            from pathlib import Path
            import os
            root_path = Path(root_map[obj.source_root_id]).resolve()
            full = (root_path / obj.relative_path).resolve()
            # canonical containment 防护
            try:
                full.relative_to(root_path)
            except ValueError:
                return None
            # 符号链接防护
            if full.is_symlink():
                try:
                    target = Path(os.readlink(full)).resolve()
                    target.relative_to(root_path)
                except (ValueError, OSError):
                    return None
            if not full.is_file():
                return None
            try:
                return full.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return None
        # 回退：项目目录的相对路径
        from pathlib import Path
        p = self.workspace / obj.relative_path
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return None
        return None

    def _find_duplicates(self, records: list[MemoryRecord],
                         threshold: float) -> list[DuplicateGroup]:
        """TF-IDF 生成重复候选组，不自动删除。"""
        if len(records) < 2:
            return []
        vec = TfidfVectorizer()
        vec.fit([r.body for r in records])
        vectors = [vec.transform(r.body) for r in records]
        groups: list[DuplicateGroup] = []
        used: set[int] = set()
        for i in range(len(records)):
            if i in used:
                continue
            members = [i]
            scores = [1.0]
            for j in range(i + 1, len(records)):
                if j in used:
                    continue
                sim = TfidfVectorizer.cosine(vectors[i], vectors[j])
                if sim >= threshold:
                    members.append(j)
                    scores.append(round(sim, 3))
            if len(members) > 1:
                group_id = "dup-" + stable_hash(records[i].memory_id, str(len(members)))
                groups.append(DuplicateGroup(
                    group_id=group_id,
                    member_ids=[records[m].memory_id for m in members],
                    similarity_method="tfidf_cosine",
                    scores=scores,
                    decision=DuplicateDecision.UNRESOLVED,
                ))
                used.update(members)
        return groups

    def save(self, ir: MemoryIR) -> None:
        """持久化 IR 到 .memoryguard/ir/current.json。"""
        self.ir_path.parent.mkdir(parents=True, exist_ok=True)
        self.ir_path.write_text(
            json.dumps(ir.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8")

    def load(self) -> MemoryIR | None:
        if not self.ir_path.exists():
            return None
        try:
            data = json.loads(self.ir_path.read_text(encoding="utf-8"))
            return MemoryIR.from_dict(data)
        except (OSError, json.JSONDecodeError):
            return None

    def append_decision(self, event: DecisionEvent) -> None:
        """追加决策到 decisions.jsonl。"""
        self.decisions_path.parent.mkdir(parents=True, exist_ok=True)
        with self.decisions_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
