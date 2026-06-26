#!/usr/bin/env bash
# pt-passport CLI install/update script
# 三级 fallback：本地 .tgz → 本地 .tgz.txt → curl Gitee raw
#   - 本地 .tgz       ：开发者 clone GitHub/Gitee 仓库
#   - 本地 .tgz.txt   ：历史 ClawHub 包形态 (兼容保留)
#   - 远程 Gitee raw  ：ClawHub 包内不带 tgz, 安装时按需拉取
set -euo pipefail

# 升级 pt-passport 时同步改这里
PT_PASSPORT_VERSION="0.1.4"
GITEE_RAW_URL="https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill/raw/main/references/meituan-queue/references/meituan-passport-user-auth/scripts/mtuser-pt-passport-${PT_PASSPORT_VERSION}.tgz"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

if ! command -v npm &>/dev/null; then
  echo "npm: command not found. Please install Node.js >=18" >&2
  exit 2
fi

TMP_DIR=""
cleanup() { [ -n "$TMP_DIR" ] && rm -rf "$TMP_DIR"; }
trap cleanup EXIT

# 1) 优先：本地 .tgz（glob 无匹配时 || true 兜底, 避免 set -e 误退出）
TGZ_FILE=$(for f in "$SCRIPT_DIR"/mtuser-pt-passport-*.tgz; do [ -f "$f" ] && echo "$f"; done | sort -V | tail -1 || true)

# 2) 次选：本地 .tgz.txt（兼容历史 ClawHub 包形态）
TXT_FILE=""
if [ -z "$TGZ_FILE" ]; then
  TXT_FILE=$(for f in "$SCRIPT_DIR"/mtuser-pt-passport-*.tgz.txt; do [ -f "$f" ] && echo "$f"; done | sort -V | tail -1 || true)
fi

# 3) 兜底：从 Gitee raw 远程拉取（ClawHub 安装场景）
if [ -z "$TGZ_FILE" ] && [ -z "$TXT_FILE" ]; then
  if ! command -v curl >/dev/null 2>&1; then
    echo "本地未找到 tgz 包且 curl 未安装, 无法远程拉取" >&2
    exit 3
  fi
  TMP_DIR=$(mktemp -d)
  TGZ_FILE="$TMP_DIR/mtuser-pt-passport-${PT_PASSPORT_VERSION}.tgz"
  echo "本地未找到 tgz 包, 从 Gitee raw 拉取 v${PT_PASSPORT_VERSION}..."
  if ! curl -fsSL "$GITEE_RAW_URL" -o "$TGZ_FILE"; then
    echo "远程拉取失败: $GITEE_RAW_URL" >&2
    exit 3
  fi
fi

# 从源文件名提取版本号，兼容 .tgz 和 .tgz.txt
SOURCE_NAME=$(basename "${TGZ_FILE:-$TXT_FILE}")
BUNDLE_VERSION=$(echo "$SOURCE_NAME" | sed 's/mtuser-pt-passport-//; s/\.txt$//; s/\.tgz$//')
if [ -z "$BUNDLE_VERSION" ]; then
  echo "Failed to parse version from: $SOURCE_NAME" >&2
  exit 3
fi

# 获取已安装版本（直接用 pt-passport --version，取最后一行以跳过 CLIGuard Wrapper 前缀行）
LOCAL=$(pt-passport --version 2>/dev/null | tail -1 || true)

# 版本一致则跳过
if [ "$LOCAL" = "$BUNDLE_VERSION" ]; then
  echo "Already up-to-date (pt-passport@$LOCAL), skipping."
  exit 0
fi

# .tgz.txt 形态：复制成临时真 .tgz 喂给 npm（npm 看扩展名识别包格式）
if [ -z "$TGZ_FILE" ]; then
  TMP_DIR=$(mktemp -d)
  TGZ_FILE="$TMP_DIR/mtuser-pt-passport-$BUNDLE_VERSION.tgz"
  cp "$TXT_FILE" "$TGZ_FILE"
fi

# 安装本地包
echo "Installing pt-passport@$BUNDLE_VERSION from local bundle..."
npm install -g "$TGZ_FILE" --save-exact --force || {
  echo "Install failed." >&2; exit 1
}
