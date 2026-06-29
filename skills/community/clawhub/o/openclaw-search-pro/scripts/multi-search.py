#!/usr/bin/env python3
"""
Multi-Engine Search Script
Usage: python3 multi-search.py "搜索关键词" [--all-engines]

特点：
  ✅ 无需 API Key
  ✅ 安装即用
  ✅ 国内可访问
"""

import argparse
import sys
from pathlib import Path

# 修复Windows GBK编码兼容问题
if sys.platform.startswith('win'):
    try:
        # Python 3.7+ 支持 reconfigure
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # 旧版本Python兼容
        import io
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

# 导入免费搜索引擎
sys.path.insert(0, str(Path(__file__).parent))
from free_search import FreeSearch

class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def main():
    parser = argparse.ArgumentParser(description='多引擎搜索 - 无需 API Key')
    parser.add_argument('query', type=str, help='搜索关键词')
    parser.add_argument('--max-results', type=int, default=10, help='最大结果数')
    parser.add_argument('--engine', type=str, choices=['free', 'bing-cn', 'sogou', 'so360'], default='free', help='指定引擎')
    args = parser.parse_args()
    
    print_header("🔍 Search Pro - 免费搜索引擎")
    
    # 创建免费搜索引擎实例
    search_engine = FreeSearch()
    
    # 执行搜索
    print(f"{Colors.BOLD}搜索：{args.query}{Colors.NC}")
    print(f"{Colors.BOLD}最大结果：{args.max_results}{Colors.NC}")
    print(f"{Colors.BOLD}引擎：{args.engine}（无需 API Key）{Colors.NC}\n")
    
    results = search_engine.search(args.query, max_results=args.max_results)
    
    if not results:
        print(f"{Colors.YELLOW}未找到结果{Colors.NC}")
        print(f"\n{Colors.CYAN}提示：{Colors.NC}")
        print("  - 检查网络连接")
        print("  - 尝试其他关键词")
        print("  - 如果配置了 API Key，可以使用 --engine baidu 等引擎")
        return
    
    # 按引擎分组统计
    engine_stats = {}
    for result in results:
        engine = result.get('engine', 'unknown')
        engine_stats[engine] = engine_stats.get(engine, 0) + 1
    
    print(f"{Colors.GREEN}找到 {len(results)} 个结果:{Colors.NC}")
    for engine, count in engine_stats.items():
        print(f"  {engine}: {count} 个")
    print()
    
    # 显示结果
    for i, result in enumerate(results, 1):
        print(f"{Colors.BOLD}{i}. {result['title']}{Colors.NC}")
        print(f"   链接：{Colors.CYAN}{result['url']}{Colors.NC}")
        print(f"   来源：{Colors.YELLOW}{result['engine']}{Colors.NC}")
        print(f"   评分：{result['score']}")
        if result.get('content'):
            content = result['content'][:200] + '...' if len(result.get('content', '')) > 200 else result.get('content', '')
            print(f"   摘要：{content}")
        print()

if __name__ == '__main__':
    main()
