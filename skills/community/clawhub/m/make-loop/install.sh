#!/usr/bin/env bash
# 把 make-loop 装到本机的 Codex / Claude Code。
# 用法：bash install.sh                  （自动检测装到哪个）
#       bash install.sh codex            （只装 Codex）
#       bash install.sh claude           （只装 Claude Code）
#       以上命令都可以再加 --force        （别人的同名目录：备份之后才覆盖）
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="auto"
FORCE=0
SEEN_TARGET=0

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    codex|claude|auto)
      if [ "$SEEN_TARGET" -eq 1 ]; then
        echo "用法: bash install.sh [codex|claude] [--force]"
        exit 1
      fi
      SEEN_TARGET=1
      TARGET="$arg"
      ;;
    *) echo "用法: bash install.sh [codex|claude] [--force]"; exit 1 ;;
  esac
done

TARGETS=()
case "$TARGET" in
  codex)  TARGETS=("$HOME/.codex/skills/make-loop") ;;
  claude) TARGETS=("$HOME/.claude/skills/make-loop") ;;
  auto)
    [ -d "$HOME/.codex" ]  && TARGETS+=("$HOME/.codex/skills/make-loop")
    [ -d "$HOME/.claude" ] && TARGETS+=("$HOME/.claude/skills/make-loop")
    ;;
esac

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "没找到 ~/.codex 或 ~/.claude —— 先装 Codex 或 Claude Code 再跑这个脚本。"
  exit 1
fi

# 别人的同名目录：先整份备份。没有 --force 就停，不 rsync、不覆盖。
# （典型情况：你本来就有一个同名的私人版 skill。）
STOPPED=0
for DST in "${TARGETS[@]}"; do
  if [ -d "$DST" ] && [ ! -f "$DST/.make-loop-installed" ]; then
    BAK="$DST.bak-$(date +%Y%m%d-%H%M%S)"
    if [ -e "$BAK" ]; then
      n=2
      while [ -e "${BAK}-${n}" ]; do
        n=$((n + 1))
      done
      BAK="${BAK}-${n}"
    fi
    cp -R "$DST" "$BAK"
    echo "⚠️  $DST 已存在且不是本仓库装的，已整份备份到："
    echo "    $BAK"
    if [ "$FORCE" -eq 0 ]; then
      STOPPED=1
    else
      echo "    已加上 --force，备份之后继续安装。"
    fi
  fi
done

if [ "$STOPPED" -eq 1 ]; then
  echo "没有 --force，安装停在这里，上面的目录都没有被覆盖。"
  echo "确认要覆盖，在原来的命令后面加上 --force。"
  exit 1
fi

for DST in "${TARGETS[@]}"; do
  mkdir -p "$DST"
  # 不用 --delete：目标里多出来的文件（你自己的档案、笔记）一律保留
  rsync -a \
    --exclude '.git' --exclude 'install.sh' --exclude '.DS_Store' \
    "$SRC"/ "$DST"/
  touch "$DST/.make-loop-installed"
  echo "✅ 已安装到 $DST"
done

echo
echo "打开 Codex 或 Claude Code，说一句「帮我变成 loop」，或者用 /make-loop 你的任务 就会触发。"
