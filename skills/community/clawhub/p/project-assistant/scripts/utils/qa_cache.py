#!/usr/bin/env python3
"""
问答缓存管理器
缓存问题和答案，支持快速检索相似问题

特性：
- 问题规范化（去除无关词、统一表述）
- 相似问题匹配
- 答案缓存和检索
- 过期清理
"""

import os
import json
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class QACacheEntry:
    """问答缓存条目"""
    question: str                          # 原始问题
    normalized: str                        # 规范化问题
    intent: str = ""                       # 意图类型
    answer: str = ""                       # 答案内容
    answer_format: str = "markdown"        # 答案格式
    file_refs: List[str] = field(default_factory=list)  # 涉及的文件
    created_at: str = ""                   # 创建时间
    access_count: int = 0                  # 访问次数
    last_accessed: str = ""                # 最后访问时间
    confidence: float = 1.0                # 置信度


# 问题规范化映射
QUESTION_NORMALIZE_PATTERNS = [
    # 去除语气词
    (r'(请问|请教|帮我|帮忙|能不能|可以|能否|我想知道)', ''),
    (r'(吗|呢|呀|吧|啊)\?*$', '?'),
    (r'(怎么样|如何|怎么)', '怎么'),
    (r'(在哪里|在哪|哪个文件|哪个位置)', '在哪里'),
    (r'(是什么|是啥|啥是)', '是什么'),
    (r'(为什么|为啥)', '为什么'),
    # 统一表述
    (r'(实现|实现方式|实现方法)', '实现'),
    (r'(函数|方法|接口)', '函数'),
    (r'(文件|代码|源码)', '文件'),
    (r'(模块|组件|功能)', '模块'),
]

# 问题类型关键词
INTENT_KEYWORDS = {
    'LOCATION': ['在哪里', '哪个文件', '位置', '在哪', '路径'],
    'EXPLAIN': ['怎么实现', '原理', '如何工作', '实现方式', '机制'],
    'MODIFY': ['如何修改', '怎么改', '添加', '删除', '变更'],
    'DEBUG': ['为什么', '报错', '错误', '问题', '不工作', '失败'],
    'IMPACT': ['影响', '后果', '会怎样', '风险'],
    'GUIDE': ['怎么构建', '如何运行', '命令', '怎么用', '如何部署'],
    'COMPARE': ['区别', '对比', '差异', '不同'],
    'ARCHITECTURE': ['架构', '设计', '结构', '整体'],
}


class QACacheManager:
    """问答缓存管理器"""

    def __init__(self, project_dir: str, ttl_days: int = 7):
        self.project_dir = Path(project_dir).resolve()
        self.ttl_days = ttl_days
        self._cache_path = self.project_dir / '.claude' / 'qa_cache.json'
        self._cache: Dict[str, QACacheEntry] = {}
        self._dirty = False

    def _load(self) -> Dict[str, QACacheEntry]:
        """加载缓存"""
        if self._cache:
            return self._cache

        if self._cache_path.exists():
            try:
                with open(self._cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for key, entry in data.get('entries', {}).items():
                    self._cache[key] = QACacheEntry(
                        question=entry.get('question', ''),
                        normalized=entry.get('normalized', ''),
                        intent=entry.get('intent', ''),
                        answer=entry.get('answer', ''),
                        answer_format=entry.get('answer_format', 'markdown'),
                        file_refs=entry.get('file_refs', []),
                        created_at=entry.get('created_at', ''),
                        access_count=entry.get('access_count', 0),
                        last_accessed=entry.get('last_accessed', ''),
                        confidence=entry.get('confidence', 1.0),
                    )
            except Exception:
                self._cache = {}
        return self._cache

    def _save(self) -> None:
        """保存缓存"""
        if not self._dirty:
            return

        self._cache_path.parent.mkdir(parents=True, exist_ok=True)

        entries = {}
        for key, entry in self._cache.items():
            entries[key] = {
                'question': entry.question,
                'normalized': entry.normalized,
                'intent': entry.intent,
                'answer': entry.answer,
                'answer_format': entry.answer_format,
                'file_refs': entry.file_refs,
                'created_at': entry.created_at,
                'access_count': entry.access_count,
                'last_accessed': entry.last_accessed,
                'confidence': entry.confidence,
            }

        data = {
            'version': '1.0',
            'updated_at': datetime.now().isoformat(),
            'entries': entries,
        }

        with open(self._cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self._dirty = False

    def normalize_question(self, question: str) -> str:
        """规范化问题"""
        q = question.strip().lower()

        # 应用规范化模式
        for pattern, replacement in QUESTION_NORMALIZE_PATTERNS:
            q = re.sub(pattern, replacement, q)

        # 去除多余空格
        q = re.sub(r'\s+', ' ', q).strip()

        # 去除标点（保留问号）
        q = re.sub(r'[，。！、；：""''【】（）]', '', q)

        return q

    def detect_intent(self, question: str) -> str:
        """检测问题意图"""
        q_lower = question.lower()

        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in q_lower:
                    return intent

        return 'GENERAL'

    def generate_key(self, question: str) -> str:
        """生成缓存键"""
        normalized = self.normalize_question(question)
        return hashlib.md5(normalized.encode()).hexdigest()[:16]

    def find_similar(self, question: str, threshold: float = 0.6
                     ) -> Optional[Tuple[str, QACacheEntry, float]]:
        """查找相似问题

        Args:
            question: 用户问题
            threshold: 相似度阈值

        Returns:
            (key, entry, similarity) 或 None
        """
        cache = self._load()
        normalized = self.normalize_question(question)
        intent = self.detect_intent(question)

        best_match = None
        best_score = 0.0

        for key, entry in cache.items():
            # 意图相同加分
            if entry.intent == intent:
                score = self._calculate_similarity(normalized, entry.normalized)
                score += 0.1  # 意图加分
            else:
                score = self._calculate_similarity(normalized, entry.normalized) * 0.8

            if score > best_score and score >= threshold:
                best_score = score
                best_match = (key, entry, score)

        return best_match

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单Jaccard）"""
        words1 = set(text1)
        words2 = set(text2)

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def get(self, question: str) -> Optional[QACacheEntry]:
        """获取缓存的答案"""
        cache = self._load()
        key = self.generate_key(question)

        entry = cache.get(key)
        if entry:
            # 更新访问记录
            entry.access_count += 1
            entry.last_accessed = datetime.now().isoformat()
            self._dirty = True
            self._save()
            return entry

        # 尝试查找相似问题
        similar = self.find_similar(question)
        if similar:
            key, entry, score = similar
            entry.access_count += 1
            entry.last_accessed = datetime.now().isoformat()
            entry.confidence = score  # 更新置信度
            self._dirty = True
            self._save()
            return entry

        return None

    def set(self, question: str, answer: str,
            intent: str = None,
            file_refs: List[str] = None,
            answer_format: str = "markdown") -> None:
        """缓存问答"""
        cache = self._load()
        key = self.generate_key(question)
        normalized = self.normalize_question(question)

        if intent is None:
            intent = self.detect_intent(question)

        now = datetime.now().isoformat()

        entry = QACacheEntry(
            question=question,
            normalized=normalized,
            intent=intent,
            answer=answer,
            answer_format=answer_format,
            file_refs=file_refs or [],
            created_at=now,
            access_count=1,
            last_accessed=now,
            confidence=1.0,
        )

        cache[key] = entry
        self._dirty = True
        self._save()

    def invalidate_files(self, changed_files: List[str]) -> int:
        """使涉及变更文件的缓存失效

        Args:
            changed_files: 变更的文件列表

        Returns:
            失效的缓存条目数
        """
        cache = self._load()
        invalidated = 0

        keys_to_remove = []
        for key, entry in cache.items():
            # 检查是否有涉及变更文件的引用
            for ref in entry.file_refs:
                for changed in changed_files:
                    if changed in ref or ref in changed:
                        keys_to_remove.append(key)
                        invalidated += 1
                        break

        for key in keys_to_remove:
            del cache[key]

        if invalidated > 0:
            self._dirty = True
            self._save()

        return invalidated

    def cleanup_expired(self) -> int:
        """清理过期缓存

        Returns:
            清理的条目数
        """
        cache = self._load()
        cutoff = datetime.now() - timedelta(days=self.ttl_days)

        keys_to_remove = []
        for key, entry in cache.items():
            try:
                created = datetime.fromisoformat(entry.created_at)
                if created < cutoff:
                    keys_to_remove.append(key)
            except Exception:
                pass

        for key in keys_to_remove:
            del cache[key]

        if keys_to_remove:
            self._dirty = True
            self._save()

        return len(keys_to_remove)

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        cache = self._load()

        intents = {}
        total_access = 0

        for entry in cache.values():
            intents[entry.intent] = intents.get(entry.intent, 0) + 1
            total_access += entry.access_count

        return {
            'total_entries': len(cache),
            'total_access': total_access,
            'by_intent': intents,
            'cache_file': str(self._cache_path),
        }

    def clear(self) -> None:
        """清空缓存"""
        self._cache = {}
        self._dirty = True
        self._save()


def main():
    """命令行接口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: qa_cache.py <command> <project_dir> [args]")
        print("\nCommands:")
        print("  get <project_dir> <question>      Get cached answer")
        print("  set <project_dir> <question> <answer>  Set cache")
        print("  stats <project_dir>              Show statistics")
        print("  cleanup <project_dir>            Cleanup expired")
        print("  clear <project_dir>              Clear all cache")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'get':
        if len(sys.argv) < 4:
            print("Usage: qa_cache.py get <project_dir> <question>")
            sys.exit(1)

        project_dir = sys.argv[2]
        question = sys.argv[3]

        manager = QACacheManager(project_dir)
        entry = manager.get(question)

        if entry:
            print(json.dumps({
                'found': True,
                'question': entry.question,
                'intent': entry.intent,
                'answer': entry.answer[:200] + '...' if len(entry.answer) > 200 else entry.answer,
                'confidence': entry.confidence,
                'access_count': entry.access_count,
            }, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({'found': False}))

    elif command == 'set':
        if len(sys.argv) < 5:
            print("Usage: qa_cache.py set <project_dir> <question> <answer>")
            sys.exit(1)

        project_dir = sys.argv[2]
        question = sys.argv[3]
        answer = sys.argv[4]

        manager = QACacheManager(project_dir)
        manager.set(question, answer)

        print(json.dumps({'success': True, 'message': 'Cache saved'}))

    elif command == 'stats':
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

        manager = QACacheManager(project_dir)
        stats = manager.get_stats()

        print(json.dumps(stats, indent=2, ensure_ascii=False))

    elif command == 'cleanup':
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

        manager = QACacheManager(project_dir)
        removed = manager.cleanup_expired()

        print(json.dumps({'success': True, 'removed': removed}))

    elif command == 'clear':
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

        manager = QACacheManager(project_dir)
        manager.clear()

        print(json.dumps({'success': True, 'message': 'Cache cleared'}))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()