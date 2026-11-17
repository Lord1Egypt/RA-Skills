#!/usr/bin/env bash
# pt-passport CLI install/update script
# Installs from local package directory. Skips if installed version == local version.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/pt-passport"

if ! command -v npm &>/dev/null; then
  echo "npm: command not found. Please install Node.js >=18" >&2
  exit 2
fi

if [ ! -d "$PACKAGE_DIR" ]; then
  echo "No local package found in $SCRIPT_DIR" >&2
  exit 3
fi

# 从 package.json 读取版本号
BUNDLE_VERSION=$(node -e "console.log(require('$PACKAGE_DIR/package.json').version)")
if [ -z "$BUNDLE_VERSION" ]; then
  echo "Failed to read version from package.json" >&2
  exit 3
fi

# 获取已安装版本（直接用 pt-passport --version，取最后一行以跳过 CLIGuard Wrapper 前缀行）
LOCAL=$(pt-passport --version 2>/dev/null | tail -1 || true)

# 版本一致则跳过
if [ "$LOCAL" = "$BUNDLE_VERSION" ]; then
  echo "Already up-to-date (pt-passport@$LOCAL), skipping."
  exit 0
fi

# 安装本地包目录
echo "Installing pt-passport@$BUNDLE_VERSION from local package..."
npm install -g "$PACKAGE_DIR" --save-exact --force || {
  echo "Install failed." >&2; exit 1
}
