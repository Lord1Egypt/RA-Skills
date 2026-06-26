#!/bin/bash
# Claude Code 任务脚本 - fix_db_kairos_001
# 生成时间: 2026-04-03T09:22:52.956096

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: fix_db_kairos_001"
echo "提示: 读取文件 /Users/mars/.openclaw/workspace/skills/kairos-mode/setup_trading_monitors.py，检查第20行附近的数据库连接代码。
..."
echo ""

# 执行 Claude Code
claude -p "读取文件 /Users/mars/.openclaw/workspace/skills/kairos-mode/setup_trading_monitors.py，检查第20行附近的数据库连接代码。

当前代码:
    conn = sqlite3.connect(db_path)

需要改为使用上下文管理器:
    with sqlite3.connect(db_path) as conn:

请执行修复并保存文件。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_kairos_001.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_db_kairos_001.json"

echo "✅ 任务完成: fix_db_kairos_001"
