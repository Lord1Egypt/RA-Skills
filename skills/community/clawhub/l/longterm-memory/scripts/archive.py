#!/usr/bin/env python3
"""
永久记忆归档脚本
将重要记忆条目追加到 MEMORY.md
"""
import sys
import os
from datetime import datetime

MEMORY_PATH = os.path.expanduser("~/.openclaw/workspace/MEMORY.md")

def append_memory(entry: str, category: str = None):
    """追加记忆到 MEMORY.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d")

    section = f"## {category}" if category else "## 记忆"
    entry_text = f"- [{timestamp}] {entry}"

    # 检查是否已存在（防止重复）
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if entry in content:
        print(f"[记忆] 已存在，跳过: {entry}")
        return

    # 追加到对应分类或通用分类
    with open(MEMORY_PATH, "a", encoding="utf-8") as f:
        if category and f"\n## {category}\n" in content:
            # 追加到现有分类
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line == f"## {category}":
                    # 找到分类最后一行，插入其后
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("## "):
                        j += 1
                    lines.insert(j, entry_text)
                    break
            with open(MEMORY_PATH, "w", encoding="utf-8") as f2:
                f2.write("\n".join(lines))
        else:
            # 新增通用分类
            f.write(f"\n{section}\n{entry_text}\n")

    print(f"[记忆] 已归档: {entry}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 archive.py <记忆内容> [分类]")
        sys.exit(1)

    entry = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    append_memory(entry, category)
