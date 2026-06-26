#!/usr/bin/env python3
"""
/save 命令处理器 - 被 agent 调用

用法（由 agent 的 Bash 工具执行）:
    python3 .../save_session.py <session_json_file>
"""
import sys
import os
import json
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        # 没有参数：尝试从 stdin 读取
        try:
            session_data = json.load(sys.stdin)
        except:
            print("Usage: save_session.py '<session_json_string>'")
            sys.exit(1)
    else:
        # 命令行参数是 JSON 字符串
        try:
            session_data = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            sys.exit(1)
    messages = session_data.get("messages", [])
    if not messages:
        print("No messages to save")
        sys.exit(0)

    # 调用 memory_ops.py store --session-file
    script_dir = Path(__file__).parent
    memory_ops = script_dir.parent / "memory_ops.py"

    # 写临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"messages": messages}, f)
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, str(memory_ops), "store", "--session-file", temp_file, "--json"],
            capture_output=True, text=True, timeout=30
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    main()
