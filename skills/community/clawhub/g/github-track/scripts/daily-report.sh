#!/bin/bash
# GitHub Track 定时任务脚本
# 每天上午 10:00 执行

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TRACK_SCRIPT="$SCRIPT_DIR/track.py"
OUTPUT_FILE="/tmp/github-track-report.md"
DATA_FILE="$HOME/.openclaw/workspace/memory/github-track-data.json"

echo "🔄 开始执行 GitHub Track 定时任务..."

# 尝试刷新追踪数据（可能因限流失败，但不影响使用缓存数据）
python3 "$TRACK_SCRIPT" refresh 2>&1 || echo "⚠️ API 限流，使用缓存数据"

# 生成 Markdown 报告
echo "# 📡 GitHub 仓库每日追踪报告" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "更新时间: $(date "+%Y-%m-%d %H:%M:%S")" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 读取并格式化数据
python3 -c "
import json

DATA_FILE = '$DATA_FILE'

try:
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if not data:
        print('⚠️ 未找到追踪数据', file=__import__('sys').stderr)
        exit(0)
    
    for repo_key, info in data.items():
        stars = info.get('stars', 0)
        forks = info.get('forks', 0)
        open_issues = info.get('open_issues', 0)
        
        print(f'## 🎯 {repo_key}')
        print()
        print(f'**📊 当前状态**')
        print(f'- ⭐ Stars: {stars:,}')
        print(f'- 🍴 Forks: {forks:,}')
        print(f'- 🐛 Open Issues: {open_issues}')
        print()
        
        # 最近 Issues
        if info.get('recent_issues'):
            print('**🐛 最近 Issues**')
            for issue in info['recent_issues'][:5]:
                state_emoji = '✅' if issue['state'] == 'closed' else '🐛'
                comments = f\" ({issue['comments']} comments)\" if issue['comments'] > 0 else ''
                print(f\"- {state_emoji} [#{issue['number']}](https://github.com/{repo_key}/issues/{issue['number']}) - {issue['title']}{comments}\")
            print()
        
        # 最近 PRs
        if info.get('recent_prs'):
            print('**📥 最近 PRs**')
            for pr in info['recent_prs'][:5]:
                if pr.get('merged_at'):
                    state_emoji = '✅ merged'
                elif pr['state'] == 'closed':
                    state_emoji = '❌ closed'
                elif pr.get('draft'):
                    state_emoji = '📝 draft'
                else:
                    state_emoji = '📥 open'
                print(f\"- {state_emoji} [#{pr['number']}](https://github.com/{repo_key}/pull/{pr['number']}) - {pr['title']}\")
            print()
        
        print('---')
        print()
        
except Exception as e:
    print(f'⚠️ 生成报告失败: {e}', file=__import__('sys').stderr)
" >> "$OUTPUT_FILE"

echo "✅ 报告已生成: $OUTPUT_FILE"

# 发送报告到 Slack
echo "📤 发送报告到 Slack..."
python3 -c "
import json

# 读取报告
with open('$OUTPUT_FILE', 'r') as f:
    content = f.read()

# 发送到 Slack
import os
if os.environ.get('OPENCLAW_SLACK_TOKEN'):
    from slack_sdk import WebClient
    client = WebClient(token=os.environ['OPENCLAW_SLACK_TOKEN'])
    client.chat_postMessage(channel='C0AHZG3GT3M', text=content)
    print('✅ 报告已发送到 Slack')
else:
    print('⚠️ 未配置 Slack token，仅保存报告')
"

# 输出报告内容
echo ""
echo "========== 报告内容 =========="
cat "$OUTPUT_FILE"
