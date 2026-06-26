#!/usr/bin/env python3
"""
弘脑记忆系统 - 统一 API 接口
HongNao Memory OS - Unified API Interface

功能：提供统一的记忆系统 API，整合抽取、巩固、检索、更新功能
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from memory_extraction_v3 import MemCell, MemoryType, MemoryExtractor
from memory_consolidation import MemoryConsolidator, MemScene
from memory_retrieval import HybridRetriever, RetrievalResult
from memory_update import MemoryUpdater, MemoryForgetter, ForgettingCurve


@dataclass
class MemorySystemConfig:
    """记忆系统配置"""
    enable_extraction: bool = True
    enable_consolidation: bool = True
    enable_retrieval: bool = True
    enable_forgetting: bool = True
    retrieval_top_k: int = 10
    retrieval_min_score: float = 0.15  # 降低阈值
    forgetting_half_life_days: float = 30.0
    auto_cleanup_days: int = 90


class HongNaoMemorySystem:
    """弘脑记忆系统 - 主类"""
    
    def __init__(self, config: MemorySystemConfig = None):
        """
        初始化记忆系统
        
        Args:
            config: 系统配置
        """
        self.config = config or MemorySystemConfig()
        
        # 初始化各模块
        self.extractor = MemoryExtractor() if self.config.enable_extraction else None
        self.consolidator = MemoryConsolidator() if self.config.enable_consolidation else None
        self.retriever = None  # 延迟初始化
        self.updater = MemoryUpdater() if self.config.enable_forgetting else None
        self.forgetter = MemoryForgetter(
            ForgettingCurve(half_life_days=self.config.forgetting_half_life_days)
        ) if self.config.enable_forgetting else None
        
        # 记忆库
        self.mem_cells: List[MemCell] = []
        self.scenes: List[MemScene] = []
        
        # 统计信息
        self.stats = {
            'total_extractions': 0,
            'total_retrievals': 0,
            'total_updates': 0,
            'total_forgetting_ops': 0
        }
    
    def add_memories_from_text(self, text: str, source: str = "conversation") -> Dict[str, Any]:
        """
        从文本中添加记忆
        
        Args:
            text: 输入文本
            source: 来源标识
        
        Returns:
            操作结果
        """
        result = {
            'success': False,
            'extracted_count': 0,
            'consolidated_count': 0,
            'mem_cells': []
        }
        
        if not self.extractor:
            result['error'] = 'Extraction module disabled'
            return result
        
        # 步骤 1: 抽取记忆
        extracted_cells = self.extractor.extract_from_text(text, source)
        result['extracted_count'] = len(extracted_cells)
        
        # 步骤 2: 巩固记忆
        if self.consolidator:
            consolidated_cells = self.consolidator.consolidate(extracted_cells)
            result['consolidated_count'] = len(consolidated_cells)
            self.mem_cells.extend(consolidated_cells)
        else:
            self.mem_cells.extend(extracted_cells)
            result['consolidated_count'] = len(extracted_cells)
        
        # 步骤 3: 重新初始化检索器
        self._rebuild_retriever()
        
        # 更新统计
        self.stats['total_extractions'] += 1
        
        result['success'] = True
        result['mem_cells'] = [cell.to_dict() for cell in self.mem_cells]
        
        return result
    
    def retrieve_memories(
        self,
        query: str,
        top_k: int = None,
        min_score: float = None
    ) -> Dict[str, Any]:
        """
        检索记忆
        
        Args:
            query: 查询文本
            top_k: 返回数量（使用配置默认值）
            min_score: 最低分数（使用配置默认值）
        
        Returns:
            检索结果
        """
        result = {
            'success': False,
            'query': query,
            'results': [],
            'context': ''
        }
        
        if not self.retriever or len(self.mem_cells) == 0:
            result['error'] = 'Retriever not initialized or no memories'
            return result
        
        # 使用配置或传入参数
        top_k = top_k or self.config.retrieval_top_k
        min_score = min_score or self.config.retrieval_min_score
        
        # 执行检索
        retrieval_results = self.retriever.retrieve(query, top_k, min_score)
        
        # 格式化结果
        result['results'] = [r.to_dict() for r in retrieval_results]
        
        # 重建上下文
        if retrieval_results:
            result['context'] = self.retriever.rebuild_context(
                retrieval_results,
                max_tokens=1000
            )
        
        # 更新统计
        self.stats['total_retrievals'] += 1
        
        result['success'] = True
        result['count'] = len(retrieval_results)
        
        return result
    
    def update_memories(self, new_text: str, source: str = "conversation") -> Dict[str, Any]:
        """
        更新记忆（处理新信息）
        
        Args:
            new_text: 新文本
            source: 来源标识
        
        Returns:
            更新结果
        """
        result = {
            'success': False,
            'logs': []
        }
        
        if not self.extractor or not self.updater:
            result['error'] = 'Updater module disabled'
            return result
        
        # 抽取新记忆
        new_cells = self.extractor.extract_from_text(new_text, source)
        
        # 执行更新
        updated_cells, logs = self.updater.update_memory(self.mem_cells, new_cells)
        
        self.mem_cells = updated_cells
        result['logs'] = logs
        
        # 重新初始化检索器
        self._rebuild_retriever()
        
        # 更新统计
        self.stats['total_updates'] += 1
        
        result['success'] = True
        result['total_memories'] = len(self.mem_cells)
        
        return result
    
    def apply_forgetting(self) -> Dict[str, Any]:
        """
        应用遗忘曲线
        
        Returns:
            遗忘操作结果
        """
        result = {
            'success': False,
            'kept': 0,
            'updated': 0,
            'archived': 0,
            'deleted': 0
        }
        
        if not self.forgetter:
            result['error'] = 'Forgetter module disabled'
            return result
        
        # 应用遗忘
        keep, updated, archive, delete = self.forgetter.apply_forgetting(self.mem_cells)
        
        self.mem_cells = keep + archive  # 保留 + 归档，删除的移除
        
        result['kept'] = len(keep)
        result['updated'] = len(updated)
        result['archived'] = len(archive)
        result['deleted'] = len(delete)
        
        # 清理旧记忆
        cleaned = self.forgetter.cleanup_old_memories(self.mem_cells)
        result['cleaned'] = len(self.mem_cells) - len(cleaned)
        self.mem_cells = cleaned
        
        # 重新初始化检索器
        self._rebuild_retriever()
        
        # 更新统计
        self.stats['total_forgetting_ops'] += 1
        
        result['success'] = True
        result['total_memories'] = len(self.mem_cells)
        
        return result
    
    def create_scene(
        self,
        title: str,
        scene_type: str,
        query: str = None
    ) -> Dict[str, Any]:
        """
        创建记忆场景
        
        Args:
            title: 场景标题
            scene_type: 场景类型
            query: 用于筛选记忆的查询（可选）
        
        Returns:
            创建的场景
        """
        result = {
            'success': False,
            'scene': None
        }
        
        if not self.consolidator:
            result['error'] = 'Consolidator module disabled'
            return result
        
        # 如果有查询，先检索相关记忆
        if query:
            retrieval_result = self.retrieve_memories(query)
            if retrieval_result['success']:
                scene_cells = [
                    cell for cell in self.mem_cells
                    if any(r['mem_cell']['id'] == cell.id for r in retrieval_result['results'])
                ]
            else:
                scene_cells = self.mem_cells
        else:
            scene_cells = self.mem_cells
        
        # 创建场景
        scene = self.consolidator.create_scene(title, scene_type, scene_cells)
        self.scenes.append(scene)
        
        result['success'] = True
        result['scene'] = scene.to_dict()
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取系统统计信息
        
        Returns:
            统计信息
        """
        return {
            'total_memories': len(self.mem_cells),
            'total_scenes': len(self.scenes),
            'operations': self.stats.copy(),
            'memory_types': self._count_by_type()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """按类型统计记忆数量"""
        type_counts = {}
        for cell in self.mem_cells:
            type_counts[cell.memory_type] = type_counts.get(cell.memory_type, 0) + 1
        return type_counts
    
    def _rebuild_retriever(self):
        """重新初始化检索器"""
        if self.config.enable_retrieval and len(self.mem_cells) > 0:
            self.retriever = HybridRetriever(self.mem_cells)
        else:
            self.retriever = None
    
    def add_memory(self,
                   content: str,
                   cell_type: str = "fact",
                   tags: List[str] = None,
                   importance: float = 5.0,
                   source: str = "manual") -> Dict[str, Any]:
        """
        添加单条记忆
        
        Args:
            content: 记忆内容
            cell_type: 记忆类型 (fact/preference/skill/emotion/constraint)
            tags: 标签列表
            importance: 重要性评分 (1-10)
            source: 来源标识
        
        Returns:
            添加结果
        """
        result = {'success': False, 'cell_id': None}
        
        if not self.extractor:
            result['error'] = 'Extraction module disabled'
            return result
        
        try:
            mem_type = MemoryType(cell_type.lower())
        except ValueError:
            mem_type = MemoryType.FACT
        
        now = datetime.now().isoformat()
        cell = MemCell(
            id=str(uuid.uuid4())[:8],
            content=content,
            memory_type=mem_type.value,
            tags=tags or [],
            importance=int(importance),
            source=source,
            created_at=now,
            updated_at=now
        )
        
        self.mem_cells.append(cell)
        self._rebuild_retriever()
        
        result['success'] = True
        result['cell_id'] = cell.id
        result['cell'] = cell.to_dict()
        return result
    
    def create_scene(self,
                     title: str,
                     scene_type: str = "project") -> Dict[str, Any]:
        """
        创建记忆场景
        
        Args:
            title: 场景标题
            scene_type: 场景类型
        
        Returns:
            创建结果
        """
        now = datetime.now().isoformat()
        scene = MemScene(
            id=str(uuid.uuid4())[:8],
            title=title,
            scene_type=scene_type,
            memcell_ids=[],
            created_at=now,
            updated_at=now
        )
        
        self.scenes.append(scene)
        return {'success': True, 'scene_id': scene.id, 'scene': scene.to_dict()}
    
    def export_to_json(self) -> str:
        """
        导出记忆库为 JSON
        
        Returns:
            JSON 字符串
        """
        data = {
            'mem_cells': [cell.to_dict() for cell in self.mem_cells],
            'scenes': [scene.to_dict() for scene in self.scenes],
            'stats': self.get_stats(),
            'exported_at': datetime.now().isoformat()
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def import_from_json(self, json_str: str) -> Dict[str, Any]:
        """
        从 JSON 导入记忆库
        
        Args:
            json_str: JSON 字符串
        
        Returns:
            导入结果
        """
        result = {
            'success': False,
            'imported_memories': 0,
            'imported_scenes': 0
        }
        
        try:
            data = json.loads(json_str)
            
            # 导入记忆
            for cell_data in data.get('mem_cells', []):
                cell = MemCell.from_dict(cell_data)
                self.mem_cells.append(cell)
            
            result['imported_memories'] = len(data.get('mem_cells', []))
            
            # 导入场景
            for scene_data in data.get('scenes', []):
                scene = MemScene(**scene_data)
                self.scenes.append(scene)
            
            result['imported_scenes'] = len(data.get('scenes', []))
            
            # 重新初始化检索器
            self._rebuild_retriever()
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result


def test_memory_system():
    """测试完整的记忆系统"""
    print("=" * 60)
    print("弘脑记忆系统 - 完整系统测试")
    print("=" * 60)
    
    # 创建系统
    system = HongNaoMemorySystem()
    
    # 测试 1: 添加记忆
    print("\n【测试 1】添加记忆")
    print("-" * 60)
    
    text1 = """
    用户叫唐锋，在燧弘华创工作，职位是执行总裁。
    用户喜欢简洁商务风格，偏好使用 PPT 做演示。
    项目预算为 100 万元。
    必须保证数据安全。
    """
    
    result = system.add_memories_from_text(text1, source="test")
    print(f"抽取：{result['extracted_count']} 条")
    print(f"巩固后：{result['consolidated_count']} 条")
    print(f"总记忆数：{len(system.mem_cells)}")
    
    # 测试 2: 检索记忆
    print("\n【测试 2】检索记忆")
    print("-" * 60)
    
    query = "用户信息和偏好"
    result = system.retrieve_memories(query, top_k=3)
    print(f"查询：{query}")
    print(f"找到：{result['count']} 条")
    print(f"上下文:\n{result['context']}")
    
    # 测试 3: 更新记忆
    print("\n【测试 3】更新记忆")
    print("-" * 60)
    
    text2 = """
    用户职位是 CEO，偏好科技感风格。
    用户讨厌冗长的会议。
    """
    
    result = system.update_memories(text2)
    print(f"更新日志：{len(result['logs'])} 条")
    for log in result['logs'][:3]:
        print(f"  [{log['action']}] {log['reason']}")
    print(f"总记忆数：{result['total_memories']}")
    
    # 测试 4: 创建场景
    print("\n【测试 4】创建记忆场景")
    print("-" * 60)
    
    result = system.create_scene("燧弘华创项目", "project", query="燧弘华创")
    print(f"场景：{result['scene']['title']}")
    print(f"类型：{result['scene']['scene_type']}")
    print(f"包含记忆：{len(result['scene']['memcell_ids'])} 条")
    
    # 测试 5: 系统统计
    print("\n【测试 5】系统统计")
    print("-" * 60)
    
    stats = system.get_stats()
    print(f"总记忆数：{stats['total_memories']}")
    print(f"总场景数：{stats['total_scenes']}")
    print(f"抽取操作：{stats['operations']['total_extractions']}")
    print(f"检索操作：{stats['operations']['total_retrievals']}")
    print(f"更新操作：{stats['operations']['total_updates']}")
    print(f"记忆类型分布：{stats['memory_types']}")
    
    # 测试 6: 导出/导入
    print("\n【测试 6】导出/导入测试")
    print("-" * 60)
    
    json_str = system.export_to_json()
    print(f"导出 JSON 长度：{len(json_str)} 字符")
    
    # 创建新系统并导入
    system2 = HongNaoMemorySystem()
    result = system2.import_from_json(json_str)
    print(f"导入成功：{result['success']}")
    print(f"导入记忆：{result['imported_memories']} 条")
    print(f"导入场景：{result['imported_scenes']} 个")
    
    print("\n" + "=" * 60)
    print("✅ 弘脑记忆系统测试完成！")
    print("=" * 60)
    
    return system


if __name__ == '__main__':
    test_memory_system()
