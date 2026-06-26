#!/usr/bin/env python3
"""
Cognitive Memory - 深度认知能力
时间感知网络、情感权重系统、记忆压缩合并、元认知反思
"""

import os
import sys
import json
import time
import math
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

from memory_cell import MemoryCell, CellState, CellGene, Synapse, SynapseType
from neural_network import MemoryNeuralNetwork
from semantic_memory import SemanticMemoryEngine


class EmotionType(Enum):
    """情感类型"""
    JOY = "joy"             # 喜悦
    TRUST = "trust"         # 信任
    FEAR = "fear"           # 恐惧
    SURPRISE = "surprise"   # 惊讶
    SADNESS = "sadness"     # 悲伤
    DISGUST = "disgust"     # 厌恶
    ANGER = "anger"         # 愤怒
    ANTICIPATION = "anticipation"  # 期待
    NEUTRAL = "neutral"     # 中性


class TemporalRelation(Enum):
    """时间关系"""
    BEFORE = "before"       # 在...之前
    AFTER = "after"         # 在...之后
    DURING = "during"       # 在...期间
    SIMULTANEOUS = "simultaneous"  # 同时
    SEQUENTIAL = "sequential"  # 顺序


@dataclass
class TemporalLink:
    """时间链接"""
    source_id: str
    target_id: str
    relation: TemporalRelation
    time_delta: float  # 秒
    strength: float = 1.0


@dataclass
class EmotionWeight:
    """情感权重"""
    emotion_type: EmotionType
    intensity: float  # 0-1
    confidence: float  # 0-1


class TemporalMemoryNetwork:
    """
    时间感知记忆网络
    
    核心能力：
    1. 时间链构建：自动发现时间顺序的记忆链
    2. 时间衰减：基于艾宾浩斯曲线的精确衰减
    3. 时间预测：预测未来的记忆需求
    4. 周期性发现：发现周期性出现的记忆模式
    """
    
    # 艾宾浩斯遗忘曲线参数
    EBBINGHAUS_S = 1.0  # 记忆强度因子
    EBBINGHAUS_C = 0.1  # 衰减速率
    
    def __init__(self, network: MemoryNeuralNetwork = None):
        self.network = network
        self.temporal_links: List[TemporalLink] = []
        self.time_index: Dict[str, datetime] = {}  # cell_id -> 创建时间
    
    def build_temporal_chains(self) -> Dict[str, List[str]]:
        """
        构建时间链
        
        Returns:
            {chain_id: [cell_ids in temporal order]}
        """
        if not self.network:
            return {}
        
        # 按时间排序细胞
        cells_with_time = []
        for cell_id, cell in self.network.cells.items():
            try:
                created = datetime.fromisoformat(cell.created_at)
                cells_with_time.append((cell_id, created))
            except:
                pass
        
        cells_with_time.sort(key=lambda x: x[1])
        
        # 构建链
        chains = {}
        current_chain = []
        chain_id = 0
        
        for i, (cell_id, created) in enumerate(cells_with_time):
            if not current_chain:
                current_chain = [cell_id]
            else:
                # 检查时间间隔
                prev_time = cells_with_time[i-1][1]
                delta = (created - prev_time).total_seconds()
                
                # 如果间隔小于1小时，认为是同一条链
                if delta < 3600:
                    current_chain.append(cell_id)
                    # 创建时间链接
                    self.temporal_links.append(TemporalLink(
                        source_id=current_chain[-2],
                        target_id=cell_id,
                        relation=TemporalRelation.SEQUENTIAL,
                        time_delta=delta
                    ))
                else:
                    # 开始新链
                    if len(current_chain) > 1:
                        chains[f"chain_{chain_id}"] = current_chain
                        chain_id += 1
                    current_chain = [cell_id]
        
        # 保存最后一条链
        if len(current_chain) > 1:
            chains[f"chain_{chain_id}"] = current_chain
        
        return chains
    
    def ebbinghaus_retention(self, time_passed: float, strength: float = 1.0) -> float:
        """
        艾宾浩斯遗忘曲线
        
        R = e^(-t/S) where S = strength
        
        Args:
            time_passed: 经过的时间（天）
            strength: 记忆强度
        
        Returns:
            保持率 (0-1)
        """
        return math.exp(-time_passed / (strength * self.EBBINGHAUS_S))
    
    def calculate_decay(self, cell: MemoryCell, days_passed: float) -> float:
        """
        计算衰减
        
        结合艾宾浩斯曲线和记忆属性计算衰减
        """
        # 基础衰减
        base_retention = self.ebbinghaus_retention(
            days_passed,
            strength=cell.importance * 10  # 放大强度
        )
        
        # 访问强化
        access_boost = min(0.5, cell.access_count * 0.05)
        
        # 综合保持率
        retention = min(1.0, base_retention + access_boost)
        
        return retention
    
    def discover_patterns(self, min_occurrences: int = 3) -> List[Dict]:
        """
        发现周期性模式
        
        检测是否有记忆在固定周期重复出现
        """
        if not self.network:
            return []
        
        patterns = []
        
        # 按基因类型分组
        by_gene = defaultdict(list)
        for cell_id, cell in self.network.cells.items():
            by_gene[cell.gene.value].append((cell_id, cell.created_at))
        
        # 检测每种类型的周期性
        for gene, cells in by_gene.items():
            if len(cells) < min_occurrences:
                continue
            
            # 计算时间间隔
            times = sorted([c[1] for c in cells])
            intervals = []
            
            for i in range(1, len(times)):
                try:
                    t1 = datetime.fromisoformat(times[i-1])
                    t2 = datetime.fromisoformat(times[i])
                    interval = (t2 - t1).total_seconds()
                    intervals.append(interval)
                except:
                    pass
            
            if intervals:
                avg_interval = sum(intervals) / len(intervals)
                
                # 如果间隔相对稳定（方差小），认为有周期性
                if len(intervals) >= 3:
                    variance = sum((i - avg_interval)**2 for i in intervals) / len(intervals)
                    std_dev = math.sqrt(variance)
                    
                    # 变异系数
                    cv = std_dev / avg_interval if avg_interval > 0 else 1
                    
                    if cv < 0.3:  # 变异系数小于30%认为稳定
                        patterns.append({
                            'type': gene,
                            'avg_interval_days': avg_interval / 86400,
                            'occurrences': len(cells),
                            'stability': round(1 - cv, 2)
                        })
        
        return patterns
    
    def predict_temporal_needs(self, context_time: datetime = None) -> List[str]:
        """
        基于时间预测需要的记忆
        
        例如：每天早上需要的记忆 vs 晚上需要的记忆
        """
        if context_time is None:
            context_time = datetime.now()
        
        hour = context_time.hour
        
        # 简单的时段分析
        predicted_ids = []
        
        if self.network:
            for cell_id, cell in self.network.cells.items():
                try:
                    created = datetime.fromisoformat(cell.created_at)
                    
                    # 如果该记忆在相同时段创建，可能相关
                    if abs(created.hour - hour) <= 2:
                        predicted_ids.append(cell_id)
                except:
                    pass
        
        return predicted_ids


class EmotionalMemorySystem:
    """
    情感权重记忆系统
    
    核心理念：
    - 情感强度决定记忆强度
    - 高情感记忆更容易被记住
    - 情感可以用来分类和检索记忆
    
    基于心理学研究：
    - 情感事件记忆更深刻（闪光灯记忆）
    - 负面情感记忆更持久（生存机制）
    - 情感可以触发联想回忆
    """
    
    # 情感关键词映射
    EMOTION_KEYWORDS = {
        EmotionType.JOY: ['开心', '高兴', '快乐', '成功', '完成', 'happy', 'joy', 'success', 'great'],
        EmotionType.TRUST: ['信任', '可靠', '确定', '确认', 'trust', 'reliable', 'sure'],
        EmotionType.FEAR: ['担心', '害怕', '风险', '问题', '错误', 'fear', 'worry', 'risk', 'error'],
        EmotionType.SURPRISE: ['意外', '惊喜', '突然', '发现', 'surprise', 'unexpected'],
        EmotionType.SADNESS: ['遗憾', '失败', '失望', 'sad', 'fail', 'disappointed'],
        EmotionType.DISGUST: ['讨厌', '糟糕', 'disgust', 'hate', 'bad'],
        EmotionType.ANGER: ['愤怒', '生气', '不满', 'angry', 'frustrated'],
        EmotionType.ANTICIPATION: ['期待', '希望', '计划', '未来', 'expect', 'plan', 'future'],
    }
    
    # 情感对记忆强度的影响系数
    EMOTION_INTENSITY_MULTIPLIER = {
        EmotionType.JOY: 1.2,
        EmotionType.TRUST: 1.1,
        EmotionType.FEAR: 1.5,  # 负面情感影响更大
        EmotionType.SURPRISE: 1.3,
        EmotionType.SADNESS: 1.4,
        EmotionType.DISGUST: 1.2,
        EmotionType.ANGER: 1.4,
        EmotionType.ANTICIPATION: 1.1,
        EmotionType.NEUTRAL: 1.0,
    }
    
    def __init__(self):
        self.emotion_weights: Dict[str, EmotionWeight] = {}
    
    def detect_emotion(self, content: str) -> EmotionWeight:
        """
        检测文本中的情感
        
        Args:
            content: 文本内容
        
        Returns:
            情感权重
        """
        content_lower = content.lower()
        
        scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            scores[emotion] = score
        
        # 找最高分
        max_score = max(scores.values()) if scores else 0
        if max_score > 0:
            best_emotion = max(scores, key=scores.get)
            intensity = min(1.0, max_score * 0.3)
            confidence = min(1.0, max_score * 0.2)
        else:
            best_emotion = EmotionType.NEUTRAL
            intensity = 0.0
            confidence = 0.0
        
        return EmotionWeight(
            emotion_type=best_emotion,
            intensity=intensity,
            confidence=confidence
        )
    
    def apply_emotion_weight(self, cell: MemoryCell) -> float:
        """
        应用情感权重到记忆
        
        Returns:
            修正后的能量
        """
        if cell.id not in self.emotion_weights:
            self.emotion_weights[cell.id] = self.detect_emotion(cell.content)
        
        ew = self.emotion_weights[cell.id]
        multiplier = self.EMOTION_INTENSITY_MULTIPLIER[ew.emotion_type]
        
        # 情感强度修正
        emotion_boost = ew.intensity * (multiplier - 1.0)
        
        return min(1.0, cell.energy + emotion_boost)
    
    def get_emotion_distribution(self) -> Dict[str, int]:
        """获取情感分布"""
        distribution = defaultdict(int)
        for ew in self.emotion_weights.values():
            distribution[ew.emotion_type.value] += 1
        return dict(distribution)
    
    def find_emotional_memories(self, emotion: EmotionType) -> List[str]:
        """查找特定情感的记忆"""
        return [
            cell_id for cell_id, ew in self.emotion_weights.items()
            if ew.emotion_type == emotion
        ]


class MemoryCompression:
    """
    记忆压缩系统
    
    核心能力：
    1. 相似记忆合并：将高度相似的记忆合并
    2. 抽象化：从具体记忆中提炼抽象概念
    3. 总结：生成记忆的摘要
    4. 去重：识别并处理重复记忆
    """
    
    # 压缩参数
    SIMILARITY_THRESHOLD = 0.85
    MIN_CLUSTER_SIZE = 3
    
    def __init__(self, network: MemoryNeuralNetwork = None,
                 semantic_engine: SemanticMemoryEngine = None):
        self.network = network
        self.semantic_engine = semantic_engine
    
    def find_similar_clusters(self) -> List[List[str]]:
        """
        发现相似记忆簇
        
        Returns:
            [[cell_ids], ...] 每个列表是一个相似记忆簇
        """
        if not self.network or not self.semantic_engine:
            return []
        
        cells = list(self.network.cells.values())
        clusters = []
        processed = set()
        
        for cell in cells:
            if cell.id in processed:
                continue
            
            similar = self.semantic_engine.find_similar_cells(cell.id, top_k=10)
            cluster = [cell.id]
            processed.add(cell.id)
            
            for other_id, similarity in similar:
                if similarity >= self.SIMILARITY_THRESHOLD:
                    cluster.append(other_id)
                    processed.add(other_id)
            
            if len(cluster) >= 2:
                clusters.append(cluster)
        
        return clusters
    
    def compress_cluster(self, cluster: List[str]) -> Optional[MemoryCell]:
        """
        压缩一个记忆簇
        
        生成一个抽象记忆代表整个簇
        
        Args:
            cluster: 细胞ID列表
        
        Returns:
            压缩后的抽象记忆
        """
        if not self.network or len(cluster) < 2:
            return None
        
        # 收集簇中所有记忆的内容
        contents = []
        total_importance = 0
        total_energy = 0
        
        for cell_id in cluster:
            cell = self.network.get_cell(cell_id)
            if cell:
                contents.append(cell.content)
                total_importance += cell.importance
                total_energy += cell.energy
        
        # 生成抽象内容（简化：取最长内容）
        abstract_content = max(contents, key=len) if contents else ""
        
        # 添加抽象标记
        abstract_content = f"[抽象] {abstract_content}"
        
        # 创建抽象细胞
        abstract_cell = MemoryCell(
            id=f"abstract_{uuid.uuid4().hex[:8]}",
            gene=CellGene.PATTERN,
            content=abstract_content,
            importance=total_importance / len(cluster),
            energy=total_energy / len(cluster)
        )
        
        # 标记原细胞为已压缩
        for cell_id in cluster:
            cell = self.network.get_cell(cell_id)
            if cell:
                cell.state = CellState.HIBERNATE
                cell.energy = 0.01
        
        return abstract_cell
    
    def auto_compress(self, threshold: int = 10) -> Dict:
        """
        自动压缩
        
        当记忆数量超过阈值时自动压缩
        
        Returns:
            压缩统计
        """
        clusters = self.find_similar_clusters()
        
        stats = {
            'clusters_found': len(clusters),
            'cells_compressed': 0,
            'abstract_cells_created': 0
        }
        
        for cluster in clusters:
            if len(cluster) >= self.MIN_CLUSTER_SIZE:
                abstract = self.compress_cluster(cluster)
                if abstract:
                    stats['cells_compressed'] += len(cluster)
                    stats['abstract_cells_created'] += 1
        
        return stats


class MetaCognition:
    """
    元认知系统
    
    记忆系统对自己的认知和反思能力
    
    核心能力：
    1. 自我评估：评估记忆系统的健康状态
    2. 盲区识别：发现缺失的记忆类型
    3. 质量监控：检测低质量记忆
    4. 改进建议：提出系统改进建议
    """
    
    def __init__(self, network: MemoryNeuralNetwork = None):
        self.network = network
    
    def assess_health(self) -> Dict:
        """
        评估记忆系统健康状态
        
        Returns:
            健康评估报告
        """
        if not self.network:
            return {'status': 'no_network'}
        
        cells = list(self.network.cells.values())
        
        # 计算各项指标
        total = len(cells)
        active = sum(1 for c in cells if c.state == CellState.ACTIVE)
        dormant = sum(1 for c in cells if c.state == CellState.DORMANT)
        hibernate = sum(1 for c in cells if c.state == CellState.HIBERNATE)
        
        avg_energy = sum(c.energy for c in cells) / total if total > 0 else 0
        avg_importance = sum(c.importance for c in cells) / total if total > 0 else 0
        
        # 计算连接密度
        total_connections = sum(len(c.synapses) for c in cells)
        connection_density = total_connections / total if total > 0 else 0
        
        # 计算多样性
        gene_distribution = defaultdict(int)
        for c in cells:
            gene_distribution[c.gene.value] += 1
        diversity = len(gene_distribution)
        
        # 健康分数
        health_score = 0
        if total > 0:
            # 活跃度分数
            health_score += (active / total) * 30
            # 连接密度分数
            health_score += min(30, connection_density * 10)
            # 多样性分数
            health_score += min(20, diversity * 5)
            # 平均能量分数
            health_score += avg_energy * 20
        
        return {
            'total_cells': total,
            'active_ratio': round(active / total, 2) if total > 0 else 0,
            'avg_energy': round(avg_energy, 3),
            'avg_importance': round(avg_importance, 3),
            'connection_density': round(connection_density, 2),
            'diversity': diversity,
            'health_score': round(health_score, 1),
            'status': 'healthy' if health_score >= 50 else 'needs_attention'
        }
    
    def identify_blind_spots(self) -> List[str]:
        """
        识别记忆盲区
        
        返回缺失或不足的记忆类型
        """
        if not self.network:
            return []
        
        blind_spots = []
        
        # 检查各类型记忆的覆盖
        gene_coverage = defaultdict(int)
        for cell in self.network.cells.values():
            if cell.state != CellState.HIBERNATE:
                gene_coverage[cell.gene.value] += 1
        
        # 检查是否缺失重要类型
        important_genes = ['user', 'feedback', 'project']
        for gene in important_genes:
            if gene not in gene_coverage or gene_coverage[gene] < 3:
                blind_spots.append(f"缺少足够的 {gene} 类型记忆")
        
        # 检查连接密度
        low_connection_cells = [
            c for c in self.network.cells.values()
            if len(c.synapses) < 2 and c.state == CellState.ACTIVE
        ]
        if len(low_connection_cells) > len(self.network.cells) * 0.5:
            blind_spots.append("记忆关联不足，建议增加连接")
        
        return blind_spots
    
    def detect_low_quality(self) -> List[str]:
        """
        检测低质量记忆
        
        Returns:
            低质量记忆ID列表
        """
        if not self.network:
            return []
        
        low_quality = []
        
        for cell in self.network.cells.values():
            issues = []
            
            # 内容过短
            if len(cell.content) < 10:
                issues.append('content_too_short')
            
            # 能量过低但活跃
            if cell.energy < 0.2 and cell.state == CellState.ACTIVE:
                issues.append('low_energy_active')
            
            # 无关键词
            if not cell.keywords:
                issues.append('no_keywords')
            
            # 无连接
            if not cell.synapses and cell.state == CellState.ACTIVE:
                issues.append('isolated')
            
            if len(issues) >= 2:
                low_quality.append(cell.id)
        
        return low_quality
    
    def suggest_improvements(self) -> List[str]:
        """
        提出改进建议
        """
        suggestions = []
        
        # 健康评估
        health = self.assess_health()
        if health['health_score'] < 50:
            suggestions.append("系统健康分数较低，建议增加高质量记忆")
        
        # 盲区检查
        blind_spots = self.identify_blind_spots()
        suggestions.extend(blind_spots)
        
        # 低质量检查
        low_quality = self.detect_low_quality()
        if len(low_quality) > 0:
            suggestions.append(f"发现 {len(low_quality)} 个低质量记忆，建议清理或补充")
        
        # 连接建议
        if health['connection_density'] < 2:
            suggestions.append("记忆关联密度低，建议增加细胞间的连接")
        
        return suggestions
    
    def generate_report(self) -> Dict:
        """生成完整的元认知报告"""
        return {
            'health_assessment': self.assess_health(),
            'blind_spots': self.identify_blind_spots(),
            'low_quality_count': len(self.detect_low_quality()),
            'improvement_suggestions': self.suggest_improvements(),
            'generated_at': datetime.now().isoformat()
        }


class CognitiveMemorySystem:
    """
    认知记忆系统 - 整合所有深度认知能力
    
    整合：
    - 时间感知网络
    - 情感权重系统
    - 记忆压缩
    - 元认知反思
    """
    
    def __init__(self, network: MemoryNeuralNetwork = None,
                 semantic_engine: SemanticMemoryEngine = None):
        self.temporal = TemporalMemoryNetwork(network)
        self.emotional = EmotionalMemorySystem()
        self.compression = MemoryCompression(network, semantic_engine)
        self.meta = MetaCognition(network)
        
        self.network = network
        self.semantic_engine = semantic_engine
    
    def process_with_emotion(self, cell: MemoryCell) -> MemoryCell:
        """应用情感权重处理记忆"""
        self.emotional.apply_emotion_weight(cell)
        return cell
    
    def build_temporal_context(self) -> Dict:
        """构建时间上下文"""
        return {
            'chains': self.temporal.build_temporal_chains(),
            'patterns': self.temporal.discover_patterns(),
            'predicted_needs': self.temporal.predict_temporal_needs()
        }
    
    def compress_memories(self) -> Dict:
        """执行记忆压缩"""
        return self.compression.auto_compress()
    
    def reflect(self) -> Dict:
        """元认知反思"""
        return self.meta.generate_report()
    
    def get_full_status(self) -> Dict:
        """获取完整认知状态"""
        return {
            'temporal': {
                'chains_count': len(self.temporal.build_temporal_chains()),
                'patterns': self.temporal.discover_patterns()
            },
            'emotional': {
                'distribution': self.emotional.get_emotion_distribution()
            },
            'meta': self.meta.assess_health(),
            'suggestions': self.meta.suggest_improvements()
        }


def main():
    parser = argparse.ArgumentParser(description="Cognitive Memory System - 认知记忆系统")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # temporal命令
    subparsers.add_parser("temporal", help="构建时间链")
    
    # emotion命令
    emotion_parser = subparsers.add_parser("emotion", help="检测情感")
    emotion_parser.add_argument("--text", required=True, help="文本内容")
    
    # compress命令
    subparsers.add_parser("compress", help="压缩记忆")
    
    # reflect命令
    subparsers.add_parser("reflect", help="元认知反思")
    
    # status命令
    subparsers.add_parser("status", help="完整状态")
    
    args = parser.parse_args()
    
    system = CognitiveMemorySystem()
    
    if args.command == "temporal":
        chains = system.temporal.build_temporal_chains()
        print(f"[TEMPORAL] Found {len(chains)} temporal chains")
        for chain_id, cells in chains.items():
            print(f"  {chain_id}: {len(cells)} cells")
    
    elif args.command == "emotion":
        ew = system.emotional.detect_emotion(args.text)
        print(f"[EMOTION] Detected: {ew.emotion_type.value}")
        print(f"  Intensity: {ew.intensity:.2f}")
        print(f"  Confidence: {ew.confidence:.2f}")
    
    elif args.command == "compress":
        stats = system.compress_memories()
        print(f"[COMPRESS] {stats}")
    
    elif args.command == "reflect":
        report = system.reflect()
        print(json.dumps(report, ensure_ascii=False, indent=2))
    
    elif args.command == "status":
        status = system.get_full_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
