#!/usr/bin/env python3
"""
UI Design Consultation Script
Usage: python3 design-consult.py "<design request>"
"""

import sys
import json
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/design-config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def analyze_request(request: str):
    """分析设计需求"""
    keywords = {
        'landing_page': ['登录页', 'landing', '首页'],
        'dashboard': ['后台', 'dashboard', '管理'],
        'mobile': ['移动', 'mobile', 'app', '手机'],
        'ecommerce': ['电商', '购物', '商品'],
        'form': ['表单', 'form', '输入'],
        'component': ['组件', 'component', '按钮', '卡片']
    }
    
    detected = []
    request_lower = request.lower()
    for category, words in keywords.items():
        if any(word in request_lower for word in words):
            detected.append(category)
    
    return detected if detected else ['general']

def generate_suggestions(categories: list, config: dict):
    """生成设计建议"""
    suggestions = {
        'landing_page': {
            'layout': '单页滚动布局，突出核心价值主张',
            'components': ['Hero Section', '功能展示', '客户评价', 'CTA 按钮'],
            'colors': '使用品牌主色作为 CTA，保持简洁',
            'tips': '首屏加载速度 < 3 秒，移动端优先'
        },
        'dashboard': {
            'layout': '侧边栏导航 + 内容区域，支持响应式',
            'components': ['数据卡片', '图表', '表格', '筛选器'],
            'colors': '中性色为主，数据可视化使用鲜明色彩',
            'tips': '信息层级清晰，关键指标突出显示'
        },
        'mobile': {
            'layout': '底部导航或汉堡菜单，大触控区域',
            'components': ['底部 TabBar', '卡片列表', '下拉刷新'],
            'colors': '高对比度，户外可视性',
            'tips': '最小触控区域 44x44pt，支持手势操作'
        },
        'general': {
            'layout': '根据内容类型选择合适的布局',
            'components': ['导航', '内容区', '页脚'],
            'colors': config.get('colorPalettes', {}).get('modern', {}),
            'tips': '保持一致性，遵循设计系统规范'
        }
    }
    
    result = []
    for cat in categories:
        if cat in suggestions:
            result.append((cat, suggestions[cat]))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("用法：python3 design-consult.py \"<设计需求>\"")
        print("\n示例:")
        print('  python3 design-consult.py "帮我设计一个登录页面"')
        print('  python3 design-consult.py "后台管理系统界面设计"')
        sys.exit(1)
    
    request = ' '.join(sys.argv[1:])
    config = load_config()
    
    print_header("🎨 UI 设计咨询")
    
    print(f"{Colors.BOLD}设计需求:{Colors.NC} {request}\n")
    
    # 分析需求
    categories = analyze_request(request)
    print(f"{Colors.BOLD}检测类型:{Colors.NC} {', '.join(categories)}\n")
    
    # 生成建议
    suggestions = generate_suggestions(categories, config)
    
    for category, suggestion in suggestions:
        print(f"{Colors.BOLD}{Colors.GREEN}【{category.replace('_', ' ').title()}】{Colors.NC}")
        print(f"  {Colors.CYAN}布局:{Colors.NC} {suggestion['layout']}")
        print(f"  {Colors.CYAN}组件:{Colors.NC} {', '.join(suggestion['components'])}")
        print(f"  {Colors.CYAN}配色:{Colors.NC} {suggestion['colors']}")
        print(f"  {Colors.CYAN}提示:{Colors.NC} {suggestion['tips']}")
        print()
    
    print(f"{Colors.YELLOW}💡 需要更详细的设计方案吗？可以进一步描述具体需求。{Colors.NC}")

if __name__ == '__main__':
    main()
