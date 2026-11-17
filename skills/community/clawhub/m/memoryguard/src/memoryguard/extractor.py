"""记忆萃取模块（参考 merakagent FactDistiller + KnowledgePlugin）。

把工作区的 AGR（指令/Skill/记忆/RAG）萃取成 KnowledgeClaim，
供 LightGraphManager 挂到光点神经树。

萃取策略（确定性，不调 LLM，保持零依赖）:
- 指令文件：按 ## 标题段落萃取，每段是一条 claim
- Skill：SKILL.md 的 name/description + 脚本的功能注释
- 记忆/RAG：按段落萃取，标题作为 display_label，内容作为 body
- 去重：TF-IDF 相似度 >= 0.85 合并
- 分类：按文件类型/目录推断 memoryType
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from .schema import AGR, AGRType
from .light_graph import KnowledgeClaim, LightGraphManager, TfidfVectorizer

if TYPE_CHECKING:
    from .rules import RuleContext


# ---------------------------------------------------------------------------
# memoryType 推断
# ---------------------------------------------------------------------------


def infer_memory_type(agr: AGR) -> str:
    """根据 AGR 类型/路径推断 memoryType（对应 merakagent claim.memoryType）。"""
    if agr.type == AGRType.INSTRUCTION:
        return "instruction"
    if agr.type == AGRType.SKILL:
        if agr.path.endswith(".py") or agr.path.endswith(".sh"):
            return "skill_script"
        return "skill"
    if agr.type == AGRType.MEMORY:
        return "memory"
    if agr.type == AGRType.RAG_SOURCE:
        # 按目录细分
        lower = agr.metadata.get("rel_path", agr.path).lower()
        if "doc" in lower:
            return "knowledge"
        if "knowledge" in lower:
            return "knowledge"
        return "rag"
    return "misc"


# ---------------------------------------------------------------------------
# 萃取器
# ---------------------------------------------------------------------------


class MemoryExtractor:
    """从 AGR 列表萃取 KnowledgeClaim。

    用法:
        ext = MemoryExtractor(ctx)
        claims = ext.extract_all()
        graph = LightGraphManager()
        for c in claims: graph._claims[c.id] = c; graph._next_claim_id = max(...)
        graph.fit_vectorizer(); graph.attach_all_claims()
    """

    def __init__(self, ctx: "RuleContext"):
        self.ctx = ctx
        self._vectorizer = TfidfVectorizer()

    def extract_all(self) -> list[KnowledgeClaim]:
        """萃取所有 AGR 为 KnowledgeClaim。"""
        raw: list[tuple[str, str, str, str]] = []  # (label, body, memory_type, source)
        for agr in self.ctx.agrs:
            content = self.ctx.read_content(agr)
            if not content.strip():
                continue
            mem_type = infer_memory_type(agr)
            rel = agr.metadata.get("rel_path", agr.path)
            for label, body in self._split_claims(content, agr):
                raw.append((label, body, mem_type, rel))
        # 去重合并
        deduped = self._dedup(raw)
        # 生成 KnowledgeClaim
        claims = []
        for i, (label, body, mem_type, source) in enumerate(deduped, 1):
            claims.append(KnowledgeClaim(
                id=i, display_label=label, body=body,
                memory_type=mem_type, source=source,
                confidence=0.6, created_at=self._now(),
            ))
        return claims

    def _now(self) -> float:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).timestamp()

    def _split_claims(self, content: str, agr: AGR) -> list[tuple[str, str]]:
        """把文件内容拆成 (label, body) 列表。按 AGR 类型用不同策略。"""
        if agr.type == AGRType.INSTRUCTION or agr.path.endswith(".md"):
            return self._split_markdown(content)
        if agr.type == AGRType.SKILL and agr.path.endswith("SKILL.md"):
            return self._split_markdown(content)
        # 纯文本/脚本：按段落
        return self._split_paragraphs(content)

    def _split_markdown(self, content: str) -> list[tuple[str, str]]:
        """Markdown：按 ## 标题拆段。"""
        lines = content.splitlines()
        result: list[tuple[str, str]] = []
        current_label = ""
        current_body: list[str] = []
        for line in lines:
            m = re.match(r"^(#{1,4})\s+(.+)$", line)
            if m:
                if current_body and current_label:
                    body = "\n".join(current_body).strip()
                    if body:
                        result.append((current_label, body))
                current_label = m.group(2).strip()
                current_body = []
            else:
                current_body.append(line)
        if current_body and current_label:
            body = "\n".join(current_body).strip()
            if body:
                result.append((current_label, body))
        # 无标题的文件：整篇作为一条
        if not result:
            first_line = next((l for l in lines if l.strip()), "untitled")
            result.append((first_line[:60], content.strip()))
        return result

    def _split_paragraphs(self, content: str) -> list[tuple[str, str]]:
        """纯文本：按空行分段。"""
        blocks = re.split(r"\n\s*\n", content)
        result = []
        for b in blocks:
            b = b.strip()
            if not b or len(b) < 10:
                continue
            first = b.splitlines()[0][:60]
            result.append((first, b))
        return result

    def _dedup(self, raw: list[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
        """TF-IDF 去重：相似度 >= 0.85 合并。"""
        if len(raw) <= 1:
            return raw
        docs = [r[1] for r in raw]
        self._vectorizer.fit(docs)
        kept: list[tuple[str, str, str, str]] = []
        kept_vecs: list[list[float]] = []
        for item in raw:
            vec = self._vectorizer.transform(item[1])
            is_dup = False
            for kv in kept_vecs:
                if self._vectorizer.cosine(vec, kv) >= 0.85:
                    is_dup = True
                    break
            if not is_dup:
                kept.append(item)
                kept_vecs.append(vec)
        return kept
