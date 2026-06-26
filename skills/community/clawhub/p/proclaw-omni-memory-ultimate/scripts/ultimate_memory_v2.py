#!/usr/bin/env python3
"""
Omni-Memory Ultimate V2
世界级AI记忆系统 - Phase 5-8 全面升级版

整合:
- Phase 5: HNSW索引 + 真正的向量嵌入
- Phase 6: 休眠系统 + 梦境整理 + 记忆创造性
- Phase 7: 备份恢复 + 一致性校验
- Phase 8: 多模态 + 记忆联邦

架构:
Cellular → Semantic → Evolution → Proactive → Cognitive → Advanced
"""

import json
import os
import sys
import argparse
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading

# 导入Phase 5-8模块
from hnsw_index import HNSWIndex
from vector_embedding import VectorEmbeddingEngine, EmbeddingConfig
from dormancy_system import DormancySystem, CellState as DormCellState, WakeTrigger
from memory_dream import MemoryDream, DreamConfig
from memory_creativity import MemoryCreativity, CreativityType
from memory_backup import MemoryBackup
from memory_consistency import MemoryConsistency
from multimodal_memory import MultimodalMemorySystem, ModalityType
from memory_federation import MemoryFederation, SharingLevel

# 导入原有模块
from memory_cell import MemoryCell, CellState as MemCellState, CellGene
from neural_network import MemoryNeuralNetwork
from cell_lifecycle import CellLifecycleManager


class OmniMemoryUltimateV2:
    """
    Omni-Memory Ultimate V2
    
    世界级AI记忆系统 - 八层架构完整实现
    """
    
    def __init__(self, memory_path: str = "./omni_memory_ultimate_v2"):
        self.memory_path = memory_path
        os.makedirs(memory_path, exist_ok=True)
        
        # ===== Phase 1-4: 基础系统 =====
        # Cellular Layer
        self.cells: Dict[str, MemoryCell] = {}
        self.network = MemoryNeuralNetwork(storage_path=os.path.join(memory_path, "network"))
        self.lifecycle = CellLifecycleManager(self.network)
        
        # ===== Phase 5: 算法正确化 =====
        # 真正的HNSW索引
        self.hnsw_index = HNSWIndex(dim=128, M=16, ef_construction=200, ef_search=50)
        # 真正的向量嵌入引擎
        self.embedding_engine = VectorEmbeddingEngine(
            EmbeddingConfig(provider="simulation", dimension=128)
        )
        
        # ===== Phase 6: 细胞状态完善 =====
        # 休眠系统（取代"遗忘"）
        self.dormancy_system = DormancySystem(
            storage_path=os.path.join(memory_path, "dormancy")
        )
        # 梦境整理
        self.dream_system = MemoryDream(
            storage_path=os.path.join(memory_path, "dream")
        )
        # 记忆创造性
        self.creativity_system = MemoryCreativity(
            storage_path=os.path.join(memory_path, "creativity")
        )
        
        # ===== Phase 7: 鲁棒性 =====
        # 备份系统
        self.backup_system = MemoryBackup(
            memory_path=memory_path,
            backup_path=os.path.join(memory_path, "backups")
        )
        # 一致性检查
        self.consistency_checker = MemoryConsistency(memory_path=memory_path)
        
        # ===== Phase 8: 多模态 + 联邦 =====
        # 多模态记忆
        self.multimodal_system = MultimodalMemorySystem(
            memory_path=os.path.join(memory_path, "multimodal")
        )
        # 记忆联邦
        self.federation_system = MemoryFederation(
            agent_id="omni_memory_agent",
            memory_path=memory_path
        )
        
        # 索引
        self.vector_index: Dict[str, List[float]] = {}
        self.type_index: Dict[str, List[str]] = {}
        
        # 锁
        self._lock = threading.Lock()
        
        # 统计
        self.stats = {
            'total_cells': 0,
            'by_type': {},
            'by_status': {},
            'total_searches': 0,
            'total_remembers': 0,
            'avg_search_time': 0,
            'last_dream': None,
            'last_backup': None,
            'last_consistency_check': None
        }
        
        # 加载
        self._load_state()
    
    # ==================== 核心操作 ====================
    
    def remember(self, content: str, cell_type: str = "knowledge",
                 importance: float = 0.5, keywords: List[str] = None,
                 metadata: Dict = None, image_data: bytes = None,
                 audio_data: bytes = None) -> MemoryCell:
        """
        记忆 - 创建新的记忆细胞
        
        支持:
        - 文本记忆
        - 多模态记忆（图像、音频）
        - 自动语义索引
        - 休眠系统注册
        """
        with self._lock:
            # 创建细胞ID
            cell_id = f"cell_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
            
            # 映射类型到基因
            type_to_gene = {
                'user': CellGene.USER,
                'feedback': CellGene.FEEDBACK,
                'project': CellGene.PROJECT,
                'reference': CellGene.REFERENCE,
                'insight': CellGene.INSIGHT,
                'pattern': CellGene.PATTERN,
                'knowledge': CellGene.REFERENCE
            }
            gene = type_to_gene.get(cell_type, CellGene.REFERENCE)
            
            # 创建细胞
            cell = MemoryCell(
                id=cell_id,
                gene=gene,
                content=content,
                importance=importance
            )
            
            # 添加关键词
            if keywords:
                cell.keywords = keywords
            else:
                # 自动提取关键词
                cell.keywords = self._extract_keywords(content)
            
            # 添加元数据到cell（使用动态属性）
            if metadata:
                if not hasattr(cell, 'metadata'):
                    cell.metadata = {}
                cell.metadata.update(metadata)
            else:
                cell.metadata = {}
            
            # 注册到系统
            self.cells[cell.id] = cell
            
            # ===== Phase 5: 真正的语义索引 =====
            # 使用向量嵌入引擎生成向量
            vector = self.embedding_engine.embed(content)
            cell.metadata['vector'] = vector
            
            # 添加到HNSW索引
            self.hnsw_index.insert(cell.id, vector)
            
            # 保存向量索引
            self.vector_index[cell.id] = vector
            
            # ===== Phase 6: 注册到休眠系统 =====
            # 创建唤醒触发器
            wake_triggers = [
                WakeTrigger(
                    trigger_type="semantic",
                    keywords=cell.keywords[:5],
                    min_intensity=0.3
                )
            ]
            self.dormancy_system.register_cell(
                cell.id,
                initial_energy=importance + 0.5,
                wake_triggers=wake_triggers
            )
            
            # ===== Phase 8: 多模态支持 =====
            if image_data or audio_data:
                mm_memory = self.multimodal_system.create_memory(
                    text=content,
                    image_data=image_data,
                    audio_data=audio_data,
                    importance=importance
                )
                cell.metadata['multimodal_id'] = mm_memory.id
            
            # 更新类型索引
            if cell_type not in self.type_index:
                self.type_index[cell_type] = []
            self.type_index[cell_type].append(cell.id)
            
            # 添加到梦境整理队列
            self.dream_system.add_to_consolidation_queue(cell.id)
            
            # 更新统计
            self.stats['total_cells'] += 1
            self.stats['total_remembers'] += 1
            self.stats['by_type'][cell_type] = self.stats['by_type'].get(cell_type, 0) + 1
            
            self._save_state()
            return cell
    
    def recall(self, query: str, top_k: int = 10,
               include_dormant: bool = False,
               use_hnsw: bool = True) -> List[Tuple[MemoryCell, float, Dict]]:
        """
        回忆 - 检索相关记忆
        
        支持:
        - HNSW O(log n)检索
        - 时间增强
        - 休眠唤醒
        - 跨模态检索
        """
        import time
        start_time = time.time()
        
        results = []
        
        # ===== Phase 5: HNSW检索 =====
        if use_hnsw:
            query_vector = self.embedding_engine.embed(query)
            hnsw_results = self.hnsw_index.search(query_vector, top_k * 2)
            
            for node_id, distance, similarity in hnsw_results:
                if node_id in self.cells:
                    cell = self.cells[node_id]
                    
                    # 检查休眠状态
                    state = self.dormancy_system.cell_states.get(node_id, DormCellState.ACTIVE)
                    
                    if not include_dormant and state in [DormCellState.DORMANT, DormCellState.DEEP_DORMANT, DormCellState.CRYO]:
                        # 尝试唤醒
                        stimulus = {'text': query, 'type': 'semantic'}
                        matched, intensity = self.dormancy_system.check_wake_triggers(node_id, stimulus)
                        
                        if matched:
                            self.dormancy_system.activate_cell(node_id, intensity * 0.5)
                        else:
                            continue
                    
                    # 时间增强
                    time_boost = self._calculate_time_boost(cell.created_at)
                    
                    # 综合评分
                    final_score = similarity * 0.6 + time_boost * 0.2 + cell.importance * 0.2
                    
                    results.append((cell, final_score, {
                        'similarity': similarity,
                        'time_boost': time_boost,
                        'dormancy_state': state.value if hasattr(state, 'value') else str(state)
                    }))
                    
                    # 更新访问计数
                    cell.access_count += 1
        
        # ===== Phase 8: 多模态检索 =====
        mm_results = self.multimodal_system.search_by_text(query, top_k)
        for mm_id, score in mm_results:
            # 查找关联的细胞
            for cell in self.cells.values():
                if cell.metadata.get('multimodal_id') == mm_id:
                    if cell not in [r[0] for r in results]:
                        results.append((cell, score * 0.8, {'modality': 'multimodal'}))
        
        # 排序
        results.sort(key=lambda x: -x[1])
        
        # 更新统计
        elapsed = time.time() - start_time
        self.stats['total_searches'] += 1
        n = self.stats['total_searches']
        self.stats['avg_search_time'] = (self.stats['avg_search_time'] * (n-1) + elapsed) / n
        
        return results[:top_k]
    
    def push(self, context: str, top_k: int = 5) -> List[Tuple[MemoryCell, float, str]]:
        """
        主动推送 - 预测并推送相关记忆
        """
        results = []
        
        # 分析上下文意图
        intent_keywords = self._extract_keywords(context)
        
        # 找到相关记忆
        for cell_id, cell in self.cells.items():
            # 关键词匹配
            overlap = len(set(cell.keywords) & set(intent_keywords))
            if overlap > 0:
                relevance = overlap / max(len(cell.keywords), len(intent_keywords))
                
                # 考虑能量状态
                state = self.dormancy_system.cell_states.get(cell_id, CellState.ACTIVE)
                energy = self.dormancy_system.cell_energy.get(cell_id)
                energy_factor = energy.current if energy else 1.0
                
                final_score = relevance * 0.6 + energy_factor * 0.4
                
                if final_score > 0.3:
                    results.append((cell, final_score, f"关键词匹配({overlap}个)"))
        
        results.sort(key=lambda x: -x[1])
        return results[:top_k]
    
    def evolve(self, cell_id: str, new_content: str = None,
               importance_delta: float = 0, metadata_update: Dict = None) -> bool:
        """
        演化 - 更新记忆细胞
        """
        if cell_id not in self.cells:
            return False
        
        cell = self.cells[cell_id]
        
        # 更新内容
        if new_content:
            cell.content = new_content
            # 重新生成向量
            vector = self.embedding_engine.embed(new_content)
            cell.metadata['vector'] = vector
            self.vector_index[cell_id] = vector
            # 更新HNSW索引
            self.hnsw_index.insert(cell_id, vector)
        
        # 更新重要性
        if importance_delta != 0:
            cell.importance = max(0, min(1, cell.importance + importance_delta))
        
        # 更新元数据
        if metadata_update:
            cell.metadata.update(metadata_update)
        
        # 激活细胞
        self.dormancy_system.activate_cell(cell_id, 0.3)
        
        self._save_state()
        return True
    
    def divide(self, parent_id: str, child_content: str,
               child_type: str = "insight") -> Optional[MemoryCell]:
        """
        分裂 - 从父细胞产生新洞察
        """
        if parent_id not in self.cells:
            return None
        
        parent = self.cells[parent_id]
        
        # 创建子细胞
        child = self.remember(
            content=child_content,
            cell_type=child_type,
            importance=parent.importance * 0.8,
            keywords=parent.keywords[:3],
            metadata={'parent_id': parent_id}
        )
        
        # 建立连接
        self.network.connect(parent_id, child.id, weight=0.8)
        parent.children.append(child.id)
        
        self._save_state()
        return child
    
    # ==================== Phase 6: 高级认知 ====================
    
    def dormant_stats(self) -> Dict:
        """获取休眠统计"""
        return self.dormancy_system.get_report()
    
    def wake_cell(self, cell_id: str, intensity: float = 0.5) -> bool:
        """唤醒休眠细胞"""
        return self.dormancy_system.activate_cell(cell_id, intensity)
    
    def dream(self, duration: float = 60) -> Dict:
        """
        执行梦境整理
        
        整理记忆、建立关联、生成洞察
        """
        # 准备数据
        cells_data = {
            cid: {
                'content': c.content,
                'keywords': c.keywords,
                'importance': c.importance,
                'energy': self.dormancy_system.cell_energy.get(cid).current if self.dormancy_system.cell_energy.get(cid) else 1.0,
                'access_count': c.access_count,
                'created_time': c.created_at
            }
            for cid, c in self.cells.items()
        }
        
        network_data = self.network.connections if hasattr(self.network, 'connections') else {}
        
        # 执行梦境
        result = self.dream_system.dream(cells_data, network_data, duration)
        
        # 应用梦境结果
        for cell_id, energy in result.energy_changes.items():
            if cell_id in self.cells:
                self.dormancy_system.cell_energy[cell_id].current = energy
        
        # 创建新关联
        for cell1_id, cell2_id, strength in result.associations_created:
            self.network.connect(cell1_id, cell2_id, weight=strength)
        
        # 保存洞察
        for insight in result.insights_generated:
            self.creativity_system.save_idea(
                self.creativity_system._create_pattern_idea(
                    tuple(insight.get('pattern', [])),
                    [(cid, self.cells[cid]) for cid in insight.get('related_cells', []) if cid in self.cells]
                )
            )
        
        self.stats['last_dream'] = datetime.now().isoformat()
        self._save_state()
        
        return {
            'phase': result.phase.value,
            'cells_processed': result.cells_processed,
            'cells_consolidated': result.cells_consolidated,
            'associations_created': len(result.associations_created),
            'insights_generated': len(result.insights_generated),
            'duration': result.duration
        }
    
    def create_insights(self) -> List[Dict]:
        """生成创造性洞察"""
        cells_data = {
            cid: {
                'content': c.content,
                'keywords': c.keywords,
                'type': c.cell_type,
                'importance': c.importance,
                'energy': self.dormancy_system.cell_energy.get(cid).current if self.dormancy_system.cell_energy.get(cid) else 1.0
            }
            for cid, c in self.cells.items()
        }
        
        # 组合创新
        combinations = self.creativity_system.combine(cells_data)
        
        # 模式发现
        patterns = self.creativity_system.discover_patterns(cells_data)
        
        # 综合洞察
        synthesis = self.creativity_system.synthesize(cells_data)
        
        # 保存所有洞察
        for idea in combinations + patterns + synthesis:
            self.creativity_system.save_idea(idea)
        
        return [
            {
                'id': idea.id,
                'type': idea.type.value,
                'description': idea.description,
                'novelty': idea.novelty_score,
                'relevance': idea.relevance_score,
                'utility': idea.utility_score
            }
            for idea in combinations + patterns + synthesis
        ]
    
    # ==================== Phase 7: 鲁棒性 ====================
    
    def backup(self, description: str = "") -> Dict:
        """创建备份"""
        metadata = self.backup_system.create_full_backup(description)
        self.stats['last_backup'] = metadata.timestamp
        self._save_state()
        
        return {
            'id': metadata.id,
            'type': metadata.type.value,
            'size': metadata.size_bytes,
            'cell_count': metadata.cell_count,
            'timestamp': metadata.timestamp
        }
    
    def restore(self, backup_id: str) -> bool:
        """从备份恢复"""
        success = self.backup_system.restore(backup_id)
        if success:
            # 重新加载状态
            self._load_state()
        return success
    
    def check_consistency(self, auto_fix: bool = False) -> Dict:
        """一致性检查"""
        report = self.consistency_checker.run_full_check(auto_fix)
        self.stats['last_consistency_check'] = report.timestamp
        
        return {
            'passed': report.overall_passed,
            'total_issues': report.total_issues,
            'total_warnings': report.total_warnings,
            'recommendations': report.recommendations,
            'check_details': [
                {
                    'type': r.check_type.value,
                    'passed': r.passed,
                    'issues': len(r.issues),
                    'warnings': len(r.warnings)
                }
                for r in report.check_results
            ]
        }
    
    # ==================== Phase 8: 多模态 + 联邦 ====================
    
    def remember_multimodal(self, text: str = None,
                           image_path: str = None,
                           audio_path: str = None,
                           importance: float = 0.5) -> MemoryCell:
        """多模态记忆"""
        image_data = None
        audio_data = None
        
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                image_data = f.read()
        
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
        
        return self.remember(
            content=text or "多模态记忆",
            cell_type="multimodal",
            importance=importance,
            image_data=image_data,
            audio_data=audio_data
        )
    
    def share_memory(self, cell_id: str,
                     sharing_level: str = "selective",
                     authorized_agents: List[str] = None) -> Dict:
        """共享记忆到联邦"""
        if cell_id not in self.cells:
            return {'success': False, 'message': '记忆不存在'}
        
        cell = self.cells[cell_id]
        
        level = SharingLevel(sharing_level)
        shared = self.federation_system.share_memory(
            cell_id,
            {
                'content': cell.content,
                'type': cell.cell_type,
                'importance': cell.importance,
                'keywords': cell.keywords
            },
            level,
            authorized_agents
        )
        
        if shared:
            return {
                'success': True,
                'memory_id': shared.memory_id,
                'sharing_level': shared.sharing_level.value,
                'authorized_count': len(shared.authorized_agents)
            }
        
        return {'success': False, 'message': '共享失败'}
    
    def federated_search(self, query: str) -> List[Dict]:
        """联邦搜索"""
        results = self.federation_system.federated_search(query)
        
        return [
            {
                'memory_id': mem_id,
                'score': score,
                'owner': owner
            }
            for mem_id, score, owner in results
        ]
    
    # ==================== 统计与报告 ====================
    
    def get_stats(self) -> Dict:
        """获取系统统计"""
        # 更新状态分布
        status_dist = {}
        for cell in self.cells.values():
            status = cell.state.value if hasattr(cell.state, 'value') else str(cell.state)
            status_dist[status] = status_dist.get(status, 0) + 1
        self.stats['by_status'] = status_dist
        
        # HNSW统计
        hnsw_stats = self.hnsw_index.get_stats()
        
        # 休眠统计
        dormancy_report = self.dormancy_system.get_report()
        
        # 创造性统计
        creativity_report = self.creativity_system.get_report()
        
        return {
            'basic': self.stats,
            'hnsw': hnsw_stats,
            'dormancy': dormancy_report,
            'creativity': creativity_report,
            'vector_count': len(self.vector_index),
            'network_density': self.network.get_network_stats().get('total_synapses', 0) / max(1, len(self.cells))
        }
    
    def visualize(self) -> str:
        """可视化系统状态"""
        stats = self.get_stats()
        
        lines = [
            "=" * 70,
            "             OMNI-MEMORY ULTIMATE V2 - 系统状态",
            "=" * 70,
            "",
            "【基础统计】",
            f"  总细胞数: {stats['basic']['total_cells']}",
            f"  总记忆数: {stats['basic']['total_remembers']}",
            f"  总搜索数: {stats['basic']['total_searches']}",
            f"  平均搜索时间: {stats['basic']['avg_search_time']*1000:.2f}ms",
            "",
            "【类型分布】",
        ]
        
        for t, count in stats['basic']['by_type'].items():
            lines.append(f"  {t}: {count}")
        
        lines.extend([
            "",
            "【HNSW索引】",
            f"  节点数: {stats['hnsw']['total_nodes']}",
            f"  最大层级: {stats['hnsw']['max_level']}",
            f"  平均连接: {stats['hnsw']['avg_connections_per_node']}",
            f"  理论复杂度: {stats['hnsw']['theoretical_complexity']}",
            "",
            "【休眠系统】",
            f"  活跃细胞: {stats['dormancy']['active_count']}",
            f"  休眠细胞: {stats['dormancy']['dormant_count']}",
            f"  唤醒事件: {stats['dormancy']['wake_events']}",
            "",
            "【创造性系统】",
            f"  总洞察数: {stats['creativity']['total_ideas']}",
            f"  平均新颖度: {stats['creativity']['averages']['novelty']:.3f}",
            f"  平均实用性: {stats['creativity']['averages']['utility']:.3f}",
            "",
            "=" * 70
        ])
        
        return "\n".join(lines)
    
    # ==================== 内部方法 ====================
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简化实现
        import re
        words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
        
        # 过滤停用词
        stop_words = {'的', '是', '在', '了', '和', '与', '或', '这', '那', '有', '我', '你', '他', 'the', 'a', 'an', 'is', 'are', 'was', 'were'}
        
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        
        # 去重并返回
        return list(set(keywords))[:10]
    
    def _calculate_time_boost(self, created_time: str) -> float:
        """计算时间增强"""
        try:
            created = datetime.fromisoformat(created_time)
            age_days = (datetime.now() - created).days
            
            # 艾宾浩斯曲线
            return math.exp(-age_days / 30)  # 30天半衰期
        except:
            return 0.5
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.memory_path, "ultimate_v2_state.json")
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                # 加载细胞
                for cid, cdata in data.get('cells', {}).items():
                    cell = MemoryCell(
                        content=cdata['content'],
                        cell_type=cdata.get('type', 'knowledge'),
                        importance=cdata.get('importance', 0.5)
                    )
                    cell.id = cid
                    cell.keywords = cdata.get('keywords', [])
                    cell.access_count = cdata.get('access_count', 0)
                    cell.created_time = cdata.get('created_time', datetime.now().isoformat())
                    cell.metadata = cdata.get('metadata', {})
                    
                    self.cells[cid] = cell
                    
                    # 重建HNSW索引
                    if 'vector' in cell.metadata:
                        self.hnsw_index.insert(cid, cell.metadata['vector'])
                        self.vector_index[cid] = cell.metadata['vector']
                
                self.type_index = data.get('type_index', {})
                
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.memory_path, "ultimate_v2_state.json")
        
        data = {
            'stats': self.stats,
            'cells': {
                cid: {
                    'content': c.content,
                    'type': c.gene.value if hasattr(c.gene, 'value') else str(c.gene),
                    'importance': c.importance,
                    'keywords': c.keywords,
                    'access_count': c.access_count,
                    'created_time': c.created_at if hasattr(c, 'created_at') else c.created_time,
                    'metadata': getattr(c, 'metadata', {})
                }
                for cid, c in self.cells.items()
            },
            'type_index': self.type_index
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 保存HNSW索引
        self.hnsw_index.save(os.path.join(self.memory_path, "hnsw_index.json"))
        
        # 保存休眠状态
        self.dormancy_system.save_state()


# ==================== CLI接口 ====================

def main():
    parser = argparse.ArgumentParser(description="Omni-Memory Ultimate V2")
    parser.add_argument("command", choices=[
        "remember", "recall", "push", "evolve", "divide",
        "dream", "insights", "backup", "restore", "check",
        "stats", "visualize", "wake"
    ])
    
    # 参数
    parser.add_argument("--content", "-c", type=str, default="")
    parser.add_argument("--type", "-t", type=str, default="knowledge")
    parser.add_argument("--importance", "-i", type=float, default=0.5)
    parser.add_argument("--query", "-q", type=str, default="")
    parser.add_argument("--top-k", "-k", type=int, default=5)
    parser.add_argument("--id", type=str, default="")
    parser.add_argument("--intensity", type=float, default=0.5)
    parser.add_argument("--backup-id", type=str, default="")
    parser.add_argument("--auto-fix", action="store_true")
    
    args = parser.parse_args()
    
    # 初始化系统
    memory = OmniMemoryUltimateV2()
    
    if args.command == "remember":
        cell = memory.remember(
            content=args.content,
            cell_type=args.type,
            importance=args.importance
        )
        print(f"记忆创建成功: {cell.id}")
        print(f"内容: {cell.content[:50]}...")
        print(f"关键词: {cell.keywords}")
        
    elif args.command == "recall":
        results = memory.recall(query=args.query, top_k=args.top_k)
        print(f"\n找到 {len(results)} 条相关记忆:\n")
        for i, (cell, score, meta) in enumerate(results, 1):
            print(f"{i}. [{cell.id}] 分数: {score:.3f}")
            print(f"   内容: {cell.content[:60]}...")
            print(f"   状态: {meta.get('dormancy_state', 'active')}")
            print()
    
    elif args.command == "push":
        results = memory.push(context=args.query, top_k=args.top_k)
        print(f"\n主动推送 {len(results)} 条相关记忆:\n")
        for i, (cell, score, reason) in enumerate(results, 1):
            print(f"{i}. [{cell.id}] 分数: {score:.3f}")
            print(f"   原因: {reason}")
            print(f"   内容: {cell.content[:60]}...")
            print()
    
    elif args.command == "evolve":
        success = memory.evolve(
            cell_id=args.id,
            new_content=args.content,
            importance_delta=args.intensity
        )
        print(f"演化{'成功' if success else '失败'}")
    
    elif args.command == "divide":
        child = memory.divide(
            parent_id=args.id,
            child_content=args.content
        )
        if child:
            print(f"分裂成功: {child.id}")
            print(f"内容: {child.content[:50]}...")
        else:
            print("分裂失败")
    
    elif args.command == "dream":
        result = memory.dream()
        print("梦境整理完成:")
        print(f"  处理细胞: {result['cells_processed']}")
        print(f"  巩固记忆: {len(result['cells_consolidated'])}")
        print(f"  创建关联: {result['associations_created']}")
        print(f"  生成洞察: {result['insights_generated']}")
        print(f"  耗时: {result['duration']:.3f}秒")
    
    elif args.command == "insights":
        insights = memory.create_insights()
        print(f"生成 {len(insights)} 个洞察:\n")
        for i, insight in enumerate(insights[:10], 1):
            print(f"{i}. [{insight['type']}] {insight['description'][:60]}...")
            print(f"   新颖度: {insight['novelty']:.2f}, 实用性: {insight['utility']:.2f}")
    
    elif args.command == "backup":
        result = memory.backup(args.content)
        print(f"备份创建成功:")
        print(f"  ID: {result['id']}")
        print(f"  大小: {result['size']} bytes")
        print(f"  细胞数: {result['cell_count']}")
    
    elif args.command == "restore":
        success = memory.restore(args.backup_id)
        print(f"恢复{'成功' if success else '失败'}")
    
    elif args.command == "check":
        result = memory.check_consistency(auto_fix=args.auto_fix)
        print(f"一致性检查: {'通过' if result['passed'] else '发现问题'}")
        print(f"问题数: {result['total_issues']}")
        print(f"警告数: {result['total_warnings']}")
        if result['recommendations']:
            print("\n建议:")
            for rec in result['recommendations']:
                print(f"  - {rec}")
    
    elif args.command == "stats":
        stats = memory.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.command == "visualize":
        print(memory.visualize())
    
    elif args.command == "wake":
        success = memory.wake_cell(args.id, args.intensity)
        print(f"唤醒{'成功' if success else '失败'}")


if __name__ == "__main__":
    main()
