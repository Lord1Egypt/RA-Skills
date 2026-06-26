#!/bin/bash
# 选题专家 - 查看运行状态

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_ROOT/data/topic_expert.pid"
LOG_FILE="$PROJECT_ROOT/logs/daemon.log"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 选题专家正在运行 (PID: $PID)"
        echo ""
        echo "📊 进程信息："
        ps -p $PID -o pid,ppid,etime,rss,cmd
        echo ""
        echo "📋 最新日志（最后20行）："
        tail -20 "$LOG_FILE" 2>/dev/null || echo "  (暂无日志)"
    else
        echo "❌ PID 文件存在但进程未运行"
        rm -f "$PID_FILE"
    fi
else
    echo "⚠️  选题专家未运行"
fi

echo ""
echo "📊 选题库统计："
cd "$PROJECT_ROOT"
python3 << 'EOF'
from core.database import TopicDatabase
db = TopicDatabase()
stats = db.get_stats(days=7)
print(f"  近7天选题：{stats['total']} 个")
print(f"  状态分布：{stats['status']}")
db.close()
EOF
