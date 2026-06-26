"""
moyu-make-xhs-pics - 小红书图片生成工具
"""

from .types import (
    Article,
    Section,
    ImageResult,
    ArticleImagesResult,
    STYLES,
    LAYOUTS,
    VALID_STYLES,
    VALID_LAYOUTS
)
from .article_parser import ArticleParser
from .prompt_engine import PromptEngine
from .layout_selector import LayoutSelector
from .image_generator import ImageGenerator
from .watermark import add_watermark

__version__ = "1.0.0"
__all__ = [
    "ArticleParser",
    "PromptEngine",
    "LayoutSelector",
    "ImageGenerator",
    "add_watermark",
    "generate_article_images",
    "STYLES",
    "LAYOUTS",
    "VALID_STYLES",
    "VALID_LAYOUTS",
]


def generate_article_images(
    article_path: str,
    cover_count: int = 1,
    illustration_count: int = 1,
    decoration_count: int = 2,
    style: str = "fresh",
    layout: str = "auto",
    provider: str = "minimax"
) -> ArticleImagesResult:
    """
    生成文章的图片（封面 + 插图 + 配图）
    
    Args:
        article_path: 文章文件路径
        cover_count: 封面图数量
        illustration_count: 插图数量
        decoration_count: 配图数量
        style: 风格 (fresh/warm/notion/cute)
        layout: 布局 (balanced/list/comparison/flow/auto)
        provider: API 提供商 (minimax/dashscope)
    
    Returns:
        ArticleImagesResult
    """
    try:
        # 1. 解析文章
        article = ArticleParser.parse(article_path)
        
        # 2. 解析布局
        resolved_layout = LayoutSelector.resolve_layout(layout, article)
        
        # 3. 初始化图片生成器
        generator = ImageGenerator(provider)
        
        covers = []
        illustrations = []
        decorations = []
        
        # 4. 生成封面图
        for i in range(cover_count):
            prompt = PromptEngine.generate_cover_prompt(article, style)
            result = generator.generate(prompt, style, "cover")
            
            if result["success"]:
                covers.append(result["local_path"])
            else:
                return ArticleImagesResult(
                    success=False,
                    covers=[],
                    illustrations=[],
                    decorations=[],
                    total=0,
                    error=f"封面图生成失败: {result['error']}"
                )
        
        # 5. 生成插图
        for i in range(illustration_count):
            prompt = PromptEngine.generate_illustration_prompt(article, style, resolved_layout)
            result = generator.generate(prompt, style, "illustration")
            
            if result["success"]:
                illustrations.append(result["local_path"])
            else:
                return ArticleImagesResult(
                    success=False,
                    covers=covers,
                    illustrations=[],
                    decorations=[],
                    total=len(covers),
                    error=f"插图生成失败: {result['error']}"
                )
        
        # 6. 生成配图
        selected_sections = PromptEngine.select_random_sections(
            article["sections"], 
            decoration_count
        )
        
        for section in selected_sections:
            prompt = PromptEngine.generate_decoration_prompt(section, style)
            result = generator.generate(prompt, style, "decoration")
            
            if result["success"]:
                decorations.append(result["local_path"])
            else:
                return ArticleImagesResult(
                    success=False,
                    covers=covers,
                    illustrations=illustrations,
                    decorations=[],
                    total=len(covers) + len(illustrations),
                    error=f"配图生成失败: {result['error']}"
                )
        
        # 7. 添加水印
        for path in covers + illustrations + decorations:
            add_watermark(path)
        
        return ArticleImagesResult(
            success=True,
            covers=covers,
            illustrations=illustrations,
            decorations=decorations,
            total=len(covers) + len(illustrations) + len(decorations),
            error=None
        )
        
    except FileNotFoundError as e:
        return ArticleImagesResult(
            success=False,
            covers=[],
            illustrations=[],
            decorations=[],
            total=0,
            error=str(e)
        )
    except ValueError as e:
        return ArticleImagesResult(
            success=False,
            covers=[],
            illustrations=[],
            decorations=[],
            total=0,
            error=str(e)
        )
    except Exception as e:
        return ArticleImagesResult(
            success=False,
            covers=[],
            illustrations=[],
            decorations=[],
            total=0,
            error=f"未知错误: {str(e)}"
        )
