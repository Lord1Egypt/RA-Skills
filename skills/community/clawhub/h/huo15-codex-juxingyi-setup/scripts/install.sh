#!/usr/bin/env bash
# Codex 安装检测与引导
# 用法: bash install.sh
set -euo pipefail

echo "=== Codex 安装检测 ==="
echo ""

# --- ChatGPT 桌面版（含 Codex 面板）---
echo "[1/2] 检测 ChatGPT 桌面版..."
CHATGPT_APP="/Applications/ChatGPT.app"
if [ -d "$CHATGPT_APP" ]; then
  VERSION=$(defaults read "$CHATGPT_APP/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null || echo "未知")
  echo "  已安装 (版本 $VERSION)"
  echo "  路径: $CHATGPT_APP"
  CODEX_CLI_PATH="$CHATGPT_APP/Contents/Resources/codex"
  if [ -x "$CODEX_CLI_PATH" ]; then
    echo "  Codex CLI (桌面版内置): $CODEX_CLI_PATH"
  fi
else
  echo "  未安装"
  echo ""
  echo "  安装方式（选一）："
  echo "    A) Homebrew:  brew install --cask chatgpt"
  echo "    B) 手动下载:  https://chatgpt.com/download"
  echo ""
  read -p "  是否现在用 Homebrew 安装？(y/N) " -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v brew &>/dev/null; then
      echo "  正在安装..."
      brew install --cask chatgpt
      echo "  安装完成"
    else
      echo "  Homebrew 未安装，请先安装: https://brew.sh"
      echo "  或手动下载: https://chatgpt.com/download"
    fi
  fi
fi

echo ""

# --- Codex CLI（独立安装）---
echo "[2/2] 检测 Codex CLI..."
if command -v codex &>/dev/null; then
  CODEX_VERSION=$(codex --version 2>/dev/null || echo "未知")
  echo "  已安装 (版本 $CODEX_VERSION)"
  echo "  路径: $(which codex)"
else
  CODEX_CLI_PATH="/Applications/ChatGPT.app/Contents/Resources/codex"
  if [ -x "$CODEX_CLI_PATH" ]; then
    echo "  已安装 (桌面版内置)"
    echo "  路径: $CODEX_CLI_PATH"
  else
    echo "  未安装"
    echo ""
    echo "  安装方式: npm install -g @openai/codex"
    echo ""
    read -p "  是否现在安装？(y/N) " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      if command -v npm &>/dev/null; then
        echo "  正在安装..."
        npm install -g @openai/codex
        echo "  安装完成"
      else
        echo "  npm 未安装，请先安装 Node.js"
      fi
    fi
  fi
fi

echo ""

# --- Codex 配置目录 ---
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
echo "Codex 配置目录: $CODEX_HOME"
if [ -f "$CODEX_HOME/config.toml" ]; then
  echo "  配置文件已存在"
  CURRENT_PROVIDER=$(grep -E '^model_provider' "$CODEX_HOME/config.toml" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "")
  CURRENT_BASE=$(grep -E '^openai_base_url' "$CODEX_HOME/config.toml" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "")
  if [ -n "$CURRENT_PROVIDER" ]; then
    echo "  当前 provider: $CURRENT_PROVIDER"
  fi
  if [ -n "$CURRENT_BASE" ]; then
    echo "  当前 base_url: $CURRENT_BASE"
  fi
else
  echo "  配置文件不存在（运行 configure.sh 创建）"
fi

echo ""
echo "=== 安装检测完成 ==="
echo "下一步: bash scripts/configure.sh"
