#!/usr/bin/env bash
# hekouwang-doctor-suite · 三件套一键体检
# 用法: bash scripts/run-all-doctors.sh [项目根目录]
# 依赖: 三个 doctor skill 已装在 HEKOUWANG_SKILLS_DIR（默认 ~/.claude/skills）
set -uo pipefail

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
  python3 -c "import sys,json; print(json.load(sys.stdin).get('score','—'))" 2>/dev/null || echo "—"
}

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  HEKOUWANG DOCTOR SUITE  ·  三件套一键体检              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "项目: $ROOT"
echo ""

echo "━━━━ ① md-doctor · AGENTS.md / CLAUDE.md ━━━━"
MD_SCORE=$(python3 "$MD/check.py" "$ROOT" --json 2>/dev/null | json_score)
python3 "$MD/check.py" "$ROOT" || true
echo ""

echo "━━━━ ② skill-doctor · 项目内 Agent Skills ━━━━"
SKILL_HITS=0
SD_MIN=100
for base in "$ROOT/.agents/skills" "$ROOT/.cursor/skills" "$ROOT/skills"; do
  [ -d "$base" ] || continue
  for d in "$base"/*; do
    [ -f "$d/SKILL.md" ] || continue
    SKILL_HITS=$((SKILL_HITS + 1))
    echo "  → $(basename "$d")"
    J=$(python3 "$SD/check.py" "$d" --json 2>/dev/null) || true
    S=$(echo "$J" | json_score)
  if [ "$S" != "—" ] && [ "$S" -lt "$SD_MIN" ] 2>/dev/null; then SD_MIN=$S; fi
    python3 "$SD/check.py" "$d" || true
    echo ""
  done
done
if [ "$SKILL_HITS" -eq 0 ]; then
  echo "  (未找到 .agents/skills/ / .cursor/skills/ 下的 SKILL.md，跳过)"
  SD_MIN="—"
  echo ""
fi

echo "━━━━ ③ env-doctor · 本机开发环境（--profile ai-dev）━━━━"
bash "$ED/scripts/scan.sh" --profile ai-dev
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
echo ""
echo "  免费 CLI · MIT 开源 · 可视化报告卡（付费）→ GitHub/ClawHub @huiyonghkw"
echo "  套件说明: references/doctor-suite.md"
