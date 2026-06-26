"""
记忆去重模块

检测并处理重复记忆，避免存储冗余数据
"""

import hashlib
import sqlite3
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DedupResult:
    """去重结果"""
    is_duplicate: bool
    similar_memories: List[Dict]
    similarity_score: float
    recommendation: str  # "SKIP", "MERGE", "STORE"


class MemoryDeduplicator:
    """记忆去重器"""

    def __init__(self, db_path: Optional[str] = None):
        """
        初始化去重器

        Args:
            db_path: SQLite 数据库路径
        """
        if db_path is None:
            db_path = str(Path.home() / ".openclaw" / "memory" / "main.sqlite")

        self.db_path = db_path
        self.similarity_threshold = 0.85  # 相似度阈值

    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        # 规范化内容（移除空白、转小写）
        normalized = ' '.join(content.lower().split())
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]

    def _compute_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度（简单版本）

        使用 Jaccard 相似度
        """
        # 分词
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())

        # 计算 Jaccard 相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    def check_duplicate(self, content: str, user_id: str = "default") -> DedupResult:
        """
        检查记忆是否重复

        Args:
            content: 记忆内容
            user_id: 用户 ID

        Returns:
            DedupResult: 去重结果
        """
        # 计算哈希
        content_hash = self._compute_hash(content)

        # 查询数据库
        similar_memories = []
        max_similarity = 0.0

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 查询所有记忆（简化版本，实际应该用向量搜索）
            cursor.execute("""
                SELECT id, content, user_id, created_at
                FROM memories
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 100
            """, (user_id,))

            rows = cursor.fetchall()

            for row in rows:
                similarity = self._compute_similarity(content, row['content'])

                if similarity >= self.similarity_threshold:
                    similar_memories.append({
                        'id': row['id'],
                        'content': row['content'][:200],  # 截断
                        'similarity': similarity,
                        'created_at': row['created_at']
                    })

                    if similarity > max_similarity:
                        max_similarity = similarity

            conn.close()

        except Exception as e:
            # 数据库不存在或查询失败
            pass

        # 判断是否重复
        is_duplicate = max_similarity >= self.similarity_threshold

        # 生成建议
        if is_duplicate:
            if max_similarity >= 0.95:
                recommendation = "SKIP"  # 几乎完全相同，跳过
            elif max_similarity >= 0.90:
                recommendation = "MERGE"  # 高度相似，建议合并
            else:
                recommendation = "STORE"  # 相似度较低，可以存储
        else:
            recommendation = "STORE"

        return DedupResult(
            is_duplicate=is_duplicate,
            similar_memories=similar_memories,
            similarity_score=max_similarity,
            recommendation=recommendation
        )

    def batch_check_duplicates(self, contents: List[str], user_id: str = "default") -> List[DedupResult]:
        """
        批量检查重复

        Args:
            contents: 记忆内容列表
            user_id: 用户 ID

        Returns:
            List[DedupResult]: 去重结果列表
        """
        results = []
        for content in contents:
            result = self.check_duplicate(content, user_id)
            results.append(result)
        return results


if __name__ == "__main__":
    # 测试去重功能
    print("=== 记忆去重测试 ===\n")

    deduplicator = MemoryDeduplicator()

    # 测试样本
    test_contents = [
        "2026-04-03 完成 Memory-Plus 开发。",
        "2026-04-03 完成 Memory-Plus 开发。",  # 完全重复
        "2026-04-03 完成了 Memory-Plus 的开发工作。",  # 高度相似
        "2026-04-03 参加 AI 架构评审会议。",  # 不同内容
    ]

    for i, content in enumerate(test_contents, 1):
        print(f"\n测试 {i}: {content[:50]}...")
        result = deduplicator.check_duplicate(content)

        print(f"  是否重复：{result.is_duplicate}")
        print(f"  相似度：{result.similarity_score:.2f}")
        print(f"  建议：{result.recommendation}")

        if result.similar_memories:
            print(f"  相似记忆：{len(result.similar_memories)} 条")
            for mem in result.similar_memories[:3]:
                print(f"    - {mem['content'][:50]}... (相似度：{mem['similarity']:.2f})")

    print("\n=== 测试完成 ===")
