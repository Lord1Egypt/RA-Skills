#!/usr/bin/env python3
"""
langgraph-idea-generator 核心逻辑 v1.1.0
==========================================

升级点：
  - 新增 @tool：list_existing_scripts（查 ~/scripts 现有脚本）
  - plan_node 注入现有脚本 context，避免重复造轮子
  - 文件路径修正为 ~/.openclaw/workspace-coding-advisor/scripts/（老板实际位置）
"""
from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool


# ===== 1. 状态定义 =====
class State(TypedDict):
    request: str
    category: str
    complexity: str
    plan: str
    existing_scripts: str  # v1.1 新增：注入的现有脚本列表
    trace: Annotated[list[str], add]


# ===== 2. LLM 初始化 =====
def make_llm() -> ChatAnthropic:
    api_key = os.environ.get("EM_API_KEY") or os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError("需要 EM_API_KEY 或 MINIMAX_API_KEY 环境变量")
    return ChatAnthropic(
        model="MiniMax-M3",
        api_key=api_key,
        base_url="https://api.minimaxi.com/anthropic",
        max_tokens=1024,
    )


# ===== 3. Tool：查现有脚本 =====
SCRIPTS_DIR = "~/.openclaw/workspace-coding-advisor/scripts"


@tool
def list_existing_scripts(directory: str = SCRIPTS_DIR) -> str:
    """列出指定目录下现有的 Python 脚本文件名（用于避免重复造轮子）。

    Args:
        directory: 要扫描的目录路径，默认 ~/.openclaw/workspace-coding-advisor/scripts

    Returns:
        目录下的 .py 文件列表（最多 30 个），目录不存在时返回提示
    """
    p = Path(os.path.expanduser(directory))
    if not p.exists():
        return f"目录不存在：{p}"
    if not p.is_dir():
        return f"不是目录：{p}"
    files = sorted([f.name for f in p.glob("*.py")])
    if not files:
        return f"{p} 下没有 .py 文件"
    return f"{p} 下现有 {len(files)} 个脚本：\n" + "\n".join(f"- {f}" for f in files[:30])


# ===== 4. 三个节点 =====
def classify_node(state: State) -> State:
    """节点 1：分类（[工作]/[生活]/[学习]）"""
    llm = make_llm()
    prompt = f"""判断分类（**只输出一个标签**）：
「{state['request']}」
- [工作] IT/数据/自动化
- [生活] 信息/习惯/财务
- [学习] 课程/案例/模板"""
    category = llm.invoke(prompt).content.strip()
    if "[" not in category:
        category = f"[未分类] {category[:20]}"
    return {"category": category, "trace": [f"✅ 分类完成 → {category}"]}


def complexity_node(state: State) -> State:
    """节点 2：评估复杂度（高/中/低）"""
    llm = make_llm()
    prompt = f"""评估复杂度（**只输出一个词**：高/中/低）：
「{state['request']}」 ({state['category']})
- 高 = 外部API/数据库/异步
- 中 = 几个文件/第三方库
- 低 = 几十行"""
    complexity = llm.invoke(prompt).content.strip()
    if complexity not in ("高", "中", "低"):
        complexity = "中"
    return {"complexity": complexity, "trace": [f"✅ 复杂度评估 → {complexity}"]}


def plan_node(state: State) -> State:
    """节点 3：生成 3 行落地（命令→场景→存 scripts/）

    v1.1 升级：
      - 调用 list_existing_scripts tool 查老板现有脚本
      - 注入 prompt 让 LLM 避免重复造轮子
    """
    # 调用 tool 查现有脚本（直接调 .func()，M3 tool-calling 支持待验证）
    existing = list_existing_scripts.func()
    existing_count = existing.count("- ")  # 简单计数

    llm = make_llm()
    prompt = f"""生成 **3 行落地**（每行 ≤ 50 字）：
需求：「{state['request']}」 ({state['category']}/{state['complexity']})

老板已有脚本：
{existing}

格式：
命令：<具体可执行>
场景：<解决什么问题>
文件：~/.openclaw/workspace-coding-advisor/scripts/xxx.py
（已有类似请改进，不要重写）"""
    plan = llm.invoke(prompt).content.strip()
    return {
        "plan": plan,
        "existing_scripts": existing,
        "trace": [f"✅ 3 行落地（参考了 {existing_count} 个现有脚本）"],
    }


# ===== 5. 图构建 =====
def build_graph():
    g = StateGraph(State)
    g.add_node("classify", classify_node)
    g.add_node("complexity", complexity_node)
    g.add_node("plan", plan_node)

    g.add_edge(START, "classify")
    g.add_edge("classify", "complexity")
    g.add_edge("complexity", "plan")
    g.add_edge("plan", END)

    return g.compile()


# ===== 6. 入口 =====
def main():
    if len(sys.argv) > 1:
        request = " ".join(sys.argv[1:]).strip()
    elif not sys.stdin.isatty():
        request = sys.stdin.read().strip()
    else:
        request = input("老板，今天想写什么代码？\n> ").strip()

    if not request:
        print("❌ 需求不能为空", file=sys.stderr)
        sys.exit(1)

    # JSON 输出模式（给 agent 调用）
    if os.environ.get("IDEA_GEN_JSON") == "1":
        try:
            app = build_graph()
            result = app.invoke({"request": request, "trace": []})
            print(json.dumps({
                "request": result["request"],
                "category": result["category"],
                "complexity": result["complexity"],
                "plan": result["plan"],
                "existing_scripts": result.get("existing_scripts", ""),
                "trace": result["trace"],
            }, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        return

    # 人类可读输出
    print(f"\n🦀 码虫启动 LangGraph 流水线 (v1.1)")
    print(f"📥 需求：{request}\n")

    try:
        app = build_graph()
        result = app.invoke({"request": request, "trace": []})
    except Exception as e:
        print(f"❌ 出错了：{e}", file=sys.stderr)
        sys.exit(1)

    print("━" * 50)
    print(f"🏷️  分类：{result['category']}")
    print(f"📊 复杂度：{result['complexity']}")
    print("━" * 50)
    print(f"📋 3 行落地：\n{result['plan']}")
    print("━" * 50)
    if result.get("existing_scripts"):
        print(f"📚 参考的现有脚本（前 5 行）：")
        for line in result["existing_scripts"].splitlines()[:5]:
            print(f"   {line}")
        print("━" * 50)
    print(f"🔍 节点轨迹：")
    for t in result["trace"]:
        print(f"   {t}")


if __name__ == "__main__":
    main()