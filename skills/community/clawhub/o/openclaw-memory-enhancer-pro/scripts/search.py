#!/usr/bin/env python3
"""
Memory Search Script
Usage: python3 search.py "<search query>"
"""

import sys
import os
from pathlib import Path
from datetime import datetime

class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"

def search_files(query: str):
    """搜索记忆文件"""
    results = []
    
    # 搜索 MEMORY.md
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if query.lower() in content.lower():
                results.append(("MEMORY.md", "长期记忆"))
    
    # 搜索每日日志
    if MEMORY_DIR.exists():
        for file in MEMORY_DIR.glob("*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append((f"memory/{file.name}", "每日日志"))
    
    # 搜索 SESSION-STATE.md
    session_file = WORKSPACE / "SESSION-STATE.md"
    if session_file.exists():
        with open(session_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if query.lower() in content.lower():
                results.append(("SESSION-STATE.md", "当前状态"))
    
    return results

def main():
    if len(sys.argv) < 2:
        print("用法：python3 search.py \"<搜索关键词>\"")
        print("\n示例:")
        print('  python3 search.py "飞书配置"')
        print('  python3 search.py "API Key"')
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    
    print(f"\n{Colors.BOLD}🔍 搜索：{query}{Colors.NC}\n")
    
    results = search_files(query)
    
    if not results:
        print(f"{Colors.YELLOW}未找到相关内容{Colors.NC}")
        return
    
    print(f"{Colors.GREEN}找到 {len(results)} 个结果:{Colors.NC}\n")
    
    for file, type_ in results:
        print(f"  {Colors.CYAN}{file}{Colors.NC} ({type_})")
    
    print()

if __name__ == '__main__':
    main()
