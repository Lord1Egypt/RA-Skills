#!/bin/bash
# <bitbar.title>Context Monitor</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>OpenClaw Community</bitbar.author>
# <bitbar.desc>Real-time OpenClaw agent context monitoring in macOS menu bar</bitbar.desc>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>

MINI="${OPENCLAW_SSH_TARGET:-localhost}"
SSH_OPTS="-o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new -o BatchMode=yes"
STATUS_SCRIPT="${OPENCLAW_STATUS_SCRIPT:-~/.openclaw/openclaw-status.py}"

RAW=$(ssh $SSH_OPTS $MINI "python3 $STATUS_SCRIPT" 2>/dev/null)

if [ -z "$RAW" ]; then
  echo "🦞 ❌"
  echo "---"
  echo "Cannot connect to OpenClaw host"
  exit 0
fi

echo "$RAW" | python3 -c "
import sys

agents = {}
for line in sys.stdin:
    line = line.strip()
    if not line or '\t' not in line:
        continue
    parts = line.split('\t')
    if len(parts) >= 8:
        agents[parts[0]] = {
            'status': parts[1],
            'tokens': int(float(parts[2])),
            'context': int(float(parts[3])),
            'updated': int(float(parts[4])),
            'emoji': parts[5],
            'model': parts[6],
            'ago': parts[7],
        }

if not agents:
    print('🦞 ⚠️')
    print('---')
    print('No agent data')
    sys.exit(0)

# Menu bar: most recently updated agent
latest_name, latest = max(agents.items(), key=lambda x: x[1]['updated'])
tk = f\"{latest['tokens']//1000}k\" if latest['tokens'] >= 1000 else str(latest['tokens'])
label = latest['emoji'] if latest['emoji'] != '🤖' else latest_name
print(f'{label} {tk}')

print('---')
print(f'🦞 OpenClaw Agents ({len(agents)}) | size=14 bash=/usr/bin/true terminal=false')
print('---')

WARN_THRESHOLD = 100000

for name, a in sorted(agents.items(), key=lambda x: -x[1]['updated']):
    tk = f\"{a['tokens']//1000}k\" if a['tokens'] >= 1000 else str(a['tokens'])
    ctx = f\"{a['context']//1000}k\" if a['context'] >= 1000 else str(a['context'])
    emoji_str = f'{a[\"emoji\"]} ' if a['emoji'] != '🤖' else ''

    if a['status'] == 'running':
        tag = '▶'
    elif a['status'] == 'failed':
        tag = '✖'
    else:
        tag = '—'

    pct = int(a['tokens'] / a['context'] * 100) if a['context'] > 0 else 0
    warn = ' 🫠' if a['tokens'] >= WARN_THRESHOLD else ''

    print(f'{tag} {emoji_str}{name}  {tk}/{ctx} ({pct}%)  {a[\"model\"]}  {a[\"ago\"]} ago{warn} | bash=/usr/bin/true terminal=false')

print('---')
print('Refresh | refresh=true')
"
