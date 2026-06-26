# -*- coding: utf-8 -*-
"""
Memory子Skill
用户记忆的存储和检索
"""

import re
from typing import List, Dict, Optional, Set
from pathlib import Path
from datetime import datetime
import jieba


class MemorySkill:
    """
    Memory子Skill - 供Agent主动查阅用户记忆
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory_dir = Path(__file__).parent.parent / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_dir / f"{user_id}.md"
        self._memories: List[Dict] = []
        self._loaded = False

    def _ensure_loaded(self):
        """确保记忆已加载"""
        if not self._loaded:
            self._memories = self._parse_file()
            self._loaded = True

    def _parse_file(self) -> List[Dict]:
        """
        解析markdown记忆文件

        Returns:
            记忆条目列表
        """
        if not self.memory_file.exists():
            return []

        memories = []
        current = None
        current_category = ""

        with open(self.memory_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # 识别记忆条目标题 (### 标题)
                if line.startswith("### "):
                    if current:
                        memories.append(current)
                    current = {
                        "title": line[4:],
                        "tags": [],
                        "content": "",
                        "category": current_category
                    }

                # 识别Tags行
                elif line.startswith("Tags:") and current:
                    tags_str = line[5:].strip()
                    current["tags"] = [t.strip() for t in tags_str.split(",") if t.strip()]

                # 识别Content行
                elif line.startswith("Content:") and current:
                    current["content"] = line[8:].strip()

                # 识别分类标题 (## 分类)
                elif line.startswith("## "):
                    current_category = line[3:]

            # 最后一条
            if current:
                memories.append(current)

        return memories

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        根据query检索相关记忆

        Args:
            query: 查询文本（如segment的content_focus）
            top_k: 返回条数

        Returns:
            格式化后的记忆文本列表
        """
        self._ensure_loaded()

        if not self._memories:
            return []

        # 分词
        query_words = set(jieba.cut(query.lower()))
        # 过滤停用词（简单过滤单字和标点）
        query_words = {w for w in query_words if len(w) > 1}

        if not query_words:
            return []

        # 计算匹配分数
        scored = []
        for mem in self._memories:
            # 从tags和content中提取关键词
            mem_tags = set(t.lower() for t in mem.get("tags", []))
            mem_content_words = set(jieba.cut(mem.get("content", "").lower()))

            # 计算匹配
            tag_match = len(query_words & mem_tags)
            content_match = len(query_words & mem_content_words)

            # Tags权重3倍，Content权重1倍
            score = tag_match * 3 + content_match * 1

            if score > 0:
                scored.append((mem, score))

        # 按分数排序
        scored.sort(key=lambda x: -x[1])

        # 格式化返回
        results = []
        for mem, score in scored[:top_k]:
            formatted = f"[{mem['title']}] {mem['content']}"
            results.append(formatted)

        return results

    def add(self, title: str, content: str, tags: List[str], category: str = "") -> bool:
        """
        添加新记忆

        Args:
            title: 记忆标题
            content: 记忆内容
            tags: 标签列表
            category: 分类（如"经历类"、"观点类"）

        Returns:
            是否添加成功
        """
        try:
            # 确保文件有基础结构
            if not self.memory_file.exists():
                self._init_memory_file()

            # 追加新记忆
            with open(self.memory_file, "a", encoding="utf-8") as f:
                if category:
                    f.write(f"\n## {category}\n")
                f.write(f"\n### {title}\n")
                f.write(f"Tags: {', '.join(tags)}\n")
                f.write(f"Content: {content}\n")

            # 刷新缓存
            self._memories = self._parse_file()

            return True

        except Exception as e:
            print(f"添加记忆失败: {e}")
            return False

    def _init_memory_file(self):
        """初始化记忆文件"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            f.write(f"# Memory: {self.user_id}\n")
            f.write(f"# Created: {datetime.now().isoformat()}\n\n")
            f.write("## 经历类\n\n")
            f.write("## 观点类\n\n")

    def init_from_persona(self, memory_seed: List[Dict]) -> bool:
        """
        从Persona的memory_seed初始化记忆文件

        Args:
            memory_seed: Persona提取时的记忆种子

        Returns:
            是否初始化成功
        """
        if not memory_seed:
            return False

        try:
            # 清空或创建文件
            with open(self.memory_file, "w", encoding="utf-8") as f:
                f.write(f"# Memory: {self.user_id}\n")
                f.write(f"# Created: {datetime.now().isoformat()}\n")
                f.write(f"# Source: Persona extraction\n\n")

                f.write("## 经历类\n\n")

                for mem in memory_seed:
                    if isinstance(mem, dict):
                        title = mem.get("title", "")
                        content = mem.get("content", "")
                        tags = mem.get("tags", [])

                        if title and content:
                            f.write(f"### {title}\n")
                            f.write(f"Tags: {', '.join(tags)}\n")
                            f.write(f"Content: {content}\n\n")

            # 刷新缓存
            self._memories = self._parse_file()

            return True

        except Exception as e:
            print(f"从Persona初始化记忆失败: {e}")
            return False

    def get_all_tags(self) -> Set[str]:
        """获取所有标签（用于调试）"""
        self._ensure_loaded()
        tags = set()
        for mem in self._memories:
            tags.update(mem.get("tags", []))
        return tags

    def get_stats(self) -> Dict:
        """获取记忆统计"""
        self._ensure_loaded()
        return {
            "total_memories": len(self._memories),
            "total_tags": len(self.get_all_tags()),
            "file_exists": self.memory_file.exists()
        }


# 便捷函数
def quick_retrieve(user_id: str, query: str, top_k: int = 3) -> List[str]:
    """便捷检索函数"""
    skill = MemorySkill(user_id)
    return skill.retrieve(query, top_k)
