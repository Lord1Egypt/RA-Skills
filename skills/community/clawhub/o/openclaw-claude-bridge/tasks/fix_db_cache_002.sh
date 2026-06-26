#!/bin/bash
# Claude Code 任务脚本 - fix_db_cache_002
# 生成时间: 2026-04-03T09:23:20.023902

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: fix_db_cache_002"
echo "提示: 读取文件 /Users/mars/.openclaw/workspace/skills/a-stock-monitor/scripts/stock_cache_db.py。

找到所有使用 sqlit..."
echo ""

# 执行 Claude Code
claude -p "读取文件 /Users/mars/.openclaw/workspace/skills/a-stock-monitor/scripts/stock_cache_db.py。

找到所有使用 sqlite3.connect() 但没有使用 with 语句的地方。
将类似:
    self.conn = sqlite3.connect(self.db_path)

改为:
    with sqlite3.connect(self.db_path) as conn:
        self.conn = conn

或者如果 conn 在多个方法中使用，改为在需要时创建连接并使用 with 语句。

请执行修复并保存文件。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_cache_002.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_cache_002.json"

echo "✅ 任务完成: fix_db_cache_002"
