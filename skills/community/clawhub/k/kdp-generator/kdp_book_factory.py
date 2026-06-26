# KDP Book Factory - 低内容书籍自动化工厂
# 专为亚马逊KDP设计，支持日记本、计划本、练习册等多种类型
# 版本: v2.0 - 可进化架构

import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

# ============ 配置区域 ============
VERSION = "2.0.0"
AUTHOR = "Luna & Boss"
DEFAULT_PAGE_SIZE = (6, 9)  # 英寸
DEFAULT_PAGE_COUNT = 108
DEFAULT_PAPER_COLOR = "#FFFEF5"  # Cream护眼纸

# ============ 书籍类型定义 ============
class BookType(Enum):
    GUIDED_JOURNAL = "引导日记"      # 每日引导问题
    DAILY_PLANNER = "每日计划本"      # 日程安排
    WORKBOOK = "练习册"              # 互动练习
    LOG_BOOK = "记录本"              # 追踪记录
    GRATITUDE_JOURNAL = "感恩日记"   # 感恩主题
    ACTIVITY_BOOK = "活动书"         # 儿童/成人活动
    NOTEBOOK = "笔记本"              # 简单横线/点阵

# ============ 书籍规格模板 ============
BOOK_TEMPLATES = {
    BookType.GUIDED_JOURNAL: {
        "name": "90天引导日记",
        "pages": 108,
        "sections": [
            {"name": "前言", "pages": 3},
            {"name": "目标设定", "pages": 2},
            {"name": "每日日志", "pages": 90, "repeat": True},
            {"name": "周复盘", "pages": 12},
            {"name": "月度总结", "pages": 1}
        ],
        "daily_prompts": [
            "今天最重要的3件事是什么？",
            "我取得了什么进展？",
            "明天我要改进什么？",
            "今天的感悟："
        ]
    },
    BookType.DAILY_PLANNER: {
        "name": "每日计划本",
        "pages": 120,
        "sections": [
            {"name": "年度计划", "pages": 12},
            {"name": "月度规划", "pages": 24},
            {"name": "每日计划", "pages": 90, "repeat": True}
        ],
        "fields": ["日期", "优先事项", "待办清单", "会议", "备注"]
    },
    BookType.GRATITUDE_JOURNAL: {
        "name": "感恩日记",
        "pages": 100,
        "sections": [
            {"name": "前言", "pages": 2},
            {"name": "每日感恩", "pages": 90, "repeat": True},
            {"name": "月度回顾", "pages": 8}
        ],
        "prompts": [
            "今天我感恩的3件事：",
            "今天最好的时刻是：",
            "我想对____说声谢谢："
        ]
    }
}

# ============ 封面风格模板 ============
COVER_STYLES = {
    "minimalist": {
        "name": "极简商务",
        "prompt": "minimalist book cover, clean lines, professional, {theme}, elegant typography space, monochrome with accent color, suitable for 6x9 inch book",
        "best_for": [BookType.GUIDED_JOURNAL, BookType.DAILY_PLANNER]
    },
    "watercolor": {
        "name": "水彩艺术",
        "prompt": "watercolor book cover, soft artistic style, {theme}, pastel colors, gentle brush strokes, dreamy atmosphere, 6x9 book format",
        "best_for": [BookType.GRATITUDE_JOURNAL, BookType.NOTEBOOK]
    },
    "geometric": {
        "name": "几何抽象",
        "prompt": "abstract geometric book cover, modern patterns, bold shapes, {theme}, vibrant gradients, contemporary design, 6x9 format",
        "best_for": [BookType.WORKBOOK, BookType.ACTIVITY_BOOK]
    },
    "photographic": {
        "name": "摄影写实",
        "prompt": "photographic book cover, realistic high-quality image, {theme}, natural lighting, professional composition, 6x9 book",
        "best_for": [BookType.LOG_BOOK]
    }
}

# ============ KDP关键词库 ============
KEYWORD_DATABASE = {
    "entrepreneur": [
        "entrepreneur journal", "business planner", "productivity workbook",
        "daily journal for entrepreneurs", "90 day planner", "startup workbook",
        "business owner journal", "entrepreneurship guide", "success planner"
    ],
    "gratitude": [
        "gratitude journal", "thankfulness diary", "daily gratitude",
        "mindfulness journal", "positivity workbook", "happiness planner"
    ],
    "productivity": [
        "productivity planner", "time management", "daily planner",
        "goal setting journal", "habit tracker", "focus workbook"
    ]
}

# ============ 核心类定义 ============
@dataclass
class BookConfig:
    """书籍配置"""
    title: str
    subtitle: str
    book_type: BookType
    page_size: tuple = DEFAULT_PAGE_SIZE
    page_count: int = DEFAULT_PAGE_COUNT
    paper_color: str = DEFAULT_PAPER_COLOR
    cover_style: str = "minimalist"
    target_audience: str = ""
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

class KDPBookFactory:
    """KDP书籍工厂 - 核心类"""
    
    def __init__(self, output_dir: str = "./books"):
        self.output_dir = output_dir
        self.version = VERSION
        self.created_books = []
        
    def create_book(self, config: BookConfig) -> Dict:
        """创建完整书籍"""
        print(f"🚀 开始生成书籍: {config.title}")
        print(f"📐 规格: {config.page_size[0]}x{config.page_size[1]}英寸, {config.page_count}页")
        
        book_id = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 1. 生成内页结构
        interior_plan = self._plan_interior(config)
        
        # 2. 生成封面Prompt
        cover_prompt = self._generate_cover_prompt(config)
        
        # 3. 生成KDP元数据
        metadata = self._generate_metadata(config)
        
        # 4. 组装结果
        book_package = {
            "id": book_id,
            "config": config,
            "interior_plan": interior_plan,
            "cover_prompt": cover_prompt,
            "metadata": metadata,
            "files_to_generate": [
                f"{book_id}_interior.pdf",
                f"{book_id}_cover.pdf", 
                f"{book_id}_metadata.json"
            ]
        }
        
        self.created_books.append(book_package)
        return book_package
    
    def _plan_interior(self, config: BookConfig) -> Dict:
        """规划内页结构"""
        template = BOOK_TEMPLATES.get(config.book_type, BOOK_TEMPLATES[BookType.GUIDED_JOURNAL])
        
        pages = []
        current_page = 1
        
        for section in template.get("sections", []):
            section_pages = section.get("pages", 1)
            repeat = section.get("repeat", False)
            
            if repeat:
                # 重复页面（如每日日志）
                for i in range(section_pages):
                    pages.append({
                        "page": current_page + i,
                        "section": section["name"],
                        "day": i + 1,
                        "template": "daily_log"
                    })
            else:
                # 独立页面
                for i in range(section_pages):
                    pages.append({
                        "page": current_page + i,
                        "section": section["name"],
                        "template": f"{section['name'].lower()}_page"
                    })
            
            current_page += section_pages
        
        return {
            "total_pages": len(pages),
            "paper_color": config.paper_color,
            "page_plan": pages
        }
    
    def _generate_cover_prompt(self, config: BookConfig) -> str:
        """生成AI封面绘画Prompt"""
        style = COVER_STYLES.get(config.cover_style, COVER_STYLES["minimalist"])
        
        # 根据书籍类型选择主题关键词
        theme_keywords = {
            BookType.GUIDED_JOURNAL: "rising sun, compass, mountain path, success journey",
            BookType.DAILY_PLANNER: "organized desk, calendar, clock, productivity",
            BookType.GRATITUDE_JOURNAL: "warm sunrise, flowers, heart, thankfulness",
            BookType.WORKBOOK: "open book, pencil, lightbulb, learning"
        }
        
        theme = theme_keywords.get(config.book_type, "professional business theme")
        
        prompt = style["prompt"].format(theme=theme)
        
        # 添加Midjourney参数
        mj_prompt = f"""{prompt}
Book title: "{config.title}"
Professional book cover design, high resolution, print-ready quality,
space for title and subtitle text, centered composition,
--ar 2:3 --v 6 --style raw --s 250

Negative: text, watermark, signature, low quality, blurry"""
        
        return {
            "base": prompt,
            "midjourney": mj_prompt,
            "style": config.cover_style,
            "recommendation": f"推荐使用 {style['name']} 风格"
        }
    
    def _generate_metadata(self, config: BookConfig) -> Dict:
        """生成KDP元数据"""
        # 自动提取关键词
        auto_keywords = self._extract_keywords(config)
        
        # 生成描述
        description = self._generate_description(config)
        
        return {
            "title": config.title,
            "subtitle": config.subtitle,
            "author": AUTHOR,
            "keywords": (config.keywords + auto_keywords)[:7],  # KDP限制7个关键词
            "description": description,
            "categories": self._suggest_categories(config.book_type),
            "price_recommendation": "$6.99 - $9.99",
            "paper_color": "Cream" if config.paper_color == DEFAULT_PAPER_COLOR else "White"
        }
    
    def _extract_keywords(self, config: BookConfig) -> List[str]:
        """智能提取关键词"""
        keywords = []
        title_lower = config.title.lower()
        
        # 根据标题匹配关键词库
        for category, words in KEYWORD_DATABASE.items():
            if category in title_lower or any(w in title_lower for w in words):
                keywords.extend(words[:3])
        
        # 根据类型添加关键词
        type_keywords = {
            BookType.GUIDED_JOURNAL: ["guided journal", "daily prompts", "self reflection"],
            BookType.DAILY_PLANNER: ["daily planner", "organizer", "schedule book"],
            BookType.GRATITUDE_JOURNAL: ["gratitude journal", "mindfulness", "positive thinking"]
        }
        
        if config.book_type in type_keywords:
            keywords.extend(type_keywords[config.book_type])
        
        return list(set(keywords))  # 去重
    
    def _generate_description(self, config: BookConfig) -> str:
        """生成书籍描述"""
        templates = {
            BookType.GUIDED_JOURNAL: """
Transform your business journey with {title}.

This beautifully designed {page_count}-page journal guides you through 90 days of focused entrepreneurship. Each day features thoughtful prompts to help you track progress, set priorities, and reflect on your wins.

Features:
✓ Daily guided prompts for clarity and focus
✓ Weekly reflection pages to celebrate wins
✓ Monthly goal tracking
✓ Premium cream paper for comfortable writing
✓ Professional 6" x 9" format, perfect for desk or bag

Whether you're launching a startup or scaling your business, this journal keeps you accountable and inspired every step of the way.

Start your 90-day transformation today.
""",
            BookType.GRATITUDE_JOURNAL: """
Discover the power of gratitude with {title}.

This {page_count}-page journal helps you cultivate a daily gratitude practice that transforms your mindset and attracts positivity into your life.

Features:
✓ Daily prompts to spark thankfulness
✓ Space for reflections and insights
✓ Monthly review pages
✓ Beautiful cream paper for a luxurious writing experience
✓ Portable 6" x 9" size

Make gratitude a daily habit and watch your life flourish.
"""
        }
        
        template = templates.get(config.book_type, templates[BookType.GUIDED_JOURNAL])
        return template.format(title=config.title, page_count=config.page_count).strip()
    
    def _suggest_categories(self, book_type: BookType) -> List[str]:
        """推荐KDP分类"""
        categories = {
            BookType.GUIDED_JOURNAL: [
                "Books > Self-Help > Personal Transformation",
                "Books > Business & Money > Entrepreneurship",
                "Books > Reference > Personal Organizers"
            ],
            BookType.DAILY_PLANNER: [
                "Books > Self-Help > Personal Transformation", 
                "Books > Reference > Personal Organizers"
            ],
            BookType.GRATITUDE_JOURNAL: [
                "Books > Self-Help > Happiness",
                "Books > Health, Fitness & Dieting > Mental Health"
            ]
        }
        return categories.get(book_type, categories[BookType.GUIDED_JOURNAL])
    
    def batch_create(self, configs: List[BookConfig]) -> List[Dict]:
        """批量创建书籍"""
        results = []
        print(f"\n📚 批量生成 {len(configs)} 本书籍\n")
        
        for i, config in enumerate(configs, 1):
            print(f"[{i}/{len(configs)}] ", end="")
            result = self.create_book(config)
            results.append(result)
        
        print(f"\n✅ 完成！共生成 {len(results)} 本书籍")
        return results
    
    def export_production_list(self, filename: str = "production_list.md"):
        """导出生产清单"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# KDP 书籍生产清单\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"工厂版本: {self.version}\n\n")
            
            for i, book in enumerate(self.created_books, 1):
                config = book["config"]
                f.write(f"## {i}. {config.title}\n\n")
                f.write(f"- **类型**: {config.book_type.value}\n")
                f.write(f"- **页数**: {config.page_count}\n")
                f.write(f"- **风格**: {config.cover_style}\n")
                f.write(f"- **输出文件**:\n")
                for file in book["files_to_generate"]:
                    f.write(f"  - [ ] {file}\n")
                f.write(f"\n**封面Prompt**:\n```\n{book['cover_prompt']['midjourney']}\n```\n\n")
                f.write(f"---\n\n")
        
        print(f"📋 生产清单已导出: {filename}")

# ============ 使用示例 ============
def demo():
    """演示：生成创业者日记"""
    factory = KDPBookFactory()
    
    # 创建创业者日记配置
    config = BookConfig(
        title="The Entrepreneur's Daily Journal",
        subtitle="A 90-Day Guided Workbook for High-Performance Business Owners",
        book_type=BookType.GUIDED_JOURNAL,
        page_count=108,
        cover_style="minimalist",
        target_audience="entrepreneurs, startup founders, business owners",
        keywords=["entrepreneur journal", "business planner", "productivity"]
    )
    
    # 生成书籍
    book = factory.create_book(config)
    
    # 打印结果
    print("\n" + "="*60)
    print("📦 书籍生成完成！")
    print("="*60)
    print(f"\n📝 内页结构: {book['interior_plan']['total_pages']} 页")
    print(f"\n🎨 封面风格: {book['cover_prompt']['style']}")
    print(f"\n📊 推荐关键词: {', '.join(book['metadata']['keywords'][:5])}")
    print(f"\n💰 建议定价: {book['metadata']['price_recommendation']}")
    
    # 导出生产清单
    factory.export_production_list()
    
    return book

def batch_demo():
    """演示：批量生成多本书籍"""
    factory = KDPBookFactory()
    
    configs = [
        BookConfig(
            title="The Entrepreneur's Daily Journal",
            subtitle="90-Day Business Success Planner",
            book_type=BookType.GUIDED_JOURNAL,
            cover_style="minimalist"
        ),
        BookConfig(
            title="Gratitude Journal for Moms",
            subtitle="Daily Reflections for Joyful Motherhood",
            book_type=BookType.GRATITUDE_JOURNAL,
            cover_style="watercolor"
        ),
        BookConfig(
            title="Productivity Planner 2024",
            subtitle="Daily Organizer for High Achievers",
            book_type=BookType.DAILY_PLANNER,
            cover_style="geometric"
        )
    ]
    
    return factory.batch_create(configs)

if __name__ == "__main__":
    print("🚀 KDP Book Factory v2.0")
    print("="*60)
    
    # 运行演示
    demo()
    
    print("\n✨ 提示: 使用 batch_demo() 可以批量生成多本书籍")
