#!/usr/bin/env python3
"""
PreferenceEngine - 偏好推断引擎

从对话历史和 KG 实体中推断用户偏好，
使用 LLM 判断任务是否"实质相同"。

使用方法:
    python3 preference_engine.py extract --session-id xxx
    python3 preference_engine.py infer-preference --task-a "xxx" --task-b "yyy"
    python3 preference_engine.py list
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent

# 导入 memory_ontology (在 main() 中动态导入)
sys.path.insert(0, str(SCRIPT_DIR))
from utils.llm_client import LLMClient  # noqa: E402


# ========== LLM 判断缓存 ==========

class LLMCache:
    """LLM 判断结果缓存

    使用内存缓存 + TTL，避免重复 LLM 调用
    """

    def __init__(self, ttl_seconds: int = 1800):  # 默认 30 分钟
        self._cache: Dict[str, Tuple[str, float]] = {}  # key -> (result, timestamp)
        self._ttl = ttl_seconds

    def _make_key(self, task_a: str, task_b: str) -> str:
        """生成缓存 key"""
        # 确保 task_a < task_b（顺序无关）
        if task_a > task_b:
            task_a, task_b = task_b, task_a
        hash_input = f"{task_a}|{task_b}".encode('utf-8')
        return hashlib.md5(hash_input).hexdigest()

    def get(self, task_a: str, task_b: str) -> Optional[str]:
        """获取缓存结果

        Returns:
            缓存结果字符串，如果不存在或过期返回 None
        """
        key = self._make_key(task_a, task_b)
        if key not in self._cache:
            return None

        result, timestamp = self._cache[key]
        if time.time() - timestamp > self._ttl:
            # TTL 过期
            del self._cache[key]
            return None

        return result

    def set(self, task_a: str, task_b: str, result: str):
        """设置缓存"""
        key = self._make_key(task_a, task_b)
        self._cache[key] = (result, time.time())

    def clear(self):
        """清空缓存"""
        self._cache.clear()


# 全局缓存实例
_llm_cache = LLMCache()


# ========== LLM 任务相似度判断 ==========

SIMILARITY_PROMPT = """你是一个任务相似度判断专家。判断两个任务是否"实质相同"。

任务 A: {task_a}

任务 B: {task_b}

判断标准：
- "实质相同": 两个任务的目标相同，即使具体参数不同也算
  - 例如："访问 moltbook" 和 "查看 moltbook 帖子" 是实质相同
  - 例如："优化数据库" 和 "修复数据库性能问题" 是实质相同
- "实质不同": 任务目标完全不同
  - 例如："写代码" 和 "回复邮件" 是实质不同

输出格式（只输出 JSON，不要有其他内容）：
{{
  "is_same": true 或 false,
  "reasoning": "简短解释原因"
}}

注意：
- 只输出 JSON，不要有其他内容
- is_same 为 true 表示实质相同，false 表示实质不同"""

# (LLMClient imported from utils.llm_client above)

def judge_task_similarity(task_a: str, task_b: str, client: LLMClient,
                         use_cache: bool = True) -> Tuple[bool, str]:
    """判断两个任务是否实质相同

    Args:
        task_a: 任务 A 描述
        task_b: 任务 B 描述
        client: LLM 客户端
        use_cache: 是否使用缓存

    Returns:
        (is_same, reasoning) 元组
    """
    # 检查缓存
    if use_cache:
        cached = _llm_cache.get(task_a, task_b)
        if cached:
            print("  [Cache hit] Using cached similarity judgment")
            data = json.loads(cached)
            return data['is_same'], f"[Cache] {data['reasoning']}"

    # 调用 LLM
    prompt = SIMILARITY_PROMPT.format(task_a=task_a, task_b=task_b)
    messages = [
        {"role": "system", "content": "你是一个专业的任务相似度判断助手，只输出 JSON 格式。"},
        {"role": "user", "content": prompt}
    ]

    response = client.call(messages)
    if not response:
        return False, "LLM call failed"

    # 解析响应
    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            data = json.loads(json_str)

            is_same = bool(data.get('is_same', False))
            reasoning = data.get('reasoning', '')

            # 写入缓存
            if use_cache:
                _llm_cache.set(task_a, task_b, json.dumps(data))

            return is_same, reasoning
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Failed to parse LLM response: {e}")
        return False, f"Parse error: {e}"

    return False, "Unknown error"


# ========== PreferenceEngine ==========

# Preference 默认衰减率 (与 memory_ontology.DECAY_RATES['Preference'] 保持一致)
PREFERENCE_DECAY_RATE = 0.90


class PreferenceEngine:
    """偏好推断引擎

    从对话历史和 KG 实体中推断用户偏好。
    """

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self._entities = None

    def _load_entities(self):
        """加载 KG 实体"""
        if self._entities is None:
            from memory_ontology import load_all_entities
            self._entities = load_all_entities()
        return self._entities

    def extract_from_session(self, session_id: str) -> List[Dict]:
        """从会话中提取偏好

        Args:
            session_id: 会话 ID

        Returns:
            提取的偏好列表
        """
        from memory_ontology import (
            create_entity, get_default_decay_rate, get_entities_by_type
        )

        entities = self._load_entities()

        # 查找与该 session 相关的实体
        session_entities = []
        for entity in entities.values():
            props = entity.get('properties', {})
            source = props.get('source', '')
            if session_id in source:
                session_entities.append(entity)

        if not session_entities:
            print(f"  No entities found for session {session_id}")
            return []

        # 尝试推断偏好
        preferences = []
        for entity in session_entities:
            props = entity.get('properties', {})
            title = props.get('title', '')

            # 检查是否有相似实体
            similar = self._find_similar_entities(entity, entities)
            if similar:
                # 发现了偏好模式
                preference = self._infer_preference(entity, similar)
                if preference:
                    preferences.append(preference)

        # 创建偏好实体
        created_prefs = []
        for pref in preferences:
            try:
                entity = create_entity('Preference', pref)
                print(f"  ✓ Created Preference: {pref.get('title', 'unnamed')}")
                created_prefs.append(entity)
            except Exception as e:
                print(f"  ✗ Failed to create preference: {e}")

        return created_prefs

    def _find_similar_entities(self, entity: Dict, all_entities: Dict) -> List[Dict]:
        """查找相似的实体（用于偏好推断）

        Args:
            entity: 当前实体
            all_entities: 所有实体

        Returns:
            相似实体列表
        """
        similar = []
        title = entity.get('properties', {}).get('title', '')

        if not title:
            return similar

        for other in all_entities.values():
            if other['id'] == entity['id']:
                continue

            other_title = other.get('properties', {}).get('title', '')
            if not other_title:
                continue

            # 使用 LLM 判断相似性
            is_same, reasoning = judge_task_similarity(
                title, other_title, self.llm_client
            )

            if is_same:
                similar.append({
                    'entity': other,
                    'reasoning': reasoning
                })
                print(f"  Found similar: {title} <-> {other_title} ({reasoning})")

        return similar

    def _infer_preference(self, entity: Dict, similar: List[Dict]) -> Optional[Dict]:
        """从相似实体推断偏好

        Args:
            entity: 当前实体
            similar: 相似实体列表

        Returns:
            偏好属性字典
        """
        if not similar:
            return None

        entity_type = entity['type']
        props = entity.get('properties', {})
        title = props.get('title', '')

        # 推断偏好类型
        preference_type = self._classify_preference_type(entity_type, title, similar)

        # 计算置信度（基于相似实体数量）
        confidence = min(1.0, 0.5 + 0.1 * len(similar))

        now = datetime.now().astimezone().isoformat()

        preference = {
            'title': f"偏好: {title}",
            'pattern': title,
            'preference_type': preference_type,
            'confidence': confidence,
            'learned_from': [e['entity']['id'] for e in similar],
            'learned_at': now,
            'last_accessed': now,
            'strength': 1.0,
            'decay_rate': PREFERENCE_DECAY_RATE,
            'source_trust': 'medium' if len(similar) < 3 else 'high',
            'provenance': ['inference:preference_engine'],
            'tags': ['#preference', f'#{preference_type}']
        }

        return preference

    def _classify_preference_type(self, entity_type: str, title: str,
                                   similar: List[Dict]) -> str:
        """分类偏好类型

        Returns:
            preference_type: temporal | tool | frequency | action
        """
        title_lower = title.lower()

        # 时间模式
        time_keywords = ['早上', '中午', '晚上', '周', '周末', '工作日', 'am', 'pm', 'morning', 'afternoon', 'evening']
        if any(kw in title_lower for kw in time_keywords):
            return 'temporal'

        # 工具选择
        tool_keywords = ['使用', '用', 'token', 'api', '网页', '直接', '访问', '工具', 'method', 'way']
        if any(kw in title_lower for kw in tool_keywords):
            return 'tool'

        # 频率
        freq_keywords = ['每天', '每周', '经常', '总是', '定期', 'daily', 'weekly', 'often']
        if any(kw in title_lower for kw in freq_keywords):
            return 'frequency'

        # 默认：动作偏好
        return 'action'


# ========== Preference Entity Schema ==========

PREFERENCE_SCHEMA = """
Preference:
  required: [title, pattern, preference_type, learned_at]
  properties:
    title:
      type: string
      description: "偏好标题"
    pattern:
      type: string
      description: "偏好模式（任务描述）"
    preference_type:
      type: string
      enum: [temporal, tool, frequency, action]
      description: "偏好类型"
    confidence:
      type: number
      description: "置信度 (0.0-1.0)"
    learned_from:
      type: array
      description: "学习来源实体 ID 列表"
    learned_at:
      type: string
      description: "学习时间 (ISO 8601)"
    tags:
      type: array
      description: "标签列表"
"""


# ========== Main ==========

def main():
    import argparse

    parser = argparse.ArgumentParser(description='PreferenceEngine - 偏好推断引擎')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='从会话提取偏好')
    extract_parser.add_argument('--session-id', required=True, help='会话 ID')

    # infer-preference 命令
    infer_parser = subparsers.add_parser('infer-preference', help='判断任务相似性')
    infer_parser.add_argument('--task-a', required=True, help='任务 A 描述')
    infer_parser.add_argument('--task-b', required=True, help='任务 B 描述')
    infer_parser.add_argument('--no-cache', action='store_true', help='禁用缓存')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有偏好')

    # cache-clear 命令
    cache_parser = subparsers.add_parser('cache-clear', help='清空缓存')

    args = parser.parse_args()

    # 动态导入 memory_ontology
    sys.path.insert(0, str(SCRIPT_DIR))
    from memory_ontology import (
        query_entities, create_entity, get_default_decay_rate, load_all_entities
    )

    if args.command == 'extract':
        print(f"\n🔍 从会话 {args.session_id} 提取偏好...")

        engine = PreferenceEngine()
        preferences = engine.extract_from_session(args.session_id)

        print(f"\n✓ 提取了 {len(preferences)} 个偏好")

    elif args.command == 'infer-preference':
        print(f"\n🤔 判断任务相似性...")
        print(f"任务 A: {args.task_a}")
        print(f"任务 B: {args.task_b}")

        client = LLMClient()
        is_same, reasoning = judge_task_similarity(
            args.task_a, args.task_b, client,
            use_cache=not args.no_cache
        )

        print(f"\n结果: {'实质相同' if is_same else '实质不同'}")
        print(f"原因: {reasoning}")

    elif args.command == 'list':
        print("\n📋 所有偏好实体:")
        preferences = query_entities(entity_type='Preference')
        print(f"共 {len(preferences)} 个偏好")

        for pref in preferences:
            props = pref.get('properties', {})
            title = props.get('title', 'unnamed')
            ptype = props.get('preference_type', 'unknown')
            confidence = props.get('confidence', 0)
            print(f"  - {title} ({ptype}) - confidence: {confidence:.0%}")

    elif args.command == 'cache-clear':
        _llm_cache.clear()
        print("✓ 缓存已清空")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
