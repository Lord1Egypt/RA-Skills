#!/usr/bin/env bash
# 把 job-screening 装到本机的 Codex / Claude Code。
# 用法：bash install.sh                 （自动检测装到哪个）
#       bash install.sh codex           （只装 Codex）
#       bash install.sh claude          （只装 Claude Code）
#       bash install.sh --force [codex|claude]
#           目标里已有一份无法识别的安装时，默认先备份再停止、不覆盖。
#           只有显式传入 --force 才会在备份之后继续安装。
# profile/ 始终排除，安装脚本不改写用户档案。
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORCE=0
TARGET="auto"
SEEN_TARGET=0

usage() {
  echo "用法: bash install.sh [--force] [codex|claude]"
  exit 1
}

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    codex|claude)
      if [ "$SEEN_TARGET" -eq 1 ]; then
        usage
      fi
      TARGET="$arg"
      SEEN_TARGET=1
      ;;
    *) usage ;;
  esac
done

TARGETS=()
case "$TARGET" in
  codex)  TARGETS=("$HOME/.codex/skills/job-screening") ;;
  claude) TARGETS=("$HOME/.claude/skills/job-screening") ;;
  auto)
    [ -d "$HOME/.codex" ]  && TARGETS+=("$HOME/.codex/skills/job-screening")
    [ -d "$HOME/.claude" ] && TARGETS+=("$HOME/.claude/skills/job-screening")
    ;;
esac

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "没找到 ~/.codex 或 ~/.claude —— 先装 Codex 或 Claude Code 再跑这个脚本。"
  exit 1
fi

install_one() {
  local DST="$1"
  mkdir -p "$DST"
  # 不用 --delete：目标里多出来的文件（你自己的档案、笔记）一律保留。
  # profile/ 排除：已有档案不会被仓库内容盖掉。
  rsync -a \
    --exclude '.git' --exclude 'profile' --exclude 'install.sh' --exclude '.DS_Store' \
    "$SRC"/ "$DST"/
  mkdir -p "$DST/profile"
  touch "$DST/.job-screening-installed"
  echo "✅ 已安装到 $DST"
}

for DST in "${TARGETS[@]}"; do
  # 目标已存在且没有本仓库的安装标记：先整份备份。
  # 没传 --force 就停在这里，不 rsync、不覆盖。
  # 传了 --force 才在备份之后继续安装。
  if [ -d "$DST" ] && [ ! -f "$DST/.job-screening-installed" ]; then
    BAK="$DST.bak-$(date +%Y%m%d-%H%M%S)"
    if [ -e "$BAK" ]; then
      BAK="${BAK}-$$"
    fi
    cp -R "$DST" "$BAK"
    echo "⚠️  $DST 已存在，且不是本仓库留下的安装，已整份备份到："
    echo "    $BAK"
    if [ "$FORCE" -eq 0 ]; then
      echo "已停止，没有覆盖这份安装。"
      echo "确认要用本仓库替换它，请加上 --force 再跑一次。"
      echo "无论是否 --force，profile/ 都不会被安装脚本改写。"
      exit 1
    fi
  fi

  install_one "$DST"
done

echo
echo "打开 Codex 或 Claude Code，说一句「帮我筛一下秋招岗位」就会触发。"
echo "第一次用它会问你要简历，走一遍建档（约 10 分钟），之后每次直接丢岗位列表就行。"
