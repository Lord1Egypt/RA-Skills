#!/usr/bin/env python3
"""
RedNote (小红书) Cover Image Generator
Generate 1080x1440 cover images for GitHub repository promotion.
"""

import os
import sys
import re
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, List

# RedNote standard cover size
COVER_WIDTH = 1080
COVER_HEIGHT = 1440

# Color schemes for different languages/tech stacks (Light theme)
COLOR_SCHEMES = {
    'python': {'bg': '#E8F4F8', 'accent': '#306998', 'text': '#1a1a2e', 'secondary': '#FFD43B'},
    'javascript': {'bg': '#FFF9E6', 'accent': '#F7DF1E', 'text': '#323330', 'secondary': '#F7DF1E'},
    'typescript': {'bg': '#E8F1FA', 'accent': '#3178C6', 'text': '#1a1a2e', 'secondary': '#3178C6'},
    'go': {'bg': '#E6F7FA', 'accent': '#00ADD8', 'text': '#1a1a2e', 'secondary': '#CE3262'},
    'rust': {'bg': '#FFE8E6', 'accent': '#CE422B', 'text': '#1a1a2e', 'secondary': '#CE422B'},
    'java': {'bg': '#E8F4F8', 'accent': '#007396', 'text': '#1a1a2e', 'secondary': '#F8981D'},
    'cpp': {'bg': '#E6EEFA', 'accent': '#00599C', 'text': '#1a1a2e', 'secondary': '#00599C'},
    'c': {'bg': '#F0F4F8', 'accent': '#A8B9CC', 'text': '#1a1a2e', 'secondary': '#283593'},
    'ruby': {'bg': '#FFE8E8', 'accent': '#CC342D', 'text': '#1a1a2e', 'secondary': '#CC342D'},
    'php': {'bg': '#F0E8F8', 'accent': '#777BB4', 'text': '#1a1a2e', 'secondary': '#777BB4'},
    'swift': {'bg': '#FFE8E6', 'accent': '#F05138', 'text': '#1a1a2e', 'secondary': '#F05138'},
    'kotlin': {'bg': '#F0E8FF', 'accent': '#7F52FF', 'text': '#1a1a2e', 'secondary': '#7F52FF'},
    'default': {'bg': '#F8F9FA', 'accent': '#e94560', 'text': '#1a1a2e', 'secondary': '#e94560'}
}


def get_color_scheme(language: Optional[str]) -> Dict[str, str]:
    """Get color scheme based on programming language."""
    if not language:
        return COLOR_SCHEMES['default']
    
    lang_lower = language.lower()
    lang_map = {
        'python': 'python',
        'javascript': 'javascript', 'js': 'javascript',
        'typescript': 'typescript', 'ts': 'typescript',
        'go': 'go', 'golang': 'go',
        'rust': 'rust',
        'java': 'java',
        'c++': 'cpp', 'cpp': 'cpp',
        'c': 'c',
        'ruby': 'ruby',
        'php': 'php',
        'swift': 'swift',
        'kotlin': 'kotlin'
    }
    mapped = lang_map.get(lang_lower, 'default')
    return COLOR_SCHEMES.get(mapped, COLOR_SCHEMES['default'])


def format_stars(stars: int) -> str:
    """Format stars count for display."""
    if stars >= 1000:
        return f"{stars/1000:.1f}k"
    elif stars >= 100:
        return str(stars)
    return ""


def should_show_stars(stars: int) -> bool:
    return stars >= 100


def truncate_text(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def extract_key_points(article_text: str, max_points: int = 4) -> List[str]:
    """Extract practical key points from article text for image display.
    
    Prioritizes:
    1. Installation instructions
    2. Usage examples/commands
    3. Feature descriptions with specific functionality
    4. Results/effects of using the tool
    """
    points = []
    
    # Priority patterns for valuable content
    priority_patterns = [
        # Installation patterns
        r'(?:pip install|npm install|yarn add|cargo install|go get|brew install|apt install)[^\n]+',
        # Usage/command patterns
        r'(?:python|npm|yarn|cargo|go|docker|kubectl)[^\n]+(?:run|start|serve|deploy|exec)[^\n]*',
        # Feature patterns with specific actions
        r'(?:支持|提供|可以|能够|自动|一键|快速|实时)[^\n]{5,40}',
        # Effect/result patterns
        r'(?:生成|输出|显示|分析|计算|导出)[^\n]{5,40}',
    ]
    
    # First pass: look for high-value patterns
    for pattern in priority_patterns:
        matches = re.findall(pattern, article_text, re.IGNORECASE)
        for match in matches:
            clean = match.strip()
            # Remove excessive emoji and normalize
            clean = re.sub(r'[🔥💡⚡️🚀📌🎯💻📊🔍📈🟢🟡🔴⭐✨🎉]+', '', clean)
            clean = clean.strip()
            if len(clean) > 8 and len(clean) < 45 and clean not in points:
                points.append(clean)
                if len(points) >= max_points:
                    return points
    
    # Second pass: look for bullet points with specific content
    bullet_pattern = r'[•\-\*]\s*([^\n]+)'
    matches = re.findall(bullet_pattern, article_text)
    
    for match in matches:
        clean = match.strip()
        # Remove excessive emoji
        clean = re.sub(r'[🔥💡⚡️🚀📌🎯💻📊🔍📈🟢🟡🔴⭐✨🎉]+', '', clean)
        clean = clean.strip()
        
        # Skip generic/empty phrases
        skip_patterns = [
            r'^(OpenClaw|GitHub|开源|技术|项目|工具)',
            r'^(学习|了解|掌握|熟悉)',
            r'^(适用|适合|针对|面向)',
            r'^(功能强大|易于使用|值得关注)',
        ]
        if any(re.match(p, clean, re.IGNORECASE) for p in skip_patterns):
            continue
            
        if len(clean) > 8 and len(clean) < 45 and clean not in points:
            points.append(clean)
            if len(points) >= max_points:
                return points
    
    # Third pass: look for numbered lists
    numbered_pattern = r'\d+\.\s*([^\n]+)'
    matches = re.findall(numbered_pattern, article_text)
    
    for match in matches:
        clean = match.strip()
        clean = re.sub(r'[🔥💡⚡️🚀📌🎯💻📊🔍📈🟢🟡🔴⭐✨🎉]+', '', clean)
        clean = clean.strip()
        
        if len(clean) > 8 and len(clean) < 45 and clean not in points:
            points.append(clean)
            if len(points) >= max_points:
                return points
    
    # Final fallback: extract from sections
    if not points:
        # Look for content after specific section headers
        section_patterns = [
            r'(?:安装|使用|功能|特性)[：:]\s*\n?([^\n]{10,40})',
            r'```[^`]*```',  # Code blocks
        ]
        for pattern in section_patterns:
            matches = re.findall(pattern, article_text)
            for match in matches[:2]:
                clean = match.strip().replace('```', '')
                if len(clean) > 8 and len(clean) < 45:
                    points.append(clean)
                    if len(points) >= max_points:
                        return points
    
    return points[:max_points]


def generate_svg_cover(repo_data: dict, output_path: str, article_text: str = "") -> Optional[str]:
    """
    Generate SVG cover image.
    
    Args:
        repo_data: Repository data dictionary
        output_path: Path to save the image
        article_text: Full article text to extract key points from
    """
    colors = get_color_scheme(repo_data.get('language'))
    
    repo_name = repo_data.get('repo', 'Unknown')
    description = repo_data.get('description', '')
    language = repo_data.get('language', 'Unknown') or 'Unknown'
    stars = repo_data.get('stars', 0)
    github_url = repo_data.get('url', '') or f"github.com/{repo_data.get('owner', '')}/{repo_name}"
    
    # Escape XML special chars
    display_name = escape_xml(truncate_text(repo_name, 22))
    desc_text = escape_xml(truncate_text(description, 80))
    lang_text = escape_xml(language)
    
    # Extract key points from article
    key_points = extract_key_points(article_text, 4)
    
    # Stars display
    stars_badge = ""
    stars_section = ""
    if should_show_stars(stars):
        stars_formatted = format_stars(stars)
        stars_badge = f"⭐ {stars_formatted} stars"
        stars_section = f'''<rect x="390" y="680" width="300" height="60" rx="30" fill="#FFD700"/>
  <text x="540" y="720" font-family="Arial, sans-serif" font-size="28" 
        font-weight="bold" fill="#1a1a2e" text-anchor="middle">{stars_badge}</text>'''
    
    # Build key points section - use Chinese font
    points_y_start = 880
    points_section = ""
    for i, point in enumerate(key_points):
        y_pos = points_y_start + (i * 60)
        escaped_point = escape_xml(truncate_text(point, 40))
        points_section += f'''<text x="100" y="{y_pos}" font-family="WenQuanYi Zen Hei, Noto Sans CJK SC, Arial, sans-serif" 
        font-size="28" fill="rgba(0,0,0,0.8)">• {escaped_point}</text>
'''
    
    # If no key points, show description instead
    if not points_section:
        points_section = f'''<text x="540" y="900" font-family="WenQuanYi Zen Hei, Noto Sans CJK SC, Arial, sans-serif" 
        font-size="28" fill="rgba(0,0,0,0.7)" text-anchor="middle">{desc_text}</text>'''
    
    # Font family for Chinese text
    chinese_font = "WenQuanYi Zen Hei, Noto Sans CJK SC, Arial, sans-serif"
    
    # Light theme colors
    text_color = colors['text']
    accent_color = colors['accent']
    bg_color = colors['bg']
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{COVER_WIDTH}" height="{COVER_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="50%" style="stop-color:#FFFFFF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:{bg_color};stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#bgGrad)"/>
  
  <!-- Subtle grid pattern -->
  <g stroke="rgba(0,0,0,0.05)" stroke-width="1">
    {' '.join([f'<line x1="{i}" y1="0" x2="{i}" y2="{COVER_HEIGHT}"/>' for i in range(40, COVER_WIDTH, 80)])}
    {' '.join([f'<line x1="0" y1="{i}" x2="{COVER_WIDTH}" y2="{i}"/>' for i in range(40, COVER_HEIGHT, 80)])}
  </g>
  
  <!-- Top accent line -->
  <rect x="60" y="80" width="120" height="6" fill="{accent_color}" rx="3"/>
  
  <!-- GitHub icon circle -->
  <circle cx="180" cy="200" r="70" fill="rgba(0,0,0,0.05)"/>
  <circle cx="180" cy="210" r="45" fill="{accent_color}"/>
  <circle cx="180" cy="220" r="30" fill="{bg_color}"/>
  
  <!-- Main title -->
  <text x="540" y="400" font-family="{chinese_font}" 
        font-size="64" font-weight="bold" fill="{text_color}" text-anchor="middle">
    {display_name}
  </text>
  
  <!-- Description subtitle -->
  <text x="540" y="480" font-family="{chinese_font}" 
        font-size="28" fill="rgba(0,0,0,0.6)" text-anchor="middle">
    {desc_text}
  </text>
  
  <!-- OpenClaw Logo Badge -->
  <rect x="390" y="540" width="300" height="50" rx="25" fill="{accent_color}"/>
  <!-- Claw icon -->
  <g transform="translate(420, 555)">
    <path d="M5,10 Q0,5 5,0 Q10,5 5,10 M8,8 Q12,12 8,16 Q4,12 8,8" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="1.5"/>
  </g>
  <text x="540" y="573" font-family="{chinese_font}" font-size="20" 
        font-weight="bold" fill="#FFFFFF" text-anchor="middle">
    OpenClaw Skill
  </text>
  
  <!-- Stars badge -->
  {stars_section}
  
  <!-- Divider line -->
  <line x1="80" y1="800" x2="1000" y2="800" stroke="{accent_color}" stroke-width="2" opacity="0.5"/>
  
  <!-- Key points section -->
  {points_section}
  
  <!-- GitHub URL -->
  <text x="540" y="1220" font-family="Courier New, monospace" 
        font-size="20" fill="{accent_color}" text-anchor="middle">
    {github_url}
  </text>
  
  <!-- Bottom decoration -->
  <line x1="80" y1="1250" x2="1000" y2="1250" stroke="{accent_color}" stroke-width="2" opacity="0.5"/>
  
  <!-- Code decoration -->
  <text x="80" y="1300" font-family="Courier New, monospace" 
        font-size="22" fill="rgba(0,0,0,0.3)">const awesome = true;</text>
  <text x="80" y="1335" font-family="Courier New, monospace" 
        font-size="22" fill="rgba(0,0,0,0.3)">#GitHub #OpenSource</text>
  
  <!-- Corner decoration -->
  <circle cx="980" cy="1340" r="35" fill="{accent_color}" opacity="0.8"/>
  <circle cx="980" cy="1340" r="22" fill="{bg_color}"/>
</svg>'''
    
    # Save SVG
    svg_path = output_path.replace('.png', '.svg')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    # Convert SVG to PNG
    return convert_svg_to_png(svg_path, output_path)


def convert_svg_to_png(svg_path: str, output_path: str) -> Optional[str]:
    """Convert SVG to PNG using available tools."""
    
    # Try using cairosvg first
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=output_path, 
                        output_width=COVER_WIDTH, output_height=COVER_HEIGHT)
        if os.path.exists(output_path):
            os.unlink(svg_path)
            return output_path
    except Exception as e:
        print(f"  cairosvg failed: {e}")
    
    # Try using ImageMagick with proper font configuration
    try:
        # Set up font config to handle Chinese
        env = os.environ.copy()
        result = subprocess.run(
            ['convert', '-background', 'none', svg_path, 
             '-resize', f'{COVER_WIDTH}x{COVER_HEIGHT}!', 
             '-density', '150',
             output_path],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode == 0 and os.path.exists(output_path):
            os.unlink(svg_path)
            return output_path
        else:
            print(f"  ImageMagick stderr: {result.stderr[:200]}")
    except Exception as e:
        print(f"  ImageMagick failed: {e}")
    
    # Try using Inkscape
    try:
        result = subprocess.run(
            ['inkscape', svg_path, '--export-type=png', 
             f'--export-filename={output_path}',
             f'--export-width={COVER_WIDTH}', f'--export-height={COVER_HEIGHT}',
             '--export-dpi=150'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and os.path.exists(output_path):
            os.unlink(svg_path)
            return output_path
    except Exception as e:
        print(f"  Inkscape failed: {e}")
    
    # Fallback: return SVG path
    print(f"  PNG conversion unavailable, saved SVG: {svg_path}")
    return svg_path


def generate_cover_image(repo_data: dict, output_dir: str = ".", article_text: str = "") -> Optional[str]:
    """
    Generate RedNote cover image for a GitHub repository.
    
    Args:
        repo_data: Repository data dictionary
        output_dir: Directory to save the image
        article_text: Full article text to extract content from
    
    Returns:
        Path to the generated image file, or None if generation failed
    """
    repo_name = repo_data.get('repo', 'unknown')
    output_path = os.path.join(output_dir, f"{repo_name}_cover.png")
    
    return generate_svg_cover(repo_data, output_path, article_text)


def main():
    """CLI test for image generator."""
    test_repo = {
        'repo': 'stock-pe-pb-analyzer-skill',
        'description': '股票PE/PB历史水位分析器 - OpenClaw Skill',
        'language': 'Python',
        'stars': 0
    }
    
    test_article = """🔥 stock-pe-pb-analyzer-skill - 股票PE/PB历史水位分析器 - OpenClaw Skill

💻 Python

📌 这是什么
股票PE/PB历史水位分析器 - OpenClaw Skill

🎯 适用场景
• 开发者寻找相关工具和解决方案
• 学习 Python 和开源技术
• 技术实践参考和代码示例

⚡ 核心功能
• 🔍 智能股票搜索：支持通过股票名称或代码查询
• 📈 多周期分析：自动计算 10年、5年、3年、1年 的历史水位
• 🎯 可视化评级：低估/适中/偏高
• 📊 详细统计：最低、最高、中位数、平均值
• 💾 数据导出：支持导出CSV格式

💡 技术亮点
• 使用 Python 开发
• 基于 BaoStock 数据源
• 开源免费，社区驱动
"""
    
    print("Generating test cover image...")
    result = generate_cover_image(test_repo, ".", test_article)
    
    if result:
        print(f"✓ Generated: {result}")
    else:
        print("✗ Generation failed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
