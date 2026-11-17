#!/usr/bin/env bash
# 一键把 netease-dynamic-avatar 装进本机 harness 的技能目录。
# 用法:  bash install.sh   [目标技能根目录]
# 默认目标: $DSH_HOME/skills  (DSH_HOME 默认 ~/.dsh)
set -euo pipefail

REPO="https://github.com/yuan-dev39/netease-dynamic-avatar.git"
ROOT="${1:-${DSH_HOME:-$HOME/.dsh}/skills}"
DEST="$ROOT/netease-dynamic-avatar"

echo "==> 目标目录: $DEST"
mkdir -p "$ROOT"

if [ -d "$DEST/.git" ]; then
  echo "==> 已存在 git 仓库，改为 pull"
  git -C "$DEST" pull --ff-only
elif [ -d "$DEST" ]; then
  echo "==> 已存在同名目录但不是 git 仓库，备份后重装"
  mv "$DEST" "$DEST.bak.$(date +%s)"
  git clone --depth 1 "$REPO" "$DEST"
else
  git clone --depth 1 "$REPO" "$DEST"
fi

if [ ! -f "$DEST/SKILL.md" ]; then
  echo "!! 安装失败：$DEST/SKILL.md 不存在" >&2
  exit 1
fi

echo
echo "✅ 装好了: $DEST"
echo "   重开一次会话（或刷新 harness 的 Web GUI）即可在技能列表里看到 netease-dynamic-avatar"
echo
echo "可选：转码脚本需要 Pillow"
echo "   python -m pip install --no-user --target \"$DEST/pylibs\" pillow"
