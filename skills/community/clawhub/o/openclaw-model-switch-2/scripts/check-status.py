#!/usr/bin/env python3
"""
Check Status Script
Usage: python3 check-status.py
"""

import json
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/models.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    if not CONFIG_FILE.exists():
        print(f"{Colors.YELLOW}配置文件不存在：{CONFIG_FILE}{Colors.NC}")
        return
    
    config = load_json(CONFIG_FILE)
    current = config.get('current', '未设置')
    models = config.get('models', {})
    
    print(f"{Colors.BOLD}当前模型:{Colors.NC} {Colors.GREEN}{current}{Colors.NC}")
    
    current_info = models.get(current, {})
    if current_info:
        print(f"{Colors.BOLD}提供商:{Colors.NC} {current_info.get('provider', 'N/A')}")
        print(f"{Colors.BOLD}模型 ID:{Colors.NC} {current_info.get('modelId', 'N/A')}")
        images = "✅" if current_info.get('supportsImages', False) else "❌"
        print(f"{Colors.BOLD}支持图片:{Colors.NC} {images}")
    else:
        print(f"{Colors.YELLOW}⚠️  模型信息不存在{Colors.NC}")
    
    print(f"\n{Colors.BOLD}可用模型:{Colors.NC} {len(models)} 个")

if __name__ == '__main__':
    main()
