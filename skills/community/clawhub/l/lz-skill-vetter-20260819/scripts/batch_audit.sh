#!/usr/bin/env bash
# lz-skill-vetter-plus v2.1.0 — 批量审计脚本
# 扫描所有 OpenClaw skills 目录，输出汇总报告

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/audit.py"

# 默认扫描路径
SCAN_DIRS=(
  "/home/zuoyunlai/.openclaw/workspace/skills"
  "/home/zuoyunlai/.npm-global/lib/node_modules/openclaw/skills"
)

# 收集所有技能目录
SKILLS=()
for scan_dir in "${SCAN_DIRS[@]}"; do
  if [ -d "$scan_dir" ]; then
    while IFS= read -r skill_md; do
      skill_dir=$(dirname "$skill_md")
      SKILLS+=("$skill_dir")
    done < <(find "$scan_dir" -maxdepth 3 -name "SKILL.md" 2>/dev/null)
  fi
done

# 去重
SKILLS=($(printf "%s\n" "${SKILLS[@]}" | sort -u))

echo "═════════════════════════════════════════════════════════════"
echo "  skill-vetter v2.0 — 批量审计"
echo "═════════════════════════════════════════════════════════════"
echo "扫描目录:"
for d in "${SCAN_DIRS[@]}"; do echo "  - $d"; done
echo "找到 ${#SKILLS[@]} 个 SKILL.md"
echo "═════════════════════════════════════════════════════════════"
echo ""

# 表格 header
printf "%-40s | %5s | %5s | %5s | %5s | %5s | %s\n" "SKILL" "CRIT" "HIGH" "MED" "LOW" "INFO" "VERDICT"
printf "%-40s-+-%-5s-+-%-5s-+-%-5s-+-%-5s-+-%-5s-+-%s\n" "$(printf '%.0s-' {1..40})" "-----" "-----" "-----" "-----" "-----" "----------"

TOTAL_CRIT=0
TOTAL_HIGH=0
TOTAL_MED=0
TOTAL_LOW=0
TOTAL_INFO=0
TOTAL_FAIL=0
TOTAL_CAUTION=0
TOTAL_REVIEW=0
TOTAL_OK=0

# 详细结果记录
DETAIL=()
FAIL_LIST=()
CAUTION_LIST=()

for skill_dir in "${SKILLS[@]}"; do
  skill_name=$(basename "$skill_dir")

  # 调 audit.py 拿 JSON
  json=$(LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 PYTHONIOENCODING=utf-8 \
    python3 "$PYTHON_SCRIPT" "$skill_dir" --format json --quiet 2>/dev/null || echo '{"summary":{"by_severity":{}}}')

  # 解析
  summary=$(echo "$json" | python3 -c "
import sys, json
try:
    r = json.load(sys.stdin)
    s = r['summary']['by_severity']
    crit = s.get('critical', 0)
    high = s.get('high', 0)
    med  = s.get('medium', 0)
    low  = s.get('low', 0)
    info = s.get('info', 0)
    v = r.get('verdict_code', 'unknown')
    print(f'{crit}|{high}|{med}|{low}|{info}|{v}')
except Exception as e:
    print('0|0|0|0|0|error')
" 2>/dev/null)

  IFS='|' read -r crit high med low info vc <<< "$summary"

  case "$vc" in
    fail)    verdict="⛔ FAIL";     TOTAL_FAIL=$((TOTAL_FAIL+1)); FAIL_LIST+=("$skill_name") ;;
    caution) verdict="🔴 CAUTION";  TOTAL_CAUTION=$((TOTAL_CAUTION+1)); CAUTION_LIST+=("$skill_name") ;;
    review)  verdict="🟡 REVIEW";   TOTAL_REVIEW=$((TOTAL_REVIEW+1)) ;;
    ok)      verdict="🟢 OK";       TOTAL_OK=$((TOTAL_OK+1)) ;;
    *)       verdict="❓ ERROR" ;;
  esac

  printf "%-40s | %5d | %5d | %5d | %5d | %5d | %s\n" \
    "$skill_name" "$crit" "$high" "$med" "$low" "$info" "$verdict"

  TOTAL_CRIT=$((TOTAL_CRIT + crit))
  TOTAL_HIGH=$((TOTAL_HIGH + high))
  TOTAL_MED=$((TOTAL_MED + med))
  TOTAL_LOW=$((TOTAL_LOW + low))
  TOTAL_INFO=$((TOTAL_INFO + info))
done

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "  汇总"
echo "═════════════════════════════════════════════════════════════"
printf "扫描技能总数:    %d\n" "${#SKILLS[@]}"
printf "  ⛔ FAIL:       %d\n" "$TOTAL_FAIL"
printf "  🔴 CAUTION:    %d\n" "$TOTAL_CAUTION"
printf "  🟡 REVIEW:     %d\n" "$TOTAL_REVIEW"
printf "  🟢 OK:         %d\n" "$TOTAL_OK"
echo ""
printf "Finding 总计:\n"
printf "  🔴 critical:   %d\n" "$TOTAL_CRIT"
printf "  🟠 high:       %d\n" "$TOTAL_HIGH"
printf "  🟡 medium:     %d\n" "$TOTAL_MED"
printf "  🔵 low:        %d\n" "$TOTAL_LOW"
printf "  ⚪ info:       %d\n" "$TOTAL_INFO"

if [ ${#FAIL_LIST[@]} -gt 0 ]; then
  echo ""
  echo "═══ ⛔ FAIL（必须处理）═══"
  printf '  - %s\n' "${FAIL_LIST[@]}"
fi

if [ ${#CAUTION_LIST[@]} -gt 0 ]; then
  echo ""
  echo "═══ 🔴 CAUTION（需关注）═══"
  printf '  - %s\n' "${CAUTION_LIST[@]}"
fi

echo ""
echo "═════════════════════════════════════════════════════════════"