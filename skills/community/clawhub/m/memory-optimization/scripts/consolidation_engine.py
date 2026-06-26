#!/usr/bin/env python3
"""
ConsolidationEngine - Phase 3 Consolidation Engine

将重复的 Episodic Memory (Decision, Finding等) 合并为 Semantic Memory (SkillCard)。
使用 LLM 判断实体是否"实质相同"，采用保守策略：冲突 → 标记待审核，不自动合并。

使用方法:
    python3 consolidation_engine.py run --dry-run
    python3 consolidation_engine.py run
    python3 consolidation_engine.py status
"""

import json
import os
import sys
import time
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent

# 导入 memory_ontology 和 preference_engine
sys.path.insert(0, str(SCRIPT_DIR))
from utils.llm_client import LLMClient  # noqa: E402

# ========== LLM 判断缓存 (从 preference_engine 复用) ==========

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
        """获取缓存结果"""
        key = self._make_key(task_a, task_b)
        if key not in self._cache:
            return None

        result, timestamp = self._cache[key]
        if time.time() - timestamp > self._ttl:
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

# (LLMClient imported from utils.llm_client above)

# ========== Consolidation Prompt ==========

CONSOLIDATION_PROMPT = """你是一个任务/知识合并判断专家。判断两个实体是否"实质相同"可以合并为技能卡片。

实体 A:
- 类型: {type_a}
- 标题: {title_a}
- 内容: {content_a}
- 标签: {tags_a}

实体 B:
- 类型: {type_b}
- 标题: {title_b}
- 内容: {content_b}
- 标签: {tags_b}

判断标准：
- "merge": 两个实体描述的是同一个概念/技能/经验，核心信息高度重叠，可以合并为一个技能卡片
  - 例如：两个 Decision 都关于"使用知识图谱管理记忆"
  - 例如：两个 Finding 都关于"上下文压缩后恢复效率低"
- "conflict": 两个实体描述了相关但不兼容的信息，存在潜在冲突
  - 例如：一个说"应该用方法A"，另一个说"应该用方法B"
  - 例如：一个 Finding 说"X是正确的"，另一个 Finding 说"X是错误的"
- "keep_separate": 两个实体虽然可能相似，但描述的是不同的具体内容，不应合并

输出格式（只输出 JSON，不要有其他内容）：
{{
  "decision": "merge" 或 "conflict" 或 "keep_separate",
  "reasoning": "简短解释判断原因",
  "summary": "如果决定 merge，提供合并后的技能卡片摘要",
  "confidence": 0.0 到 1.0 的置信度
}}

注意：
- 只输出 JSON，不要有其他内容
- decision 为 merge 时，summary 应该是一个简洁的技能卡片描述（50字以内）
- confidence 反映你对判断的自信程度"""


# ========== 数据类 ==========

@dataclass
class ConsolidationDecision:
    """LLM 的合并判断结果"""
    decision: str  # "merge" | "conflict" | "keep_separate"
    reasoning: str
    summary: str
    confidence: float


@dataclass
class CandidatePair:
    """候选实体对"""
    entity1: Dict
    entity2: Dict
    blocking_key: str  # 用于去重的键


# ========== BlockingIndex ==========

class BlockingIndex:
    """多级 Blocking 索引

    用于高效地找到可能需要合并的候选实体对。
    采用多级 blocking 策略：
    - Level 1: 同 type
    - Level 2: 共享 tags (最多3个)
    - Level 3: 共享 title words (最多3个)
    """

    # 允许跨类型合并的类型组合
    ALLOWED_CROSS_TYPES = {
        ('Decision', 'Finding'),
        ('LessonLearned', 'Finding'),
        ('LessonLearned', 'Decision'),
        ('Finding', 'Finding'),
        ('Decision', 'Decision'),
    }

    # 停用词
    STOPWORDS = {'的', '是', '在', '和', '了', '与', '或', 'a', 'an', 'the', 'is', 'and', 'or'}

    def __init__(self, entities: List[Dict]):
        self.entities = entities
        self._by_type: Dict[str, List[Dict]] = defaultdict(list)
        self._by_tag: Dict[str, List[Dict]] = defaultdict(list)
        self._by_word: Dict[str, List[Dict]] = defaultdict(list)
        self._entity_ids: Set[str] = set()
        self._consolidated_ids: Set[str] = set()

        self.build()

    def build(self):
        """构建索引"""
        for entity in self.entities:
            entity_id = entity['id']
            props = entity.get('properties', {})

            # CRITICAL: 过滤掉已经合并到 SkillCard 的实体
            if props.get('consolidated_into'):
                self._consolidated_ids.add(entity_id)
                continue

            # Phase 8: 过滤掉显著性过低的实体
            # significance_score < 0.3 的实体不参与 consolidation
            sig_score = props.get('significance_score', 0.5)  # 默认 0.5 向后兼容
            if sig_score < 0.3:
                self._consolidated_ids.add(entity_id)
                continue

            self._entity_ids.add(entity_id)

            # Level 1: 按 type 索引
            entity_type = entity['type']
            self._by_type[entity_type].append(entity)

            # Level 2: 按 tags 索引
            tags = props.get('tags', [])
            for tag in tags[:3]:  # 最多3个标签
                self._by_tag[tag].append(entity)

            # Level 3: 按 title words 索引
            title = props.get('title', '')
            words = self._normalize_for_blocking(title)[:3]  # 最多3个词
            for word in words:
                self._by_word[word].append(entity)

    def _normalize_for_blocking(self, text: str) -> List[str]:
        """标准化文本用于 blocking

        Args:
            text: 输入文本

        Returns:
            词列表（去停用词，小写）
        """
        if not text:
            return []

        # 移除标点符号
        for char in [' ', ',', '.', '!', '?', '，', '。', '！', '？', '(', ')', '（', '）']:
            text = text.replace(char, '')

        # 对于中文文本，使用 bigrams（2字符组合）作为词
        # 对于英文文本，按空格分割
        words = []
        if any('\u4e00' <= c <= '\u9fff' for c in text):  # 包含中文
            # 中文 bigrams
            text_lower = text.lower()
            for i in range(len(text_lower) - 1):
                bigram = text_lower[i:i+2]
                if bigram not in self.STOPWORDS:
                    words.append(bigram)
        else:
            # 英文按空格分割
            for word in text.split():
                word = word.lower().strip()
                if word and word not in self.STOPWORDS:
                    words.append(word)

        return words

    def get_candidates(self, max_candidates: int = 100) -> List[CandidatePair]:
        """获取候选实体对

        Args:
            max_candidates: 最大候选对数量限制

        Returns:
            候选实体对列表
        """
        seen_pairs: Set[Tuple[str, str]] = set()
        candidates: List[CandidatePair] = []

        # 按 type 分组获取候选
        for entity_type, type_entities in self._by_type.items():
            for i, e1 in enumerate(type_entities):
                for e2 in type_entities[i + 1:]:
                    pair_key = tuple(sorted([e1['id'], e2['id']]))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    if self._is_allowed_pair(e1, e2):
                        blocking_key = f"type:{entity_type}"
                        candidates.append(CandidatePair(e1, e2, blocking_key))

                    if len(candidates) >= max_candidates:
                        return candidates

        # 按共享 tags 获取候选
        for tag, tag_entities in self._by_tag.items():
            for i, e1 in enumerate(tag_entities):
                for e2 in tag_entities[i + 1:]:
                    pair_key = tuple(sorted([e1['id'], e2['id']]))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    if self._is_allowed_pair(e1, e2):
                        blocking_key = f"tag:{tag}"
                        candidates.append(CandidatePair(e1, e2, blocking_key))

                    if len(candidates) >= max_candidates:
                        return candidates

        # 按共享 title words 获取候选
        for word, word_entities in self._by_word.items():
            for i, e1 in enumerate(word_entities):
                for e2 in word_entities[i + 1:]:
                    pair_key = tuple(sorted([e1['id'], e2['id']]))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    if self._is_allowed_pair(e1, e2):
                        blocking_key = f"word:{word}"
                        candidates.append(CandidatePair(e1, e2, blocking_key))

                    if len(candidates) >= max_candidates:
                        return candidates

        return candidates

    def _is_allowed_pair(self, e1: Dict, e2: Dict) -> bool:
        """检查实体对是否允许合并

        Args:
            e1: 实体1
            e2: 实体2

        Returns:
            是否允许
        """
        type1 = e1['type']
        type2 = e2['type']

        # 同类型总是允许
        if type1 == type2:
            return True

        # 跨类型检查是否在允许列表中
        pair = tuple(sorted([type1, type2]))
        return pair in self.ALLOWED_CROSS_TYPES


# ========== ConsolidationEngine ==========

class ConsolidationEngine:
    """Consolidation Engine

    将重复的 Episodic Memory 合并为 Semantic Memory (SkillCard)。
    """

    # Jaccard 相似度阈值，低于此值不考虑合并
    JACCARD_THRESHOLD = 0.3

    def __init__(self, llm_client: Optional[LLMClient] = None, cache: Optional[LLMCache] = None):
        self.llm_client = llm_client or LLMClient()
        self.cache = cache or _llm_cache

        # 动态导入 memory_ontology 函数
        from memory_ontology import (
            load_all_entities, create_entity, mark_entity_consolidated,
            generate_entity_id, get_default_decay_rate, ensure_ontology_dir
        )
        self._load_entities = load_all_entities
        self._create_entity = create_entity
        self._mark_consolidated = mark_entity_consolidated
        self._generate_id = generate_entity_id
        self._get_decay_rate = get_default_decay_rate
        self._ensure_dir = ensure_ontology_dir

        # 统计
        self.stats = {
            'candidates_evaluated': 0,
            'merges': 0,
            'conflicts': 0,
            'kept_separate': 0,
            'errors': 0,
            'cache_hits': 0,
        }

    def _text_similarity(self, text1: str, text2: str) -> float:
        """计算文本 Jaccard 相似度

        Args:
            text1: 文本1
            text2: 文本2

        Returns:
            Jaccard 相似度 (0.0 - 1.0)
        """
        if not text1 or not text2:
            return 0.0

        # 分词
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # Jaccard 相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        if union == 0:
            return 0.0

        return intersection / union

    def _get_entity_content(self, entity: Dict) -> str:
        """获取实体的主要内容"""
        props = entity.get('properties', {})
        content_parts = []

        for field in ['title', 'rationale', 'content', 'lesson', 'description']:
            if field in props and props[field]:
                content_parts.append(str(props[field]))

        return ' '.join(content_parts)

    def _make_llm_cache_key(self, entity1: Dict, entity2: Dict) -> Tuple[str, str]:
        """生成 LLM 缓存 key"""
        content1 = self._get_entity_content(entity1)
        content2 = self._get_entity_content(entity2)
        return (content1, content2)

    def find_candidate_pairs(self, max_pairs: int = 100) -> List[CandidatePair]:
        """找到需要评估的候选实体对

        Args:
            max_pairs: 最大候选对数量

        Returns:
            候选实体对列表
        """
        entities = self._load_entities()
        entity_list = list(entities.values())

        # 过滤掉非 Episodic Memory 类型
        allowed_types = {'Decision', 'Finding', 'LessonLearned', 'Commitment'}
        entity_list = [e for e in entity_list if e['type'] in allowed_types]

        # 构建 BlockingIndex
        index = BlockingIndex(entity_list)

        # 获取候选
        candidates = index.get_candidates(max_candidates=max_pairs)

        # Jaccard 预过滤
        filtered = []
        for pair in candidates:
            content1 = self._get_entity_content(pair.entity1)
            content2 = self._get_entity_content(pair.entity2)
            similarity = self._text_similarity(content1, content2)

            if similarity >= self.JACCARD_THRESHOLD:
                filtered.append(pair)

        return filtered

    def judge_consolidation(self, entity1: Dict, entity2: Dict) -> ConsolidationDecision:
        """使用 LLM 判断两个实体是否应该合并

        Args:
            entity1: 实体1
            entity2: 实体2

        Returns:
            ConsolidationDecision 判断结果
        """
        # 检查缓存
        cache_key = self._make_llm_cache_key(entity1, entity2)
        cached = self.cache.get(cache_key[0], cache_key[1])
        if cached:
            self.stats['cache_hits'] += 1
            print("  [Cache hit] Using cached consolidation judgment")
            try:
                data = json.loads(cached)
                return ConsolidationDecision(
                    decision=data['decision'],
                    reasoning=f"[Cache] {data.get('reasoning', '')}",
                    summary=data.get('summary', ''),
                    confidence=data.get('confidence', 0.0)
                )
            except json.JSONDecodeError:
                pass

        # 构建 prompt
        props1 = entity1.get('properties', {})
        props2 = entity2.get('properties', {})

        prompt = CONSOLIDATION_PROMPT.format(
            type_a=entity1['type'],
            title_a=props1.get('title', ''),
            content_a=self._get_entity_content(entity1),
            tags_a=', '.join(props1.get('tags', [])[:5]),
            type_b=entity2['type'],
            title_b=props2.get('title', ''),
            content_b=self._get_entity_content(entity2),
            tags_b=', '.join(props2.get('tags', [])[:5])
        )

        messages = [
            {"role": "system", "content": "你是一个专业的知识合并判断助手，只输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.call(messages)
        if not response:
            logging.error(f"LLM call failed for entities {entity1['id']} and {entity2['id']}")
            return ConsolidationDecision(
                decision="keep_separate",
                reasoning="LLM call failed",
                summary="",
                confidence=0.0
            )

        # 解析响应
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                decision = ConsolidationDecision(
                    decision=data.get('decision', 'keep_separate'),
                    reasoning=data.get('reasoning', ''),
                    summary=data.get('summary', ''),
                    confidence=float(data.get('confidence', 0.0))
                )

                # 写入缓存
                self.cache.set(cache_key[0], cache_key[1], json.dumps(data))

                return decision
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logging.error(f"Failed to parse LLM response: {e}, response: {response}")
            return ConsolidationDecision(
                decision="keep_separate",
                reasoning=f"Parse error: {e}",
                summary="",
                confidence=0.0
            )

        return ConsolidationDecision(
            decision="keep_separate",
            reasoning="Unknown error",
            summary="",
            confidence=0.0
        )

    def consolidate(self, entity1: Dict, entity2: Dict, decision: ConsolidationDecision,
                    dry_run: bool = False) -> Optional[Dict]:
        """执行合并或创建冲突标记

        Args:
            entity1: 实体1
            entity2: 实体2
            decision: LLM 判断结果
            dry_run: 是否只执行dry-run（不实际写入）

        Returns:
            创建的实体（SkillCard 或 ConflictReview），dry_run 时返回描述信息
        """
        if decision.decision == "merge":
            if dry_run:
                return {
                    'type': 'SkillCard',
                    'action': 'merge',
                    'entity1_id': entity1['id'],
                    'entity2_id': entity2['id'],
                    'summary': decision.summary
                }

            # 创建 SkillCard
            now = datetime.now().astimezone().isoformat()
            skillcard_id = self._generate_id('SkillCard')

            props1 = entity1.get('properties', {})
            props2 = entity2.get('properties', {})

            # 合并标签
            tags1 = set(props1.get('tags', []))
            tags2 = set(props2.get('tags', []))
            merged_tags = list(tags1 | tags2)

            skillcard_props = {
                'title': decision.summary if decision.summary else f"Merged: {props1.get('title', entity1['id'])}",
                'summary': decision.summary,
                'source_episodes': [entity1['id'], entity2['id']],
                'consolidated_at': now,
                'conflict_notes': '',
                'entity_types_consolidated': [entity1['type'], entity2['type']],
                'confidence': decision.confidence,
                'tags': merged_tags + ['#skillcard', '#consolidated'],
                'strength': 1.0,
                'decay_rate': 0.99,  # SkillCard 几乎不衰减
                'last_accessed': now,
                'provenance': ['consolidation:engine'],
                'source_trust': 'high' if decision.confidence > 0.8 else 'medium'
            }

            # 创建 SkillCard
            skillcard = self._create_entity('SkillCard', skillcard_props, entity_id=skillcard_id)

            # 标记原始实体已被合并
            self._mark_consolidated(entity1['id'], skillcard_id)
            self._mark_consolidated(entity2['id'], skillcard_id)

            return skillcard

        elif decision.decision == "conflict":
            if dry_run:
                return {
                    'type': 'ConflictReview',
                    'action': 'conflict',
                    'entity1_id': entity1['id'],
                    'entity2_id': entity2['id'],
                    'description': decision.reasoning
                }

            # 创建 ConflictReview
            now = datetime.now().astimezone().isoformat()
            conflict_id = self._generate_id('ConflictReview')

            conflict_props = {
                'entity1_id': entity1['id'],
                'entity2_id': entity2['id'],
                'conflict_type': 'decision',  # 默认类型
                'description': decision.reasoning,
                'status': 'pending',
                'created_at': now
            }

            conflict = self._create_entity('ConflictReview', conflict_props, entity_id=conflict_id)

            return conflict

        else:  # keep_separate
            return None

    def run_consolidation_cycle(self, dry_run: bool = False, max_pairs: int = 100) -> Dict:
        """运行一个完整的合并周期

        Args:
            dry_run: 是否只执行 dry-run
            max_pairs: 最大评估的候选对数量

        Returns:
            统计信息字典
        """
        self._ensure_dir()

        print(f"\n{'='*60}")
        print(f"Consolidation Engine - {'DRY RUN' if dry_run else 'LIVE RUN'}")
        print(f"{'='*60}\n")

        # 重置统计
        self.stats = {
            'candidates_evaluated': 0,
            'merges': 0,
            'conflicts': 0,
            'kept_separate': 0,
            'errors': 0,
            'cache_hits': 0,
        }

        # 找到候选实体对
        print("🔍 Finding candidate pairs...")
        candidates = self.find_candidate_pairs(max_pairs=max_pairs)
        print(f"   Found {len(candidates)} candidate pairs\n")

        # 评估每个候选
        for i, pair in enumerate(candidates, 1):
            print(f"[{i}/{len(candidates)}] Evaluating: {pair.entity1['id']} <-> {pair.entity2['id']}")

            self.stats['candidates_evaluated'] += 1

            try:
                # LLM 判断
                decision = self.judge_consolidation(pair.entity1, pair.entity2)
                print(f"   Decision: {decision.decision} (confidence: {decision.confidence:.2f})")
                print(f"   Reason: {decision.reasoning[:80]}...")

                # 执行合并或冲突标记
                result = self.consolidate(pair.entity1, pair.entity2, decision, dry_run=dry_run)

                if result:
                    if result.get('action') == 'merge':
                        self.stats['merges'] += 1
                        if dry_run:
                            print(f"   [DRY RUN] Would create SkillCard: {result['summary'][:50]}...")
                        else:
                            print(f"   ✓ Created SkillCard")
                    elif result.get('action') == 'conflict':
                        self.stats['conflicts'] += 1
                        if dry_run:
                            print(f"   [DRY RUN] Would create ConflictReview")
                        else:
                            print(f"   ✓ Created ConflictReview (pending review)")
                else:
                    self.stats['kept_separate'] += 1
                    print(f"   → Keeping separate")

            except Exception as e:
                self.stats['errors'] += 1
                print(f"   ✗ Error: {e}")
                logging.error(f"Error consolidating pair {pair.entity1['id']}-{pair.entity2['id']}: {e}")

            print()

        # 打印统计
        print(f"\n{'='*60}")
        print(f"Consolidation Cycle Complete")
        print(f"{'='*60}")
        print(f"Candidates evaluated: {self.stats['candidates_evaluated']}")
        print(f"  - Merges: {self.stats['merges']}")
        print(f"  - Conflicts: {self.stats['conflicts']}")
        print(f"  - Kept separate: {self.stats['kept_separate']}")
        print(f"  - Errors: {self.stats['errors']}")
        print(f"Cache hits: {self.stats['cache_hits']}")

        return self.stats


# ========== Main ==========

def main():
    import argparse

    parser = argparse.ArgumentParser(description='ConsolidationEngine - Phase 3 Consolidation Engine')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # run 命令
    run_parser = subparsers.add_parser('run', help='运行合并周期')
    run_parser.add_argument('--dry-run', action='store_true', help='Dry run 模式')
    run_parser.add_argument('--max-pairs', type=int, default=100, help='最大评估候选对数量')

    # status 命令
    status_parser = subparsers.add_parser('status', help='显示状态')

    args = parser.parse_args()

    if args.command == 'run':
        engine = ConsolidationEngine()
        engine.run_consolidation_cycle(dry_run=args.dry_run, max_pairs=args.max_pairs)

    elif args.command == 'status':
        from memory_ontology import load_all_entities, query_entities

        entities = load_all_entities()

        # 统计各类型
        by_type = {}
        for entity in entities.values():
            t = entity['type']
            by_type[t] = by_type.get(t, 0) + 1

        # 统计已合并的实体
        consolidated_count = 0
        for entity in entities.values():
            if entity.get('properties', {}).get('consolidated_into'):
                consolidated_count += 1

        # 统计 SkillCard 和 ConflictReview
        skillcards = query_entities(entity_type='SkillCard')
        conflicts = query_entities(entity_type='ConflictReview')
        pending_conflicts = [c for c in conflicts if c.get('properties', {}).get('status') == 'pending']

        print(f"\n📊 Consolidation Status")
        print(f"{'='*60}")
        print(f"\nEntity counts:")
        for t, count in sorted(by_type.items()):
            print(f"  {t}: {count}")

        print(f"\nConsolidation stats:")
        print(f"  Entities consolidated: {consolidated_count}")
        print(f"  SkillCards: {len(skillcards)}")
        print(f"  ConflictReviews: {len(conflicts)} (pending: {len(pending_conflicts)})")

        print(f"\nConsolidation rate: {consolidated_count / max(1, len(entities)) * 100:.1f}%")

    else:
        parser.print_help()


if __name__ == '__main__':
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    main()
