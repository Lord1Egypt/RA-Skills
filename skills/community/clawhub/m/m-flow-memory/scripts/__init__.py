"""
M-Flow Memory Client
封装 M-Flow 的 Python API，提供简洁的记忆管理接口
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# 添加 M-Flow 到路径
M_FLOW_PATH = Path(__file__).parent.parent.parent / "m_flow"
sys.path.insert(0, str(M_FLOW_PATH))

# 设置 HF_HUB_OFFLINE 环境变量
os.environ["HF_HUB_OFFLINE"] = os.environ.get("HF_HUB_OFFLINE", "1")


class MFlowMemory:
    """M-Flow 记忆客户端"""
    
    def __init__(
        self,
        m_flow_path: Optional[str] = None,
        log_level: str = "ERROR"
    ):
        """
        初始化 M-Flow 记忆客户端
        
        Args:
            m_flow_path: M-Flow 项目路径，默认从 skill 目录推断
            log_level: 日志级别
        """
        if m_flow_path:
            self.m_flow_path = Path(m_flow_path)
        else:
            # 从 skill 目录推断 m_flow 路径
            self.m_flow_path = Path(__file__).parent.parent.parent / "m_flow"
        
        # 导入 M-Flow
        import m_flow
        self.m_flow = m_flow
        
        # 设置日志
        from m_flow.shared.logging_utils import setup_logging
        setup_logging(log_level=log_level)
        
        # 导入搜索模式
        from m_flow.api.v1.search.search import RecallMode
        self.RecallMode = RecallMode
        
        # 缓存已添加的内容ID
        self._added_ids: List[str] = []
    
    async def add(self, content: str) -> Dict[str, Any]:
        """
        添加记忆内容
        
        Args:
            content: 要记忆的内容
            
        Returns:
            添加结果
        """
        result = await self.m_flow.add(content)
        return result
    
    async def memorize(self) -> Dict[str, Any]:
        """
        索引所有未处理的内容
        
        Returns:
            索引结果
        """
        result = await self.m_flow.memorize()
        return result
    
    async def search(
        self,
        query: str,
        mode: str = "episodic",
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索记忆
        
        Args:
            query: 查询文本
            mode: 搜索模式 ("lexical", "episodic", "triplet", "procedural")
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        # 映射模式名称到 RecallMode
        mode_map = {
            "lexical": self.RecallMode.CHUNKS_LEXICAL,
            "episodic": self.RecallMode.EPISODIC,
            "triplet": self.RecallMode.TRIPLET_COMPLETION,
            "procedural": self.RecallMode.PROCEDURAL,
            "cypher": self.RecallMode.CYPHER,
        }
        
        recall_mode = mode_map.get(mode.lower(), self.RecallMode.EPISODIC)
        
        results = await self.m_flow.search(query, recall_mode)
        return results
    
    async def distill(self, session_content: str) -> List[str]:
        """
        从会话内容中蒸馏知识要点
        
        使用 LLM 从会话中提取关键信息
        
        Args:
            session_content: 会话内容
            
        Returns:
            知识要点列表
        """
        # TODO: 实现 LLM 蒸馏逻辑
        # 暂时返回原始内容作为单个要点
        return [session_content]
    
    async def add_knowledge_points(
        self,
        points: List[str],
        source: str = "manual"
    ) -> None:
        """
        添加知识要点列表
        
        Args:
            points: 知识要点列表
            source: 来源标识
        """
        for point in points:
            content = f"[{source}] {point}"
            await self.add(content)
        
        await self.memorize()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "added_count": len(self._added_ids),
            "m_flow_path": str(self.m_flow_path),
        }


async def create_memory_client() -> MFlowMemory:
    """创建 M-Flow 记忆客户端"""
    return MFlowMemory()
