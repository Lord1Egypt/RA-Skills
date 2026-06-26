#!/usr/bin/env python3
"""
Component Code Generator
Usage: python3 component-gen.py --type button --variant primary
"""

import argparse
import sys
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent

# 组件模板
COMPONENT_TEMPLATES = {
    'button': {
        'primary': '''
<!-- Primary Button -->
<button class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
  按钮文本
</button>

/* Tailwind CSS */
<button className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
  按钮文本
</button>
''',
        'secondary': '''
<!-- Secondary Button -->
<button class="px-6 py-3 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors">
  按钮文本
</button>
''',
        'outline': '''
<!-- Outline Button -->
<button class="px-6 py-3 border-2 border-blue-600 text-blue-600 font-semibold rounded-lg hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
  按钮文本
</button>
'''
    },
    'card': {
        'basic': '''
<!-- Basic Card -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-xl font-semibold text-gray-900 mb-2">卡片标题</h3>
  <p class="text-gray-600">卡片内容描述...</p>
  <button class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
    操作按钮
  </button>
</div>
''',
        'with-image': '''
<!-- Card with Image -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <img src="/image.jpg" alt="卡片图片" class="w-full h-48 object-cover">
  <div class="p-6">
    <h3 class="text-xl font-semibold text-gray-900 mb-2">卡片标题</h3>
    <p class="text-gray-600 mb-4">卡片内容描述...</p>
    <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
      操作按钮
    </button>
  </div>
</div>
'''
    },
    'form': {
        'login': '''
<!-- Login Form -->
<form class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
  <h2 class="text-2xl font-bold text-gray-900 mb-6">登录</h2>
  
  <div class="mb-4">
    <label class="block text-gray-700 text-sm font-medium mb-2" for="email">
      邮箱
    </label>
    <input class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
           type="email" id="email" required>
  </div>
  
  <div class="mb-6">
    <label class="block text-gray-700 text-sm font-medium mb-2" for="password">
      密码
    </label>
    <input class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
           type="password" id="password" required>
  </div>
  
  <button class="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700">
    登录
  </button>
</form>
'''
    }
}

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def generate_component(component_type: str, variant: str):
    """生成组件代码"""
    if component_type not in COMPONENT_TEMPLATES:
        return None
    
    variants = COMPONENT_TEMPLATES[component_type]
    if variant not in variants:
        return None
    
    return variants[variant]

def main():
    parser = argparse.ArgumentParser(description='生成 UI 组件代码')
    parser.add_argument('--type', type=str, required=True,
                       help=f'组件类型 (button, card, form)')
    parser.add_argument('--variant', type=str, default='primary',
                       help='组件变体')
    args = parser.parse_args()
    
    print_header("🧩 UI 组件生成器")
    
    code = generate_component(args.type, args.variant)
    
    if not code:
        print(f"{Colors.RED}未找到组件：{args.type} - {args.variant}{Colors.NC}")
        print(f"\n可用组件:")
        for comp_type, variants in COMPONENT_TEMPLATES.items():
            print(f"  {comp_type}: {', '.join(variants.keys())}")
        sys.exit(1)
    
    print(f"{Colors.BOLD}组件类型:{Colors.NC} {args.type}")
    print(f"{Colors.BOLD}变体:{Colors.NC} {args.variant}")
    print()
    
    print(f"{Colors.BOLD}{Colors.GREEN}HTML/Tailwind CSS:{Colors.NC}")
    print(code)
    
    print(f"\n{Colors.YELLOW}💡 提示：可以根据需要调整样式和结构{Colors.NC}")

if __name__ == '__main__':
    main()
