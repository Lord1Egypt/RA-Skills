#!/usr/bin/env python3
"""
弘脑记忆系统 - 记忆巩固模块
HongNao Memory OS - Memory Consolidation Module

功能：对原始记忆进行压缩、摘要、关联建立、重要性评分
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

from memory_extraction import MemCell, MemoryType


@dataclass
class MemScene:
    """记忆场景 - 围绕主题/人物/任务形成的记忆集合"""
    id: str
    title: str  # 场景标题
    scene_type: str  # 场景类型（project/user/task/relationship）
    memcell_ids: List[str]  # 包含的 MemCell ID 列表
    created_at: str
    updated_at: str
    activity_level: float = 1.0  # 场景活跃度 0-1
    last_accessed: str = None  # 最后访问时间
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.memcell_ids is None:
            self.memcell_ids = []
        if self.metadata is None:
            self.metadata = {}
        if self.last_accessed is None:
            self.last_accessed = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class MemoryConsolidator:
    """记忆巩固器"""
    
    def __init__(self):
        """初始化巩固器"""
        self.similarity_threshold = 0.8  # 相似度阈值
    
    def consolidate(self, mem_cells: List[MemCell]) -> List[MemCell]:
        """
        对记忆进行巩固处理
        
        Args:
            mem_cells: 原始 MemCell 列表
        
        Returns:
            巩固后的 MemCell 列表
        """
        # 步骤 1: 去重 - 合并重复/冲突记忆
        deduped_cells = self._deduplicate(mem_cells)
        
        # 步骤 2: 压缩 - 生成简洁摘要
        compressed_cells = self._compress(deduped_cells)
        
        # 步骤 3: 关联 - 建立与其他记忆的链接
        associated_cells = self._associate(compressed_cells)
        
        # 步骤 4: 评分 - 重新计算重要性分数
        scored_cells = self._recalculate_importance(associated_cells)
        
        return scored_cells
    
    def _deduplicate(self, mem_cells: List[MemCell]) -> List[MemCell]:
        """
        去重：合并重复/冲突记忆
        
        Args:
            mem_cells: 原始 MemCell 列表
        
        Returns:
            去重后的 MemCell 列表
        """
        # 按内容分组
        content_groups = defaultdict(list)
        for cell in mem_cells:
            # 标准化内容（去除空格、标点）
            normalized = self._normalize_content(cell.content)
            content_groups[normalized].append(cell)
        
        deduped_cells = []
        
        for normalized, group in content_groups.items():
            if len(group) == 1:
                # 无重复，直接保留
                deduped_cells.append(group[0])
            else:
                # 有重复，合并
                merged_cell = self._merge_cells(group)
                deduped_cells.append(merged_cell)
        
        print(f"  去重：{len(mem_cells)} → {len(deduped_cells)} 条")
        return deduped_cells
    
    def _normalize_content(self, content: str) -> str:
        """标准化内容（去除空格、标点）"""
        import re
        # 去除空格和常见标点
        normalized = re.sub(r'[\s\.,;:,.!?]+', '', content)
        return normalized.lower()
    
    def _merge_cells(self, cells: List[MemCell]) -> MemCell:
        """
        合并多个重复的 MemCell
        
        Args:
            cells: 待合并的 MemCell 列表
        
        Returns:
            合并后的 MemCell
        """
        # 保留最新的内容
        latest_cell = max(cells, key=lambda c: c.updated_at)
        
        # 合并标签
        all_tags = set()
        for cell in cells:
            all_tags.update(cell.tags)
        
        # 更新元数据
        merged_metadata = latest_cell.metadata.copy()
        merged_metadata['merged_from'] = [c.id for c in cells if c.id != latest_cell.id]
        merged_metadata['merge_count'] = len(cells)
        
        # 提升重要性（因为重复出现）
        new_importance = min(latest_cell.importance + 1, 10)
        
        return MemCell(
            id=latest_cell.id,
            content=latest_cell.content,
            memory_type=latest_cell.memory_type,
            source=latest_cell.source,
            created_at=latest_cell.created_at,
            updated_at=datetime.now().isoformat(),
            importance=new_importance,
            access_count=sum(c.access_count for c in cells),
            tags=list(all_tags),
            metadata=merged_metadata
        )
    
    def _compress(self, mem_cells: List[MemCell]) -> List[MemCell]:
        """
        压缩：生成简洁摘要
        
        Args:
            mem_cells: MemCell 列表
        
        Returns:
            压缩后的 MemCell 列表
        """
        compressed_cells = []
        
        for cell in mem_cells:
            # 简单压缩策略：截断过长内容
            if len(cell.content) > 200:
                compressed_content = cell.content[:197] + "..."
            else:
                compressed_content = cell.content
            
            # 创建压缩后的副本
            compressed_cell = MemCell(
                id=cell.id,
                content=compressed_content,
                memory_type=cell.memory_type,
                source=cell.source,
                created_at=cell.created_at,
                updated_at=cell.updated_at,
                importance=cell.importance,
                access_count=cell.access_count,
                tags=cell.tags,
                metadata=cell.metadata
            )
            
            # 记录压缩信息
            compressed_cell.metadata['original_length'] = len(cell.content)
            compressed_cell.metadata['compressed_length'] = len(compressed_content)
            compressed_cell.metadata['compression_ratio'] = len(compressed_content) / len(cell.content) if len(cell.content) > 0 else 1.0
            
            compressed_cells.append(compressed_cell)
        
        if compressed_cells:
            avg_ratio = sum(c.metadata['compression_ratio'] for c in compressed_cells) / len(compressed_cells)
            print(f"  压缩：平均压缩率 {avg_ratio:.2%}")
        else:
            print(f"  压缩：无数据")
        
        return compressed_cells
    
    def _associate(self, mem_cells: List[MemCell]) -> List[MemCell]:
        """
        关联：建立与其他记忆的链接
        
        Args:
            mem_cells: MemCell 列表
        
        Returns:
            关联后的 MemCell 列表
        """
        # 按标签分组
        tag_groups = defaultdict(list)
        for cell in mem_cells:
            for tag in cell.tags:
                tag_groups[tag].append(cell.id)
        
        # 为每个记忆添加关联
        for cell in mem_cells:
            related_ids = set()
            for tag in cell.tags:
                related_ids.update(tag_groups[tag])
            
            # 移除自身
            related_ids.discard(cell.id)
            
            # 添加关联 ID
            cell.metadata['related_ids'] = list(related_ids)
            cell.metadata['relation_count'] = len(related_ids)
        
        if mem_cells:
            avg_relations = sum(c.metadata['relation_count'] for c in mem_cells) / len(mem_cells)
            print(f"  关联：平均每个记忆关联 {avg_relations:.1f} 个其他记忆")
        else:
            print(f"  关联：无数据")
        
        return mem_cells
    
    def _recalculate_importance(self, mem_cells: List[MemCell]) -> List[MemCell]:
        """
        重新计算重要性评分
        
        考虑因素：
        - 基础重要性（记忆类型）
        - 访问频率
        - 关联数量
        - 时间衰减
        
        Args:
            mem_cells: MemCell 列表
        
        Returns:
            重新评分后的 MemCell 列表
        """
        for cell in mem_cells:
            # 基础分（来自记忆类型）
            base_scores = {
                MemoryType.FACT.value: 5,
                MemoryType.PREFERENCE.value: 6,
                MemoryType.CONSTRAINT.value: 8,
                MemoryType.SKILL.value: 5,
                MemoryType.EMOTION.value: 6,
            }
            base_score = base_scores.get(cell.memory_type, 5)
            
            # 访问频率加分（最多 +2）
            access_bonus = min(cell.access_count * 0.5, 2)
            
            # 关联数量加分（最多 +1）
            relation_bonus = min(cell.metadata.get('relation_count', 0) * 0.2, 1)
            
            # 计算最终分数
            final_score = base_score + access_bonus + relation_bonus
            final_score = min(round(final_score), 10)
            
            # 记录评分详情
            cell.metadata['importance_breakdown'] = {
                'base': base_score,
                'access_bonus': access_bonus,
                'relation_bonus': relation_bonus,
                'final': final_score
            }
            
            cell.importance = final_score
        
        if mem_cells:
            avg_importance = sum(c.importance for c in mem_cells) / len(mem_cells)
            print(f"  评分：平均重要性 {avg_importance:.1f}/10")
        else:
            print(f"  评分：无数据")
        
        return mem_cells
    
    def create_scene(
        self,
        title: str,
        scene_type: str,
        mem_cells: List[MemCell]
    ) -> MemScene:
        """
        创建记忆场景
        
        Args:
            title: 场景标题
            scene_type: 场景类型
            mem_cells: 包含的 MemCell 列表
        
        Returns:
            创建的 MemScene
        """
        import uuid
        
        timestamp = datetime.now().isoformat()
        
        scene = MemScene(
            id=f"scene_{uuid.uuid4().hex[:12]}",
            title=title,
            scene_type=scene_type,
            memcell_ids=[cell.id for cell in mem_cells],
            created_at=timestamp,
            updated_at=timestamp,
            activity_level=1.0,
            last_accessed=timestamp,
            metadata={
                'cell_count': len(mem_cells),
                'avg_importance': sum(c.importance for c in mem_cells) / len(mem_cells) if mem_cells else 0
            }
        )
        
        return scene


def test_consolidator():
    """测试记忆巩固器"""
    from memory_extraction import MemoryExtractor
    
    print("=" * 60)
    print("弘脑记忆系统 - 记忆巩固模块测试")
    print("=" * 60)
    
    # 先抽取一些记忆
    extractor = MemoryExtractor()
    test_text = """
    用户叫唐锋，在燧弘华创工作，职位是执行总裁。
    用户喜欢简洁商务风格，偏好使用 PPT 做演示。
    用户喜欢简洁风格，讨厌复杂的流程。
    项目预算为 100 万元。
    必须保证数据安全，不能泄露敏感信息。
    """
    
    mem_cells = extractor.extract_from_text(test_text, source="test")
    
    print(f"\n原始记忆：{len(mem_cells)} 条\n")
    
    # 巩固处理
    consolidator = MemoryConsolidator()
    consolidated_cells = consolidator.consolidate(mem_cells)
    
    print(f"\n巩固后记忆：{len(consolidated_cells)} 条\n")
    print("=" * 60)
    print("巩固后的记忆详情：")
    print("=" * 60)
    
    for i, cell in enumerate(consolidated_cells, 1):
        print(f"\n{i}. [{cell.memory_type}] {cell.content}")
        print(f"   重要性：{cell.importance}/10")
        print(f"   标签：{', '.join(cell.tags)}")
        if cell.metadata.get('related_ids'):
            print(f"   关联：{len(cell.metadata['related_ids'])} 个")
    
    # 测试场景创建
    print("\n" + "=" * 60)
    print("创建记忆场景测试")
    print("=" * 60)
    
    scene = consolidator.create_scene(
        title="燧弘华创项目",
        scene_type="project",
        mem_cells=consolidated_cells
    )
    
    print(f"\n场景 ID: {scene.id}")
    print(f"场景标题：{scene.title}")
    print(f"场景类型：{scene.scene_type}")
    print(f"包含记忆：{len(scene.memcell_ids)} 条")
    print(f"平均重要性：{scene.metadata['avg_importance']:.1f}/10")
    
    return consolidated_cells, scene


if __name__ == '__main__':
    test_consolidator()
