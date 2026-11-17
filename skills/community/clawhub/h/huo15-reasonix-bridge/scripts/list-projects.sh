#!/bin/bash
# huo15-reasonix-bridge: 列出 Reasonix 所有项目
# 用法: bash list-projects.sh

PROJECTS_FILE="$HOME/.reasonix/desktop-projects.json"

if [ ! -f "$PROJECTS_FILE" ]; then
  echo "错误: 找不到 desktop-projects.json。Reasonix 桌面版可能未运行过。"
  exit 1
fi

python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    d = json.load(f)
projects = d.get('projects', [])
for p in projects:
    root = p['root']
    topic_count = len(p.get('topics', []))
    print(f'{root} ({topic_count} topics)')
"