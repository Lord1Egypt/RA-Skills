"""
vector_retriever.py — 从 LanceDB 向量库检索记忆

功能：
- 根据用户 query 语义检索已导入的 markdown 记忆
- 与 MemoryManager 记忆层融合
- 支持自定义召回数量和相似度阈值
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class RetrievedChunk:
    """检索到的记忆块"""
    chunk_id: str
    source_file: str
    title: str
    heading: str
    content: str
    score: float  # 相似度分数 0-1


class VectorRetriever:
    """
    从 LanceDB 向量库检索 markdown 记忆
    与 MemoryManager 共享同一个 LanceDB 实例
    """

    def __init__(
        self,
        table_name: str = "memory_chunks",
        db_path: str = "~/.hawk/lancedb",
        top_k: int = 5,
        min_score: float = 0.6,
    ):
        self.table_name = table_name
        self.db_path = os.path.expanduser(db_path)
        self.top_k = top_k
        self.min_score = min_score
        self._table = None
        self._openai_client = None

    def _get_table(self):
        """延迟初始化 LanceDB 表"""
        if self._table is not None:
            return self._table
        import lancedb
        db = lancedb.connect(self.db_path)
        if self.table_name not in db.table_names():
            return None
        self._table = db.open_table(self.table_name)
        return self._table

    def _get_openai_client(self):
        """延迟初始化 OpenAI 客户端"""
        if self._openai_client is not None:
            return self._openai_client
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("请设置 OPENAI_API_KEY 环境变量")
        from openai import OpenAI
        self._openai_client = OpenAI(api_key=api_key)
        return self._openai_client

    def recall(self, query: str) -> list[RetrievedChunk]:
        """
        根据 query 语义检索记忆
        返回 top_k 条最相关的记忆块（按相似度排序）
        """
        table = self._get_table()
        if table is None:
            return []

        # 1. query → embedding
        client = self._get_openai_client()
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=[query],
        )
        vector = resp.data[0].embedding

        # 2. LanceDB ANN 检索
        results = table.search(vector).limit(self.top_k).to_list()

        # 3. 过滤低分结果
        chunks = []
        for item in results:
            score = item.get("_score", 0)
            if score < self.min_score:
                continue
            chunks.append(RetrievedChunk(
                chunk_id=item["chunk_id"],
                source_file=item["source_file"],
                title=item.get("title", ""),
                heading=item.get("heading", ""),
                content=item["content"],
                score=score,
            ))

        return chunks

    def format_for_context(self, chunks: list[RetrievedChunk]) -> str:
        """
        将检索结果格式化为可注入上下文的文本
        """
        if not chunks:
            return ""
        lines = ["[记忆检索结果]"]
        for c in chunks:
            tag = f"[{c.source_file}]"
            if c.heading:
                tag += f" {c.heading}"
            lines.append(f"{tag} (相似度 {c.score:.0%}):")
            lines.append(c.content)
            lines.append("")
        return "\n".join(lines)


# 便捷函数
def recall_memory(query: str, top_k: int = 5) -> list[RetrievedChunk]:
    """一行调用：recall_memory('之前做过什么')"""
    retriever = VectorRetriever(top_k=top_k)
    return retriever.recall(query)
