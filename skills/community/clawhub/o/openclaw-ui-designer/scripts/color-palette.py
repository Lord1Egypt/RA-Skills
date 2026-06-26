#!/usr/bin/env python3
"""
Color Palette Generator
Usage: python3 color-palette.py [--style modern] [--primary blue]
"""

import argparse
import sys
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent

# 预定义配色方案
COLOR_PALETTES = {
    'modern': {
        'primary': '#3B82F6',
        'secondary': '#10B981',
        'accent': '#F59E0B',
        'neutral': '#6B7280',
        'background': '#FFFFFF',
        'surface': '#F3F4F6',
        'text': '#1F2937'
    },
    'minimal': {
        'primary': '#000000',
        'secondary': '#6B7280',
        'accent': '#EF4444',
        'neutral': '#9CA3AF',
        'background': '#FFFFFF',
        'surface': '#F9FAFB',
        'text': '#111827'
    },
    'bold': {
        'primary': '#DC2626',
        'secondary': '#7C3AED',
        'accent': '#F59E0B',
        'neutral': '#1F2937',
        'background': '#FFFFFF',
        'surface': '#FEF3C7',
        'text': '#111827'
    },
    'corporate': {
        'primary': '#1E3A8A',
        'secondary': '#059669',
        'accent': '#D97706',
        'neutral': '#6B7280',
        'background': '#FFFFFF',
        'surface': '#F8FAFC',
        'text': '#1E293B'
    },
    'playful': {
        'primary': '#EC4899',
        'secondary': '#8B5CF6',
        'accent': '#10B981',
        'neutral': '#6B7280',
        'background': '#FFF1F2',
        'surface': '#F3E8FF',
        'text': '#831843'
    },
    'luxury': {
        'primary': '#1F2937',
        'secondary': '#D4AF37',
        'accent': '#B91C1C',
        'neutral': '#9CA3AF',
        'background': '#FAFAFA',
        'surface': '#F5F5F5',
        'text': '#111827'
    }
}

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def print_color(name: str, hex: str):
    """打印颜色样本"""
    # ANSI 256 色近似
    print(f"  {Colors.BOLD}{name}:{Colors.NC} {hex}")

def generate_palette(style: str, primary: str = None):
    """生成配色方案"""
    if style not in COLOR_PALETTES:
        print(f"{Colors.YELLOW}未知风格：{style}{Colors.NC}")
        print(f"可用风格：{', '.join(COLOR_PALETTES.keys())}")
        return None
    
    palette = COLOR_PALETTES[style].copy()
    
    if primary:
        # 覆盖主色
        primary_colors = {
            'blue': '#3B82F6',
            'green': '#10B981',
            'red': '#DC2626',
            'purple': '#7C3AED',
            'orange': '#F59E0B',
            'pink': '#EC4899',
            'indigo': '#4F46E5',
            'teal': '#14B8A6'
        }
        if primary.lower() in primary_colors:
            palette['primary'] = primary_colors[primary.lower()]
    
    return palette

def main():
    parser = argparse.ArgumentParser(description='生成配色方案')
    parser.add_argument('--style', type=str, default='modern',
                       help=f'设计风格 (default: modern). 可用：{", ".join(COLOR_PALETTES.keys())}')
    parser.add_argument('--primary', type=str, default=None,
                       help=f'主色 (blue, green, red, purple, orange, pink, indigo, teal)')
    args = parser.parse_args()
    
    print_header("🎨 配色方案生成器")
    
    palette = generate_palette(args.style, args.primary)
    
    if not palette:
        sys.exit(1)
    
    print(f"{Colors.BOLD}风格:{Colors.NC} {args.style}")
    if args.primary:
        print(f"{Colors.BOLD}主色:{Colors.NC} {args.primary}")
    print()
    
    print(f"{Colors.BOLD}{Colors.CYAN}配色方案:{Colors.NC}\n")
    
    for name, hex in palette.items():
        print_color(name.title(), hex)
    
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}CSS 变量:{Colors.NC}\n")
    print(":root {")
    for name, hex in palette.items():
        print(f"  --color-{name}: {hex};")
    print("}")
    
    print()
    print(f"{Colors.YELLOW}💡 提示：可以使用 --style 和 --primary 参数自定义配色{Colors.NC}")

if __name__ == '__main__':
    main()
