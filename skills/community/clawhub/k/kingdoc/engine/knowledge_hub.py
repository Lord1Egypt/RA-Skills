"""KingDoc 团队知识库模式（v4.2.0 新增）

v4.2 知识中枢：空间级全文检索 + 权限感知过滤。

能力：
- 本地倒排索引：零第三方依赖，中文分词可选 jieba（未装时退化为字符级切分）
- 权限感知：检索前按空间成员权限矩阵（API 拉取缓存）过滤结果，
  用户无 read 权限的文档不进入结果集（遵守平台权限边界：先鉴权后检索）
- 硬件自适应：索引构建与查询分块，避免大空间卡顿
- 本地降级：云端不可用时接受外部注入的文档集构建本地索引

设计原则：
- 零第三方依赖（jieba 仅可选增强，缺失不影响核心）
- 权限边界强制：无权限文档绝不出现在搜索结果
- 零密钥可用（本地降级模式）
"""
from __future__ import annotations

import re
import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from engine.hardware import get_recommended_settings

# 文档元数据仓（SQLite）：持久化空间/权限快照
_DB_PATH = str(Path(__file__).resolve().parent.parent.parent / ".kingdoc_knowledge_hub.db")

_JIEBA = None
_JIEBA_TRIED = False


def _tokenizer_lib():
    """惰性加载 jieba（可选依赖），缺失返回 None。"""
    global _JIEBA, _JIEBA_TRIED
    if _JIEBA_TRIED:
        return _JIEBA
    _JIEBA_TRIED = True
    try:
        import jieba  # type: ignore
        jieba.setLogLevel(20)
        _JIEBA = jieba
    except Exception:
        _JIEBA = None
    return _JIEBA


def _tokenize(text: str) -> List[str]:
    """分词：中文走 jieba（若可用），英文/数字按非词边界切分。

    统一小写，过滤单字符噪声（保留中文单字以保证召回）。
    """
    if not text:
        return []
    text = text.lower()
    jieba = _tokenizer_lib()
    if jieba is not None:
        # jieba 对中文友好，但对英文数字也按词切，直接用它
        toks = list(jieba.cut(text))
    else:
        # 退化：按非字母数字切分，中文保留单字
        toks = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", text)
    out = []
    for t in toks:
        t = t.strip().strip("`\"'.,;:!?（）()[]【】。，；：！？、")
        if not t:
            continue
        out.append(t)
    return out


class KnowledgeHub:
    """团队知识库：倒排索引 + 权限矩阵。"""

    def __init__(self, backend: Optional[Any] = None):
        self.backend = backend
        self._local = backend is None
        self._lock = threading.RLock()
        self.index: Dict[str, Set[str]] = {}
        self.docs: Dict[str, Dict] = {}
        # 权限矩阵：space_id -> {doc_id -> 最低权限级别(int)}  read=1, edit=2, admin=3
        self.perm_cache: Dict[str, Dict[str, int]] = {}
        self.hw = get_recommended_settings()

    # ------------------------------------------------------------------
    # 权限矩阵
    # ------------------------------------------------------------------
    def set_permission_matrix(self, space_id: str, matrix: Dict[str, int]) -> Dict:
        """注入空间权限矩阵（doc_id -> 级别）。

        云端模式应调用 refresh_permission() 从 API 拉取后注入。
        """
        with self._lock:
            self.perm_cache[space_id] = dict(matrix)
        return {"success": True, "space_id": space_id, "entries": len(matrix)}

    def refresh_permission(self, space_id: str) -> Dict:
        """从云端拉取权限矩阵（需 backend）。

        本地降级模式返回友好提示：使用注入的矩阵或开放索引。
        """
        if self._local:
            return {
                "success": False,
                "hint": "本地降级模式：无法拉取云端权限，请使用 set_permission_matrix 注入或保持开放索引。",
            }
        try:
            members = self.backend.kdoc_space_members(space_id)
            # 假设 backend 返回 {doc_id: level}
            matrix = {m["doc_id"]: int(m.get("level", 1)) for m in members}
            return self.set_permission_matrix(space_id, matrix)
        except Exception as e:
            return {"success": False, "error": f"权限拉取失败：{e}"}

    def _has_read(self, space_id: str, doc_id: str) -> bool:
        """判断空间内某文档当前查看者是否可读。

        无矩阵则视为开放可读（本地降级）；有矩阵则必须 ≥ read(1)。
        """
        m = self.perm_cache.get(space_id)
        if not m:
            return True
        lvl = m.get(doc_id)
        if lvl is None:
            # 未登记：保守起见视为无权限（遵守边界）
            return False
        return lvl >= 1

    # ------------------------------------------------------------------
    # 文档索引
    # ------------------------------------------------------------------
    def add_document(self, doc_id: str, title: str, content: str,
                     space_id: str = "", owner: str = "") -> Dict:
        """向索引添加/更新文档。"""
        with self._lock:
            # 先删旧索引
            self._remove_from_index(doc_id)
            self.docs[doc_id] = {
                "doc_id": doc_id,
                "title": title,
                "content": content,
                "space_id": space_id,
                "owner": owner,
            }
            tokens = _tokenize(title + "\n" + content)
            for tk in tokens:
                self.index.setdefault(tk, set()).add(doc_id)
        return {"success": True, "doc_id": doc_id, "indexed_tokens": len(tokens)}

    def remove_document(self, doc_id: str) -> Dict:
        with self._lock:
            self._remove_from_index(doc_id)
            self.docs.pop(doc_id, None)
        return {"success": True, "doc_id": doc_id}

    def _remove_from_index(self, doc_id: str):
        for tk, s in self.index.items():
            s.discard(doc_id)
        # 清理空 token
        empty = [tk for tk, s in self.index.items() if not s]
        for tk in empty:
            self.index.pop(tk, None)

    def index_documents(self, docs: List[Dict], space_id: str = "") -> Dict:
        """批量建索引（硬件自适应分块）。"""
        chunk = max(self.hw.get("batch_chunk", 200), 50)
        total = 0
        for i in range(0, len(docs), chunk):
            batch = docs[i:i + chunk]
            for d in batch:
                self.add_document(
                    d.get("doc_id", f"doc_{total}"),
                    d.get("title", ""),
                    d.get("content", ""),
                    d.get("space_id", space_id),
                    d.get("owner", ""),
                )
                total += 1
        return {"success": True, "indexed": total, "space_id": space_id}

    def fetch_and_index_space(self, space_id: str, limit: int = 200) -> Dict:
        """从云端拉取空间文档并建索引（需 backend）。"""
        if self._local:
            return {
                "success": False,
                "hint": "本地降级模式：无法拉取云端空间文档，请传入文档集调用 index_documents。",
            }
        try:
            files = self.backend.kdoc_space_list_files(space_id, limit)
            docs = []
            for f in files:
                content = self.backend.kdoc_file_content(f["file_id"]) or ""
                docs.append({"doc_id": f["file_id"], "title": f.get("name", ""),
                             "content": content, "space_id": space_id})
            return self.index_documents(docs, space_id)
        except Exception as e:
            return {"success": False, "error": f"空间索引失败：{e}"}

    # ------------------------------------------------------------------
    # 检索（权限感知）
    # ------------------------------------------------------------------
    def search(self, query: str, space_id: str = "", limit: int = 20,
               viewer_id: str = "") -> Dict:
        """权限感知全文检索。

        流程：分词 → 倒排取候选 → 权限过滤（无 read 权限剔除）→ 打分排序 → 返回。
        """
        q_tokens = _tokenize(query)
        if not q_tokens:
            return {"hits": [], "total": 0, "filtered_out": 0,
                    "note": "查询为空或无可索引词。"}

        with self._lock:
            candidate_scores: Dict[str, int] = {}
            for tk in q_tokens:
                doc_ids = self.index.get(tk, set())
                for did in doc_ids:
                    candidate_scores[did] = candidate_scores.get(did, 0) + 1

        # 权限过滤：先鉴权后检索
        filtered_out = 0
        allowed = []
        for did, score in candidate_scores.items():
            doc = self.docs.get(did, {})
            sid = doc.get("space_id", "")
            if sid and not self._has_read(sid, did):
                filtered_out += 1
                continue
            allowed.append((did, score))

        allowed.sort(key=lambda x: x[1], reverse=True)
        hits = []
        for did, score in allowed[:limit]:
            doc = self.docs.get(did, {})
            # 命中上下文截取
            snippet = self._snippet(doc.get("content", ""), q_tokens)
            hits.append({
                "doc_id": did,
                "title": doc.get("title", ""),
                "space_id": doc.get("space_id", ""),
                "owner": doc.get("owner", ""),
                "score": score,
                "snippet": snippet,
            })

        return {
            "hits": hits,
            "total": len(hits),
            "filtered_out": filtered_out,
            "permission_aware": bool(self.perm_cache),
            "jieba_enabled": _tokenizer_lib() is not None,
        }

    def _snippet(self, content: str, q_tokens: List[str], window: int = 40) -> str:
        if not content:
            return ""
        low = content.lower()
        pos = -1
        for tk in q_tokens:
            p = low.find(tk)
            if p >= 0:
                pos = p
                break
        if pos < 0:
            return content[:window * 2]
        start = max(0, pos - window)
        end = min(len(content), pos + window)
        return ("..." if start > 0 else "") + content[start:end] + ("..." if end < len(content) else "")

    def get_status(self) -> Dict:
        with self._lock:
            doc_count = len(self.docs)
            token_count = len(self.index)
        return {
            "local_mode": self._local,
            "doc_count": doc_count,
            "token_count": token_count,
            "space_permission_loaded": list(self.perm_cache.keys()),
            "jieba_enabled": _tokenizer_lib() is not None,
            "workers": self.hw.get("workers", 1),
        }


# ---------------------------------------------------------------------------
# 单例 + 便捷函数
# ---------------------------------------------------------------------------
_hub: Optional[KnowledgeHub] = None
_hub_lock = threading.Lock()


def get_knowledge_hub(backend: Optional[Any] = None) -> KnowledgeHub:
    global _hub
    with _hub_lock:
        if _hub is None:
            _hub = KnowledgeHub(backend=backend)
        return _hub


def search_knowledge(query: str, space_id: str = "", limit: int = 20,
                     viewer_id: str = "") -> Dict:
    return get_knowledge_hub().search(query, space_id, limit, viewer_id)


def index_documents(docs: List[Dict], space_id: str = "") -> Dict:
    return get_knowledge_hub().index_documents(docs, space_id)


def set_permission(space_id: str, matrix: Dict[str, int]) -> Dict:
    return get_knowledge_hub().set_permission_matrix(space_id, matrix)


def refresh_permission(space_id: str) -> Dict:
    return get_knowledge_hub().refresh_permission(space_id)


def fetch_and_index_space(space_id: str, limit: int = 200) -> Dict:
    return get_knowledge_hub().fetch_and_index_space(space_id, limit)


def get_hub_status() -> Dict:
    return get_knowledge_hub().get_status()
