"""
内容生成器模块

负责调用LLM生成电台内容。
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RadioContent:
    """电台内容"""
    title: str
    summary: str
    content: str
    topics: List[str]
    tags: List[str]
    duration: float
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'topics': self.topics,
            'tags': self.tags,
            'duration': self.duration
        }


class ContentGenerator:
    """
    内容生成器
    
    负责调用OpenClaw的LLM生成电台内容。
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
        
        radio_template_path = self.template_dir / "radio_content.txt"
        if radio_template_path.exists():
            with open(radio_template_path, 'r', encoding='utf-8') as f:
                self.templates['radio'] = f.read()
        else:
            self.templates['radio'] = self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认模板"""
        return """你是一个专业的电台主持人，正在为用户生成个性化的资讯电台节目。

请根据以下要求生成电台内容：

**主题**: {{topics}}
**标签**: {{tags}}
**时长**: 约{{duration}}分钟

**要求**:
1. 内容要紧扣主题，提供有价值的信息
2. 语言要生动有趣，适合音频播报
3. 结构清晰，包含开场、主体内容和结尾
4. 避免使用过于专业的术语，保持通俗易懂
5. 添加适当的过渡语，让内容更流畅

**格式**:
```
【开场】
（问候语和主题介绍）

【主体内容】
（详细内容，分段呈现）

【结尾】
（总结和结束语）
```

请开始生成电台内容："""
    
    def parse_topics_and_tags(self, user_input: str) -> Dict[str, List[str]]:
        """
        解析用户输入的主题和标签
        
        Args:
            user_input: 用户输入
            
        Returns:
            Dict[str, List[str]]: 包含topics和tags的字典
        """
        topics = []
        tags = []
        
        topic_patterns = [
            r'关于(.+?)的',
            r'主题[是为](.+?)[，。]',
            r'(.+?)主题'
        ]
        
        for pattern in topic_patterns:
            matches = re.findall(pattern, user_input)
            topics.extend(matches)
        
        tag_keywords = {
            '科技': ['科技', '技术', 'AI', '人工智能', '互联网'],
            '财经': ['财经', '经济', '金融', '股市', '投资'],
            '体育': ['体育', '运动', '足球', '篮球'],
            '娱乐': ['娱乐', '明星', '电影', '音乐'],
            '国际': ['国际', '世界', '全球'],
            '国内': ['国内', '中国', '国家'],
            '教育': ['教育', '学习', '学校'],
            '健康': ['健康', '医疗', '养生'],
            '汽车': ['汽车', '车辆', '交通'],
            '房产': ['房产', '房子', '地产']
        }
        
        user_input_lower = user_input.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                tags.append(tag)
        
        if not topics and not tags:
            topics = [user_input.strip()]
        
        return {
            'topics': list(set(topics)),
            'tags': list(set(tags))
        }
    
    def generate_prompt(
        self,
        topics: List[str],
        tags: List[str],
        duration: int = 5
    ) -> str:
        """
        生成LLM提示词
        
        Args:
            topics: 主题列表
            tags: 标签列表
            duration: 时长（分钟）
            
        Returns:
            str: 提示词
        """
        template = self.templates['radio']
        
        prompt = template.replace('{{topics}}', '、'.join(topics))
        prompt = prompt.replace('{{tags}}', '、'.join(tags))
        prompt = prompt.replace('{{duration}}', str(duration))
        
        return prompt
    
    def parse_llm_response(self, response: str) -> RadioContent:
        """
        解析LLM响应
        
        Args:
            response: LLM响应文本
            
        Returns:
            RadioContent: 电台内容
        """
        title = "个性化电台"
        summary = ""
        content = response
        
        title_match = re.search(r'【标题】(.+?)\n', response)
        if title_match:
            title = title_match.group(1).strip()
        
        summary_match = re.search(r'【摘要】(.+?)\n', response)
        if summary_match:
            summary = summary_match.group(1).strip()
        else:
            paragraphs = response.split('\n\n')
            if paragraphs:
                summary = paragraphs[0][:100] + "..."
        
        # 过滤掉结构标记，保留自然内容
        content = re.sub(r'【标题】.+?\n', '', content)
        content = re.sub(r'【摘要】.+?\n', '', content)
        content = re.sub(r'【开场】\n?', '', content)
        content = re.sub(r'【主体内容】\n?', '', content)
        content = re.sub(r'【结尾】\n?', '', content)
        content = re.sub(r'【新闻\d+】', '', content)
        
        # 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()
        
        word_count = len(content.replace('\n', '').replace(' ', ''))
        duration = max(1, word_count / 200)
        
        return RadioContent(
            title=title,
            summary=summary,
            content=content,
            topics=[],
            tags=[],
            duration=duration
        )
    
    def generate(
        self,
        topics: List[str],
        tags: List[str],
        duration: int = 5
    ) -> RadioContent:
        """
        生成电台内容
        
        Args:
            topics: 主题列表
            tags: 标签列表
            duration: 时长（分钟）
            
        Returns:
            RadioContent: 电台内容
            
        Note:
            这是一个示例实现。实际使用时需要调用OpenClaw的LLM接口。
        """
        prompt = self.generate_prompt(topics, tags, duration)
        
        response = f"""【标题】{topics[0] if topics else '个性化电台'}资讯

【摘要】
今天为您带来{', '.join(topics if topics else ['资讯'])}相关的最新动态和深度解析。

【开场】
大家好，欢迎收听今天的龙虾电台。我是您的AI主播，今天我们要聊的是{', '.join(topics if topics else ['热门话题'])}。

【主体内容】
让我们先来看看今天的重点内容：

首先，在{topics[0] if topics else '科技'}领域，最近有很多令人兴奋的发展。人工智能技术正在快速进步，新的应用场景不断涌现。从智能助手到自动驾驶，AI正在改变我们的生活方式。

其次，让我们关注一下行业动态。各大科技公司都在加大研发投入，推动技术创新。这不仅带来了更多的就业机会，也为消费者提供了更好的产品和服务。

最后，我们来看看未来趋势。专家预测，未来几年{topics[0] if topics else '科技'}行业将继续保持高速增长，新的突破和发现将不断涌现。

【结尾】
以上就是今天的主要内容。感谢您的收听，我们下次节目再见！
"""
        
        radio_content = self.parse_llm_response(response)
        radio_content.topics = topics
        radio_content.tags = tags
        
        return radio_content
