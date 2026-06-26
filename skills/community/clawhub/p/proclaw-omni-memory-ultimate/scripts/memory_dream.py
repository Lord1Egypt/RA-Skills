#!/usr/bin/env python3
"""
记忆梦境系统
模拟睡眠期间的记忆整理和巩固

基于神经科学:
- 睡眠期间海马体与新皮层进行记忆整合
- REM睡眠进行记忆强化和关联重组
- 慢波睡眠进行记忆从短期向长期转移

功能:
- 离线记忆整理
- 强化重要记忆
- 建立新关联
- 清理噪音
- 能量重新分配
"""

import json
import math
import os
import random
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DreamPhase(Enum):
    """梦境阶段"""
    SLEEP_ONSET = "sleep_onset"      # 入睡期：开始整理
    LIGHT_SLEEP = "light_sleep"      # 浅睡期：轻度整理
    SWS = "sws"                       # 慢波睡眠：记忆巩固
    REM = "rem"                       # 快速眼动：记忆重组
    AWAKENING = "awakening"           # 唤醒期：完成整理


@dataclass
class DreamConfig:
    """梦境配置"""
    consolidate_threshold: float = 0.6   # 巩固阈值
    association_threshold: float = 0.7    # 关联阈值
    noise_threshold: float = 0.1          # 噪音阈值
    energy_reallocation: bool = True      # 能量重分配
    creative_combination: bool = True     # 创造性组合
    max_dream_duration: int = 300         # 最大梦境时长（秒）


@dataclass
class DreamResult:
    """梦境结果"""
    phase: DreamPhase
    cells_processed: int
    cells_consolidated: List[str]
    associations_created: List[Tuple[str, str, float]]
    insights_generated: List[Dict]
    energy_changes: Dict[str, float]
    noise_cleaned: int
    duration: float


class MemoryDream:
    """
    记忆梦境系统
    
    在系统空闲或定期执行，进行记忆整理
    """
    
    def __init__(self, storage_path: str = "./memory/dream",
                 config: DreamConfig = None):
        self.storage_path = storage_path
        self.config = config or DreamConfig()
        os.makedirs(storage_path, exist_ok=True)
        
        # 梦境历史
        self.dream_history: List[DreamResult] = []
        
        # 待整理队列
        self.pending_consolidation: Set[str] = set()
        self.pending_association: Set[str] = set()
        
        # 统计
        self.stats = {
            'total_dreams': 0,
            'total_consolidated': 0,
            'total_associations': 0,
            'total_insights': 0,
            'total_noise_cleaned': 0,
            'total_duration': 0
        }
        
        self._load_state()
    
    def add_to_consolidation_queue(self, cell_id: str) -> None:
        """添加到巩固队列"""
        self.pending_consolidation.add(cell_id)
    
    def add_to_association_queue(self, cell_id: str) -> None:
        """添加到关联队列"""
        self.pending_association.add(cell_id)
    
    def dream(self, cells: Dict[str, Dict], 
              network: Dict[str, Set[str]],
              duration: float = 60.0) -> DreamResult:
        """
        执行梦境整理
        
        Args:
            cells: 细胞数据 {cell_id: cell_data}
            network: 网络连接 {cell_id: connected_cell_ids}
            duration: 梦境时长
        
        Returns:
            DreamResult: 梦境结果
        """
        start_time = datetime.now()
        
        cells_consolidated = []
        associations_created = []
        insights_generated = []
        energy_changes = {}
        noise_cleaned = 0
        
        # Phase 1: 入睡期 - 准备整理
        phase = DreamPhase.SLEEP_ONSET
        candidates = self._select_dream_candidates(cells)
        
        # Phase 2: 浅睡期 - 轻度整理
        phase = DreamPhase.LIGHT_SLEEP
        for cell_id in candidates[:len(candidates)//4]:
            if cell_id in cells:
                # 轻度激活
                energy_changes[cell_id] = cells[cell_id].get('energy', 1.0) * 1.1
        
        # Phase 3: 慢波睡眠 - 记忆巩固
        phase = DreamPhase.SWS
        for cell_id in candidates[len(candidates)//4:len(candidates)//2]:
            if cell_id in cells:
                cell = cells[cell_id]
                
                # 检查是否应该巩固
                importance = cell.get('importance', 0.5)
                energy = cell.get('energy', 1.0)
                access_count = cell.get('access_count', 0)
                
                consolidate_score = (importance * 0.5 + 
                                    min(1.0, access_count / 10) * 0.3 +
                                    energy * 0.2)
                
                if consolidate_score >= self.config.consolidate_threshold:
                    cells_consolidated.append(cell_id)
                    energy_changes[cell_id] = min(2.0, energy * 1.3)
        
        # Phase 4: REM睡眠 - 记忆重组和创造
        phase = DreamPhase.REM
        
        # 4.1 创建新关联
        for cell_id in list(self.pending_association)[:50]:
            if cell_id in cells and cell_id in network:
                # 寻找潜在关联
                cell_vec = cells[cell_id].get('vector', [])
                cell_keywords = set(cells[cell_id].get('keywords', []))
                
                for other_id, other_data in cells.items():
                    if other_id == cell_id or other_id in network.get(cell_id, set()):
                        continue
                    
                    # 计算关联强度
                    other_keywords = set(other_data.get('keywords', []))
                    keyword_overlap = len(cell_keywords & other_keywords)
                    
                    if keyword_overlap >= 2:
                        # 发现关联
                        association_strength = keyword_overlap / max(len(cell_keywords), len(other_keywords))
                        if association_strength >= self.config.association_threshold:
                            associations_created.append((cell_id, other_id, association_strength))
        
        # 4.2 创造性洞察
        if self.config.creative_combination:
            insights_generated = self._generate_insights(cells, network)
        
        # Phase 5: 唤醒期 - 完成整理
        phase = DreamPhase.AWAKENING
        
        # 清理噪音
        for cell_id, cell in cells.items():
            if cell.get('energy', 1.0) < self.config.noise_threshold:
                # 标记为噪音，但不删除
                noise_cleaned += 1
                energy_changes[cell_id] = 0.05  # 降到最低
        
        # 能量重分配
        if self.config.energy_reallocation:
            energy_changes = self._reallocate_energy(cells, energy_changes)
        
        # 计算实际时长
        actual_duration = (datetime.now() - start_time).total_seconds()
        
        # 创建结果
        result = DreamResult(
            phase=phase,
            cells_processed=len(candidates),
            cells_consolidated=cells_consolidated,
            associations_created=associations_created,
            insights_generated=insights_generated,
            energy_changes=energy_changes,
            noise_cleaned=noise_cleaned,
            duration=actual_duration
        )
        
        # 更新统计
        self.dream_history.append(result)
        self.stats['total_dreams'] += 1
        self.stats['total_consolidated'] += len(cells_consolidated)
        self.stats['total_associations'] += len(associations_created)
        self.stats['total_insights'] += len(insights_generated)
        self.stats['total_noise_cleaned'] += noise_cleaned
        self.stats['total_duration'] += actual_duration
        
        # 清空队列
        self.pending_consolidation.clear()
        self.pending_association.clear()
        
        self._save_state()
        return result
    
    def _select_dream_candidates(self, cells: Dict[str, Dict]) -> List[str]:
        """选择梦境整理候选"""
        candidates = []
        
        # 优先选择：新记忆 + 高访问 + 中等能量
        for cell_id, cell in cells.items():
            score = 0.0
            
            # 新近度
            created_time = cell.get('created_time')
            if created_time:
                age_days = (datetime.now() - datetime.fromisoformat(created_time)).days
                score += max(0, 1 - age_days / 30) * 0.3
            
            # 访问频率
            access_count = cell.get('access_count', 0)
            score += min(1.0, access_count / 10) * 0.3
            
            # 能量适中（不太高也不太低）
            energy = cell.get('energy', 1.0)
            score += (1 - abs(energy - 0.5)) * 0.4
            
            candidates.append((cell_id, score))
        
        # 排序
        candidates.sort(key=lambda x: -x[1])
        return [c[0] for c in candidates[:100]]  # 每次最多处理100个
    
    def _generate_insights(self, cells: Dict[str, Dict], 
                          network: Dict[str, Set[str]]) -> List[Dict]:
        """生成创造性洞察"""
        insights = []
        
        # 寻找共同模式
        pattern_cells = {}
        for cell_id, cell in cells.items():
            pattern = tuple(sorted(cell.get('keywords', []))[:3])
            if pattern not in pattern_cells:
                pattern_cells[pattern] = []
            pattern_cells[pattern].append(cell_id)
        
        # 对频繁模式生成洞察
        for pattern, cell_ids in pattern_cells.items():
            if len(cell_ids) >= 3:
                insight = {
                    'type': 'pattern',
                    'pattern': list(pattern),
                    'related_cells': cell_ids[:5],
                    'description': f"发现{len(cell_ids)}个记忆具有共同模式: {', '.join(pattern)}",
                    'confidence': min(1.0, len(cell_ids) / 10),
                    'created_time': datetime.now().isoformat()
                }
                insights.append(insight)
        
        # 寻找中心节点（高连接）
        central_nodes = []
        for cell_id, connections in network.items():
            if len(connections) >= 3:
                central_nodes.append((cell_id, len(connections)))
        
        central_nodes.sort(key=lambda x: -x[1])
        
        if central_nodes:
            # 生成枢纽洞察
            for cell_id, conn_count in central_nodes[:3]:
                insight = {
                    'type': 'hub',
                    'cell_id': cell_id,
                    'connection_count': conn_count,
                    'description': f"记忆 {cell_id} 是知识网络的关键枢纽，连接了 {conn_count} 个相关记忆",
                    'confidence': min(1.0, conn_count / 10),
                    'created_time': datetime.now().isoformat()
                }
                insights.append(insight)
        
        return insights
    
    def _reallocate_energy(self, cells: Dict[str, Dict], 
                          changes: Dict[str, float]) -> Dict[str, float]:
        """能量重分配"""
        # 计算总能量
        total_energy = sum(cells.get(cid, {}).get('energy', 1.0) for cid in changes)
        total_energy += sum(cells.get(cid, {}).get('energy', 1.0) 
                          for cid in cells if cid not in changes)
        
        # 重要记忆获得更多能量
        for cell_id in changes:
            cell = cells.get(cell_id, {})
            importance = cell.get('importance', 0.5)
            base_energy = changes[cell_id]
            
            # 根据重要性调整
            adjusted = base_energy * (0.8 + importance * 0.4)
            changes[cell_id] = min(2.0, max(0.05, adjusted))
        
        return changes
    
    def get_dream_schedule(self) -> Dict:
        """获取梦境调度建议"""
        pending = len(self.pending_consolidation) + len(self.pending_association)
        
        return {
            'pending_consolidation': len(self.pending_consolidation),
            'pending_association': len(self.pending_association),
            'recommended_dream': pending >= 10,
            'last_dream': self.dream_history[-1].phase.value if self.dream_history else None,
            'total_dreams': self.stats['total_dreams']
        }
    
    def get_insights(self, limit: int = 10) -> List[Dict]:
        """获取历史洞察"""
        insights = []
        for dream in reversed(self.dream_history):
            insights.extend(dream.insights_generated)
            if len(insights) >= limit:
                break
        return insights[:limit]
    
    def get_report(self) -> Dict:
        """获取梦境报告"""
        return {
            'stats': self.stats,
            'recent_dreams': len(self.dream_history[-10:]),
            'total_insights': self.stats['total_insights'],
            'average_duration': (self.stats['total_duration'] / max(1, self.stats['total_dreams'])),
            'pending_tasks': {
                'consolidation': len(self.pending_consolidation),
                'association': len(self.pending_association)
            }
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'dream_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                self.stats = data.get('stats', self.stats)
            except Exception:
                pass
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'dream_state.json')
        
        data = {
            'stats': self.stats,
            'pending_consolidation': list(self.pending_consolidation),
            'pending_association': list(self.pending_association)
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_dream():
    """演示梦境系统"""
    print("=" * 60)
    print("记忆梦境系统演示")
    print("=" * 60)
    
    dream = MemoryDream()
    
    # 模拟细胞数据
    cells = {
        'cell_001': {
            'content': '用户是Python开发者',
            'keywords': ['python', '开发', '用户'],
            'importance': 0.8,
            'energy': 1.0,
            'access_count': 5,
            'created_time': '2024-01-01T10:00:00'
        },
        'cell_002': {
            'content': '用户偏好FastAPI框架',
            'keywords': ['fastapi', '框架', '用户', '偏好'],
            'importance': 0.7,
            'energy': 0.8,
            'access_count': 3,
            'created_time': '2024-01-02T10:00:00'
        },
        'cell_003': {
            'content': '项目使用PostgreSQL数据库',
            'keywords': ['postgresql', '数据库', '项目'],
            'importance': 0.6,
            'energy': 0.6,
            'access_count': 2,
            'created_time': '2024-01-03T10:00:00'
        },
        'cell_004': {
            'content': '用户喜欢Docker容器化',
            'keywords': ['docker', '容器', '用户'],
            'importance': 0.65,
            'energy': 0.5,
            'access_count': 4,
            'created_time': '2024-01-04T10:00:00'
        },
        'cell_005': {
            'content': '代码测试覆盖率要求80%',
            'keywords': ['测试', '代码', '覆盖率'],
            'importance': 0.55,
            'energy': 0.3,
            'access_count': 1,
            'created_time': '2024-01-05T10:00:00'
        }
    }
    
    # 模拟网络
    network = {
        'cell_001': {'cell_002', 'cell_004'},
        'cell_002': {'cell_001'},
        'cell_003': set(),
        'cell_004': {'cell_001'},
        'cell_005': set()
    }
    
    # 添加到队列
    print("\n添加细胞到整理队列...")
    for cell_id in cells:
        dream.add_to_consolidation_queue(cell_id)
        dream.add_to_association_queue(cell_id)
    
    print(f"待整理: {len(dream.pending_consolidation)}")
    print(f"待关联: {len(dream.pending_association)}")
    
    # 执行梦境
    print("\n开始梦境整理...")
    result = dream.dream(cells, network)
    
    print(f"\n梦境结果:")
    print(f"  处理细胞: {result.cells_processed}")
    print(f"  巩固记忆: {result.cells_consolidated}")
    print(f"  创建关联: {len(result.associations_created)}")
    print(f"  生成洞察: {len(result.insights_generated)}")
    print(f"  清理噪音: {result.noise_cleaned}")
    print(f"  持续时间: {result.duration:.3f}秒")
    
    # 显示洞察
    if result.insights_generated:
        print(f"\n生成的洞察:")
        for insight in result.insights_generated:
            print(f"  [{insight['type']}] {insight['description']}")
    
    # 显示报告
    print(f"\n梦境报告:")
    report = dream.get_report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    demo_dream()
