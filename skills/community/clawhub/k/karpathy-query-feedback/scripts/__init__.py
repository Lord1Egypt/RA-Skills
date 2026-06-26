"""
Karpathy Query → Wiki 回流 Pipeline
Phase 1: 将查询结果回流到 wiki 层
"""

import os
import sys
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, TYPE_CHECKING

# 懒加载 MFlowMemory
_mflow_module = None

def _get_mflow_memory():
    """懒加载 MFlowMemory"""
    global _mflow_module
    if _mflow_module is None:
        skill_path = Path(__file__).parent.parent.parent
        mflow_skill_path = skill_path / "m-flow-memory"
        scripts_path = mflow_skill_path / "scripts"
        
        # 添加 m_flow 包路径
        m_flow_path = mflow_skill_path / "m_flow"
        if str(m_flow_path) not in sys.path:
            sys.path.insert(0, str(m_flow_path))
        
        # 添加 m-flow-memory 到路径以便导入 scripts
        if str(mflow_skill_path) not in sys.path:
            sys.path.insert(0, str(mflow_skill_path))
        
        # 使用 importlib 加载 scripts 模块
        spec = importlib.util.spec_from_file_location(
            "mflow_scripts",
            scripts_path / "__init__.py"
        )
        _mflow_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mflow_module)
    
    return _mflow_module.MFlowMemory


class WikiEntry:
    """Wiki 条目"""
    
    def __init__(
        self,
        source: str,
        content: str,
        tags: List[str],
        timestamp: Optional[str] = None,
        relevance_score: float = 0.0
    ):
        self.source = source
        self.content = content
        self.tags = tags
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d")
        self.relevance_score = relevance_score
    
    def to_markdown_row(self) -> str:
        """转换为 Markdown 表格行"""
        tags_str = ",".join(self.tags)
        return f"| {self.source} | {self.content} | {tags_str} | {self.timestamp} |"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "content": self.content,
            "tags": self.tags,
            "timestamp": self.timestamp,
            "relevance_score": self.relevance_score
        }


class QueryFeedbackPipeline:
    """
    Karpathy Query → Wiki 回流管道
    
    流程:
    1. 接收用户查询
    2. 使用 M-Flow 多模式搜索
    3. 格式化结果为 wiki 条目
    4. 保存到 wiki 层
    """
    
    def __init__(
        self,
        wiki_path: str = None,
        m_flow_memory=None  # 懒加载，不指定类型
    ):
        """
        初始化管道
        
        Args:
            wiki_path: wiki 存储路径
            m_flow_memory: MFlowMemory 实例（可选）
        """
        # 默认 wiki 路径
        if wiki_path is None:
            self.wiki_path = Path(__file__).parent.parent.parent / "knowledge" / "wiki"
        else:
            self.wiki_path = Path(wiki_path)
        
        # 初始化 M-Flow memory（懒加载）
        if m_flow_memory is None:
            MFlowMemory = _get_mflow_memory()
            self.memory = MFlowMemory(log_level="ERROR")
        else:
            self.memory = m_flow_memory
        
        # 确保 wiki 目录存在
        self.wiki_path.mkdir(parents=True, exist_ok=True)
    
    async def query(
        self,
        query_text: str,
        mode: str = "hybrid",
        top_k: int = 10
    ) -> List[WikiEntry]:
        """
        执行查询并返回 wiki 条目
        
        Args:
            query_text: 查询文本
            mode: 搜索模式 (lexical/episodic/triplet/hybrid)
            top_k: 返回结果数量
            
        Returns:
            Wiki 条目列表
        """
        results = []
        
        if mode == "hybrid":
            # 混合搜索：lexical + episodic
            modes = ["lexical", "episodic"]
        else:
            modes = [mode]
        
        all_content = set()
        
        for search_mode in modes:
            try:
                search_results = await self.memory.search(
                    query_text,
                    mode=search_mode,
                    top_k=top_k
                )
                
                # 解析搜索结果
                # M-Flow 返回格式: [{'search_result': [[{item}, ...], ...]}]
                if search_results and len(search_results) > 0:
                    for result_group in search_results:
                        search_result_list = result_group.get("search_result", [])
                        # search_result_list 是嵌套列表 [[items], [items], ...]
                        for inner_list in search_result_list:
                            for item in inner_list:
                                # 从 metadata.sentence_classifications 提取文本
                                classifications = item.get("metadata", {}).get("sentence_classifications", [])
                                for sent in classifications:
                                    content = sent.get("text", "")
                                    if content and content not in all_content:
                                        all_content.add(content)
                                        
                                        # 提取标签（简单策略：从内容中提取关键词）
                                        tags = self._extract_tags(content, query_text)
                                        
                                        entry = WikiEntry(
                                            source=f"query:{search_mode}",
                                            content=content,
                                            tags=tags,
                                            relevance_score=item.get("score", 0.0)
                                        )
                                        results.append(entry)
            except Exception as e:
                print(f"Search mode {search_mode} failed: {e}")
        
        # 去重（基于内容）
        seen = set()
        unique_results = []
        for entry in results:
            if entry.content not in seen:
                seen.add(entry.content)
                unique_results.append(entry)
        
        # 按相关性排序
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return unique_results[:top_k]
    
    def _extract_tags(self, content: str, query: str) -> List[str]:
        """从内容和查询中提取标签"""
        tags = []
        
        # 从查询中提取标签（简单实现）
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # 提取匹配的关键词
        for word in query_words:
            if len(word) > 3 and word in content_lower:
                tags.append(word)
        
        # 如果没有标签，使用默认标签
        if not tags:
            tags = ["general"]
        
        return tags[:5]  # 最多5个标签
    
    def format_as_wiki(
        self,
        entries: List[WikiEntry],
        include_header: bool = True
    ) -> str:
        """
        格式化为 wiki Markdown
        
        Args:
            entries: Wiki 条目列表
            include_header: 是否包含表头
            
        Returns:
            Markdown 格式字符串
        """
        lines = []
        
        if include_header:
            lines.append("| source | content | tags | timestamp |")
            lines.append("|--------|---------|------|-----------|")
        
        for entry in entries:
            lines.append(entry.to_markdown_row())
        
        return "\n".join(lines)
    
    async def save_to_wiki(
        self,
        entries: List[WikiEntry],
        filename: str = None
    ) -> str:
        """
        保存到 wiki 文件
        
        Args:
            entries: Wiki 条目列表
            filename: 文件名（默认使用日期）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"wiki-{date_str}.md"
        
        filepath = self.wiki_path / filename
        
        # 读取现有内容
        existing_content = ""
        if filepath.exists():
            existing_content = filepath.read_text(encoding="utf-8")
        
        # 格式化新条目
        new_entries_md = self.format_as_wiki(entries, include_header=False)
        
        # 追加到文件
        with open(filepath, "a", encoding="utf-8") as f:
            if not existing_content.strip():
                # 文件为空，写入表头
                f.write("| source | content | tags | timestamp |\n")
                f.write("|--------|---------|------|-----------|\n")
            f.write(new_entries_md)
            f.write("\n")
        
        return str(filepath)
    
    async def query_and_save(
        self,
        query_text: str,
        mode: str = "hybrid",
        top_k: int = 10
    ) -> Dict[str, Any]:
        """
        查询并保存的完整流程
        
        Args:
            query_text: 查询文本
            mode: 搜索模式
            top_k: 结果数量
            
        Returns:
            包含查询结果和保存路径的字典
        """
        # 执行查询
        entries = await self.query(query_text, mode=mode, top_k=top_k)
        
        # 保存到 wiki
        if entries:
            saved_path = await self.save_to_wiki(entries)
        else:
            saved_path = None
        
        return {
            "query": query_text,
            "mode": mode,
            "entries_count": len(entries),
            "entries": [e.to_dict() for e in entries],
            "saved_path": saved_path
        }


# CLI 入口
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Karpathy Query → Wiki 回流")
    parser.add_argument("query", help="查询文本")
    parser.add_argument("--mode", default="hybrid", 
                        choices=["lexical", "episodic", "triplet", "hybrid"])
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--format", default="markdown", 
                        choices=["markdown", "json"])
    
    args = parser.parse_args()
    
    # 创建管道
    pipeline = QueryFeedbackPipeline()
    
    # 执行查询
    result = await pipeline.query_and_save(
        args.query,
        mode=args.mode,
        top_k=args.top_k
    )
    
    # 输出结果
    if args.format == "json":
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"查询: {result['query']}")
        print(f"模式: {result['mode']}")
        print(f"结果数: {result['entries_count']}")
        if result['saved_path']:
            print(f"已保存到: {result['saved_path']}")
        print()
        print("=== Wiki 条目 ===")
        print(pipeline.format_as_wiki([WikiEntry(**e) for e in result['entries']]))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
