#!/usr/bin/env python3
"""
Omni-Memory Ultimate - 终极记忆系统
整合所有Phase能力的完整系统

Phase 1: 语义检索革命 ✅
Phase 2: 记忆演化机制 ✅
Phase 3: 主动智能系统 ✅
Phase 4: 深度认知能力 ✅

架构：
┌─────────────────────────────────────────────────────────────────────────┐
│                    OMNI-MEMORY ULTIMATE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    CELLULAR LAYER                                │   │
│  │                    细胞式架构层                                   │   │
│  │                                                                  │   │
│  │   MemoryCell → NeuralNetwork → CellLifecycle                    │   │
│  │   (永恒性)      (突触网络)      (生命周期)                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    SEMANTIC LAYER                                │   │
│  │                    语义理解层                                     │   │
│  │                                                                  │   │
│  │   VectorEmbedding → ANNSearch → SemanticConnection               │   │
│  │   (向量化)          (O(log n))   (语义关联)                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    EVOLUTION LAYER                               │   │
│  │                    演化动态层                                     │   │
│  │                                                                  │   │
│  │   Enhance → Correct → Merge → Abstract → Reconstruct             │   │
│  │   (增强)     (修正)     (整合)    (抽象)      (重构)              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    PROACTIVE LAYER                               │   │
│  │                    主动智能层                                     │   │
│  │                                                                  │   │
│  │   IntentAnalysis → Prediction → WorkMemory → ProactivePush       │   │
│  │   (意图识别)        (预测)       (工作记忆)    (主动推送)          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    COGNITIVE LAYER                               │   │
│  │                    深度认知层                                     │   │
│  │                                                                  │   │
│  │   TemporalNetwork → EmotionalWeight → Compression → MetaCognition│   │
│  │   (时间感知)         (情感权重)      (压缩合并)    (元认知反思)     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
"""

import os
import sys
import json
import time
import uuid
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict

# 导入所有核心组件
from memory_cell import MemoryCell, CellState, CellGene, create_cell
from neural_network import MemoryNeuralNetwork, PulseType
from cell_lifecycle import CellLifecycleManager, DivisionTrigger
from semantic_memory import SemanticMemoryEngine, EmbeddingType
from memory_evolution import MemoryEvolutionEngine, EvolutionType, ConflictResolution
from proactive_memory import ProactiveMemorySystem, IntentType
from cognitive_memory import CognitiveMemorySystem


class OmniMemoryUltimate:
    """
    Omni-Memory Ultimate - 终极记忆系统
    
    世界级AI记忆系统，整合所有关键能力：
    
    架构层：
    1. Cellular Layer - 细胞式架构（永恒性、生命力）
    2. Semantic Layer - 语义理解（向量检索、O(log n)）
    3. Evolution Layer - 记忆演化（可更新、可重构）
    4. Proactive Layer - 主动智能（预测、推送）
    5. Cognitive Layer - 深度认知（时间、情感、元认知）
    
    核心能力矩阵：
    ┌────────────────────────────────────────────────────────────────┐
    │  能力维度           │  传统系统  │  Omni-Memory  │  提升幅度   │
    │  ─────────────────────────────────────────────────────────────│
    │  检索复杂度         │   O(n)    │   O(log n)   │  指数级     │
    │  语义理解           │   ❌      │   ✅         │  质变       │
    │  记忆动态性         │   静态    │   可演化     │  质变       │
    │  主动性             │   被动    │   预测推送   │  质变       │
    │  时间感知           │   ❌      │   ✅         │  新增       │
    │  情感维度           │   ❌      │   ✅         │  新增       │
    │  元认知             │   ❌      │   ✅         │  新增       │
    └────────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self, storage_path: str = "./omni_memory_ultimate",
                 enable_all_features: bool = True):
        """
        初始化终极记忆系统
        
        Args:
            storage_path: 存储路径
            enable_all_features: 是否启用所有功能
        """
        self.storage_path = storage_path
        self.enable_all_features = enable_all_features
        
        # 确保存储目录
        os.makedirs(storage_path, exist_ok=True)
        
        # === Layer 1: Cellular Layer ===
        print("[INIT] Initializing Cellular Layer...")
        self.network = MemoryNeuralNetwork(os.path.join(storage_path, "network"))
        self.lifecycle = CellLifecycleManager(self.network)
        
        # === Layer 2: Semantic Layer ===
        print("[INIT] Initializing Semantic Layer...")
        self.semantic = SemanticMemoryEngine(
            os.path.join(storage_path, "semantic"),
            EmbeddingType.SIMULATED
        )
        
        # === Layer 3: Evolution Layer ===
        print("[INIT] Initializing Evolution Layer...")
        self.evolution = MemoryEvolutionEngine(self.network, self.semantic)
        
        # === Layer 4: Proactive Layer ===
        print("[INIT] Initializing Proactive Layer...")
        self.proactive = ProactiveMemorySystem(self.network, self.semantic)
        
        # === Layer 5: Cognitive Layer ===
        print("[INIT] Initializing Cognitive Layer...")
        self.cognitive = CognitiveMemorySystem(self.network, self.semantic)
        
        # 系统状态
        self.initialized_at = datetime.now().isoformat()
        
        print(f"[INIT] Omni-Memory Ultimate initialized at {storage_path}")
    
    # ==================== 核心接口 ====================
    
    def remember(self, content: str, gene: str = "user",
                 importance: float = 0.7,
                 context: str = None) -> Dict:
        """
        记忆 - 创建新的记忆细胞（增强版）
        
        新增能力：
        - 语义向量索引（Phase 1）
        - 情感权重分析（Phase 4）
        - 主动推送准备（Phase 3）
        
        Args:
            content: 记忆内容
            gene: 细胞类型
            importance: 重要性
            context: 上下文
        
        Returns:
            创建结果
        """
        # 转换基因类型
        gene_map = {
            "user": CellGene.USER,
            "feedback": CellGene.FEEDBACK,
            "project": CellGene.PROJECT,
            "reference": CellGene.REFERENCE
        }
        cell_gene = gene_map.get(gene, CellGene.USER)
        
        # 创建细胞
        cell = self.lifecycle.birth(content, cell_gene, importance)
        
        # === Phase 1: 语义索引 ===
        self.semantic.index_cell(cell)
        
        # === Phase 4: 情感权重 ===
        emotion_weight = self.cognitive.emotional.detect_emotion(content)
        self.cognitive.emotional.apply_emotion_weight(cell)
        
        # === Phase 1: 语义自动连接 ===
        semantic_connections = self.semantic.auto_connect_by_semantic(
            cell, threshold=0.7
        )
        
        # 建立语义连接
        for other_id in semantic_connections:
            self.network.connect_cells(
                cell.id, other_id,
                synapse_type=self._determine_synapse_type(cell, self.network.get_cell(other_id)),
                strength=0.8
            )
        
        # === Phase 3: 更新工作记忆 ===
        if context:
            self.proactive.update_context(context)
        
        # 保存
        self.network._save_network()
        
        return {
            'success': True,
            'cell_id': cell.id,
            'state': cell.state.value,
            'energy': round(cell.energy, 3),
            'connections': len(cell.synapses),
            'semantic_connections': len(semantic_connections),
            'emotion': {
                'type': emotion_weight.emotion_type.value,
                'intensity': round(emotion_weight.intensity, 3),
                'confidence': round(emotion_weight.confidence, 3)
            }
        }
    
    def recall(self, query: str, top_k: int = 5,
               use_semantic: bool = True,
               use_temporal: bool = True,
               use_proactive: bool = True) -> List[Dict]:
        """
        回忆 - 智能检索记忆（增强版）
        
        新增能力：
        - 语义向量检索 O(log n)（Phase 1）
        - 时间感知增强（Phase 4）
        - 主动预测融合（Phase 3）
        - 记忆演化（Phase 2）
        
        Args:
            query: 查询内容
            top_k: 返回数量
            use_semantic: 是否使用语义检索
            use_temporal: 是否使用时间增强
            use_proactive: 是否使用主动预测
        
        Returns:
            记忆列表
        """
        results = []
        
        # === Phase 1: 语义检索 ===
        if use_semantic:
            semantic_results = self.semantic.search(query, top_k * 2)
            
            for result in semantic_results:
                cell_id = result['cell_id']
                cell = self.network.get_cell(cell_id)
                
                if cell:
                    # === Phase 2: 记忆演化 - 重构 ===
                    self.evolution.reconstruct_on_recall(cell, query)
                    
                    # === Phase 4: 情感权重 ===
                    energy = self.cognitive.emotional.apply_emotion_weight(cell)
                    
                    results.append({
                        'cell_id': cell.id,
                        'content': cell.content,
                        'gene': cell.gene.value,
                        'energy': round(energy, 3),
                        'state': cell.state.value,
                        'importance': cell.importance,
                        'semantic_similarity': round(result.get('similarity', 0), 3),
                        'connections': len(cell.synapses),
                        'age': cell.age
                    })
        
        # === Phase 4: 时间增强 ===
        if use_temporal:
            temporal_needs = self.cognitive.temporal.predict_temporal_needs()
            for cell_id in temporal_needs[:3]:
                if not any(r['cell_id'] == cell_id for r in results):
                    cell = self.network.get_cell(cell_id)
                    if cell and cell.state != CellState.HIBERNATE:
                        results.append({
                            'cell_id': cell.id,
                            'content': cell.content,
                            'gene': cell.gene.value,
                            'energy': cell.energy,
                            'state': cell.state.value,
                            'temporal_boost': True
                        })
        
        # === Phase 3: 主动预测 ===
        if use_proactive:
            predictions = self.proactive.predict_needed_memories(query)
            for cell_id, relevance in predictions[:3]:
                if not any(r['cell_id'] == cell_id for r in results):
                    cell = self.network.get_cell(cell_id)
                    if cell:
                        results.append({
                            'cell_id': cell.id,
                            'content': cell.content,
                            'gene': cell.gene.value,
                            'energy': cell.energy,
                            'proactive_prediction': round(relevance, 3)
                        })
        
        # 排序并截取
        results.sort(key=lambda x: x.get('semantic_similarity', 0) + x.get('energy', 0), reverse=True)
        
        return results[:top_k]
    
    def proactive_push(self, context: str) -> Dict:
        """
        主动推送 - 预测并推送相关记忆（Phase 3核心）
        
        Args:
            context: 当前上下文
        
        Returns:
            推送结果
        """
        # 分析意图
        intent = self.proactive.analyze_intent(context)
        
        # 预测并推送
        pushed = self.proactive.proactive_push(context)
        
        # 获取建议
        suggestions = self.proactive.suggest_next_actions(context)
        
        return {
            'intent': intent.value,
            'pushed_memories': pushed,
            'suggestions': suggestions,
            'work_memory_size': len(self.proactive.work_memory)
        }
    
    def evolve_memory(self, cell_id: str, new_info: Dict) -> Dict:
        """
        演化记忆 - 更新、修正或整合记忆（Phase 2核心）
        
        Args:
            cell_id: 细胞ID
            new_info: 新信息
        
        Returns:
            演化结果
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return {'success': False, 'error': 'Cell not found'}
        
        event = self.evolution.evolve(cell, new_info)
        
        if event:
            # 更新语义索引
            self.semantic.index_cell(cell)
            
            return {
                'success': True,
                'evolution_type': event.evolution_type.value,
                'before': event.before,
                'after': event.after
            }
        
        return {'success': False, 'error': 'Evolution not possible'}
    
    def cell_division(self, parent_id: str, child_content: str,
                      child_gene: str = "insight") -> Dict:
        """
        细胞分裂 - 生发新记忆
        
        Args:
            parent_id: 父细胞ID
            child_content: 子细胞内容
            child_gene: 子细胞类型
        
        Returns:
            分裂结果
        """
        gene_map = {
            "insight": CellGene.INSIGHT,
            "pattern": CellGene.PATTERN,
            "user": CellGene.USER,
            "project": CellGene.PROJECT
        }
        child_gene_type = gene_map.get(child_gene, CellGene.INSIGHT)
        
        result = self.lifecycle.divide(parent_id, child_content, child_gene_type)
        
        if result.success:
            # 索引新细胞
            child = self.network.get_cell(result.child_id)
            if child:
                self.semantic.index_cell(child)
        
        return {
            'success': result.success,
            'parent_id': result.parent_id,
            'child_id': result.child_id,
            'trigger': result.trigger.value if result.trigger else None,
            'energy_transferred': result.energy_transferred
        }
    
    def pulse_network(self, source_id: str, strength: float = 1.0) -> Dict:
        """
        脉冲传导 - 激活神经网络
        
        Args:
            source_id: 脉冲源
            strength: 脉冲强度
        
        Returns:
            激活结果
        """
        pulses = self.network.pulse(source_id, PulseType.ACTIVATION, strength)
        
        return {
            'success': True,
            'source_id': source_id,
            'activated_count': len(pulses),
            'pulse_path': [p.to_dict() for p in pulses[:5]]
        }
    
    def compress_memories(self) -> Dict:
        """
        压缩记忆 - 合并相似记忆（Phase 4）
        
        Returns:
            压缩统计
        """
        stats = self.cognitive.compress_memories()
        
        return {
            'success': True,
            **stats
        }
    
    def reflect(self) -> Dict:
        """
        元认知反思 - 系统自省（Phase 4）
        
        Returns:
            反思报告
        """
        return self.cognitive.reflect()
    
    def get_full_stats(self) -> Dict:
        """
        获取完整系统统计
        """
        return {
            # 细胞层统计
            'cellular': {
                'total_cells': len(self.network.cells),
                'active_cells': len(self.network.get_active_cells()),
                'dormant_cells': len(self.network.get_dormant_cells()),
                'hibernate_cells': len(self.network.get_hibernate_cells()),
                'avg_energy': sum(c.energy for c in self.network.cells.values()) / len(self.network.cells) if self.network.cells else 0,
                'total_synapses': sum(len(c.synapses) for c in self.network.cells.values())
            },
            
            # 语义层统计
            'semantic': self.semantic.get_memory_insights(),
            
            # 演化层统计
            'evolution': self.evolution.get_evolution_stats(),
            
            # 主动层统计
            'proactive': self.proactive.get_prediction_stats(),
            
            # 认知层统计
            'cognitive': {
                'temporal_chains': len(self.cognitive.temporal.build_temporal_chains()),
                'emotion_distribution': self.cognitive.emotional.get_emotion_distribution(),
                'health': self.cognitive.meta.assess_health()
            },
            
            # 系统信息
            'system': {
                'initialized_at': self.initialized_at,
                'storage_path': self.storage_path,
                'features_enabled': self.enable_all_features
            }
        }
    
    def visualize(self) -> str:
        """可视化系统状态"""
        stats = self.get_full_stats()
        
        lines = [
            "=" * 70,
            "              OMNI-MEMORY ULTIMATE - SYSTEM STATUS",
            "=" * 70,
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│                    CELLULAR LAYER                                │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│  Total Cells: {stats['cellular']['total_cells']:>5}    Active: {stats['cellular']['active_cells']:>4}    Dormant: {stats['cellular']['dormant_cells']:>4}    Hibernate: {stats['cellular']['hibernate_cells']:>4}  │",
            f"│  Avg Energy: {stats['cellular']['avg_energy']:.3f}    Total Synapses: {stats['cellular']['total_synapses']:>5}                        │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│                    SEMANTIC LAYER                                │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│  Total Vectors: {stats['semantic'].get('total_memories', stats['semantic'].get('total', 0)):>5}    Diversity: {stats['semantic'].get('semantic_diversity', 0):.3f}                      │",
            f"│  Avg Similarity: {stats['semantic'].get('avg_semantic_similarity', 0):.3f}    Clusters: {stats['semantic'].get('num_clusters', 0):>3}                        │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│                    EVOLUTION LAYER                               │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│  Total Evolutions: {stats['evolution']['total_evolutions']:>5}    Enhancements: {stats['evolution']['enhancements']:>4}    Corrections: {stats['evolution']['corrections']:>4}    │",
            f"│  Merges: {stats['evolution']['merges']:>4}    Reconstructions: {stats['evolution']['reconstructions']:>4}                              │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│                    PROACTIVE LAYER                               │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│  Total Predictions: {stats['proactive']['total_predictions']:>5}    Push Count: {stats['proactive']['push_count']:>4}                        │",
            f"│  Work Memory Size: {stats['proactive']['work_memory_size']:>3}    Success Rate: {stats['proactive']['success_rate']:.2%}                     │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│                    COGNITIVE LAYER                               │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│  Temporal Chains: {stats['cognitive']['temporal_chains']:>3}    Health Score: {stats['cognitive']['health']['health_score']:.1f}/100                   │",
            f"│  Status: {stats['cognitive']['health']['status']:<20}                                    │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
            "=" * 70,
            f"  Initialized: {stats['system']['initialized_at']}",
            "=" * 70
        ]
        
        return "\n".join(lines)
    
    def _determine_synapse_type(self, cell1: MemoryCell, cell2: MemoryCell):
        """确定突触类型"""
        from memory_cell import SynapseType
        
        if not cell1 or not cell2:
            return SynapseType.ASSOCIATIVE
        
        if cell1.gene == cell2.gene:
            return SynapseType.SEMANTIC
        
        return SynapseType.ASSOCIATIVE


def main():
    parser = argparse.ArgumentParser(
        description="Omni-Memory Ultimate - 终极记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建记忆（带语义索引）
  python ultimate_memory.py remember --content "用户喜欢Python编程" --type user
  
  # 语义检索
  python ultimate_memory.py recall --query "编程语言" --top-k 5
  
  # 主动推送
  python ultimate_memory.py push --context "我想学习新的编程技术"
  
  # 演化记忆
  python ultimate_memory.py evolve --id cell_xxx --info '{"content": "更新内容"}'
  
  # 细胞分裂
  python ultimate_memory.py divide --parent cell_xxx --content "洞察内容"
  
  # 系统状态
  python ultimate_memory.py stats
  
  # 可视化
  python ultimate_memory.py visualize
  
  # 元认知反思
  python ultimate_memory.py reflect
        """
    )
    
    parser.add_argument("--storage", default="./omni_memory_ultimate", help="存储路径")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # remember命令
    remember_parser = subparsers.add_parser("remember", help="创建记忆")
    remember_parser.add_argument("--content", required=True, help="记忆内容")
    remember_parser.add_argument("--type", default="user", help="细胞类型")
    remember_parser.add_argument("--importance", type=float, default=0.7, help="重要性")
    remember_parser.add_argument("--context", help="上下文")
    
    # recall命令
    recall_parser = subparsers.add_parser("recall", help="回忆记忆")
    recall_parser.add_argument("--query", required=True, help="查询内容")
    recall_parser.add_argument("--top-k", type=int, default=5, help="返回数量")
    
    # push命令
    push_parser = subparsers.add_parser("push", help="主动推送")
    push_parser.add_argument("--context", required=True, help="当前上下文")
    
    # evolve命令
    evolve_parser = subparsers.add_parser("evolve", help="演化记忆")
    evolve_parser.add_argument("--id", required=True, help="细胞ID")
    evolve_parser.add_argument("--info", required=True, help="新信息(JSON)")
    
    # divide命令
    divide_parser = subparsers.add_parser("divide", help="细胞分裂")
    divide_parser.add_argument("--parent", required=True, help="父细胞ID")
    divide_parser.add_argument("--content", required=True, help="子细胞内容")
    divide_parser.add_argument("--type", default="insight", help="子细胞类型")
    
    # pulse命令
    pulse_parser = subparsers.add_parser("pulse", help="脉冲传导")
    pulse_parser.add_argument("--source", required=True, help="脉冲源ID")
    pulse_parser.add_argument("--strength", type=float, default=1.0, help="脉冲强度")
    
    # compress命令
    subparsers.add_parser("compress", help="压缩记忆")
    
    # reflect命令
    subparsers.add_parser("reflect", help="元认知反思")
    
    # stats命令
    subparsers.add_parser("stats", help="系统统计")
    
    # visualize命令
    subparsers.add_parser("visualize", help="可视化系统")
    
    args = parser.parse_args()
    
    # 初始化系统
    system = OmniMemoryUltimate(args.storage)
    
    # 执行命令
    if args.command == "remember":
        result = system.remember(
            args.content,
            args.type,
            args.importance,
            args.context
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "recall":
        results = system.recall(args.query, args.top_k)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "push":
        result = system.proactive_push(args.context)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "evolve":
        new_info = json.loads(args.info)
        result = system.evolve_memory(args.id, new_info)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "divide":
        result = system.cell_division(args.parent, args.content, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "pulse":
        result = system.pulse_network(args.source, args.strength)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "compress":
        result = system.compress_memories()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "reflect":
        result = system.reflect()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        result = system.get_full_stats()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "visualize":
        print(system.visualize())


if __name__ == "__main__":
    main()
