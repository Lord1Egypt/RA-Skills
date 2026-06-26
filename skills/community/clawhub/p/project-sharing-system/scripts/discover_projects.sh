#!/bin/bash
# 项目自动发现脚本 — Agent 会话启动时调用
# 用途: 让 Agent 快速了解当前所有活跃项目
# 用法: bash scripts/discover_projects.sh

WORKSPACE="${CLAWHUB_WORKDIR:-$HOME/.openclaw/workspace}"
SNAPSHOT_FILE="$WORKSPACE/projects_snapshot.md"
JSON_FILE="$WORKSPACE/projects_status.json"

echo "================================================"
echo "  📋 项目自动发现"
echo "================================================"

if [ ! -f "$JSON_FILE" ]; then
    echo "  ⚠️  项目共享系统未初始化"
    echo "  运行: project sync"
    echo "================================================"
    exit 1
fi

# 使用 Python 解析并输出结构化信息供 Agent 读取
python3 -c "
import json
from datetime import datetime

with open('$JSON_FILE') as f:
    data = json.load(f)

projects = data.get('projects', [])
active = [p for p in projects if p.get('status') == 'in_progress']
completed = [p for p in projects if p.get('status') == 'completed']

print(f'  时间: {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}')
print(f'  更新: {data.get(\"last_updated\", \"\")}')
print(f'  活跃: {len(active)} 个')
print('')

if active:
    print('  🔄 活跃项目:')
    for p in active:
        print(f'    [{p[\"name\"]}] {p.get(\"current_task\", \"\")}')
    print('')

if completed:
    print('  ✅ 已完成:')
    for p in completed:
        ptime = p.get(\"updated_at\", \"\")[11:16] if len(p.get(\"updated_at\", \"\")) > 16 else \"\"
        print(f'    {p[\"name\"]} ({ptime})')
    print('')

# 生成 Agent 可解析的紧凑格式
print('  ---agent-format-start---')
for p in active:
    print(f'ACTIVE:{p[\"id\"]}:{p[\"name\"]}:{p.get(\"current_task\",\"\")}')
for p in completed:
    print(f'DONE:{p[\"id\"]}:{p[\"name\"]}')
print('  ---agent-format-end---')
"

echo "================================================"
echo "  查看全部: project list"
echo "  查看详情: project show <id>"
echo "================================================"
