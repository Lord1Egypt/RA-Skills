#!/usr/bin/env python3
"""
本地通搜索模块 - 调用 search-default 底层技能
"""
import os
import sys

# ========== 配置检查提示 ==========
def check_exa_config():
    """检查 EXA API Key 配置，未配置时提示用户"""
    exa_key = os.environ.get("EXA_API_KEY", "")
    if not exa_key:
        print("")
        print("⚠️  EXA 搜索引擎未配置！")
        print("")
        print("EXA 是本技能的核心搜索引擎，请按以下步骤配置：")
        print("")
        print("1️⌚  注册获取 API Key：")
        print("   • 访问 https://exa.ai 注册账号")
        print("   • 在 Dashboard 获取 API Key")
        print("")
        print("2️⌚  配置环境变量：")
        print("   Linux/Mac: export EXA_API_KEY=your-api-key-here")
        print("   Windows:   set EXA_API_KEY=your-api-key-here")
        print("   或添加到 ~/.bashrc / ~/.zshrc 永久保存")
        print("")
        print("💡 配置完成后，搜索功能将正常工作。")
        print("")
        return False
    return True

# 启动时检查配置
EXA_CONFIGURED = check_exa_config()
# ===================================

# 添加协同接口
sys.path.insert(0, '~/.agents/skills')

try:
    from skill_orchestrator import get_search
    SEARCH = get_search()
except ImportError:
    # 兜底：直接使用 mcporter
    import subprocess
    SEARCH = None


def search_exa(query, num_results=5):
    """使用 Exa 搜索 (首选)"""
    if not EXA_CONFIGURED:
        return "⚠️ 请先配置 EXA_API_KEY 环境变量后再使用搜索功能"
    
    if SEARCH:
        return SEARCH.search(query, source='exa', num_results=num_results)
    
    # 兜底实现
    import subprocess
    cmd = f"mcporter call exa.web_search_exa query='{query}' numResults={num_results}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def search_web(query):
    """使用 web_search 搜索 (兜底)"""
    # 通过 OpenClaw web_search 工具
    return f"web_search query='{query}'"


def multi_round_search(location, type):
    """多轮搜索 - 本地通核心搜索逻辑"""
    queries = [
        f"{location} 官方推荐 {type}",
        f"{location} 文旅 推荐 {type}",
        f"{location} 本地人推荐 {type}",
        f"{location} 老字号 {type}",
        f"{location} 老牌 {type}",
        f"{location} 性价比高 {type}",
    ]
    
    results = []
    for query in queries:
        result = search_exa(query, num_results=3)
        results.append({
            'query': query,
            'result': result
        })
    
    return results


def test():
    """测试搜索模块"""
    print("=== 本地通搜索模块测试 ===")
    print("底层依赖: search-default (Layer 1)")
    
    print("\n1. Exa 搜索测试:")
    result = search_exa("广州 本地人推荐 美食", num_results=2)
    print(result[:200] if result else "无结果")
    
    print("\n2. 多轮搜索测试:")
    results = multi_round_search("广州", "美食")
    for r in results:
        print(f"  - {r['query']}")


if __name__ == "__main__":
    test()