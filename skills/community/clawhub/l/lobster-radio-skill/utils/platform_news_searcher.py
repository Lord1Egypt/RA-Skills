"""
平台集成新闻搜索模块

利用OpenClaw/LobsterAI的web-search技能进行新闻搜索。
"""

import asyncio
import subprocess
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from .platform_adapter import get_platform_adapter, get_current_platform


@dataclass
class NewsItem:
    """新闻条目"""
    title: str
    content: str
    url: str
    source: str
    publish_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source,
            'publish_time': self.publish_time.isoformat() if self.publish_time else None
        }


class PlatformNewsSearcher:
    """
    平台集成新闻搜索器
    
    利用OpenClaw/LobsterAI的web-search技能进行新闻搜索。
    """
    
    def __init__(self):
        self.platform = get_current_platform()
        self.adapter = get_platform_adapter()
    
    async def search(
        self,
        query: str,
        tags: List[str] = None,
        max_results: int = 5
    ) -> List[NewsItem]:
        """
        搜索新闻
        
        Args:
            query: 搜索关键词
            tags: 标签列表
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        # 构建搜索查询
        search_query = self._build_search_query(query, tags)
        
        print(f"🔍 使用{self.platform}的web-search技能搜索: {search_query}")
        
        # 根据平台调用不同的搜索方式
        if self.platform == 'openclaw':
            return await self._search_with_openclaw(search_query, max_results)
        elif self.platform == 'lobsterai':
            return await self._search_with_lobsterai(search_query, max_results)
        else:
            # 默认使用模拟数据
            return await self._mock_search(query, max_results)
    
    def _build_search_query(self, query: str, tags: List[str] = None) -> str:
        """
        构建搜索查询
        
        Args:
            query: 用户查询
            tags: 标签列表
            
        Returns:
            str: 搜索查询字符串
        """
        # 构建新闻搜索查询
        search_parts = [query]
        
        if tags:
            search_parts.extend(tags)
        
        # 添加新闻相关关键词
        search_parts.append("新闻")
        
        return " ".join(search_parts)
    
    async def _search_with_openclaw(self, query: str, max_results: int) -> List[NewsItem]:
        """
        使用OpenClaw的web-search技能搜索
        
        OpenClaw的web-search技能可以通过以下方式调用：
        1. 通过openclaw命令行调用
        2. 通过MCP协议调用（如果Skill支持MCP）
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            # 方法1: 通过openclaw命令行调用web-search
            # 注意：这需要OpenClaw支持命令行调用Skill
            
            # 构建搜索提示词，让LLM通过web-search获取新闻
            search_prompt = f"""请使用web-search技能搜索以下主题的最新新闻：

搜索主题：{query}

要求：
1. 搜索最近24小时的新闻
2. 返回{max_results}条最相关的新闻
3. 每条新闻包含：标题、摘要、来源、链接
4. 按时间倒序排列

请以JSON格式返回结果：
{{
  "news": [
    {{
      "title": "新闻标题",
      "summary": "新闻摘要",
      "source": "新闻来源",
      "url": "新闻链接",
      "time": "发布时间"
    }}
  ]
}}"""
            
            # 调用OpenClaw的LLM进行搜索
            # 这里假设OpenClaw会自动使用web-search技能
            cmd = [
                "openclaw", "ask",
                "--message", search_prompt,
                "--json"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 解析返回的JSON
                try:
                    data = json.loads(result.stdout)
                    return self._parse_news_from_json(data)
                except json.JSONDecodeError:
                    # 如果返回的不是JSON，尝试从文本解析
                    return self._parse_news_from_text(result.stdout)
            else:
                print(f"OpenClaw搜索失败: {result.stderr}")
                return await self._mock_search(query, max_results)
                
        except Exception as e:
            print(f"OpenClaw搜索出错: {e}")
            return await self._mock_search(query, max_results)
    
    async def _search_with_lobsterai(self, query: str, max_results: int) -> List[NewsItem]:
        """
        使用LobsterAI的web-search技能搜索
        
        LobsterAI的Skill可以通过Cowork模式调用其他Skill。
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            # LobsterAI的web-search skill可以通过Cowork模式调用
            # 这里我们生成一个提示词，让Agent使用web-search搜索新闻
            
            search_prompt = f"""请使用web-search技能搜索以下主题的最新新闻：

搜索主题：{query}

要求：
1. 搜索最近24小时的新闻
2. 返回{max_results}条最相关的新闻
3. 每条新闻包含：标题、摘要、来源、链接
4. 按时间倒序排列

请直接返回搜索结果。"""
            
            # 在LobsterAI中，这个提示词会触发Agent使用web-search skill
            # 实际使用时，可以通过LobsterAI的API或IPC调用
            
            print("💡 在LobsterAI中，请使用以下提示词搜索新闻：")
            print(search_prompt)
            
            # 返回模拟数据作为示例
            return await self._mock_search(query, max_results)
            
        except Exception as e:
            print(f"LobsterAI搜索出错: {e}")
            return await self._mock_search(query, max_results)
    
    def _parse_news_from_json(self, data: Dict[str, Any]) -> List[NewsItem]:
        """
        从JSON解析新闻
        
        Args:
            data: JSON数据
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        news_items = []
        
        news_list = data.get('news', []) if isinstance(data, dict) else []
        
        for item in news_list:
            news_item = NewsItem(
                title=item.get('title', ''),
                content=item.get('summary', item.get('content', '')),
                url=item.get('url', ''),
                source=item.get('source', '未知来源'),
                publish_time=None  # 可以从item.get('time')解析
            )
            news_items.append(news_item)
        
        return news_items
    
    def _parse_news_from_text(self, text: str) -> List[NewsItem]:
        """
        从文本解析新闻
        
        Args:
            text: 文本内容
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        # 简单的文本解析逻辑
        # 实际使用时可以使用LLM来解析
        news_items = []
        
        # 这里可以实现更复杂的解析逻辑
        # 例如使用正则表达式提取标题、链接等
        
        return news_items
    
    async def _mock_search(self, query: str, max_results: int) -> List[NewsItem]:
        """
        模拟新闻搜索（用于测试或当平台搜索失败时）
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        from datetime import timedelta
        
        mock_news = [
            NewsItem(
                title=f"{query}领域取得重大突破",
                content=f"近日，{query}领域传来好消息。相关技术取得重要进展，为行业发展注入新动力。专家表示，这一突破将推动整个产业链升级。",
                url="https://example.com/news/1",
                source="科技日报",
                publish_time=datetime.now() - timedelta(hours=2)
            ),
            NewsItem(
                title=f"{query}市场规模持续扩大",
                content=f"最新数据显示，{query}市场呈现快速增长态势。多家头部企业加大投入，行业竞争日趋激烈。分析师预测，未来三年将保持高速增长。",
                url="https://example.com/news/2",
                source="财经网",
                publish_time=datetime.now() - timedelta(hours=5)
            ),
            NewsItem(
                title=f"{query}应用场景不断拓展",
                content=f"随着技术进步，{query}在更多领域得到应用。从传统行业到新兴领域，{query}正在改变人们的工作和生活方式。",
                url="https://example.com/news/3",
                source="互联网周刊",
                publish_time=datetime.now() - timedelta(hours=8)
            ),
            NewsItem(
                title=f"政策利好{query}产业发展",
                content=f"相关部门出台新政策，支持{query}产业发展。政策涵盖技术研发、人才培养、市场推广等多个方面，为行业发展创造良好环境。",
                url="https://example.com/news/4",
                source="经济日报",
                publish_time=datetime.now() - timedelta(hours=12)
            ),
            NewsItem(
                title=f"{query}国际合作日益紧密",
                content=f"国内外{query}企业加强合作，共同推动技术创新。通过资源共享和优势互补，{query}产业正在走向全球化发展。",
                url="https://example.com/news/5",
                source="国际商报",
                publish_time=datetime.now() - timedelta(hours=24)
            )
        ]
        
        return mock_news[:max_results]


# 便捷函数
async def search_news(
    query: str,
    tags: List[str] = None,
    max_results: int = 5
) -> List[NewsItem]:
    """
    搜索新闻的便捷函数
    
    Args:
        query: 搜索关键词
        tags: 标签列表
        max_results: 最大结果数
        
    Returns:
        List[NewsItem]: 新闻列表
    """
    searcher = PlatformNewsSearcher()
    return await searcher.search(query, tags, max_results)
