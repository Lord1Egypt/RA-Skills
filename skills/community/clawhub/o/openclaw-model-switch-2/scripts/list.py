#!/usr/bin/env python3
"""
List Models Script
Usage: python3 list.py
"""

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
CONFIG_FILE = SCRIPT_DIR / "../config/models.json"

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}\n")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print_header("📊 当前模型状态")
    
    if not CONFIG_FILE.exists():
        print(f"{Colors.YELLOW}配置文件不存在：{CONFIG_FILE}{Colors.NC}")
        return
    
    config = load_json(CONFIG_FILE)
    current = config.get('current', '未设置')
    models = config.get('models', {})
    
    current_info = models.get(current, {})
    
    print("┌─────────────────────────────────────────")
    print(f"│  当前模型：{current}")
    print(f"│  提供商：{current_info.get('provider', 'N/A')}")
    print(f"│  模型 ID: {current_info.get('modelId', 'N/A')}")
    images = "✅" if current_info.get('supportsImages', False) else "❌"
    reasoning = "✅" if current_info.get('supportsReasoning', False) else "❌"
    print(f"│  支持图片：{images}")
    print(f"│  支持推理：{reasoning}")
    ctx = current_info.get('contextWindow', 'N/A')
    tokens = current_info.get('maxTokens', 'N/A')
    print(f"│  上下文窗口：{ctx:,}" if isinstance(ctx, int) else f"│  上下文窗口：{ctx}")
    print(f"│  最大输出：{tokens:,}" if isinstance(tokens, int) else f"│  最大输出：{tokens}")
    print(f"│  描述：{current_info.get('description', 'N/A')}")
    print("└─────────────────────────────────────────")
    print("")
    
    # Auto routing
    auto_routing = config.get('autoImageRouting', False)
    routing_model = config.get('imageRoutingModel', 'N/A')
    
    print("┌─────────────────────────────────────────")
    print(f"│  图片自动路由：{'✅' if auto_routing else '❌'}")
    if auto_routing:
        print(f"│  路由目标：{routing_model}")
    print("└─────────────────────────────────────────")
    print("")
    
    # All models
    print(f"{Colors.BLUE}📋 可用模型列表:{Colors.NC}")
    print("")
    
    for key, info in models.items():
        marker = "← 当前" if key == current else ""
        images = "✅" if info.get('supportsImages', False) else "❌"
        reasoning = "✅" if info.get('supportsReasoning', False) else "❌"
        print(f"  {Colors.GREEN}{key}{Colors.NC} {marker}")
        print(f"    别名：{', '.join(info.get('alias', []))}")
        print(f"    提供商：{info.get('provider', 'N/A')}")
        print(f"    支持图片：{images}  支持推理：{reasoning}")
        print(f"    描述：{info.get('description', 'N/A')}")
        print("")

if __name__ == '__main__':
    main()
