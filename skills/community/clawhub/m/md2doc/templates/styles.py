#!/usr/bin/env python3
"""
MD2DOC 样式模板配置
支持多种文档风格
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StyleConfig:
    """样式配置类"""
    # 文档基础
    name: str
    description: str
    
    # 字体配置
    title_font: str = '微软雅黑'
    body_font: str = '宋体'
    code_font: str = 'Consolas'
    
    # 字号配置 (pt)
    title1_size: int = 16
    title2_size: int = 14
    title3_size: int = 12
    body_size: int = 11
    code_size: int = 9
    caption_size: int = 9
    
    # 颜色配置 (RGB)
    title_color: tuple = (0, 0, 0)
    body_color: tuple = (0, 0, 0)
    code_color: tuple = (50, 50, 50)
    link_color: tuple = (0, 112, 192)
    accent_color: tuple = (0, 112, 192)  # 强调色
    
    # 段落样式
    line_spacing: float = 1.5
    paragraph_spacing: float = 0.5
    
    # 页面配置
    page_margin_top: float = 2.5  # cm
    page_margin_bottom: float = 2.5
    page_margin_left: float = 2.5
    page_margin_right: float = 2.5
    
    # 表格样式
    table_header_bg: tuple = (240, 240, 240)
    table_border: bool = True
    
    # 代码块样式
    code_bg: tuple = (245, 245, 245)
    code_border: bool = False
    
    # 封面配置
    has_cover: bool = False
    cover_title_size: int = 28
    cover_subtitle_size: int = 14
    cover_bg_color: tuple = (255, 255, 255)  # 封面背景色
    cover_image: str = ''  # 封面图片路径（可选）
    
    # 目录配置
    has_toc: bool = True
    toc_title: str = '目录'
    
    # 页眉页脚
    has_header: bool = False
    has_footer: bool = True
    header_text: str = ''
    footer_text: str = '第 {page} 页'
    show_page_number: bool = True


# 预定义样式模板
STYLES = {
    'default': StyleConfig(
        name='默认',
        description='标准文档样式，适合一般用途',
        title_font='微软雅黑',
        body_font='宋体',
    ),
    
    'business': StyleConfig(
        name='商务蓝',
        description='企业报告风格，蓝色主题，专业大气',
        title_font='微软雅黑',
        body_font='微软雅黑',
        title_color=(0, 51, 102),  # 深蓝
        accent_color=(0, 112, 192),  # 商务蓝
        link_color=(0, 112, 192),
        table_header_bg=(230, 240, 250),
        has_cover=True,
        has_toc=True,
        has_header=True,
        has_footer=True,
        header_text='',
        footer_text='第 {page} 页',
    ),
    
    'tech': StyleConfig(
        name='技术灰',
        description='技术文档风格，灰色主题，简洁专业',
        title_font='微软雅黑',
        body_font='微软雅黑',
        title_color=(64, 64, 64),  # 深灰
        accent_color=(100, 100, 100),  # 中灰
        link_color=(70, 130, 180),
        table_header_bg=(240, 240, 240),
        code_bg=(248, 248, 248),
        code_border=True,
        has_cover=False,
    ),
    
    'minimal': StyleConfig(
        name='简洁白',
        description='极简风格，黑白配色，清爽干净',
        title_font='微软雅黑',
        body_font='微软雅黑',
        title1_size=18,
        title2_size=14,
        title3_size=12,
        body_size=11,
        title_color=(0, 0, 0),
        accent_color=(0, 0, 0),
        table_header_bg=(250, 250, 250),
        line_spacing=1.3,
        has_cover=False,
    ),
    
    'product': StyleConfig(
        name='产品红',
        description='PRD专用风格，红色强调，醒目突出',
        title_font='微软雅黑',
        body_font='微软雅黑',
        title1_size=18,  # 增大标题
        title2_size=15,
        title3_size=13,
        body_size=11,
        title_color=(180, 0, 0),  # 深红
        body_color=(50, 50, 50),  # 稍浅的正文字色
        accent_color=(220, 20, 60),  # 猩红
        link_color=(220, 20, 60),
        line_spacing=1.4,  # 调整行距
        paragraph_spacing=0.3,
        table_header_bg=(255, 245, 245),  # 更柔和的表格头背景
        has_cover=True,
        has_toc=True,
        has_header=False,
        has_footer=True,
        cover_title_size=36,  # 更大标题
        cover_subtitle_size=16,
        footer_text='PRD 文档',
    ),
    
    'academic': StyleConfig(
        name='学术风',
        description='学术论文风格，宋体正文，严谨规范',
        title_font='黑体',
        body_font='宋体',
        title1_size=18,
        title2_size=15,
        title3_size=12,
        body_size=12,
        code_size=10,
        line_spacing=1.5,
        paragraph_spacing=0.3,
        table_header_bg=(235, 235, 235),
        has_cover=True,
        has_toc=True,
        has_header=True,
        has_footer=True,
        header_text='',
        footer_text='第 {page} 页',
    ),
}


def get_style(style_name: str) -> StyleConfig:
    """获取样式配置"""
    if style_name not in STYLES:
        print(f"警告: 未知样式 '{style_name}'，使用默认样式")
        return STYLES['default']
    return STYLES[style_name]


def list_styles():
    """列出所有可用样式"""
    print("可用样式模板:")
    print("-" * 50)
    for key, style in STYLES.items():
        print(f"  {key:12} - {style.name}: {style.description}")
    print("-" * 50)


if __name__ == '__main__':
    list_styles()
