"""
内容生成器模块 V2

基于新闻搜索 + LLM处理的内容生成方案。
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RadioSegment:
    """电台片段"""
    title: str  # 8-20字标题
    content: str  # 200字以内文稿
    source: str  # 新闻来源
    url: str  # 原文链接
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'url': self.url
        }


@dataclass
class RadioContentV2:
    """电台内容 V2"""
    main_title: str  # 主标题
    summary: str  # 摘要
    segments: List[RadioSegment]  # 多个播报片段
    topics: List[str]
    tags: List[str]
    total_duration: float  # 总时长（分钟）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'main_title': self.main_title,
            'summary': self.summary,
            'segments': [s.to_dict() for s in self.segments],
            'topics': self.topics,
            'tags': self.tags,
            'total_duration': self.total_duration,
            'segment_count': len(self.segments)
        }
    
    def get_full_script(self, include_markers: bool = False) -> str:
        """
        获取完整播报文稿
        
        Args:
            include_markers: 是否包含【开场】等结构标记，默认False为自然流畅版本
            
        Returns:
            str: 播报文稿
        """
        if include_markers:
            # 带标记的版本（用于调试或特殊需求）
            script_parts = [
                f"【{self.main_title}】",
                "",
                "【开场】",
                f"欢迎收听今天的龙虾电台。今天为您带来{', '.join(self.topics)}相关资讯。",
                ""
            ]
            
            for i, segment in enumerate(self.segments, 1):
                script_parts.extend([
                    f"【新闻{i}】{segment.title}",
                    "",
                    segment.content,
                    "",
                    f"来源：{segment.source}",
                    ""
                ])
            
            script_parts.extend([
                "【结尾】",
                "以上就是今天的主要内容。感谢您的收听，我们下次节目再见！"
            ])
            
            return "\n".join(script_parts)
        else:
            # 自然流畅版本（默认）
            script_parts = [
                f"{self.main_title}",
                "",
                f"欢迎收听今天的龙虾电台。今天为您带来{', '.join(self.topics)}相关资讯。",
                ""
            ]
            
            for i, segment in enumerate(self.segments, 1):
                script_parts.extend([
                    f"第{i}条新闻：{segment.title}",
                    "",
                    segment.content,
                    ""
                ])
            
            script_parts.extend([
                "以上就是今天的主要内容。感谢您的收听，我们下次节目再见！"
            ])
            
            return "\n".join(script_parts)


class ContentGeneratorV2:
    """
    内容生成器 V2
    
    基于新闻搜索 + LLM处理的内容生成方案。
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        初始化内容生成器
        
        Args:
            template_dir: 提示词模板目录
        """
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates" / "prompts"
        
        self.template_dir = template_dir
        self._load_templates()
    
    def _load_templates(self):
        """加载提示词模板"""
        self.templates = {}
        
        # 标题生成模板
        self.templates['title'] = """你是一个专业的电台编辑，请为以下新闻生成一个吸引人的标题。

**要求**:
1. 标题长度必须在8-20字之间
2. 标题要简洁有力，吸引听众
3. 标题要准确概括新闻核心内容
4. 避免使用过于夸张的词汇

**新闻内容**:
{content}

**原标题**: {original_title}

请直接输出标题（8-20字），不要添加任何其他内容："""

        # 文稿生成模板
        self.templates['script'] = """你是一个专业的电台主持人，请将以下新闻改写成适合播报的文稿。

**要求**:
1. 文稿长度必须在200字以内
2. 语言要口语化，适合听觉传播
3. 保留新闻的核心信息点
4. 添加适当的过渡语，让内容更流畅
5. 避免使用专业术语，保持通俗易懂

**新闻标题**: {title}
**新闻内容**: {content}
**新闻来源**: {source}

请直接输出播报文稿（200字以内），不要添加任何其他内容："""

        # 开场白模板
        self.templates['opening'] = """请为以下主题的电台节目生成一个开场白。

**主题**: {topics}
**标签**: {tags}
**新闻条数**: {count}条

**要求**:
1. 开场白要亲切自然，吸引听众
2. 简要介绍今天的节目内容
3. 控制在50字以内
4. 适合音频播报

请直接输出开场白："""

        # 主标题生成模板
        self.templates['main_title'] = """请为以下主题的电台节目生成一个主标题。

**主题**: {topics}
**标签**: {tags}
**新闻条数**: {count}条

**要求**:
1. 标题长度在10-15字之间
2. 标题要有吸引力
3. 概括节目核心内容

请直接输出主标题："""

    def generate_title(self, news_title: str, news_content: str) -> str:
        """
        生成8-20字的标题
        
        智能提取原标题的核心信息，生成符合长度要求的标题。
        
        Args:
            news_title: 原标题
            news_content: 新闻内容
            
        Returns:
            str: 8-20字的标题
        """
        import re
        
        # 清理原标题，移除搜索关键词重复部分
        title = news_title.strip()
        
        # 移除常见的搜索关键词重复（如"人工智能 科技 新闻"）
        noise_words = ['人工智能', '科技', '新闻', '最新', '今日', '热点']
        for word in noise_words:
            # 如果标题以这些词开头或包含重复，尝试清理
            title = re.sub(rf'^\s*{word}\s+', '', title)
        
        # 提取核心主题词
        # 寻找"取得"、"突破"、"发布"等关键词前的内容
        core_match = re.search(r'(.+?)(?:取得|实现|发布|推出|突破|迎来|加速)', title)
        if core_match:
            core_topic = core_match.group(1).strip()
            # 如果核心主题合适，使用它
            if 8 <= len(core_topic) <= 20:
                return core_topic
        
        # 寻找逗号、顿号分隔的第一部分
        if '，' in title:
            first_part = title.split('，')[0].strip()
            if 8 <= len(first_part) <= 20:
                return first_part
        
        if '、' in title:
            first_part = title.split('、')[0].strip()
            if 8 <= len(first_part) <= 20:
                return first_part
        
        # 如果原标题太长，智能截断
        if len(title) > 20:
            # 尝试在合适的位置截断（避免截断在词中间）
            # 优先在"，"、"、"、"的"等位置截断
            for sep in ['，', '、', '的', '和', '与']:
                pos = title.rfind(sep, 8, 20)
                if pos > 8:
                    return title[:pos]
            
            # 如果找不到合适位置，直接截断到18字加省略号
            return title[:18] + "..."
        
        # 如果原标题太短，补充内容
        if len(title) < 8:
            # 从内容中提取关键词补充
            content_keywords = ['突破', '进展', '动态', '发展', '机遇']
            for keyword in content_keywords:
                if keyword in news_content:
                    extended = f"{title}{keyword}"
                    if len(extended) >= 8:
                        return extended
            
            # 如果还是不够，添加通用后缀
            suffixes = ['新进展', '新突破', '新动态', '新机遇']
            for suffix in suffixes:
                if len(title) + len(suffix) <= 20:
                    return title + suffix
        
        return title
    
    def generate_script(self, title: str, content: str, source: str) -> str:
        """
        生成200字以内的播报文稿
        
        Args:
            title: 新闻标题
            content: 新闻内容
            source: 新闻来源
            
        Returns:
            str: 200字以内的文稿
        """
        # 实际使用时调用LLM
        # 这里使用简化逻辑
        
        # 提取核心内容
        script = content[:80] if len(content) > 80 else content
        
        # 添加过渡语
        transitions = ["据了解，", "最新消息显示，", "相关报道指出，"]
        import random
        transition = random.choice(transitions)
        
        script = f"{transition}{script}"
        
        # 确保长度在200字以内
        if len(script) > 200:
            script = script[:197] + "..."
        
        return script
    
    def generate_main_title(self, topics: List[str], tags: List[str], count: int) -> str:
        """
        生成主标题
        
        Args:
            topics: 主题列表
            tags: 标签列表
            count: 新闻条数
            
        Returns:
            str: 主标题
        """
        topic_str = topics[0] if topics else "资讯"
        tag_str = tags[0] if tags else "热点"
        
        templates = [
            f"{topic_str}{tag_str}播报",
            f"今日{topic_str}要闻",
            f"{topic_str}最新动态",
            f"{tag_str}新闻速递"
        ]
        
        import random
        return random.choice(templates)
    
    def generate_opening(self, topics: List[str], tags: List[str], count: int) -> str:
        """
        生成开场白
        
        Args:
            topics: 主题列表
            tags: 标签列表
            count: 新闻条数
            
        Returns:
            str: 开场白
        """
        topic_str = "、".join(topics) if topics else "热点"
        
        templates = [
            f"欢迎收听龙虾电台。今天为您带来{count}条{topic_str}相关资讯。",
            f"大家好，这里是龙虾电台。接下来为您播报{topic_str}领域的最新动态。",
            f"欢迎收听今天的{topic_str}资讯播报，共{count}条新闻。"
        ]
        
        import random
        return random.choice(templates)
    
    async def generate_from_news(
        self,
        news_items: List[Dict[str, Any]],
        topics: List[str],
        tags: List[str]
    ) -> RadioContentV2:
        """
        从新闻生成电台内容
        
        Args:
            news_items: 新闻列表
            topics: 主题列表
            tags: 标签列表
            
        Returns:
            RadioContentV2: 电台内容
        """
        segments = []
        
        for news in news_items:
            # 生成8-20字的标题
            title = self.generate_title(
                news.get('title', ''),
                news.get('content', '')
            )
            
            # 生成200字以内的文稿
            content = self.generate_script(
                news.get('title', ''),
                news.get('content', ''),
                news.get('source', '未知来源')
            )
            
            segment = RadioSegment(
                title=title,
                content=content,
                source=news.get('source', '未知来源'),
                url=news.get('url', '')
            )
            
            segments.append(segment)
        
        # 生成主标题
        main_title = self.generate_main_title(topics, tags, len(segments))
        
        # 生成摘要
        summary = f"本期节目为您带来{len(segments)}条{topics[0] if topics else '热点'}资讯"
        
        # 计算总时长（每条约30秒）
        total_duration = len(segments) * 0.5 + 1  # 加上开场和结尾
        
        return RadioContentV2(
            main_title=main_title,
            summary=summary,
            segments=segments,
            topics=topics,
            tags=tags,
            total_duration=total_duration
        )
    
    async def generate(
        self,
        topics: List[str],
        tags: List[str],
        news_items: Optional[List[Dict[str, Any]]] = None,
        max_segments: int = 5,
        use_platform_search: bool = True
    ) -> RadioContentV2:
        """
        生成电台内容
        
        流程：
        1. 使用平台web-search技能搜索新闻（或用户提供新闻）
        2. 使用LLM加工生成8-20字标题
        3. 使用LLM加工生成200字以内文稿
        4. 组合多条内容
        
        Args:
            topics: 主题列表
            tags: 标签列表
            news_items: 新闻列表（可选，不提供则自动搜索）
            max_segments: 最大片段数
            use_platform_search: 是否使用平台的web-search技能
            
        Returns:
            RadioContentV2: 电台内容
        """
        # 如果没有提供新闻，使用平台web-search技能搜索
        if not news_items:
            if use_platform_search:
                # 使用平台集成的web-search技能（推荐）
                from .platform_news_searcher_v2 import search_news
                
                query = topics[0] if topics else "热点"
                print(f"🔍 使用平台web-search技能搜索新闻: {query}")
                news_list = await search_news(query, tags, max_segments)
                news_items = [n.to_dict() for n in news_list]
            else:
                # 使用独立的新闻搜索（需要API Key）
                from .news_searcher import NewsSearcher
                
                async with NewsSearcher() as searcher:
                    query = topics[0] if topics else "热点"
                    news_list = await searcher.search(query, tags, max_segments)
                    news_items = [n.to_dict() for n in news_list]
        
        # 使用V2方案加工新闻内容
        return await self.generate_from_news(news_items, topics, tags)
