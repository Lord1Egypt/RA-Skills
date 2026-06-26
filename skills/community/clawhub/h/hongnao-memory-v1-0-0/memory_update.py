#!/usr/bin/env python3
"""
弘脑记忆系统 - 记忆更新与遗忘模块
HongNao Memory OS - Memory Update & Forgetting Module

功能：定期清理过期/低价值记忆，更新冲突/过时记忆，基于遗忘曲线主动清理
"""

import json
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from memory_extraction import MemCell, MemoryType


class UpdateAction(Enum):
    """更新操作类型"""
    KEEP = "keep"  # 保留
    UPDATE = "update"  # 更新
    MERGE = "merge"  # 合并
    ARCHIVE = "archive"  # 归档
    DELETE = "delete"  # 删除


@dataclass
class ForgettingCurve:
    """艾宾浩斯遗忘曲线参数"""
    half_life_days: float = 30.0  # 半衰期（天）
    retention_threshold: float = 0.2  # 保留阈值
    archive_threshold: float = 0.1  # 归档阈值
    delete_threshold: float = 0.05  # 删除阈值


class MemoryUpdater:
    """记忆更新器"""
    
    def __init__(self):
        """初始化更新器"""
        self.conflict_threshold = 0.8  # 冲突判定阈值
    
    def update_memory(
        self,
        existing_cells: List[MemCell],
        new_cells: List[MemCell]
    ) -> Tuple[List[MemCell], List[Dict[str, Any]]]:
        """
        更新记忆库
        
        Args:
            existing_cells: 现有记忆
            new_cells: 新记忆
        
        Returns:
            (更新后的记忆列表，操作日志)
        """
        updated_cells = existing_cells.copy()
        logs = []
        
        for new_cell in new_cells:
            # 查找是否有冲突/重复的记忆
            conflict_cell = self._find_conflict(updated_cells, new_cell)
            
            if conflict_cell:
                # 发现冲突，执行更新/合并
                action = self._resolve_conflict(conflict_cell, new_cell)
                
                if action == UpdateAction.UPDATE:
                    # 更新旧记忆
                    self._update_cell(conflict_cell, new_cell)
                    logs.append({
                        'action': 'update',
                        'cell_id': conflict_cell.id,
                        'reason': '新信息覆盖旧信息'
                    })
                
                elif action == UpdateAction.MERGE:
                    # 合并记忆
                    merged_cell = self._merge_cells(conflict_cell, new_cell)
                    idx = updated_cells.index(conflict_cell)
                    updated_cells[idx] = merged_cell
                    logs.append({
                        'action': 'merge',
                        'cell_id': merged_cell.id,
                        'reason': '合并相似记忆'
                    })
                
                elif action == UpdateAction.KEEP:
                    # 保留旧记忆，忽略新记忆
                    logs.append({
                        'action': 'keep_existing',
                        'cell_id': conflict_cell.id,
                        'reason': '旧记忆更重要'
                    })
            else:
                # 无冲突，直接添加
                updated_cells.append(new_cell)
                logs.append({
                    'action': 'add',
                    'cell_id': new_cell.id,
                    'reason': '新记忆'
                })
        
        return updated_cells, logs
    
    def _find_conflict(
        self,
        cells: List[MemCell],
        new_cell: MemCell
    ) -> Optional[MemCell]:
        """
        查找冲突的记忆
        
        Args:
            cells: 现有记忆列表
            new_cell: 新记忆
        
        Returns:
            冲突的记忆（如有）
        """
        for cell in cells:
            # 检查类型是否相同
            if cell.memory_type != new_cell.memory_type:
                continue
            
            # 检查内容相似度
            similarity = self._calculate_similarity(cell.content, new_cell.content)
            
            if similarity >= self.conflict_threshold:
                return cell
        
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 文本 1
            text2: 文本 2
        
        Returns:
            相似度 0-1
        """
        # 简化版：基于字符重叠
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = set1 & set2
        union = set1 | set2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _resolve_conflict(self, old_cell: MemCell, new_cell: MemCell) -> UpdateAction:
        """
        解决冲突
        
        Args:
            old_cell: 旧记忆
            new_cell: 新记忆
        
        Returns:
            更新操作类型
        """
        # 新记忆重要性更高 → 更新
        if new_cell.importance > old_cell.importance + 1:
            return UpdateAction.UPDATE
        
        # 旧记忆访问次数更多 → 保留
        if old_cell.access_count > new_cell.access_count * 2:
            return UpdateAction.KEEP
        
        # 否则合并
        return UpdateAction.MERGE
    
    def _update_cell(self, target: MemCell, source: MemCell):
        """
        更新记忆内容
        
        Args:
            target: 目标记忆
            source: 源记忆
        """
        target.content = source.content
        target.updated_at = datetime.now().isoformat()
        target.importance = max(target.importance, source.importance)
        
        # 合并标签
        target.tags = list(set(target.tags + source.tags))
        
        # 记录更新历史
        if 'update_history' not in target.metadata:
            target.metadata['update_history'] = []
        target.metadata['update_history'].append({
            'updated_at': target.updated_at,
            'old_content': target.content,
            'new_content': source.content
        })
    
    def _merge_cells(self, cell1: MemCell, cell2: MemCell) -> MemCell:
        """
        合并两个记忆
        
        Args:
            cell1: 记忆 1
            cell2: 记忆 2
        
        Returns:
            合并后的记忆
        """
        import uuid
        
        # 保留较新的记忆作为基础
        base_cell = cell1 if cell1.updated_at > cell2.updated_at else cell2
        other_cell = cell2 if base_cell == cell1 else cell1
        
        # 创建合并后的记忆
        merged = MemCell(
            id=f"mem_{uuid.uuid4().hex[:12]}",
            content=f"{base_cell.content}; {other_cell.content}",
            memory_type=base_cell.memory_type,
            source=base_cell.source,
            created_at=base_cell.created_at,
            updated_at=datetime.now().isoformat(),
            importance=max(base_cell.importance, other_cell.importance) + 1,
            access_count=base_cell.access_count + other_cell.access_count,
            tags=list(set(base_cell.tags + other_cell.tags)),
            metadata={
                'merged_from': [cell1.id, cell2.id],
                'merge_count': 2
            }
        )
        
        return merged


class MemoryForgetter:
    """记忆遗忘器 - 基于艾宾浩斯遗忘曲线"""
    
    def __init__(self, curve: ForgettingCurve = None):
        """
        初始化遗忘器
        
        Args:
            curve: 遗忘曲线参数
        """
        self.curve = curve or ForgettingCurve()
    
    def apply_forgetting(
        self,
        mem_cells: List[MemCell]
    ) -> Tuple[List[MemCell], List[MemCell], List[MemCell], List[MemCell]]:
        """
        应用遗忘曲线
        
        Args:
            mem_cells: 记忆列表
        
        Returns:
            (保留的记忆，更新的重要性，归档的记忆，删除的记忆)
        """
        keep_cells = []
        updated_cells = []
        archive_cells = []
        delete_cells = []
        
        now = datetime.now()
        
        for cell in mem_cells:
            # 计算保留率
            retention = self._calculate_retention(cell.created_at, now)
            
            # 计算有效重要性（考虑访问频率）
            effective_importance = self._calculate_effective_importance(cell, retention)
            
            # 判定操作
            if effective_importance >= self.curve.retention_threshold:
                # 保留
                keep_cells.append(cell)
                
                # 如果重要性变化，记录更新
                if effective_importance != cell.importance / 10.0:
                    cell.importance = round(effective_importance * 10)
                    updated_cells.append(cell)
            
            elif effective_importance >= self.curve.archive_threshold:
                # 归档
                cell.metadata['archived'] = True
                cell.metadata['archive_date'] = now.isoformat()
                archive_cells.append(cell)
            
            elif effective_importance >= self.curve.delete_threshold:
                # 标记删除（软删除）
                cell.metadata['pending_delete'] = True
                cell.metadata['delete_date'] = now.isoformat()
                archive_cells.append(cell)  # 先归档，等待确认
            
            else:
                # 直接删除
                delete_cells.append(cell)
        
        return keep_cells, updated_cells, archive_cells, delete_cells
    
    def _calculate_retention(self, created_at: str, now: datetime) -> float:
        """
        计算记忆保留率（基于艾宾浩斯遗忘曲线）
        
        Args:
            created_at: 创建时间
            now: 当前时间
        
        Returns:
            保留率 0-1
        """
        try:
            created_time = datetime.fromisoformat(created_at)
            days_elapsed = (now - created_time).days
            
            # 艾宾浩斯遗忘曲线：R = e^(-t/S)
            # S 是半衰期
            retention = math.exp(-days_elapsed / self.curve.half_life_days)
            
            return retention
        except Exception:
            return 0.5
    
    def _calculate_effective_importance(
        self,
        cell: MemCell,
        retention: float
    ) -> float:
        """
        计算有效重要性
        
        考虑因素：
        - 基础重要性
        - 访问频率（提升）
        - 时间衰减（降低）
        
        Args:
            cell: 记忆单元
            retention: 保留率
        
        Returns:
            有效重要性 0-1
        """
        # 基础重要性
        base_importance = cell.importance / 10.0
        
        # 访问频率加成
        access_bonus = min(cell.access_count * 0.05, 0.5)
        
        # 时间衰减
        time_decay = retention
        
        # 计算有效重要性
        effective = (base_importance * 0.5 + access_bonus + time_decay * 0.5)
        
        return min(effective, 1.0)
    
    def cleanup_old_memories(
        self,
        mem_cells: List[MemCell],
        days_threshold: int = 90
    ) -> List[MemCell]:
        """
        清理旧记忆
        
        Args:
            mem_cells: 记忆列表
            days_threshold: 天数阈值
        
        Returns:
            清理后的记忆列表
        """
        now = datetime.now()
        threshold_date = now - timedelta(days=days_threshold)
        
        cleaned_cells = []
        
        for cell in mem_cells:
            try:
                created_time = datetime.fromisoformat(cell.created_at)
                
                # 超过阈值且访问次数少 → 清理
                if created_time < threshold_date and cell.access_count < 3:
                    cell.metadata['cleanup_reason'] = '长期未访问'
                    cell.metadata['cleanup_date'] = now.isoformat()
                    continue  # 跳过，不添加到结果中
                
                cleaned_cells.append(cell)
            
            except Exception:
                # 时间解析失败，保留
                cleaned_cells.append(cell)
        
        return cleaned_cells


def test_updater_forgetter():
    """测试更新器和遗忘器"""
    from memory_extraction import MemoryExtractor
    
    print("=" * 60)
    print("弘脑记忆系统 - 记忆更新与遗忘模块测试")
    print("=" * 60)
    
    # 创建测试数据
    extractor = MemoryExtractor()
    
    # 现有记忆
    existing_text = """
    用户叫唐锋，在燧弘华创工作。
    用户喜欢简洁风格。
    """
    existing_cells = extractor.extract_from_text(existing_text, source="test")
    
    # 新记忆（部分冲突）
    new_text = """
    用户叫唐锋，职位是执行总裁。
    用户偏好简洁商务风格。
    用户讨厌复杂流程。
    """
    new_cells = extractor.extract_from_text(new_text, source="test")
    
    print(f"\n现有记忆：{len(existing_cells)} 条")
    print(f"新记忆：{len(new_cells)} 条\n")
    
    # 测试更新器
    updater = MemoryUpdater()
    updated_cells, logs = updater.update_memory(existing_cells, new_cells)
    
    print("=" * 60)
    print("更新操作日志")
    print("=" * 60)
    for log in logs:
        print(f"  [{log['action']}] {log['cell_id']}: {log['reason']}")
    
    print(f"\n更新后记忆：{len(updated_cells)} 条")
    
    # 测试遗忘器
    print("\n" + "=" * 60)
    print("遗忘曲线应用")
    print("=" * 60)
    
    forgetter = MemoryForgetter()
    keep, updated, archive, delete = forgetter.apply_forgetting(updated_cells)
    
    print(f"  保留：{len(keep)} 条")
    print(f"  更新重要性：{len(updated)} 条")
    print(f"  归档：{len(archive)} 条")
    print(f"  删除：{len(delete)} 条")
    
    # 测试清理
    print("\n" + "=" * 60)
    print("旧记忆清理")
    print("=" * 60)
    
    cleaned = forgetter.cleanup_old_memories(updated_cells, days_threshold=30)
    print(f"  清理前：{len(updated_cells)} 条")
    print(f"  清理后：{len(cleaned)} 条")
    print(f"  清理掉：{len(updated_cells) - len(cleaned)} 条")
    
    return updated_cells


if __name__ == '__main__':
    test_updater_forgetter()
