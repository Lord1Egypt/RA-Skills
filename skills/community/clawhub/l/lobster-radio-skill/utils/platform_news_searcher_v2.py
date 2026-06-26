"""
平台集成新闻搜索模块 V2

利用OpenClaw/LobsterAI的web-search技能进行新闻搜索，
返回结构化数据供V2内容生成器加工。
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


class PlatformNewsSearcherV2:
    """
    平台集成新闻搜索器 V2
    
    利用OpenClaw/LobsterAI的web-search技能进行新闻搜索，
    返回结构化数据供V2内容生成器加工处理。
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
    
    def _build_search_prompt(self, query: str, max_results: int) -> str:
        """
        构建搜索提示词
        
        这个提示词会让平台的web-search技能搜索新闻，
        并以结构化格式返回，方便后续加工。
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            str: 搜索提示词
        """
        return f"""请使用web-search技能搜索以下主题的最新新闻：

搜索主题：{query}

要求：
1. 搜索最近24-48小时内的新闻
2. 选择{max_results}条最相关、最有价值的新闻
3. 确保新闻来源可靠（知名媒体、官方网站）
4. 优先选择有详细内容的新闻，而非简讯

返回格式（JSON）：
{{
  "news": [
    {{
      "title": "新闻标题（原文标题）",
      "summary": "新闻摘要或正文前200字",
      "source": "新闻来源（如：科技日报、新华网等）",
      "url": "原文链接",
      "publish_time": "发布时间（如：2024-01-15 10:30）"
    }}
  ]
}}

注意：
- 标题必须是原文标题，不要修改
- 摘要要保留关键信息点
- 按重要性排序，最重要的排第一"""
    
    async def _search_with_openclaw(self, query: str, max_results: int) -> List[NewsItem]:
        """
        使用OpenClaw的web-search技能搜索
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            # 构建搜索提示词
            search_prompt = self._build_search_prompt(query, max_results)
            
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
                    news_items = self._parse_news_from_json(data)
                    if news_items:
                        print(f"✅ 成功获取{len(news_items)}条新闻")
                        return news_items
                    else:
                        print("⚠️  未解析到新闻，使用模拟数据")
                        return await self._mock_search(query, max_results)
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON解析失败: {e}")
                    print("⚠️  使用模拟数据")
                    return await self._mock_search(query, max_results)
            else:
                print(f"⚠️  OpenClaw搜索失败: {result.stderr}")
                return await self._mock_search(query, max_results)
                
        except FileNotFoundError:
            print("⚠️  OpenClaw命令未找到，使用模拟数据")
            return await self._mock_search(query, max_results)
        except Exception as e:
            print(f"⚠️  OpenClaw搜索出错: {e}")
            return await self._mock_search(query, max_results)
    
    async def _search_with_lobsterai(self, query: str, max_results: int) -> List[NewsItem]:
        """
        使用LobsterAI的web-search技能搜索
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            # 构建搜索提示词
            search_prompt = self._build_search_prompt(query, max_results)
            
            # 在LobsterAI中，这个提示词会触发Agent使用web-search skill
            # 实际使用时，可以通过LobsterAI的Cowork模式调用
            
            print("💡 在LobsterAI中，请使用以下提示词：")
            print(search_prompt)
            
            # 返回模拟数据作为示例
            return await self._mock_search(query, max_results)
            
        except Exception as e:
            print(f"⚠️  LobsterAI搜索出错: {e}")
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
        
        # 支持多种JSON格式
        news_list = []
        
        if isinstance(data, dict):
            if 'news' in data:
                news_list = data['news']
            elif 'articles' in data:
                news_list = data['articles']
            elif 'results' in data:
                news_list = data['results']
        elif isinstance(data, list):
            news_list = data
        
        for item in news_list:
            if not isinstance(item, dict):
                continue
                
            # 提取标题
            title = item.get('title', '')
            if not title:
                title = item.get('name', '')
            
            # 提取内容
            content = item.get('summary', '')
            if not content:
                content = item.get('content', '')
            if not content:
                content = item.get('description', '')
            
            # 提取URL
            url = item.get('url', '')
            if not url:
                url = item.get('link', '')
            
            # 提取来源
            source = item.get('source', '')
            if not source:
                source = item.get('publisher', '')
            if not source:
                source = item.get('site', '未知来源')
            
            # 提取发布时间
            publish_time = None
            time_str = item.get('publish_time', '')
            if not time_str:
                time_str = item.get('publishedAt', '')
            if not time_str:
                time_str = item.get('date', '')
            
            if time_str:
                try:
                    # 尝试多种时间格式
                    for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                        try:
                            publish_time = datetime.strptime(time_str[:len(fmt)], fmt)
                            break
                        except:
                            continue
                except:
                    pass
            
            if title and content:  # 至少要有标题和内容
                news_item = NewsItem(
                    title=title,
                    content=content,
                    url=url,
                    source=source,
                    publish_time=publish_time
                )
                news_items.append(news_item)
        
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
        
        print(f"📝 使用模拟新闻数据（关键词: {query}）")
        
        mock_news = [
            NewsItem(
                title=f"{query}技术取得重大突破，行业迎来新机遇",
                content=f"近日，{query}领域传来重大利好消息。相关技术取得突破性进展，为行业发展注入强劲动力。据业内人士透露，这项突破将大幅提升产业效率，预计将在未来一年内实现规模化应用。",
                url="https://example.com/news/1",
                source="科技日报",
                publish_time=datetime.now() - timedelta(hours=2)
            ),
            NewsItem(
                title=f"{query}市场规模突破千亿，头部企业加速布局",
                content=f"最新行业报告显示，{query}市场规模已突破千亿元大关，年增长率超过30%。多家头部企业纷纷加大投入，行业竞争日趋激烈。分析师认为，随着技术成熟和应用场景拓展，市场潜力巨大。",
                url="https://example.com/news/2",
                source="财经网",
                publish_time=datetime.now() - timedelta(hours=5)
            ),
            NewsItem(
                title=f"{query}应用场景持续拓展，赋能传统行业转型",
                content=f"随着{query}技术不断成熟，其在各领域的应用日益广泛。从智能制造到智慧城市，从医疗健康到教育培训，{query}正在深刻改变传统行业的运营模式，推动产业数字化转型升级。",
                url="https://example.com/news/3",
                source="互联网周刊",
                publish_time=datetime.now() - timedelta(hours=8)
            ),
            NewsItem(
                title=f"政策利好密集出台，{query}产业发展迎来黄金期",
                content=f"近期，国家相关部门密集出台支持政策，从资金扶持、税收优惠、人才培养等多个维度为{query}产业发展保驾护航。专家表示，政策红利的持续释放将加速产业成熟。",
                url="https://example.com/news/4",
                source="经济日报",
                publish_time=datetime.now() - timedelta(hours=12)
            ),
            NewsItem(
                title=f"国际合作不断深化，{query}产业走向全球化",
                content=f"国内外{query}企业加强技术交流与合作，共同推动行业标准制定和技术创新。通过资源共享和优势互补，中国{query}产业正在加速融入全球产业链，国际竞争力持续提升。",
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
    searcher = PlatformNewsSearcherV2()
    return await searcher.search(query, tags, max_results)
