"""
moyu-make-xhs-pics 类型定义
"""

from typing import TypedDict, Optional


class Section(TypedDict):
    """章节"""
    title: str
    content: str


class Article(TypedDict):
    """文章"""
    title: str
    sections: list[Section]
    summary: str


class ImageResult(TypedDict):
    """图片生成结果"""
    success: bool
    image_url: Optional[str]
    local_path: Optional[str]
    error: Optional[str]


class ArticleImagesResult(TypedDict):
    """文章图片生成结果"""
    success: bool
    covers: list[str]
    illustrations: list[str]
    decorations: list[str]
    total: int
    error: Optional[str]


# 风格定义
STYLES = {
    "fresh": {
        "keywords": ["清新", "自然", "干净", "明亮", "通透"],
        "description": "清新自然的风格，适合生活分享类内容"
    },
    "warm": {
        "keywords": ["温暖", "友好", "柔和", "温馨", "舒适"],
        "description": "温暖友好的风格，适合情感类内容"
    },
    "notion": {
        "keywords": ["极简", "手绘", "知识感", "专业", "简洁"],
        "description": "极简手绘风格，适合知识干货类内容"
    },
    "cute": {
        "keywords": ["可爱", "卡通", "萌趣", "活泼", "卡通风格"],
        "description": "可爱卡通风格，适合轻松趣味类内容"
    }
}

# 布局定义
LAYOUTS = {
    "balanced": "信息均匀分布在画面中，画面整洁平衡",
    "list": "垂直列表布局，明确的1、2、3、4数字序号或圆点标记，每个要点独立一行，清晰的条目分隔线，视觉上垂直排列",
    "comparison": "左右对比布局，左边一个内容右边一个内容，中间用箭头或VS标记分隔，显示所有对比项",
    "flow": "从左到右的水平流程布局，清晰的步骤1→步骤2→步骤3→步骤4箭头连接，显示完整流程"
}

VALID_STYLES = list(STYLES.keys())
VALID_LAYOUTS = list(LAYOUTS.keys()) + ["auto"]
