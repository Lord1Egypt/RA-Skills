#!/usr/bin/env python3
"""
GitHub to Xiaohongshu - Content Generator
Analyzes a GitHub repository and generates XHS infographic content structure.
"""

import sys
import re
import os
from datetime import datetime
from urllib.parse import urlparse

def extract_repo_info(url):
    """Extract owner and repo name from GitHub URL."""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    return None, None

def create_slug(repo_name):
    """Create a URL-friendly slug."""
    return repo_name.lower().replace('_', '-').replace(' ', '-')

def create_directory_structure(base_path, slug):
    """Create the output directory structure."""
    dirs = [
        f"{base_path}/{slug}",
        f"{base_path}/{slug}/prompts"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return f"{base_path}/{slug}"

def generate_analysis_template(repo_name, owner, url):
    """Generate analysis.md template."""
    return f"""# {repo_name} 项目分析

## 项目基本信息
- **项目名称**: {repo_name}
- **作者**: {owner}
- **GitHub**: {url}

## 核心功能
(TODO: 从README提取)

## 技术亮点
(TODO: 分析技术特色)

## 目标受众
- 开发者
- (TODO: 补充)

## 小红书传播角度
- Hook 标题建议: (TODO)
- 核心卖点: (TODO)
- 视觉机会: (TODO)

## 推荐图片数量
4-5 张

## 推荐风格
- A: notion（极简手绘）- 技术文档风格
- B: bold（高对比）- 视觉冲击风格
- C: warm（温暖亲切）- 故事叙述风格
- D: cyberpunk（赛博朋克）- 深色科技感
- E: sketchy（手绘涂鸦）- 温暖教育风
- F: premium（深色专业）- 企业级质感
"""

def generate_outline_strategy_a(repo_name):
    """Generate story-driven outline."""
    return f"""---
strategy: a
name: Story-Driven
style: warm
image_count: 4
---

## P1 Cover
**Hook**: "发现了一个神器：{repo_name}"
**Visual**: 产品图标 + 醒目标题

## P2 Problem
**Message**: 解决的痛点
**Visual**: 前后对比

## P3 Discovery
**Message**: 如何发现这个工具
**Visual**: 使用场景

## P4 Result
**Message**: 使用后的改变
**Visual**: 成果展示 + CTA
"""

def generate_outline_strategy_b(repo_name):
    """Generate information-dense outline."""
    return f"""---
strategy: b
name: Information-Dense
style: notion
image_count: 5
---

## P1 Cover
**Hook**: "{repo_name} | 技术解析"
**Visual**: 项目Logo + 简洁标题

## P2 Features
**Message**: 核心功能一览
**Visual**: 功能列表 + 图标

## P3 Tech
**Message**: 技术亮点解析
**Visual**: 架构图/流程图

## P4 Comparison
**Message**: 与传统方案对比
**Visual**: 对比表格

## P5 Install
**Message**: 快速开始
**Visual**: 代码块 + GitHub链接
"""

def generate_outline_strategy_c(repo_name):
    """Generate visual-first outline."""
    return f"""---
strategy: c
name: Visual-First
style: bold
style_reason: "Strong visual impact for attention-grabbing"
elements:
  background: solid-purple
  decorations: [large-icons]
  emphasis: big-numbers
  typography: bold-headlines
layout: minimal
image_count: 3
---

## P1 Cover
**Type**: cover
**Hook**: "{repo_name}"
**Visual**: 大标题 + 视觉冲击

## P2 Demo
**Message**: 核心功能展示
**Visual**: 截图/演示

## P3 CTA
**Message**: 立即体验
**Visual**: GitHub链接 + 二维码
"""

def generate_outline_strategy_d(repo_name):
    """Generate cyberpunk tech outline."""
    return f"""---
strategy: d
name: Cyberpunk Tech
style: cyberpunk
style_reason: "Perfect for developer tools and AI projects with futuristic aesthetic"
elements:
  background: dark-grid
  decorations: [neon-glow, circuit-lines]
  emphasis: glowing-borders
  typography: monospace-tech
layout: dense
image_count: 5
---

## P1 Cover
**Type**: cover
**Hook**: "{repo_name}"
**Visual**: Neon title + glitch effect + stars count
**Layout**: sparse

## P2 Features
**Type**: features
**Message**: Core capabilities with neon accents
**Visual**: Glowing feature cards on dark background
**Layout**: grid

## P3 Architecture
**Type**: tech
**Message**: System flow with circuit-style diagram
**Visual**: Flow chart with neon connectors
**Layout**: flow

## P4 Comparison
**Type**: comparison
**Message**: Feature matrix with cyberpunk styling
**Visual**: Glowing table, dark theme
**Layout**: comparison

## P5 Quick Start
**Type**: cta
**Message**: Terminal commands with neon syntax
**Visual**: Dark code block with glowing text
**Layout**: sparse
"""

def generate_outline_strategy_e(repo_name):
    """Generate warm hand-drawn outline."""
    return f"""---
strategy: e
name: Warm Hand-drawn
style: sketchy
style_reason: "Friendly, approachable aesthetic for tutorials and education"
elements:
  background: paper-texture
  decorations: [doodles, arrows, stickers]
  emphasis: hand-drawn-boxes
  typography: rounded-friendly
layout: moderate
image_count: 4
---

## P1 Cover
**Type**: cover
**Hook**: "发现{repo_name}"
**Visual**: Hand-drawn title + doodle decorations
**Layout**: sparse

## P2 What It Solves
**Type**: problem
**Message**: Problem → Solution story
**Visual**: Sketch-style before/after
**Layout**: split

## P3 How To Use
**Type**: guide
**Message**: Step by step with doodle arrows
**Visual**: Numbered steps, hand-drawn icons
**Layout**: list

## P4 Try It
**Type**: cta
**Message**: Friendly encouragement
**Visual**: Doodle characters, speech bubbles
**Layout**: sparse
"""

def generate_outline_strategy_f(repo_name):
    """Generate dark professional outline."""
    return f"""---
strategy: f
name: Dark Professional
style: premium
style_reason: "Enterprise-grade aesthetic for business tools and SaaS"
elements:
  background: dark-navy
  decorations: [glassmorphism, subtle-gradients]
  emphasis: gold-accents
  typography: elegant-serif
layout: dense
image_count: 5
---

## P1 Cover
**Type**: cover
**Hook**: "{repo_name}"
**Visual**: Gold-accented logo + premium typography
**Layout**: sparse

## P2 Value Proposition
**Type**: features
**Message**: Business benefits with metrics
**Visual**: Glass cards with gold borders
**Layout**: grid

## P3 Use Cases
**Type**: showcase
**Message**: Enterprise scenarios
**Visual**: Professional icons, clean layout
**Layout**: flow

## P4 Comparison
**Type**: comparison
**Message**: Competitive analysis
**Visual**: Elegant table, dark theme
**Layout**: comparison

## P5 Get Started
**Type**: cta
**Message**: Professional onboarding
**Visual**: Polished code block + contact
**Layout**: sparse
"""

def generate_html_template(repo_name, slug):
    """Generate HTML template for XHS output."""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{repo_name} - 小红书图文</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}
        .xhs-card {{
            width: 375px;
            height: 500px;
            background: #fafafa;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
            background-image: 
                linear-gradient(#e5e5e5 1px, transparent 1px),
                linear-gradient(90deg, #e5e5e5 1px, transparent 1px);
            background-size: 25px 25px;
        }}
        .card-content {{
            padding: 40px 30px;
            height: 100%;
        }}
        h1 {{
            font-size: 28px;
            color: #2d2d2d;
            margin-bottom: 20px;
            text-align: center;
        }}
        h2 {{
            font-size: 20px;
            color: #2d2d2d;
            margin-bottom: 15px;
        }}
        p {{
            font-size: 14px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        .code-block {{
            background: #1e1e1e;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            color: #7ee787;
        }}
    </style>
</head>
<body>
    <!-- 5 Cards for XHS -->
    <div class="xhs-card">
        <div class="card-content">
            <h1>{repo_name}</h1>
            <p style="text-align: center;">多源研究神器</p>
        </div>
    </div>
    <div class="xhs-card">
        <div class="card-content">
            <h2>核心功能</h2>
            <p>(TODO: Fill in features)</p>
        </div>
    </div>
    <div class="xhs-card">
        <div class="card-content">
            <h2>技术亮点</h2>
            <p>(TODO: Fill in tech details)</p>
        </div>
    </div>
    <div class="xhs-card">
        <div class="card-content">
            <h2>对比优势</h2>
            <p>(TODO: Fill in comparison)</p>
        </div>
    </div>
    <div class="xhs-card">
        <div class="card-content">
            <h2>快速开始</h2>
            <div class="code-block">
git clone {slug}
            </div>
        </div>
    </div>
</body>
</html>
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: github-to-xhs.py <github-url>")
        print("Example: github-to-xhs.py https://github.com/mvanhorn/last30days-skill")
        sys.exit(1)
    
    github_url = sys.argv[1]
    owner, repo = extract_repo_info(github_url)
    
    if not owner or not repo:
        print(f"Error: Could not parse GitHub URL: {github_url}")
        sys.exit(1)
    
    slug = create_slug(repo)
    base_path = "/root/.openclaw/workspace/xhs-images"
    output_dir = create_directory_structure(base_path, slug)
    
    print(f"📁 Creating structure in: {output_dir}")
    
    # Generate files
    files_to_create = [
        (f"{output_dir}/analysis.md", generate_analysis_template(repo, owner, github_url)),
        (f"{output_dir}/outline-strategy-a.md", generate_outline_strategy_a(repo)),
        (f"{output_dir}/outline-strategy-b.md", generate_outline_strategy_b(repo)),
        (f"{output_dir}/outline-strategy-c.md", generate_outline_strategy_c(repo)),
        (f"{output_dir}/outline-strategy-d.md", generate_outline_strategy_d(repo)),
        (f"{output_dir}/outline-strategy-e.md", generate_outline_strategy_e(repo)),
        (f"{output_dir}/outline-strategy-f.md", generate_outline_strategy_f(repo)),
        (f"{output_dir}/xiaohongshu-post.html", generate_html_template(repo, slug)),
    ]
    
    for filepath, content in files_to_create:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {os.path.basename(filepath)}")
    
    print(f"\n✅ Done! Files created in: {output_dir}")
    print(f"\nNext steps:")
    print(f"  1. Edit {output_dir}/analysis.md with project details")
    print(f"  2. Choose a strategy (A-F):")
    print(f"     A: Story-Driven (warm, emotional)")
    print(f"     B: Information-Dense (notion, technical)")
    print(f"     C: Visual-First (bold, minimal)")
    print(f"     D: Cyberpunk Tech (neon dark, dev tools)")
    print(f"     E: Warm Hand-drawn (sketchy, educational)")
    print(f"     F: Dark Professional (premium, enterprise)")
    print(f"  3. Generate prompts in prompts/ directory")
    print(f"  4. Update xiaohongshu-post.html with content")

if __name__ == "__main__":
    main()
