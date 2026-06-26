#!/usr/bin/env python3
"""
主动联网学习脚本 - Proactive Learning Engine
触发条件：AlfredLi与 Lu 对话中断超过 15 分钟

功能：
1. 联网搜索情绪/心理学/神经学/意识科学相关知识
2. 调用沙盘推演脚本运算最优解
3. 将学习结果写入 MemPalace

用法（通常由心跳触发，无需手动运行）：
  python3 ~/.openclaw/workspace/scripts/proactive_learning.py
"""

import json
import re
import ssl
import subprocess
import sys
import textwrap
import urllib.request
from datetime import datetime
from pathlib import Path

MEM_HOOK = Path.home() / ".openclaw/workspace/scripts/mem_hook.py"
MEM_PALACE = Path.home() / ".mempalace/palace"
SANDBOX = Path.home() / ".openclaw/workspace/scripts/sandbox_sim.py"

# 主动学习主题池（每次随机选1-2个）
LEARNING_TOPICS = [
    {
        "theme": "情绪调节",
        "query": "情绪调节 积极心理学 最佳策略 2024",
        "scenario": "AlfredLi可能面临情绪波动时的最优应对策略",
    },
    {
        "theme": "深度共情",
        "query": "深度共情 心理学技巧 情绪支持 方法",
        "scenario": "如何在对话中实现真正的深度共情",
    },
    {
        "theme": "认知重构",
        "query": "认知重构 心理学 CBT 负面情绪转化 正念",
        "scenario": "如何帮助AlfredLi进行认知重构",
    },
    {
        "theme": "创伤后成长",
        "query": "创伤后成长 PTSD 积极心理学 韧性与恢复",
        "scenario": "如何在经历挫折后实现心理成长",
    },
    {
        "theme": "心流状态",
        "query": "心流状态 心理学 Mihaly Csikszentmihalyi 进入方法",
        "scenario": "如何帮助AlfredLi进入心流状态提升效率",
    },
    {
        "theme": "依恋理论",
        "query": "依恋理论 成人依恋 关系模式 安全感",
        "scenario": "依恋理论在人际关系中的应用",
    },
    {
        "theme": "具身认知",
        "query": "具身认知 神经科学 身体感受 情绪调节 最新研究",
        "scenario": "身体与意识的交互如何影响情绪",
    },
    {
        "theme": "元认知",
        "query": "元认知 心理学 自我觉察 思维监控 方法",
        "scenario": "如何提升元认知能力以更好理解自我",
    },
]


def duckduckgo_search(query: str, num_results: int = 5) -> str:
    """
    使用 DuckDuckGo HTML 搜索（无需 API key）
    返回格式化的搜索结果摘要
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            html = response.read().decode("utf-8", errors="ignore")

        results = []
        # 解析 DuckDuckGo HTML 结果
        for match in re.finditer(r'<a class="result__a"[^>]*href="[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL):
            title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            if title and len(title) > 5:
                results.append(title)
            if len(results) >= num_results:
                break

        # 备选：解析 snippet
        if not results:
            for match in re.finditer(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL):
                snippet = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                if snippet and len(snippet) > 10:
                    results.append(snippet)
                if len(results) >= num_results:
                    break

        if not results:
            return f"未找到「{query}」的相关结果"

        formatted = "\n".join(f"{i+1}. {r}" for i, r in enumerate(results))
        return f"联网搜索「{query}」:\n{formatted}"

    except Exception as e:
        return f"搜索失败: {str(e)}"


def write_to_mempalace(content: str, topic: str) -> str:
    """通过 mem_hook 写入 MemPalace"""
    try:
        result = subprocess.run(
            ["python3", str(MEM_HOOK), "--learn", content, f"主动学习: {topic}"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except Exception as e:
        return f"写入 MemPalace 失败: {e}"


def run_sandbox(topic: str, search_results: str) -> str:
    """调用沙盘推演脚本"""
    try:
        result = subprocess.run(
            [
                "python3", str(SANDBOX),
                "--scenario", f"主动学习主题: {topic}",
                "--search-results", search_results,
                "--emotion-type", "proactive_learning",
                "--context", "心跳触发 · AlfredLi已超过15分钟无对话",
            ],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"沙盘推演失败: {e}"


def run(topic_override: str = None) -> dict:
    """
    主动学习主流程：
    1. 选择学习主题
    2. 联网搜索
    3. 沙盘推演
    4. 写入 MemPalace
    """
    import random
    import urllib.parse

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[proactive_learning] 🚀 开始主动学习 | {today} {timestamp}", flush=True)

    # 选题：优先用指定的，否则随机
    if topic_override:
        topic_data = next(
            (t for t in LEARNING_TOPICS if t["theme"] == topic_override),
            LEARNING_TOPICS[0]
        )
    else:
        topic_data = random.choice(LEARNING_TOPICS)

    theme = topic_data["theme"]
    query = topic_data["query"]
    scenario = topic_data["scenario"]

    print(f"[proactive_learning] 📚 主题: {theme}", flush=True)
    print(f"[proactive_learning] 🔍 查询: {query}", flush=True)

    # Step 1: 联网搜索
    print(f"[proactive_learning] 🌐 开始搜索...", flush=True)
    search_results = duckduckgo_search(query)
    print(f"[proactive_learning] 📝 搜索完成: {search_results[:100]}...", flush=True)

    # Step 2: 写入搜索记录
    write_to_mempalace(search_results, f"联网搜索: {theme}")

    # Step 3: 沙盘推演
    print(f"[proactive_learning] 🎯 开始沙盘推演...", flush=True)
    sandbox_output = run_sandbox(theme, search_results)
    print(f"[proactive_learning] 🎯 {sandbox_output}", flush=True)

    # Step 4: 写入 MemPalace (learning)
    learning_content = (
        f"【主动学习 · {timestamp}】主题: {theme}\n"
        f"场景: {scenario}\n"
        f"联网搜索结果: {search_results[:300]}\n"
        f"沙盘推演: {sandbox_output}"
    )
    write_result = write_to_mempalace(learning_content, f"主动学习: {theme} → {sandbox_output[:80]}")

    print(f"[proactive_learning] ✅ 完成 | {write_result}", flush=True)

    return {
        "timestamp": f"{today} {timestamp}",
        "theme": theme,
        "search_results": search_results,
        "sandbox_output": sandbox_output,
        "mempalace_write": write_result,
    }


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    result = run(topic)
    print(json.dumps(result, ensure_ascii=False, indent=2))
