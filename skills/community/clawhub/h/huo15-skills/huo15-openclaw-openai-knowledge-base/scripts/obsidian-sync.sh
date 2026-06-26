#!/bin/bash
# obsidian-sync.sh — 同步 wiki/ 到 Obsidian vault
# 用法: ./obsidian-sync.sh [--watch] [--dry-run]
#依赖: obsidian-cli (brew install obsidian-cli)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(cd "$(dirname "$SCRIPT_DIR")" && pwd)"
CONFIG_FILE="$KB_ROOT/config.json"

# Agent 隔离：使用 Agent 数据目录而非技能源码目录
AGENT_DIR="${AGENT_DIR:-$HOME/.openclaw/agents/main/agent}"
KB_DATA_DIR="${AGENT_DIR}/kb"

# 默认值
OBSIDIAN_ENABLED="false"
OBSIDIAN_VAULT_PATH=""

# 读取配置
load_config() {
  if [ -f "$CONFIG_FILE" ]; then
    # 用 python3 解析 JSON（跨平台，无需 jq）
    OBSIDIAN_ENABLED=$(python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
v = cfg.get('obsidian', {}).get('enabled', False)
print('true' if v else 'false')
" 2>/dev/null || echo "false")

    OBSIDIAN_VAULT_PATH=$(python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
v = cfg.get('obsidian', {}).get('vault_path', '')
print(v if v else '')
" 2>/dev/null || echo "")
  fi
}

load_config

DRY_RUN=false
WATCH_MODE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --watch)
      WATCH_MODE=true
      shift
      ;;
    --enable)
      OBSIDIAN_ENABLED="true"
      shift
      ;;
    --disable)
      OBSIDIAN_ENABLED="false"
      shift
      ;;
    --vault)
      OBSIDIAN_VAULT_PATH="$2"
      shift 2
      ;;
    --help)
      echo "用法: obsidian-sync.sh [选项]"
      echo "  --dry-run    预览同步（不实际写入）"
      echo "  --watch      监听 wiki/ 变化并自动同步"
      echo "  --enable     启用 Obsidian 同步"
      echo "  --disable    禁用 Obsidian 同步"
      echo "  --vault <p>  指定 vault 路径"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

# 检测 obsidian-cli（优先使用，obsidian 技能已封装 vault 发现）
OBSIDIAN_CLI=""
if command -v obsidian-cli &>/dev/null; then
  OBSIDIAN_CLI="obsidian-cli"
fi

# 如果未启用，提示并退出
if [ "$OBSIDIAN_ENABLED" != "true" ]; then
  echo "⚠️  Obsidian 同步未启用"
  echo ""
  echo "启用方式（二选一）："
  echo "  1. 编辑 $CONFIG_FILE，设置 obsidian.enabled = true"
  echo "  2. 运行: $0 --enable --vault '/path/to/vault'"
  echo ""
  echo "当前配置: enabled=$OBSIDIAN_ENABLED, vault=$OBSIDIAN_VAULT_PATH"
  exit 0
fi

# 解析 vault 路径
# 优先用 obsidian-cli（来自 obsidian 技能封装），其次用配置文件，再次回退到手动指定
resolve_vault() {
  # 1. 配置文件中手动指定
  if [ -n "$OBSIDIAN_VAULT_PATH" ]; then
    echo "$OBSIDIAN_VAULT_PATH"
    return
  fi

  # 2. 用 obsidian-cli 发现默认 vault（obsidian 技能已封装此逻辑）
  if [ -n "$OBSIDIAN_CLI" ]; then
    local vault_path
    vault_path=$(obsidian-cli print-default --path-only 2>/dev/null || echo "")
    if [ -n "$vault_path" ]; then
      echo "$vault_path"
      return
    fi
  fi

  # 3. 读取 obsidian.json（兜底，与 obsidian 技能一致）
  local obsidian_json="$HOME/Library/Application Support/obsidian/obsidian.json"
  if [ -f "$obsidian_json" ]; then
    python3 -c "
import json, sys
with open('$obsidian_json') as f:
    vaults = json.load(f)
for vault in vaults:
    if vault.get('open', False):
        print(vault.get('path', ''))
        break
" 2>/dev/null || echo ""
  fi
}

VAULT_PATH=$(resolve_vault)

if [ -z "$VAULT_PATH" ]; then
  echo "❌ 未找到 Obsidian vault 路径"
  echo ""
  echo "请设置 vault 路径："
  echo "  1. 编辑 $CONFIG_FILE"
  echo "  2. 设置 obsidian.vault_path 为你的 vault 路径"
  echo ""
  echo "  或直接运行: $0 --enable --vault '/Users/xxx/Documents/我的笔记'"
  exit 1
fi

WIKI_DIR="${KB_DATA_DIR}/wiki"
VAULT_WIKI_DIR="$VAULT_PATH/知识库"

echo "📚 Obsidian 同步"
echo "   Wiki:    $WIKI_DIR"
echo "   Vault:   $VAULT_WIKI_DIR"
echo "   CLI:     ${OBSIDIAN_CLI:-无（文件直同步）}"
echo ""

if [ ! -d "$WIKI_DIR" ]; then
  echo "⚠️  wiki/ 目录不存在，请先运行编译"
  exit 1
fi

if [ "$DRY_RUN" = "true" ]; then
  echo "🔍 [dry-run] 预览同步..."
fi

# 同步文件
sync_files() {
  local src="$1"
  local dst="$2"
  local count=0

  mkdir -p "$dst"

  # 同步 wiki/ 下的 .md 文件
  while IFS= read -r -d '' f; do
    local rel="${f#$src/}"
    local dst_file="$dst/$rel"
    local dst_dir=$(dirname "$dst_file")

    mkdir -p "$dst_dir"

    if [ "$DRY_RUN" = "true" ]; then
      echo "  [dry-run] 复制: $rel"
    else
      # 只有文件内容变化才复制（减少 Obsidian 触发器）
      if [ ! -f "$dst_file" ] || ! diff -q "$f" "$dst_file" &>/dev/null; then
        cp "$f" "$dst_file"
        count=$((count + 1))
      fi
    fi
  done < <(find "$src" -name "*.md" -print0 2>/dev/null)

  echo "   同步完成: $count 个文件更新"
}

if [ "$WATCH_MODE" = "true" ]; then
  echo "👀 监听 wiki/ 变化（Ctrl+C 退出）..."
  # 使用 fswatch 或 launchd（macOS 原生）
  if command -v fswatch &>/dev/null; then
    fswatch -o "$WIKI_DIR" | while read; do
      echo "$(date '+%H:%M:%S') 检测到变化，同步中..."
      sync_files "$WIKI_DIR" "$VAULT_WIKI_DIR"
    done
  else
    # 降级：简单轮询（每30秒）
    echo "⚠️  未安装 fswatch，降级为 30 秒轮询"
    while true; do
      sleep 30
      sync_files "$WIKI_DIR" "$VAULT_WIKI_DIR"
    done
  fi
else
  sync_files "$WIKI_DIR" "$VAULT_WIKI_DIR"
fi

# 可选：用 obsidian-cli 更新索引
if [ -n "$OBSIDIAN_CLI" ] && [ "$DRY_RUN" = "false" ]; then
  echo ""
  echo "📋 更新 Obsidian 索引..."
  # obsidian-cli search-index rebuild 2>/dev/null || true
fi

echo ""
echo "✅ Obsidian 同步完成"
echo "   打开 Obsidian 即可在 vault 中看到「知识库」文件夹"
