#!/usr/bin/env bash
# hekouwang-doctor-suite · 三件套一键体检
# 用法: bash scripts/run-all-doctors.sh [项目根目录]
# 依赖: 三个 doctor skill 已装在 HEKOUWANG_SKILLS_DIR（默认 ~/.claude/skills）
set -euo pipefail

ROOT="$(cd "${1:-.}" && pwd)"
SKILLS="${HEKOUWANG_SKILLS_DIR:-$HOME/.claude/skills}"
MD="$SKILLS/hekouwang-claude-md-doctor-skill"
SD="$SKILLS/hekouwang-claude-skill-doctor-skill"
ED="$SKILLS/hekouwang-env-doctor-skill"

die() { echo "ERROR: $*" >&2; exit 1; }
[ -f "$MD/check.py" ] || die "缺 md-doctor: $MD"
[ -f "$SD/check.py" ] || die "缺 skill-doctor: $SD"
[ -f "$ED/scripts/scan.sh" ] || die "缺 env-doctor: $ED"

json_score() {
  python3 -c "import sys,json; print(json.load(sys.stdin).get('score','—'))"
}

SUITE_FAIL=0
ADVISORY_FAIL=0

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  HEKOUWANG DOCTOR SUITE  ·  三件套一键体检              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "项目: $ROOT"
echo ""

echo "━━━━ ① md-doctor · AGENTS.md / CLAUDE.md ━━━━"
MD_SCORE="—"
if MD_JSON=$(python3 "$MD/check.py" "$ROOT" --json 2>/dev/null); then
  if ! MD_SCORE=$(printf '%s' "$MD_JSON" | json_score); then
    echo "❌ md-doctor JSON 无法解析，套件失败。" >&2
    SUITE_FAIL=1
  fi
else
  echo "❌ md-doctor 运行失败，套件失败。" >&2
  SUITE_FAIL=1
fi
if ! python3 "$MD/check.py" "$ROOT"; then
  SUITE_FAIL=1
fi
echo ""

echo "━━━━ ② skill-doctor · 项目内 Agent Skills ━━━━"
SKILL_HITS=0
SD_MIN=100
for base in "$ROOT/.agents/skills" "$ROOT/.cursor/skills" "$ROOT/skills"; do
  [ -d "$base" ] || continue
  for d in "$base"/* "$base"/.[!.]* "$base"/..?*; do
    if [ -L "$d" ] && [ ! -e "$d" ]; then
      echo "❌ 发现断开的 Skill 软链：$d" >&2
      SUITE_FAIL=1
      continue
    fi
    [ -f "$d/SKILL.md" ] || continue
    SKILL_HITS=$((SKILL_HITS + 1))
    echo "  → $(basename "$d")"
    IS_EXTERNAL=0
    if [ -L "$d" ]; then
      resolved=$(cd -P "$d" 2>/dev/null && pwd) || resolved=''
      case "$resolved" in
        "$ROOT"/*) ;;
        *) IS_EXTERNAL=1 ;;
      esac
    fi
    if J=$(python3 "$SD/check.py" "$d" --json 2>/dev/null); then
      if S=$(printf '%s' "$J" | json_score); then
        if [ "$S" != "—" ] && [ "$S" -lt "$SD_MIN" ] 2>/dev/null; then SD_MIN=$S; fi
      else
        echo "❌ skill-doctor JSON 无法解析：$d" >&2
        if [ "$IS_EXTERNAL" -eq 0 ]; then SUITE_FAIL=1; else ADVISORY_FAIL=1; fi
      fi
    else
      if [ "$IS_EXTERNAL" -eq 0 ]; then
        echo "❌ skill-doctor 运行失败：$d" >&2
        SUITE_FAIL=1
      else
        echo "⚠️ 外部 Skill doctor 运行失败（不计入项目门禁）：$d" >&2
        ADVISORY_FAIL=1
      fi
    fi
    if [ "$IS_EXTERNAL" -eq 1 ]; then
      if ! python3 "$SD/check.py" "$d"; then
        echo "⚠️ 外部 Skill doctor 判定失败（不计入项目门禁）：$d" >&2
        ADVISORY_FAIL=1
      fi
    elif ! python3 "$SD/check.py" "$d"; then
      SUITE_FAIL=1
    fi
    echo ""
  done
done
if [ "$SKILL_HITS" -eq 0 ]; then
  echo "  (未找到 .agents/skills/ / .cursor/skills/ 下的 SKILL.md，跳过)"
  SD_MIN="—"
  echo ""
fi

echo "━━━━ ③ env-doctor · 本机开发环境（--profile ai-dev）━━━━"
if ! bash "$ED/scripts/scan.sh" --profile ai-dev; then
  SUITE_FAIL=1
fi
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  汇总                                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
printf "  %-14s %s\n" "md-doctor" "${MD_SCORE} / 100"
if [ "$SKILL_HITS" -gt 0 ]; then
  printf "  %-14s %d 个 skill（最低 %s / 100）\n" "skill-doctor" "$SKILL_HITS" "$SD_MIN"
else
  printf "  %-14s %s\n" "skill-doctor" "跳过（项目内无 skill）"
fi
printf "  %-14s %s\n" "env-doctor" "见上方原始数据（交模型按 rules.md 判定）"
if [ "$ADVISORY_FAIL" -gt 0 ]; then
  printf "  %-14s %s\n" "外部 Skill" "有诊断失败（仅提示，不计入项目门禁）"
fi
echo ""
echo "  免费 CLI · MIT 开源 · 可视化报告卡（付费）→ GitHub/ClawHub @huiyonghkw"
echo "  套件说明: references/doctor-suite.md"
if [ "$SUITE_FAIL" -ne 0 ]; then
  echo "❌ Doctor suite 失败：至少一个门禁检查未通过。" >&2
else
  echo "✅ Doctor suite 通过。"
fi
exit "$SUITE_FAIL"
