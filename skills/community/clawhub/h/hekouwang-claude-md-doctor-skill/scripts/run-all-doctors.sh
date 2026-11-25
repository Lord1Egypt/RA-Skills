#!/usr/bin/env bash
# hekouwang-doctor-suite · 三件套体检编排
# 用法: bash scripts/run-all-doctors.sh [项目根目录] [--with-env-doctor]
# 默认只跑 md-doctor（AGENTS.md / CLAUDE.md）；项目里有 skills 目录时顺带跑 skill-doctor。
# env-doctor 会扫本机环境（宿主目录 / 版本管理器 / 磁盘），默认不跑，需显式加 --with-env-doctor。
# 依赖: 对应 doctor skill 已装在 HEKOUWANG_SKILLS_DIR（默认 ~/.claude/skills），缺失则跳过该段。
set -uo pipefail

WITH_ENV=0
ROOT_ARG="."
for a in "$@"; do
  case "$a" in
    --with-env-doctor) WITH_ENV=1 ;;
    -h|--help)
      echo "用法: bash scripts/run-all-doctors.sh [项目根目录] [--with-env-doctor]"
      echo "  --with-env-doctor  额外调用 env-doctor 扫本机开发环境（默认关闭）"
      exit 0
      ;;
    -*)
      echo "未知参数: $a（支持 --with-env-doctor / --help）" >&2
      exit 2
      ;;
    *) ROOT_ARG="$a" ;;
  esac
done

ROOT="$(cd "$ROOT_ARG" && pwd)"
SKILLS="${HEKOUWANG_SKILLS_DIR:-$HOME/.claude/skills}"
MD="$SKILLS/hekouwang-claude-md-doctor-skill"
SD="$SKILLS/hekouwang-claude-skill-doctor-skill"
ED="$SKILLS/hekouwang-env-doctor-skill"

die() { echo "ERROR: $*" >&2; exit 1; }
[ -f "$MD/check.py" ] || die "缺 md-doctor: $MD"

json_score() {
  python3 -c "import sys,json; print(json.load(sys.stdin).get('score','—'))" 2>/dev/null || echo "—"
}

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  HEKOUWANG DOCTOR SUITE  ·  三件套体检编排              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "项目: $ROOT"
[ "$WITH_ENV" -eq 1 ] && echo "环境扫描: 已启用（--with-env-doctor）" || echo "环境扫描: 未启用（需要时加 --with-env-doctor）"
echo ""

echo "━━━━ ① md-doctor · AGENTS.md / CLAUDE.md ━━━━"
MD_SCORE=$(python3 "$MD/check.py" "$ROOT" --json 2>/dev/null | json_score)
python3 "$MD/check.py" "$ROOT" || true
echo ""

echo "━━━━ ② skill-doctor · 项目内 Agent Skills ━━━━"
SKILL_HITS=0
SD_MIN=100
SD_READY=1
[ -f "$SD/check.py" ] || SD_READY=0
for base in "$ROOT/.agents/skills" "$ROOT/.cursor/skills" "$ROOT/skills"; do
  [ -d "$base" ] || continue
  for d in "$base"/*; do
    [ -f "$d/SKILL.md" ] || continue
    SKILL_HITS=$((SKILL_HITS + 1))
    if [ "$SD_READY" -eq 0 ]; then
      echo "  → $(basename "$d")（未安装 skill-doctor，跳过）"
      continue
    fi
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
elif [ "$SD_READY" -eq 0 ]; then
  SD_MIN="—"
fi

echo "━━━━ ③ env-doctor · 本机开发环境（需 --with-env-doctor）━━━━"
ENV_RAN=0
if [ "$WITH_ENV" -eq 0 ]; then
  echo "  (默认不扫本机环境；确认需要时加 --with-env-doctor)"
elif [ ! -f "$ED/scripts/scan.sh" ]; then
  echo "  (未安装 env-doctor：$ED，跳过)"
else
  ENV_RAN=1
  bash "$ED/scripts/scan.sh" --profile ai-dev
fi
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  汇总                                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
printf "  %-14s %s\n" "md-doctor" "${MD_SCORE} / 100"
if [ "$SD_READY" -eq 0 ]; then
  printf "  %-14s %s\n" "skill-doctor" "跳过（未安装 skill-doctor）"
elif [ "$SKILL_HITS" -gt 0 ]; then
  printf "  %-14s %d 个 skill（最低 %s / 100）\n" "skill-doctor" "$SKILL_HITS" "$SD_MIN"
else
  printf "  %-14s %s\n" "skill-doctor" "跳过（项目内无 skill）"
fi
if [ "$ENV_RAN" -eq 1 ]; then
  printf "  %-14s %s\n" "env-doctor" "见上方原始数据（交模型按 rules.md 判定）"
else
  printf "  %-14s %s\n" "env-doctor" "未运行（加 --with-env-doctor 启用）"
fi
echo ""
echo "  免费 CLI · MIT 开源 · 可视化报告卡（付费）→ GitHub/ClawHub @huiyonghkw"
echo "  套件说明: references/doctor-suite.md"
