#!/bin/bash
# list-skills.sh - List all skills with descriptions
# 列出所有技能及其描述

cd "$(dirname "$0")/.."
echo "=== Physiology-PMPH-10edition — All Skills ==="
echo ""

count=0
for folder in */; do
  if [ -f "${folder}SKILL.md" ]; then
    name=$(head -1 "${folder}SKILL.md" | sed 's/^# //')
    desc=$(grep "^name:" "${folder}SKILL.md" 2>/dev/null | sed 's/^name: //')
    echo "$count. $folder → $name"
    echo "   $desc"
    echo ""
    count=$((count + 1))
  fi
done

echo "Total: $count skills"
