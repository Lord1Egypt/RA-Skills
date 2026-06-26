"""
提示词引擎 - 参照 baoyu-skills 详细模板
"""

import random
from .types import Article, Section


# 完整的风格预设（参照 baoyu-skills/references/presets/）
STYLE_PRESETS = {
    "fresh": {
        "name": "fresh",
        "category": "natural",
        "colors": {
            "primary": "薄荷绿、天空蓝、淡黄色",
            "background": "纯白色、柔和薄荷绿",
            "accents": "叶绿色、水蓝色"
        },
        "visual_elements": "植物叶片、云朵、水滴，简单几何形状，呼吸感构图，开放构图",
        "typography": "干净轻盈的手写字体，透气间距，清新配色",
        "best_layouts": ["sparse", "balanced", "flow"],
        "best_for": "健康生活、极简主义、自然主题"
    },
    "warm": {
        "name": "warm",
        "category": "emotional",
        "colors": {
            "primary": "暖橙色、淡黄色、柔和粉色",
            "background": "米白色、暖奶油色",
            "accents": "珊瑚色、杏色"
        },
        "visual_elements": "柔和曲线、温馨装饰、心形元素、温暖光晕",
        "typography": "圆润温暖的手写字体，友好间距，暖色调",
        "best_layouts": ["sparse", "balanced"],
        "best_for": "情感故事、个人分享、温暖话题"
    },
    "notion": {
        "name": "notion",
        "category": "minimal",
        "colors": {
            "primary": "黑色、深灰色",
            "background": "纯白色、浅灰色",
            "accents": "淡蓝色、淡黄色、淡粉色"
        },
        "visual_elements": "简洁线条、手绘抖动效果、几何形状、 stick figures，最大空白，单一墨水线条",
        "typography": "干净手写字体，简单无衬线标签，最少装饰",
        "best_layouts": ["sparse", "balanced", "dense", "list", "comparison", "flow"],
        "best_for": "知识分享、概念解释、SaaS内容、效率技巧、技术教程"
    },
    "cute": {
        "name": "cute",
        "category": "playful",
        "colors": {
            "primary": "粉色、薄荷绿、淡紫色",
            "background": "纯白色、柔和奶油色",
            "accents": "糖果色、彩虹色"
        },
        "visual_elements": "卡通角色、圆角方块、波点、星星、泡泡、圆润形状",
        "typography": "圆润可爱字体，活泼间距，糖果配色",
        "best_layouts": ["sparse", "balanced", "list"],
        "best_for": "轻松趣味、可爱宠物、少女心"
    }
}

# 完整的布局预设（参照 baoyu-skills/references/elements/canvas.md）
LAYOUT_PRESETS = {
    "sparse": {
        "density": "低信息密度",
        "whitespace": "60-70%",
        "structure": "单个焦点居中，呼吸感构图",
        "best_for": "封面、引用、震撼声明"
    },
    "balanced": {
        "density": "中等信息密度",
        "whitespace": "40-50%",
        "structure": "顶部标题权重，内容均匀分布，清晰的视觉层次",
        "best_for": "标准内容、教程"
    },
    "dense": {
        "density": "高信息密度",
        "whitespace": "20-30%",
        "structure": "组织化的网格结构，清晰的分隔",
        "best_for": "知识卡片、 cheat sheets"
    },
    "list": {
        "density": "高密度",
        "whitespace": "20-30%",
        "structure": "左对齐项目，清晰的数字/圆点层次，一致的项目格式，垂直列表布局，明确的1、2、3、4数字序号",
        "best_for": "排名、检查清单、步骤指南"
    },
    "comparison": {
        "density": "中等密度",
        "whitespace": "30-40%",
        "structure": "左边一个内容块，右边一个内容块，中间用箭头或VS标记分隔",
        "best_for": "前后对比、优缺点"
    },
    "flow": {
        "density": "中等密度",
        "whitespace": "30-40%",
        "structure": "从左到右的水平流程，用箭头或连接线将节点连接",
        "best_for": "流程、时间线、工作流"
    }
}


class PromptEngine:
    """提示词引擎（参照 baoyu-skills）"""
    
    @staticmethod
    def generate_cover_prompt(article: Article, style: str) -> str:
        """
        生成封面图提示词（简化版）
        封面只显示文章标题，不需要章节要点
        """
        style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["fresh"])
        
        # 封面只显示标题，不显示章节
        # 重要：可以有装饰性图片元素，但不能有额外文字
        prompt = f"""Xiaohongshu cover, {style_preset['name']} style.
Title: {article['title']}
Colors: {style_preset['colors']['primary']}.
Visual elements: {style_preset['visual_elements']}.
Clean design, hand-drawn, big title text.

IMPORTANT: 
- The title should be the ONLY text on the image
- NO subtitle text
- NO additional labels or annotations
- YES to decorative visual elements (plants, shapes, patterns)
- The visual elements should enhance, not contain text"""
        
        return prompt
    
    @staticmethod
    def generate_illustration_prompt(article: Article, style: str, layout: str) -> str:
        """
        生成插图提示词
        参照 baoyu-skills：分离文字内容和视觉概念，引导用图标/符号代替文字
        """
        style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["fresh"])
        
        # 构建章节内容（作为视觉参考）
        items = []
        for i, section in enumerate(article["sections"], 1):
            content = section["content"].replace("\n", " ").strip()[:50]
            items.append(f"{i}. {section['title']}: {content}")
        
        content_text = " | ".join(items)
        
        prompt = f"""Xiaohongshu infographic, {style_preset['name']} style.

Article: {article['title']}

## Key Sections (use as visual reference)
{content_text}

## Visual Approach
- Use icons, symbols, and visual metaphors to represent each section
- For section titles: use simple hand-drawn lettering style
- Keep text minimal - let visuals tell the story

## Text Rendering (IMPORTANT)
- If you include any text, it must be simple hand-drawn style letters
- Avoid complex text rendering - prefer icons over words
- Title text should be clean, minimal, hand-drawn aesthetic

## Style
Colors: {style_preset['colors']['primary']}.
Visual elements: {style_preset['visual_elements']}.
Clean hand-drawn minimalist design."""
        
        return prompt
    
    @staticmethod
    def generate_decoration_prompt(section: Section, style: str) -> str:
        """
        生成配图提示词
        参照 baoyu-skills：强调用视觉符号代替文字
        """
        style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["fresh"])
        
        prompt = f"""Create a Xiaohongshu (Little Red Book) style illustration:

## Article Section
Title: {section['title']}
Theme: {section['content'][:100] if section.get('content') else 'general topic'}

## Visual Concept (for AI understanding)
- Interpret the section title and theme into visual symbols
- Use icons, metaphors, or abstract shapes to represent the concept
- Let the image tell the story without text

## Style
- Style: {style_preset['name']} hand-drawn
- Colors: {style_preset['colors']['primary']}
- Background: {style_preset['colors']['background']}
- Visual Elements: {style_preset['visual_elements']}

## Text Rendering (IMPORTANT)
- If you include any text, use simple hand-drawn lettering
- Prefer icons and symbols over words
- Clean, minimalist composition
- Hand-drawn aesthetic

Please generate a decorative illustration."""
        
        return prompt
    
    @staticmethod
    def select_random_sections(sections: list[Section], count: int) -> list[Section]:
        """随机选择章节"""
        if not sections:
            return []
        if len(sections) >= count:
            return random.sample(sections, count)
        else:
            return [sections[i % len(sections)] for i in range(count)]
