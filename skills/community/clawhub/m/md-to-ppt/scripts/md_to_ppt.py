#!/usr/bin/env python3
"""
Markdown to PPT Converter v1.1
智能布局分析 + 自动配图
"""

import argparse
import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# 主题配置
THEMES = {
    "business-blue": {
        "name": "商务蓝",
        "primary": "#1e40af",
        "secondary": "#60a5fa",
        "background": "#ffffff",
        "text": "#1f2937",
        "accent": "#3b82f6",
        "style": "professional"
    },
    "business-gold": {
        "name": "黑金",
        "primary": "#000000",
        "secondary": "#d4af37",
        "background": "#ffffff",
        "text": "#000000",
        "accent": "#b8860b",
        "style": "luxury"
    },
    "tech-purple": {
        "name": "科技紫",
        "primary": "#7c3aed",
        "secondary": "#a78bfa",
        "background": "#0f172a",
        "text": "#f8fafc",
        "accent": "#8b5cf6",
        "style": "modern"
    },
    "creative-orange": {
        "name": "创意橙",
        "primary": "#ea580c",
        "secondary": "#fb923c",
        "background": "#fff7ed",
        "text": "#431407",
        "accent": "#f97316",
        "style": "creative"
    }
}

# 布局模板
LAYOUT_TEMPLATES = {
    "title": {
        "name": "标题页",
        "description": "封面、章节起始页",
        "structure": {
            "title": "center-large",
            "subtitle": "center-medium",
            "author": "bottom-small",
            "background": "gradient"
        }
    },
    "bullet_list": {
        "name": "要点列表",
        "description": "功能列表、优势说明",
        "structure": {
            "title": "top-left",
            "content": "left-60%",
            "image": "right-40%",
            "layout": "two-column"
        }
    },
    "two_column": {
        "name": "左右对比",
        "description": "对比、前后变化",
        "structure": {
            "title": "top-center",
            "left": "50%",
            "right": "50%",
            "layout": "split"
        }
    },
    "data_table": {
        "name": "数据表格",
        "description": "数据展示、对比分析",
        "structure": {
            "title": "top-left",
            "table": "center-large",
            "chart": "bottom",
            "layout": "vertical"
        }
    },
    "code_full": {
        "name": "代码展示",
        "description": "技术分享、Demo",
        "structure": {
            "title": "top-small",
            "code": "center-full",
            "notes": "bottom-small",
            "layout": "code-focused"
        }
    },
    "quote": {
        "name": "引用强调",
        "description": "金句、核心价值",
        "structure": {
            "quote": "center-large-italic",
            "author": "bottom-right",
            "background": "image-blur",
            "layout": "minimal"
        }
    },
    "timeline": {
        "name": "时间轴",
        "description": "发展历程、进度",
        "structure": {
            "title": "top-left",
            "timeline": "center-horizontal",
            "nodes": "evenly-spaced",
            "layout": "horizontal"
        }
    },
    "hero_image": {
        "name": "图文混排",
        "description": "产品展示、场景",
        "structure": {
            "title": "top-overlay",
            "image": "center-full",
            "caption": "bottom-overlay",
            "layout": "image-focused"
        }
    },
    "charts": {
        "name": "数据可视化",
        "description": "报表、数据分析",
        "structure": {
            "title": "top-left",
            "chart": "center-large",
            "insights": "bottom",
            "layout": "data-focused"
        }
    },
    "ending": {
        "name": "结束页",
        "description": "演示结束",
        "structure": {
            "thank_you": "center-large",
            "contact": "bottom-medium",
            "background": "gradient",
            "layout": "minimal"
        }
    }
}


class SlideContent:
    """幻灯片内容类"""
    
    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.content_items = []
        self.layout_type = "bullet_list"
        self.image_keywords = []
        self.image_url = None
        self.notes = ""
        self.priority = "normal"
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "content_items": self.content_items,
            "layout_type": self.layout_type,
            "image_keywords": self.image_keywords,
            "image_url": self.image_url,
            "notes": self.notes
        }


def parse_markdown_smart(content: str) -> List[SlideContent]:
    """
    智能解析 Markdown，自动分析内容和布局
    """
    slides = []
    current_slide = SlideContent()
    
    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    code_lang = ""
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 处理代码块
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = stripped[3:]
                code_lines = []
            else:
                in_code_block = False
                current_slide.content_items.append({
                    "type": "code",
                    "lang": code_lang,
                    "code": '\n'.join(code_lines),
                    "lines_count": len(code_lines)
                })
                # 长代码单独一页
                if len(code_lines) > 15:
                    current_slide.layout_type = "code_full"
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        # 分页符
        if stripped == '---':
            if current_slide.title:
                slides.append(current_slide)
            current_slide = SlideContent()
            i += 1
            continue
        
        # 演讲备注
        if stripped.startswith('<!--'):
            if '-->' in stripped:
                i += 1
                continue
            notes_lines = []
            i += 1
            while i < len(lines) and '-->' not in lines[i]:
                notes_lines.append(lines[i].strip())
                i += 1
            current_slide.notes = '\n'.join(notes_lines)
            i += 1
            continue
        
        # 一级标题 - 新页面
        if stripped.startswith('# ') and not stripped.startswith('## '):
            if current_slide.title:
                slides.append(current_slide)
                current_slide = SlideContent()
            current_slide.title = stripped[2:]
            current_slide.layout_type = "title"
        
        # 二级标题
        elif stripped.startswith('## '):
            current_slide.subtitle = stripped[3:]
        
        # 列表项
        elif stripped.startswith('- '):
            current_slide.content_items.append({
                "type": "bullet",
                "text": stripped[2:],
                "keywords": extract_keywords(stripped[2:])
            })
        
        # 引用
        elif stripped.startswith('> '):
            current_slide.content_items.append({
                "type": "quote",
                "text": stripped[2:]
            })
            current_slide.layout_type = "quote"
        
        # 表格
        elif stripped.startswith('|'):
            current_slide.content_items.append({
                "type": "table_row",
                "cells": [cell.strip() for cell in stripped.split('|')[1:-1]]
            })
            current_slide.layout_type = "data_table"
        
        # 图片
        elif stripped.startswith('!['):
            match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
            if match:
                current_slide.content_items.append({
                    "type": "image",
                    "alt": match.group(1),
                    "src": match.group(2)
                })
                current_slide.image_keywords = [match.group(1)]
        
        # 普通文本
        elif stripped:
            current_slide.content_items.append({
                "type": "text",
                "text": stripped
            })
        
        i += 1
    
    # 添加最后一页
    if current_slide.title:
        slides.append(current_slide)
    
    return slides


def extract_keywords(text: str) -> List[str]:
    """提取关键词用于配图搜索"""
    # 简单实现：提取名词
    keywords = []
    # 移除标点
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    words = text.split()
    
    # 中文关键词（简单分词）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    keywords.extend(chinese_chars)
    
    # 英文关键词
    english_words = [w for w in words if len(w) > 3 and w.isalpha()]
    keywords.extend(english_words[:3])
    
    return keywords[:5]


def determine_layout(slide: SlideContent) -> str:
    """
    根据内容确定最佳布局
    """
    # 分析内容
    content_types = [item["type"] for item in slide.content_items]
    
    # 判断规则
    if not slide.content_items:
        return "title"
    
    # 检查是否是标题页（只有标题，内容很少）
    if len(content_types) <= 2 and slide.subtitle:
        return "title"
    
    if "quote" in content_types and len(content_types) == 1:
        return "quote"
    
    if "table_row" in content_types:
        return "data_table"
    
    code_items = [item for item in slide.content_items if item["type"] == "code"]
    if code_items and any(item.get("lines_count", 0) > 15 for item in code_items):
        return "code_full"
    
    bullet_items = [item for item in slide.content_items if item["type"] == "bullet"]
    
    # 内容少，用图文混排
    if len(slide.content_items) <= 3:
        return "hero_image"
    
    # 有列表项，用要点列表
    if bullet_items:
        return "bullet_list"
    
    return "bullet_list"


def search_image_unsplash(keywords: List[str], output_dir: str, page_num: int) -> str:
    """
    从 Unsplash 搜索图片（使用免费 API）
    """
    if not keywords:
        return None
    
    # 使用 Unsplash Source（免费，无需 API key）
    query = '+'.join(keywords[:3])
    image_url = f"https://source.unsplash.com/1600x900/?{query}"
    
    # 下载图片
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            image_path = os.path.join(output_dir, "assets", f"page-{page_num}.jpg")
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return f"./assets/page-{page_num}.jpg"
    except Exception as e:
        print(f"⚠️ 图片下载失败：{e}")
    
    return None


def generate_slidev_with_layout(slides: List[SlideContent], theme: str, 
                                  output_dir: str, title: str = "Presentation", 
                                  author: str = "", auto_images: bool = False) -> Dict:
    """
    生成带智能布局的 Slidev 文件
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "assets"), exist_ok=True)
    
    theme_config = THEMES.get(theme, THEMES["business-blue"])
    
    # 生成 layout-plan.json
    layout_plan = []
    
    # 开始生成 slides.md
    content = f"""---
# {title}
theme: default
background: {theme_config['background']}
textColor: {theme_config['text']}
class: text-center
highlighter: shiki
lineNumbers: false
author: {author}
date: {datetime.now().strftime('%Y-%m-%d')}
---

<!--
background: {theme_config['primary']}
-->

# {title}

<div class="text-sm opacity-75">{author or 'Presented by AI'}</div>
<div class="text-sm opacity-75">{datetime.now().strftime('%Y-%m-%d')}</div>

"""
    
    for i, slide in enumerate(slides):
        # 确定布局
        layout = determine_layout(slide)
        slide.layout_type = layout
        
        # 记录布局计划
        layout_plan.append({
            "page": i + 1,
            "title": slide.title[:50],
            "layout": layout,
            "content_count": len(slide.content_items),
            "has_image": slide.image_url is not None
        })
        
        # 自动配图
        if auto_images and layout in ["bullet_list", "hero_image", "quote"]:
            keywords = slide.image_keywords or extract_keywords(slide.title)
            if keywords:
                image_path = search_image_unsplash(keywords, output_dir, i + 1)
                if image_path:
                    slide.image_url = image_path
        
        # 添加主题背景
        content += f"""
<!--
background:
  gradient: 'linear'
  from: '{theme_config['primary']}'
  to: '{theme_config['secondary']}'
-->

"""
        
        # 根据布局生成内容
        if layout == "title":
            content += f"# {slide.title}\n\n"
            if slide.subtitle:
                content += f"## {slide.subtitle}\n\n"
        
        elif layout == "quote":
            quote_items = [item for item in slide.content_items if item["type"] == "quote"]
            if quote_items:
                content += f"> {quote_items[0]['text']}\n\n"
            content += f"# {slide.title}\n\n"
        
        elif layout == "code_full":
            content += f"## {slide.title}\n\n"
            code_items = [item for item in slide.content_items if item["type"] == "code"]
            for code in code_items:
                content += f"```{code.get('lang', '')}\n{code['code']}\n```\n"
        
        elif layout == "data_table":
            content += f"# {slide.title}\n\n"
            table_rows = [item for item in slide.content_items if item["type"] == "table_row"]
            if table_rows:
                # 第一行作为表头
                header = table_rows[0].get("cells", [])
                content += "|" + "|".join(header) + "|\n"
                content += "|" + "|".join(["---"] * len(header)) + "|\n"
                for row in table_rows[1:]:
                    cells = row.get("cells", [])
                    content += "|" + "|".join(cells) + "|\n"
        
        elif layout == "hero_image":
            content += f"# {slide.title}\n\n"
            if slide.image_url:
                content += f"![{slide.title}]({slide.image_url})\n\n"
            for item in slide.content_items:
                if item["type"] == "bullet":
                    content += f"- {item['text']}\n"
                elif item["type"] == "text":
                    content += f"{item['text']}\n"
        
        else:  # bullet_list
            content += f"# {slide.title}\n\n"
            if slide.subtitle:
                content += f"## {slide.subtitle}\n\n"
            
            for item in slide.content_items:
                if item["type"] == "bullet":
                    content += f"- {item['text']}\n"
                elif item["type"] == "text":
                    content += f"{item['text']}\n"
                elif item["type"] == "quote":
                    content += f"> {item['text']}\n"
            
            if slide.image_url:
                content += f"\n![配图]({slide.image_url})\n"
        
        # 演讲备注
        if slide.notes:
            content += f"""
<!--
Notes:
{slide.notes}
-->
"""
        
        content += "\n---\n\n"
    
    # 写入 slides.md
    slides_path = os.path.join(output_dir, "slides.md")
    with open(slides_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 写入 layout-plan.json
    plan_path = os.path.join(output_dir, "layout-plan.json")
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump({
            "title": title,
            "theme": theme,
            "total_pages": len(slides),
            "generated_at": datetime.now().isoformat(),
            "pages": layout_plan
        }, f, ensure_ascii=False, indent=2)
    
    # 生成 style.css
    style_content = f"""/* {title} - Smart Layout Styles */

:root {{
  --theme-primary: {theme_config['primary']};
  --theme-secondary: {theme_config['secondary']};
  --theme-accent: {theme_config['accent']};
}}

/* 标题样式 */
h1 {{ font-size: 2.5em; color: {theme_config['text']}; }}
h2 {{ font-size: 1.8em; color: {theme_config['primary']}; }}

/* 列表样式 */
ul {{ list-style: none; padding-left: 0; }}
ul li {{
  padding: 0.5em 0;
  padding-left: 1.5em;
  position: relative;
}}
ul li::before {{
  content: "•";
  color: {theme_config['accent']};
  position: absolute;
  left: 0;
}}

/* 引用样式 */
blockquote {{
  border-left: 4px solid {theme_config['accent']};
  padding-left: 1em;
  margin: 1em 0;
  font-style: italic;
}}

/* 代码块样式 */
pre {{
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 1em;
  overflow-x: auto;
}}

/* 图片样式 */
img {{
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}}

/* 表格样式 */
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}}
th, td {{
  border: 1px solid {theme_config['secondary']};
  padding: 0.5em;
  text-align: left;
}}
th {{
  background: {theme_config['primary']};
  color: white;
}}
"""
    
    style_path = os.path.join(output_dir, "style.css")
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(style_content)
    
    # 生成 README
    readme_content = f"""# {title}

智能布局 PPT - 使用 Slidev 创建

## 📐 布局方案

查看 `layout-plan.json` 了解每页的布局设计

## 🖼️ 配图

自动配图已保存到 `assets/` 目录

## 预览

```bash
npx slidew dev
```

## 导出

```bash
npx slidew export         # PDF
npx slidew export --format pptx  # PPTX
npx slidew export --format html  # HTML
```

## 主题

- 名称：{theme_config['name']}
- 风格：{theme_config['style']}

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**工具**: md-to-ppt v1.1 (Smart Layout)
"""
    
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return {
        "success": True,
        "output_dir": output_dir,
        "slides_count": len(slides),
        "theme": theme_config['name'],
        "layout_plan": layout_plan,
        "files": ["slides.md", "style.css", "README.md", "layout-plan.json", "assets/"]
    }


def main():
    parser = argparse.ArgumentParser(description='Markdown to PPT Converter v1.1 (Smart Layout)')
    parser.add_argument('--input', '-i', required=True, help='输入 Markdown 文件')
    parser.add_argument('--output', '-o', default='./output', help='输出目录')
    parser.add_argument('--theme', '-t', default='business-blue', help='主题名称')
    parser.add_argument('--format', '-f', default='slidev', choices=['slidev', 'html'], help='输出格式')
    parser.add_argument('--title', help='PPT 标题')
    parser.add_argument('--author', default='', help='作者名')
    parser.add_argument('--auto-images', action='store_true', help='启用自动配图')
    parser.add_argument('--smart-layout', action='store_true', help='启用智能布局')
    
    args = parser.parse_args()
    
    print(f"🤖 Markdown to PPT Converter v1.1")
    print(f"📐 智能布局：{'启用' if args.smart_layout else '标准'}")
    print(f"🖼️ 自动配图：{'启用' if args.auto_images else '禁用'}")
    print()
    
    # 读取 Markdown
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 智能解析
    print("📊 正在分析文档结构...")
    slides = parse_markdown_smart(content)
    print(f"✅ 检测到 {len(slides)} 个内容块")
    
    # 布局分析
    if args.smart_layout:
        print("📐 正在设计每页布局...")
        for i, slide in enumerate(slides):
            layout = determine_layout(slide)
            slide.layout_type = layout
            print(f"   第{i+1}页：{layout} - {slide.title[:30]}")
    
    # 生成 PPT
    print(f"\n🎨 应用主题：{THEMES.get(args.theme, THEMES['business-blue'])['name']}")
    print("⚙️ 正在生成幻灯片...")
    
    result = generate_slidev_with_layout(
        slides, 
        args.theme, 
        args.output, 
        args.title or "Presentation",
        args.author,
        args.auto_images
    )
    
    # 输出结果
    if result["success"]:
        print(f"\n✅ 转换成功！")
        print(f"📁 输出位置：{result['output_dir']}")
        print(f"📄 页数：{result['slides_count']}")
        print(f"📐 布局方案：layout-plan.json")
        if args.auto_images:
            print(f"🖼️ 配图目录：assets/")
        
        print(f"\n🚀 预览命令：")
        print(f"   cd {result['output_dir']} && npx slidew dev")
    else:
        print("❌ 转换失败")


if __name__ == "__main__":
    main()
