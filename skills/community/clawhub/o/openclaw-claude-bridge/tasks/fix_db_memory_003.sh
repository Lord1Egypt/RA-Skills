#!/bin/bash
# Claude Code 任务脚本 - fix_db_memory_003
# 生成时间: 2026-04-03T09:24:14.673434

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: fix_db_memory_003"
echo "提示: 读取文件 /Users/mars/.openclaw/workspace/skills/agent-memory/src/memory.py。

这个文件有多个 sqlite3.connect() 调..."
echo ""

# 执行 Claude Code
claude -p "读取文件 /Users/mars/.openclaw/workspace/skills/agent-memory/src/memory.py。

这个文件有多个 sqlite3.connect() 调用（约20处），但没有使用 with 语句。

请将所有的:
    conn = sqlite3.connect(self.db_path)
    ... 使用 conn ...
    conn.close()

改为:
    with sqlite3.connect(self.db_path) as conn:
        ... 使用 conn ...

注意：有些函数可能有多处连接，请确保每处都修复。保存文件。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_memory_003.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_memory_003.json"

echo "✅ 任务完成: fix_db_memory_003"
