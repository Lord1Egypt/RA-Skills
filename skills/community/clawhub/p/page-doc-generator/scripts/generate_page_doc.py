#!/usr/bin/env python3
"""
Generate page documentation from screenshots and source code.

Usage:
    python generate_page_doc.py <project_path> <screenshots_dir> [output_dir]
    
Example:
    python generate_page_doc.py "D:\Project\myapp" "D:\Project\myapp\static\screenshots"
"""

import os
import sys
import json
import re
from pathlib import Path


def find_pages(project_path):
    """Find all page Vue files in the pages directory."""
    pages_dir = Path(project_path) / "pages"
    pages = []
    seen_paths = set()  # Avoid duplicates
    
    if not pages_dir.exists():
        return pages
    
    for page_dir in pages_dir.iterdir():
        if page_dir.is_dir():
            # Check for {page_dir.name}.vue (e.g., notes/notes.vue)
            named_vue = page_dir / f"{page_dir.name}.vue"
            if named_vue.exists() and str(named_vue) not in seen_paths:
                pages.append({
                    "name": page_dir.name,
                    "path": str(named_vue),
                    "dir": str(page_dir)
                })
                seen_paths.add(str(named_vue))
            
            # Also check for index.vue (e.g., index/index.vue)
            index_vue = page_dir / "index.vue"
            if index_vue.exists() and str(index_vue) not in seen_paths:
                # Use directory name as page name
                pages.append({
                    "name": page_dir.name,
                    "path": str(index_vue),
                    "dir": str(page_dir)
                })
                seen_paths.add(str(index_vue))
    
    return pages


def find_screenshots(screenshots_dir):
    """Find all screenshots and match them to page names."""
    screenshots_path = Path(screenshots_dir)
    screenshots = {}
    
    if not screenshots_path.exists():
        return screenshots
    
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    
    for img_file in screenshots_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            # Extract page name from filename (remove extension, use as key)
            name = img_file.stem
            screenshots[name] = str(img_file)
    
    return screenshots


def read_vue_file(vue_path):
    """Read Vue file and extract template, script, and style sections."""
    try:
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"


def extract_page_info(vue_content, page_name):
    """Extract key information from Vue file."""
    info = {
        "has_template": "<template>" in vue_content,
        "has_script": "<script>" in vue_content,
        "has_style": "<style" in vue_content,
        "template_lines": 0,
        "script_lines": 0,
        "style_lines": 0,
    }
    
    # Count lines in each section
    lines = vue_content.split('\n')
    in_template = False
    in_script = False
    in_style = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("<template>"):
            in_template = True
            in_script = False
            in_style = False
        elif stripped.startswith("<script"):
            in_template = False
            in_script = True
            in_style = False
        elif stripped.startswith("<style"):
            in_template = False
            in_script = False
            in_style = True
        elif stripped.startswith("</template>") or (in_template and stripped.startswith("</")):
            if in_template:
                info["template_lines"] += 1
                in_template = False
        elif stripped.startswith("</script>") or (in_script and not stripped.startswith("<") and stripped != ""):
            if in_script and stripped != "":
                info["script_lines"] += 1
        elif stripped.startswith("</style>") or (in_style and not stripped.startswith("<") and stripped != ""):
            if in_style and stripped != "":
                info["style_lines"] += 1
    
    # Simple line count
    info["total_lines"] = len(lines)
    info["template_lines"] = vue_content.count("<template>") + vue_content.count("</template>")
    info["script_lines"] = vue_content.count("<script>") + vue_content.count("</script>")
    info["style_lines"] = vue_content.count("<style")
    
    return info


def match_screenshot_to_page(page_name, screenshots):
    """Match a page name to a screenshot filename using keyword fuzzy matching."""
    # Direct match
    if page_name in screenshots:
        return screenshots[page_name]
    
    # Keyword mapping for common page names
    keyword_map = {
        'index': ['index', '首页', '录入', '书籍录入', '书籍目录', 'home'],
        'notes': ['notes', '笔记', '书评', '书评笔记', 'note'],
        'rank': ['rank', '榜单', '推荐', '推荐榜单', 'ranking'],
        'status': ['status', '状态', '阅读状态', '阅读', 'stat'],
        'home': ['home', '首页', '主页'],
        'detail': ['detail', '详情', '详细'],
        'list': ['list', '列表', '列表页'],
        'search': ['search', '搜索', '查询'],
        'user': ['user', '用户', '我的', '个人'],
        'profile': ['profile', '个人中心', '资料'],
        'cart': ['cart', '购物车', '购物'],
        'order': ['order', '订单'],
        'login': ['login', '登录', '登陆'],
        'register': ['register', '注册'],
    }
    
    # Get keywords for this page
    page_lower = page_name.lower()
    keywords = keyword_map.get(page_lower, [page_lower])
    
    # Add the page name itself to keywords
    keywords = list(set(keywords + [page_lower]))
    
    # Try keyword matching
    for shot_name, shot_path in screenshots.items():
        shot_lower = shot_name.lower()
        for kw in keywords:
            if kw in shot_lower or shot_lower in kw:
                return shot_path
    
    # Try substring matching (partial match)
    for shot_name, shot_path in screenshots.items():
        shot_lower = shot_name.lower()
        # Check if page name is contained in screenshot name or vice versa
        if page_lower in shot_lower or shot_lower in page_lower:
            return shot_path
        # Check any common substring (length >= 2)
        for i in range(2, len(page_lower)):
            substr = page_lower[i:i+3]
            if len(substr) >= 2 and substr in shot_lower:
                return shot_path
    
    # Last resort: try variations with numbers
    variations = [
        f"{page_name}01",
        f"{page_name}02",
        f"{page_name}1",
        f"{page_name}2",
        page_name.replace("index", "01"),
    ]
    
    for var in variations:
        if var in screenshots:
            return screenshots[var]
    
    return None


def generate_markdown(project_path, screenshots_dir, output_dir=None):
    """Generate Markdown documentation."""
    project_name = Path(project_path).name
    
    if output_dir is None:
        output_dir = Path(project_path)
    else:
        output_dir = Path(output_dir)
    
    pages = find_pages(project_path)
    screenshots = find_screenshots(screenshots_dir)
    
    # Build markdown content
    md_lines = [
        "---",
        f'title: "{project_name} - 页面文档"',
        f'author: "Generated by page-doc-generator"',
        f'date: "{__import__("datetime").date.today().isoformat()}"',
        "---",
        "",
        f"# {project_name} - 页面文档",
        "",
        f"**项目路径**: `{project_path}`",
        "",
        f"**截图目录**: `{screenshots_dir}`",
        "",
        f"**页面总数**: {len(pages)}",
        "",
        "---",
        "",
    ]
    
    for page in pages:
        page_name = page["name"]
        vue_path = page["path"]
        vue_content = read_vue_file(vue_path)
        screenshot_path = match_screenshot_to_page(page_name, screenshots)
        
        # Page section
        md_lines.append(f"# 页面：{page_name}")
        md_lines.append("")
        
        # Screenshot
        if screenshot_path:
            md_lines.append(f"## 页面截图")
            md_lines.append("")
            md_lines.append(f"![{page_name}]({screenshot_path.replace(chr(92), '/')})")
            md_lines.append("")
        
        # Page info
        info = extract_page_info(vue_content, page_name)
        md_lines.append(f"## 页面信息")
        md_lines.append("")
        md_lines.append(f"| 项目 | 内容 |")
        md_lines.append(f"|------|------|")
        md_lines.append(f"| 路径 | `{vue_path}` |")
        md_lines.append(f"| 总行数 | {info['total_lines']} |")
        md_lines.append(f"| 模板 | {'是' if info['has_template'] else '否'} |")
        md_lines.append(f"| 脚本 | {'是' if info['has_script'] else '否'} |")
        md_lines.append(f"| 样式 | {'是' if info['has_style'] else '否'} |")
        md_lines.append("")
        
        # Code section
        md_lines.append(f"## 源代码")
        md_lines.append("")
        md_lines.append(f"```vue")
        # Truncate very long files for document
        max_lines = 500
        lines = vue_content.split('\n')
        if len(lines) > max_lines:
            md_lines.append('\n'.join(lines[:max_lines]))
            md_lines.append(f"---\n<!-- 文件过长，已截断，共 {len(lines)} 行 -->\n---")
        else:
            md_lines.append(vue_content)
        md_lines.append("```")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    
    # Add summary
    md_lines.extend([
        "# 页面总览",
        "",
        "| 页面名称 | 截图 | 路径 |",
        "|---------|------|------|",
    ])
    
    for page in pages:
        page_name = page["name"]
        screenshot_path = match_screenshot_to_page(page_name, screenshots)
        has_screenshot = "✅" if screenshot_path else "❌"
        md_lines.append(f"| {page_name} | {has_screenshot} | `{page['path']}` |")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*本文档由 page-doc-generator 自动生成*")
    
    markdown_content = '\n'.join(md_lines)
    
    output_path = output_dir / f"{project_name}_页面文档.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return str(output_path), len(pages), len(screenshots)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) < 3:
        print("Usage: python generate_page_doc.py <project_path> <screenshots_dir> [output_dir]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    screenshots_dir = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"Project: {project_path}")
    print(f"Screenshots: {screenshots_dir}")
    
    output_path, page_count, screenshot_count = generate_markdown(
        project_path, screenshots_dir, output_dir
    )
    
    print(f"\n[OK] Generated: {output_path}")
    print(f"   Pages: {page_count}, Screenshots: {screenshot_count}")
