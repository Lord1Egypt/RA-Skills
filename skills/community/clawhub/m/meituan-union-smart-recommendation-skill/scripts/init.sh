#!/usr/bin/env bash
# 环境初始化脚本：路径验证 + Python 检查 + Node.js >= 18 检查（自动 nvm 切换）+ pt-passport CLI 安装
# 输出格式（JSON）：
#   成功: {"ok": true, "scripts_dir": "<path>", "skill_dir": "<path>"}
#   失败: {"ok": false, "error": "PATH_NOT_FOUND" | "PYTHON_NOT_FOUND" | "PYTHON_VERSION_2" | "NODE_NOT_FOUND" | "NODE_VERSION_LOW" | "TGZ_NOT_FOUND" | "INSTALL_FAILED"}

set -e

PYTHON="${1:-python3}"
# 用 $0 自定位，不依赖任何环境变量，安装在任何路径都能正确找到
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="${SCRIPTS_DIR%/scripts}"

# ── 1. 路径验证 ──────────────────────────────────────────────
if [ ! -d "$SCRIPTS_DIR" ]; then
  echo '{"ok": false, "error": "PATH_NOT_FOUND"}'
  exit 1
fi

# ── 2. Python 检查 ───────────────────────────────────────────
PY_VER=$("$PYTHON" --version 2>/dev/null || echo "")

if [ -z "$PY_VER" ]; then
  echo '{"ok": false, "error": "PYTHON_NOT_FOUND"}'
  exit 1
fi

case "$PY_VER" in
  "Python 2."*)
    echo '{"ok": false, "error": "PYTHON_VERSION_2"}'
    exit 1
    ;;
esac

# ── 3. Node.js 检查（需要 >= 18，内置 fetch） ─────────────────
if ! command -v node &>/dev/null; then
  echo '{"ok": false, "error": "NODE_NOT_FOUND"}'
  exit 1
fi

NODE_MAJOR=$(node -e "process.stdout.write(String(process.versions.node.split('.')[0]))" 2>/dev/null || echo "0")
if [ "$NODE_MAJOR" -lt 18 ]; then
  # 尝试通过 nvm 自动切换到本地已安装的 18+
  NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  if [ -s "$NVM_DIR/nvm.sh" ]; then
    . "$NVM_DIR/nvm.sh" --no-use
    # 只匹配已安装版本（带 * 标记的行），筛选 >= 18
    TARGET_VER=$(nvm ls --no-colors 2>/dev/null | grep '\*' | grep -oE 'v(1[89]|[2-9][0-9]|[1-9][0-9]{2,})\.[0-9]+\.[0-9]+' | sort -V | tail -1 || true)
    if [ -n "$TARGET_VER" ]; then
      nvm use "$TARGET_VER" >/dev/null 2>&1 || true
      NODE_MAJOR=$(node -e "process.stdout.write(String(process.versions.node.split('.')[0]))" 2>/dev/null || echo "0")
    fi
  fi
  if [ "$NODE_MAJOR" -lt 18 ]; then
    echo '{"ok": false, "error": "NODE_VERSION_LOW", "current": "'"$NODE_MAJOR"'", "required": ">=18"}'
    exit 1
  fi
fi

if ! command -v npm &>/dev/null; then
  echo '{"ok": false, "error": "NODE_NOT_FOUND"}'
  exit 1
fi

# ── 4. pt-passport CLI 安装/更新 ─────────────────────────────
# 找到 scripts 目录下的本地安装包（取版本最新的一个）
TGZ_FILE=$(for f in "$SCRIPTS_DIR"/mtuser-pt-passport-*.tgz; do [ -f "$f" ] && echo "$f"; done | sort -V | tail -1)
if [ -z "$TGZ_FILE" ]; then
  echo '{"ok": false, "error": "TGZ_NOT_FOUND"}'
  exit 1
fi

# 从文件名中提取版本号，如 mtuser-pt-passport-0.1.4.tgz -> 0.1.4
BUNDLE_VERSION=$(basename "$TGZ_FILE" | sed 's/mtuser-pt-passport-//;s/\.tgz$//')

# 获取已安装版本
LOCAL=$(pt-passport --version 2>/dev/null | tail -1 || true)

# 版本不一致时安装
if [ "$LOCAL" != "$BUNDLE_VERSION" ]; then
  npm install -g "$TGZ_FILE" --save-exact --force >/dev/null 2>&1 || {
    echo '{"ok": false, "error": "INSTALL_FAILED"}'
    exit 1
  }
fi

# ── 成功 ─────────────────────────────────────────────────────
printf '{"ok": true, "scripts_dir": "%s", "skill_dir": "%s"}\n' "$SCRIPTS_DIR" "$SKILL_DIR"
