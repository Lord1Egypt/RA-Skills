#!/opt/homebrew/bin/python3.12
"""记忆数据库快捷操作脚本 - 供agent通过exec调用"""

import sys
import os
import json
import subprocess

DB_DIR = os.path.dirname(os.path.abspath(__file__))
MEMDB = os.path.join(DB_DIR, "memdb.py")
PYTHON = "/opt/homebrew/bin/python3.12"


def run(args):
    """运行memdb.py命令，返回输出"""
    result = subprocess.run(
        [PYTHON, MEMDB] + args,
        capture_output=True, text=True, cwd=DB_DIR, timeout=60
    )
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def search_json(query, type_filter=None, limit=5):
    """搜索记忆，返回JSON"""
    args = ["search", query, "--limit", str(limit), "--format", "json"]
    if type_filter:
        args += ["--type", type_filter]
    output = run(args)
    return json.loads(output) if output else []


def add_memory(content, type_, entity=None, severity=None, source="conversation"):
    """添加一条记忆"""
    args = ["add", content, "--type", type_, "--source", source]
    if entity:
        args += ["--entity", entity]
    if severity:
        args += ["--severity", severity]
    return run(args)


def check_and_write(text, context=""):
    """
    智能记忆写入：分析文本内容，自动判断是否需要写入记忆
    这是给agent调用的核心方法
    """
    text_lower = text.lower()
    written = []

    # 持仓变动关键词
    position_keywords = ["买了", "卖了", "加仓", "减仓", "清仓", "建仓", "止盈", "止损",
                         "换股", "调入", "调出", "买入", "卖出", "持有", "新仓"]
    if any(kw in text_lower for kw in position_keywords):
        result = add_memory(text, "portfolio", source="conversation")
        written.append(f"portfolio: {text[:50]}")

    # 策略变动关键词
    strategy_keywords = ["新策略", "改策略", "策略调整", "情绪周期", "主线", "龙头",
                         "买点", "卖点", "仓位", "回测", "参数优化"]
    if any(kw in text_lower for kw in strategy_keywords):
        result = add_memory(text, "strategy", source="conversation")
        written.append(f"strategy: {text[:50]}")

    # 教训关键词
    lesson_keywords = ["纠正", "不对", "错误", "应该是", "其实是", "教训",
                       "忘记", "漏了", "别再", "下次注意", "踩坑"]
    if any(kw in text_lower for kw in lesson_keywords):
        result = add_memory(text, "lesson", source="conversation")
        written.append(f"lesson: {text[:50]}")

    # 偏好关键词
    pref_keywords = ["以后用", "记住", "我喜欢", "我偏好", "以后不要",
                     "改用", "换成", "以后都", "默认用"]
    if any(kw in text_lower for kw in pref_keywords):
        result = add_memory(text, "preference", source="conversation")
        written.append(f"preference: {text[:50]}")

    return {"written": written, "count": len(written)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: memory_tool.py <command> [args]")
        print("  check <text>       - 检查文本并自动写入相关记忆")
        print("  search <query>     - 搜索记忆")
        print("  add <text> <type>  - 手动添加记忆")
        print("  stats              - 统计")
        print("  decay              - 衰减过期记忆")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        text = " ".join(sys.argv[2:])
        result = check_and_write(text)
        if result["count"] > 0:
            for w in result["written"]:
                print(f"✅ 已写入: {w}")
        else:
            print("ℹ️ 无需写入")

    elif cmd == "search":
        query = " ".join(sys.argv[2:])
        print(run(["search", query, "--limit", "5"]))

    elif cmd == "add":
        if len(sys.argv) < 4:
            print("用法: memory_tool.py add <text> <type>")
            sys.exit(1)
        text = sys.argv[2]
        type_ = sys.argv[3]
        print(add_memory(text, type_))

    elif cmd == "stats":
        print(run(["stats"]))

    elif cmd == "decay":
        print(run(["decay"]))

    else:
        print(f"未知命令: {cmd}")
