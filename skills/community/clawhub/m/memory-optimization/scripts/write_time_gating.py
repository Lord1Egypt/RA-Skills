#!/usr/bin/env python3
"""
Write-Time Gating Engine (Phase 8: AEAM)

基于 Selective Memory 论文 (2603.15994) 的写入时门控机制。
在知识对象写入 KG 之前评估其显著性。

核心思想：
- 来源声誉 (source_reputation): 40% - 来源的历史准确率
- 新颖性 (novelty): 35% - 与现有KG实体的最大相似度越低越新颖
- 可靠性 (reliability): 25% - 内容置信度与来源可靠性的综合

门控决策：
- STORE: score >= threshold (默认 0.5)
- ARCHIVE: score >= auto_archive_below (默认 0.3)
- REJECT: score < auto_archive_below (默认 0.3)

Usage:
    python3 scripts/write_time_gating.py gate --entity-id dec_xxx --source-type kg_extractor
"""

import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# 路径配置
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import (
    ONTOLOGY_DIR,
    GRAPH_FILE,
    load_all_entities,
    load_schema,
    create_entity,
    get_entity,
    get_or_create_source,
    update_source_reliability,
    get_default_gating_policy,
    get_all_active_entities,
    archive_entity_to_cold_storage,
)
from utils.llm_client import LLMClient

# 嵌入缓存路径
EMBED_CACHE_FILE = ONTOLOGY_DIR / "gating_embed_cache.jsonl"

# 默认权重配置 (基于 Selective Memory 论文)
DEFAULT_WEIGHTS = {
    'source_reputation': 0.40,
    'novelty': 0.35,
    'reliability': 0.25
}


# ============== 数据结构 ==============

@dataclass
class SignificanceBreakdown:
    """显著性评分明细"""
    source_reputation: float  # 来源声誉 0-1
    novelty: float            # 新颖性 0-1
    reliability: float        # 可靠性 0-1


@dataclass
class SignificanceScore:
    """显著性评分结果"""
    entity_id: str
    total_score: float  # 0-1 综合评分
    breakdown: SignificanceBreakdown
    weights_used: Dict[str, float]
    model: str  # 使用的评分模型
    created_at: str


@dataclass
class GateResult:
    """门控决策结果"""
    status: str  # STORE | ARCHIVE | REJECT
    score: SignificanceScore
    reason: str = ""


# ============== 嵌入缓存 ==============

class EmbedCache:
    """文件-backed 嵌入缓存，24小时 TTL"""

    TTL_HOURS = 24

    def __init__(self, cache_file: Path = EMBED_CACHE_FILE):
        self.cache_file = cache_file
        self._cache: Dict[str, Tuple[str, str, List[float]]] = {}  # text_hash -> (text, created_iso, embedding)
        self._load()

    def _load(self):
        if not self.cache_file.exists():
            return
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        self._cache[entry['text_hash']] = (
                            entry['text'],
                            entry['created'],
                            entry['embedding']
                        )
                    except (json.JSONDecodeError, KeyError):
                        continue
        except Exception:
            pass

    def _save(self):
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            for text_hash, (text, created, embedding) in self._cache.items():
                f.write(json.dumps({
                    'text_hash': text_hash,
                    'text': text,
                    'created': created,
                    'embedding': embedding
                }, ensure_ascii=False) + '\n')

    def get(self, text: str) -> Optional[List[float]]:
        """获取缓存的嵌入向量，如果有效的话"""
        if not text:
            return None
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        if text_hash not in self._cache:
            return None
        text_stored, created_str, embedding = self._cache[text_hash]
        if text_stored != text:
            return None
        try:
            created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
            age_hours = (datetime.now().astimezone() - created).total_seconds() / 3600
            if age_hours > self.TTL_HOURS:
                del self._cache[text_hash]
                return None
        except (ValueError, TypeError):
            return None
        return embedding

    def set(self, text: str, embedding: List[float]):
        """缓存嵌入向量"""
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        self._cache[text_hash] = (
            text,
            datetime.now().astimezone().isoformat(),
            embedding
        )
        self._save()


# ============== 核心门控引擎 ==============

class WriteTimeGating:
    """写入时门控引擎"""

    def __init__(self, kg_path: Optional[str] = None, policy_id: str = 'gate_default'):
        """
        Args:
            kg_path: 知识图谱目录路径
            policy_id: 门控策略 ID
        """
        if kg_path:
            os.environ['KG_DIR'] = kg_path

        self.ontology = self  # 引用自身方法兼容
        self.llm = LLMClient()
        self.embed_cache = EmbedCache()
        self.policy = self._load_or_create_policy(policy_id)

    def _load_or_create_policy(self, policy_id: str) -> Dict:
        """加载或创建门控策略"""
        policy = get_default_gating_policy(policy_id)
        if policy:
            return policy['properties']
        # 返回默认值
        return {
            'threshold': 0.5,
            'auto_archive_below': 0.3,
            'weights': DEFAULT_WEIGHTS.copy(),
            'enabled': True
        }

    def gate(self, entity: Dict, source_type: str) -> GateResult:
        """
        主入口：评估实体，返回门控决策

        Args:
            entity: 待评估的实体 (包含 type 和 properties)
            source_type: 来源类型 (如 'kg_extractor', 'user_input')

        Returns:
            GateResult: 包含状态和评分
        """
        # 检查门控是否启用
        if not self.policy.get('enabled', True):
            return GateResult(
                status="STORE",
                score=SignificanceScore(
                    entity_id=entity.get('id', 'unknown'),
                    total_score=0.5,
                    breakdown=SignificanceBreakdown(0.5, 0.5, 0.5),
                    weights_used=DEFAULT_WEIGHTS,
                    model="disabled",
                    created_at=datetime.now().astimezone().isoformat()
                ),
                reason="Gating disabled"
            )

        # 计算评分
        score = self.score(entity, source_type)

        # 门控决策
        threshold = self.policy.get('threshold', 0.5)
        auto_archive_below = self.policy.get('auto_archive_below', 0.3)

        if score.total_score >= threshold:
            return GateResult(status="STORE", score=score, reason=f"Score {score.total_score:.3f} >= threshold {threshold}")
        elif score.total_score >= auto_archive_below:
            return GateResult(status="ARCHIVE", score=score, reason=f"Score {score.total_score:.3f} < {threshold}, >= {auto_archive_below}")
        else:
            return GateResult(status="REJECT", score=score, reason=f"Score {score.total_score:.3f} < {auto_archive_below}")

    def score(self, entity: Dict, source_type: str) -> SignificanceScore:
        """
        计算三元显著性评分

        Args:
            entity: 待评分的实体
            source_type: 来源类型

        Returns:
            SignificanceScore: 包含总评分和明细
        """
        # 获取三元评分
        source_rep = self._get_source_reputation(source_type)
        novelty = self._compute_novelty(entity)
        reliability = self._estimate_reliability(entity, source_type)

        # 计算加权总分
        weights = self.policy.get('weights', DEFAULT_WEIGHTS)
        total = (
            weights['source_reputation'] * source_rep +
            weights['novelty'] * novelty +
            weights['reliability'] * reliability
        )

        # 限制在 0-1
        total = max(0.0, min(1.0, total))

        return SignificanceScore(
            entity_id=entity.get('id', 'unknown'),
            total_score=total,
            breakdown=SignificanceBreakdown(source_rep, novelty, reliability),
            weights_used=weights,
            model=self.llm.model,
            created_at=datetime.now().astimezone().isoformat()
        )

    def _get_source_reputation(self, source_type: str) -> float:
        """
        获取来源声誉

        来源声誉 = 可靠性 * 0.8 + 0.2 (动态调整)
        高频准确来源获得更高声誉

        Args:
            source_type: 来源类型

        Returns:
            float: 来源声誉 0-1
        """
        source = get_or_create_source(source_type)
        if not source:
            return 0.5  # 默认值

        props = source['properties']
        reliability = props.get('reliability', 0.5)

        # 动态调整：高频准确的来源获得 boost
        # reliability * 0.8 + 0.2 确保新来源至少有 0.2
        return reliability * 0.8 + 0.2

    def _compute_novelty(self, entity: Dict) -> float:
        """
        计算新颖性

        新颖性 = 1 - max(与现有KG实体的余弦相似度)

        如果实体与现有实体高度相似，则新颖性低

        Args:
            entity: 待评分的实体

        Returns:
            float: 新颖性 0-1 (越高越新颖)
        """
        entity_text = self._extract_text(entity)
        if not entity_text:
            return 0.5  # 默认值

        entity_emb = self._get_embedding(entity_text)
        if entity_emb is None:
            return 0.5  # 嵌入失败，返回默认值

        # 获取所有活跃实体
        active_entities = get_all_active_entities()
        if not active_entities:
            return 1.0  # 空图谱，完全新颖

        max_similarity = 0.0
        for other in active_entities:
            # 跳过自身
            if other.get('id') == entity.get('id'):
                continue

            other_text = self._extract_text(other)
            if not other_text:
                continue

            other_emb = self._get_embedding(other_text)
            if other_emb is None:
                continue

            sim = self._cosine_similarity(entity_emb, other_emb)
            max_similarity = max(max_similarity, sim)

        # 新颖性 = 1 - 最大相似度
        return 1.0 - max_similarity

    def _estimate_reliability(self, entity: Dict, source_type: str) -> float:
        """
        估计可靠性

        可靠性 = (来源可靠性 + 实体置信度) / 2

        Args:
            entity: 待评分的实体
            source_type: 来源类型

        Returns:
            float: 可靠性 0-1
        """
        props = entity.get('properties', {})

        # 来源基础可靠性
        source = get_or_create_source(source_type)
        base_reliability = 0.5 if not source else source['properties'].get('reliability', 0.5)

        # 实体自身的置信度
        entity_confidence = props.get('confidence')

        if entity_confidence is None:
            return base_reliability

        # 处理不同格式的置信度
        if isinstance(entity_confidence, (int, float)):
            # 数字格式 0-1
            confidence_value = float(entity_confidence)
            return (base_reliability + confidence_value) / 2

        elif isinstance(entity_confidence, str):
            # 枚举字符串格式
            conf_map = {
                'verified': 1.0,
                'confirmed': 0.8,
                'likely': 0.6,
                'speculation': 0.4
            }
            confidence_value = conf_map.get(entity_confidence.lower(), 0.5)
            return (base_reliability + confidence_value) / 2

        return base_reliability

    def _extract_text(self, entity: Dict) -> str:
        """
        从实体提取用于嵌入的规范文本

        Args:
            entity: 实体 dict

        Returns:
            str: 连接的关键字段文本
        """
        props = entity.get('properties', {})
        parts = []

        # 优先级字段
        for field in ['title', 'rationale', 'content', 'lesson', 'description', 'summary']:
            if field in props and props[field]:
                parts.append(str(props[field]))

        # 标签
        tags = props.get('tags', [])
        if tags:
            if isinstance(tags, list):
                parts.append(' '.join(tags))
            else:
                parts.append(str(tags))

        return ' '.join(parts) if parts else ''

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """
        获取文本嵌入（带缓存）

        Args:
            text: 文本

        Returns:
            List[float] or None
        """
        if not text:
            return None

        # 缓存命中
        cached = self.embed_cache.get(text)
        if cached:
            return cached

        # API 调用
        emb = self.llm.embed(text)
        if emb:
            self.embed_cache.set(text, emb)

        return emb

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """
        计算余弦相似度

        Args:
            a, b: 嵌入向量

        Returns:
            float: 余弦相似度 -1 to 1
        """
        if not a or not b or len(a) != len(b):
            return 0.0

        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def update_policy(self, updates: Dict) -> bool:
        """
        更新门控策略

        Args:
            updates: 要更新的字段

        Returns:
            bool: 是否成功
        """
        from memory_ontology import _write_to_graph

        current = self.policy.copy()
        current.update(updates)
        current['updated_at'] = datetime.now().astimezone().isoformat()

        # 查找现有策略
        entities = load_all_entities()
        policy_id = current.get('id', 'gate_default')

        for entity in entities.values():
            if entity['type'] == 'GatingPolicy' and entity['id'] == policy_id:
                # 更新
                now = datetime.now().astimezone().isoformat()
                update_op = {
                    "op": "update",
                    "entity": {
                        "id": entity['id'],
                        "properties": current,
                        "updated": now
                    },
                    "timestamp": now
                }
                _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')
                self.policy = current
                return True

        # 创建新策略
        self.policy = current
        return True


# ============== CLI 接口 ==============

def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Write-Time Gating Engine')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # gate 命令：评估单个实体
    gate_parser = subparsers.add_parser('gate', help='评估实体的显著性评分')
    gate_parser.add_argument('--entity-id', required=True, help='实体 ID')
    gate_parser.add_argument('--source-type', default='kg_extractor',
                            help='来源类型 (默认: kg_extractor)')
    gate_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # score 命令：仅计算评分，不做决策
    score_parser = subparsers.add_parser('score', help='计算显著性评分')
    score_parser.add_argument('--entity-id', required=True, help='实体 ID')
    score_parser.add_argument('--source-type', default='user_input',
                            help='来源类型 (默认: user_input)')
    score_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    # policy 命令：查看/更新策略
    policy_parser = subparsers.add_parser('policy', help='管理门控策略')
    policy_parser.add_argument('--show', action='store_true', help='显示当前策略')
    policy_parser.add_argument('--threshold', type=float, help='设置阈值')
    policy_parser.add_argument('--auto-archive', type=float, help='设置自动归档阈值')
    policy_parser.add_argument('--enable', action='store_true', help='启用门控')
    policy_parser.add_argument('--disable', action='store_true', help='禁用门控')

    args = parser.parse_args()

    gating = WriteTimeGating()

    if args.command == 'gate':
        entity = get_entity(args.entity_id, refresh_strength=False)
        if not entity:
            print(f"✗ Entity not found: {args.entity_id}")
            sys.exit(1)

        result = gating.gate(entity, args.source_type)

        print(f"\n{'='*50}")
        print(f"Gate Result: {result.status}")
        print(f"Reason: {result.reason}")
        print(f"{'='*50}")

        if args.verbose:
            print(f"\nTotal Score: {result.score.total_score:.3f}")
            print(f"Model: {result.score.model}")
            print(f"Breakdown:")
            print(f"  Source Reputation: {result.score.breakdown.source_reputation:.3f} (weight: {result.score.weights_used['source_reputation']})")
            print(f"  Novelty:          {result.score.breakdown.novelty:.3f} (weight: {result.score.weights_used['novelty']})")
            print(f"  Reliability:      {result.score.breakdown.reliability:.3f} (weight: {result.score.weights_used['reliability']})")

    elif args.command == 'score':
        entity = get_entity(args.entity_id, refresh_strength=False)
        if not entity:
            print(f"✗ Entity not found: {args.entity_id}")
            sys.exit(1)

        score = gating.score(entity, args.source_type)

        print(f"\n{'='*50}")
        print(f"Significance Score: {score.total_score:.3f}")
        print(f"{'='*50}")

        if args.verbose:
            print(f"\nEntity ID: {score.entity_id}")
            print(f"Model: {score.model}")
            print(f"Created: {score.created_at}")
            print(f"\nBreakdown:")
            print(f"  Source Reputation: {score.breakdown.source_reputation:.3f}")
            print(f"  Novelty:          {score.breakdown.novelty:.3f}")
            print(f"  Reliability:      {score.breakdown.reliability:.3f}")
            print(f"\nWeights Used:")
            for k, v in score.weights_used.items():
                print(f"  {k}: {v}")

    elif args.command == 'policy':
        if args.show:
            print(f"\n{'='*50}")
            print(f"Gating Policy")
            print(f"{'='*50}")
            print(f"Threshold: {gating.policy.get('threshold', 0.5)}")
            print(f"Auto-Archive Below: {gating.policy.get('auto_archive_below', 0.3)}")
            print(f"Enabled: {gating.policy.get('enabled', True)}")
            print(f"\nWeights:")
            weights = gating.policy.get('weights', DEFAULT_WEIGHTS)
            for k, v in weights.items():
                print(f"  {k}: {v}")

        updates = {}
        if args.threshold is not None:
            updates['threshold'] = args.threshold
        if args.auto_archive is not None:
            updates['auto_archive_below'] = args.auto_archive
        if args.enable:
            updates['enabled'] = True
        if args.disable:
            updates['enabled'] = False

        if updates:
            gating.update_policy(updates)
            print(f"✓ Policy updated")
        else:
            policy_parser.print_help()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
