#!/bin/bash
# Work Notification Summary - Filters work-related notifications and generates a summary

# Get directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIF_SCRIPT="$SCRIPT_DIR/read_notifications.py"

TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Output directory
OUTPUT_DIR="${HOME}/.openclaw/workspace/memory/$TODAY/computer_io/notification"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="$OUTPUT_DIR/work-summary-$TIMESTAMP.md"

# Work-related apps (Teams, Outlook, and work WeChat)
WORK_APPS="teams|teams2|outlook|WeChat"

echo "=== Work Notification Summary ==="
echo "Date: $TODAY"
echo "Timestamp: $TIMESTAMP"
echo ""

# Read recent notifications (last 35 minutes)
python3 "$NOTIF_SCRIPT" --minutes 35 --output "/tmp/notif_work_$TIMESTAMP.txt" 2>/dev/null

if [ ! -f "/tmp/notif_work_$TIMESTAMP.txt" ] || [ $(wc -l < "/tmp/notif_work_$TIMESTAMP.txt") -lt 2 ]; then
    echo "No notifications found or error reading notifications"
    exit 0
fi

# Filter and analyze work notifications
python3 - "$OUTPUT_FILE" "$TODAY" "$TIMESTAMP" << 'PYEOF'
import sys
import re
from pathlib import Path

output_file = sys.argv[1]
today = sys.argv[2]
timestamp = sys.argv[3]

input_file = f"/tmp/notif_work_{timestamp}.txt"

# Work-related app patterns
work_apps = ['teams', 'teams2', 'outlook', 'wechat', 'xinwechat']

# Read notifications
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()[1:]  # Skip header

# Parse and filter work notifications
notifications = []
for line in lines:
    if '|' not in line:
        continue
    parts = line.split('|')
    if len(parts) < 3:
        continue
    
    time = parts[0].strip()
    app = parts[1].strip().lower()
    content = parts[2].strip()
    
    # Check if work-related
    is_work = any(w in app for w in work_apps)
    if is_work:
        notifications.append({
            'time': time,
            'app': app.replace('teams2', 'teams').replace('xinwechat', 'wechat'),
            'content': content[:200]
        })

# Count by app
app_counts = {}
for n in notifications:
    app = n['app']
    app_counts[app] = app_counts.get(app, 0) + 1

# Extract potential action items (simple heuristic)
action_keywords = ['请问', '能否', '帮忙', '确认', '请', '?', 'help', 'please', 'can you', 'could you']
action_items = []
for n in notifications:
    content_lower = n['content'].lower()
    if any(kw in content_lower for kw in action_keywords):
        action_items.append(f"- [{n['time']}] ({n['app']}) {n['content'][:100]}")

# Get unique notifications (by content)
seen = set()
unique_notifications = []
for n in notifications:
    key = (n['app'], n['content'][:50])
    if key not in seen:
        seen.add(key)
        unique_notifications.append(n)

# Write summary
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"# 工作通知摘要\n")
    f.write(f"- Lookback: 过去 35 分钟\n")
    f.write(f"- 总工作通知: {len(notifications)} 条\n")
    f.write(f"\n## 渠道分布\n")
    for app, count in sorted(app_counts.items(), key=lambda x: -x[1]):
        f.write(f"- {app.capitalize()}: {count}\n")
    
    f.write(f"\n## 待处理事项（自动提取）\n")
    if action_items:
        for item in action_items[:5]:  # Max 5
            f.write(f"{item}\n")
    else:
        f.write("- 无明确待处理事项\n")
    
    f.write(f"\n## 最近工作通知（去重后）\n")
    for n in unique_notifications[:10]:  # Max 10
        f.write(f"- [{n['time']}] ({n['app']}) {n['content'][:80]}\n")

# Clean up
Path(input_file).unlink(missing_ok=True)

print(f"✅ Work summary saved to: {output_file}")
print(f"   Total: {len(notifications)} notifications, {len(unique_notifications)} unique")
PYEOF
