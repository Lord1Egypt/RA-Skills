#!/bin/bash
#===============================================================================
# 每日成本报告
#===============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.openclaw/workspace/memory/activity"
STATS_FILE="$DATA_DIR/cost-stats.json"

echo "📅 每日成本报告 - $(date '+%Y-%m-%d')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 - "$STATS_FILE" << 'PYEOF'
import json
from datetime import datetime, timedelta

stats_file = __import__('sys').argv[1]

try:
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    # 过滤今日调用
    today = datetime.now().date()
    today_calls = [
        c for c in stats['calls']
        if datetime.fromisoformat(c['timestamp']).date() == today
    ]
    
    if today_calls:
        today_input = sum(c['inputTokens'] for c in today_calls)
        today_output = sum(c['outputTokens'] for c in today_calls)
        today_cost = sum(c['costUSD'] for c in today_calls)
        today_count = len(today_calls)
        
        print(f"今日 API 调用: {today_count} 次")
        print(f"今日 Token: {today_input + today_output:,}")
        print(f"今日成本: ${today_cost:.4f} USD")
        
        # 计算昨日
        yesterday = today - timedelta(days=1)
        yesterday_calls = [
            c for c in stats['calls']
            if datetime.fromisoformat(c['timestamp']).date() == yesterday
        ]
        
        if yesterday_calls:
            yesterday_cost = sum(c['costUSD'] for c in yesterday_calls)
            if yesterday_cost > 0:
                change = (today_cost - yesterday_cost) / yesterday_cost * 100
                if change > 0:
                    print(f"━━━━━━━━━━━━━━━")
                    print(f"较昨日: +{change:.0f}% 📈")
                else:
                    print(f"━━━━━━━━━━━━━━━")
                    print(f"较昨日: {change:.0f}% 📉")
    else:
        print("今日暂无 API 调用")
    
    print("━━━━━━━━━━━━━━━")
    print(f"📊 本月累计: ${stats['totalCostUSD']:.4f} USD")
    
except Exception as e:
    print(f"❌ 报告生成失败: {e}")
PYEOF

echo ""
