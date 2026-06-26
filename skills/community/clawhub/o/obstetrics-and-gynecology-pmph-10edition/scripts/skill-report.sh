#!/bin/bash
# SKILL 清单报告生成脚本
# 用法: bash scripts/skill-report.sh
# 功能: 统计各分类技能数并生成汇总报告

REPORT_FILE="skill-report-$(date +%Y%m%d).md"

echo "# 妇产科技能清单报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "生成日期: $(date '+%Y-%m-%d %H:%M')" >> "$REPORT_FILE"
echo "总技能数: $(grep -c '^- name:' SKILL.md)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 分类统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| 分类 | 技能数 |" >> "$REPORT_FILE"
echo "|------|--------|" >> "$REPORT_FILE"

grep "^## " SKILL.md | while read -r line; do
    category=$(echo "$line" | sed 's/^## //' | sed 's/ ([0-9]*)//')
    count=$(echo "$line" | grep -oP '\(\K[0-9]+(?=\))')
    if [ -n "$count" ]; then
        echo "| $category | $count |" >> "$REPORT_FILE"
    fi
done

echo "" >> "$REPORT_FILE"
echo "报告已生成: $REPORT_FILE"
cat "$REPORT_FILE"
