#!/bin/bash
# obsidian-sync.sh — 同步 wiki/ 到 Obsidian vault（支持 agent / shared 双作用域）
# 用法: ./obsidian-sync.sh [--scope agent|shared] [--all-scopes] [--watch] [--dry-run]
# 依赖: obsidian-cli (brew install obsidian-cli)（可选）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(cd "$(dirname "$SCRIPT_DIR")" && pwd)"
CONFIG_FILE="$KB_ROOT/config.json"

# shellcheck disable=SC1091
source "$SCRIPT_DIR/kb-scope.sh"

# 先抽出 --scope / --shared / --agent-scope，剩余参数回填到 $@
kb_parse_scope "$@"
set -- "${KB_ARGS[@]}"

# 默认值
OBSIDIAN_ENABLED="false"
OBSIDIAN_VAULT_PATH=""

load_config() {
  if [ -f "$CONFIG_FILE" ]; then
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
ALL_SCOPES=false
WITH_BASES=false  # v2.8.0: 同步后自动调 kb-bases --vault-out

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
    --all-scopes)
      ALL_SCOPES=true
      shift
      ;;
    --with-bases)
      WITH_BASES=true
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
      cat <<HELP
用法: obsidian-sync.sh [选项]
  --dry-run              预览同步（不实际写入）
  --watch                监听 wiki/ 变化并自动同步
  --scope agent|shared   指定作用域（默认 agent；也可用 --shared / --agent-scope）
  --all-scopes           同时同步 agent + shared（分别进独立子目录）
  --enable               启用 Obsidian 同步
  --disable              禁用 Obsidian 同步
  --vault <p>            指定 vault 路径
  --with-bases           v2.8.0: 同步后跑 kb-bases --vault-out 生成 5 个 .base 视图

同步目标布局（vault/知识库/ 下）：
  agent scope  → vault/知识库/agent/
  shared scope → vault/知识库/shared/
  --with-bases → vault/知识库/<scope>/.bases/*.base
HELP
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
resolve_vault() {
  if [ -n "$OBSIDIAN_VAULT_PATH" ]; then
    echo "$OBSIDIAN_VAULT_PATH"
    return
  fi

  if [ -n "$OBSIDIAN_CLI" ]; then
    local vault_path
    vault_path=$(obsidian-cli print-default --path-only 2>/dev/null || echo "")
    if [ -n "$vault_path" ]; then
      echo "$vault_path"
      return
    fi
  fi

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

VAULT_KB_ROOT="$VAULT_PATH/知识库"

# 计算待同步 scope 列表
if [ "$ALL_SCOPES" = "true" ]; then
  SCOPES=("agent" "shared")
else
  SCOPES=("$KB_SCOPE")
fi

# 返回 scope 对应的 wiki 源目录
scope_wiki_dir() {
  local scope="$1"
  case "$scope" in
    agent) echo "$AGENT_DIR/kb/wiki" ;;
    shared) echo "$HOME/.openclaw/kb/shared/wiki" ;;
    *) echo "" ;;
  esac
}

# 同步单个源目录到目标
sync_files() {
  local src="$1"
  local dst="$2"
  local count=0

  mkdir -p "$dst"

  while IFS= read -r -d '' f; do
    local rel="${f#$src/}"
    local dst_file="$dst/$rel"
    local dst_dir
    dst_dir=$(dirname "$dst_file")

    mkdir -p "$dst_dir"

    if [ "$DRY_RUN" = "true" ]; then
      echo "  [dry-run] 复制: $rel"
    else
      if [ ! -f "$dst_file" ] || ! diff -q "$f" "$dst_file" &>/dev/null; then
        cp "$f" "$dst_file"
        count=$((count + 1))
      fi
    fi
  done < <(find "$src" -name "*.md" -print0 2>/dev/null)

  echo "   同步完成: $count 个文件更新"
}

sync_scope() {
  local scope="$1"
  local wiki_dir
  wiki_dir=$(scope_wiki_dir "$scope")
  local dst="$VAULT_KB_ROOT/$scope"

  if [ ! -d "$wiki_dir" ]; then
    echo "⚠️  [$scope] wiki/ 不存在: $wiki_dir，跳过"
    return
  fi

  echo "📂 [$scope]"
  echo "   Wiki:  $wiki_dir"
  echo "   Vault: $dst"
  sync_files "$wiki_dir" "$dst"
}

echo "📚 Obsidian 同步"
echo "   Vault: $VAULT_KB_ROOT"
echo "   CLI:   ${OBSIDIAN_CLI:-无（文件直同步）}"
echo "   Scope: ${SCOPES[*]}"
echo ""

if [ "$DRY_RUN" = "true" ]; then
  echo "🔍 [dry-run] 预览同步..."
fi

if [ "$WATCH_MODE" = "true" ]; then
  echo "👀 监听 wiki/ 变化（Ctrl+C 退出）..."

  WATCH_PATHS=()
  for s in "${SCOPES[@]}"; do
    p=$(scope_wiki_dir "$s")
    [ -d "$p" ] && WATCH_PATHS+=("$p")
  done

  if [ ${#WATCH_PATHS[@]} -eq 0 ]; then
    echo "❌ 所有 scope 对应 wiki/ 目录都不存在"
    exit 1
  fi

  if command -v fswatch &>/dev/null; then
    fswatch -o "${WATCH_PATHS[@]}" | while read -r _; do
      echo "$(date '+%H:%M:%S') 检测到变化，同步中..."
      for s in "${SCOPES[@]}"; do
        sync_scope "$s"
      done
    done
  else
    echo "⚠️  未安装 fswatch，降级为 30 秒轮询"
    while true; do
      sleep 30
      for s in "${SCOPES[@]}"; do
        sync_scope "$s"
      done
    done
  fi
else
  for s in "${SCOPES[@]}"; do
    sync_scope "$s"
    echo ""
  done
fi

# 可选：用 obsidian-cli 更新索引
if [ -n "$OBSIDIAN_CLI" ] && [ "$DRY_RUN" = "false" ]; then
  echo "📋 更新 Obsidian 索引..."
  # obsidian-cli search-index rebuild 2>/dev/null || true
fi

echo ""
echo "✅ Obsidian 同步完成"
echo "   打开 Obsidian 即可在 vault「知识库/」下看到: ${SCOPES[*]}"

# v2.8.0: --with-bases 钩子，每个 scope 跑一次 kb-bases --vault-out
if [ "$WITH_BASES" = "true" ] && [ "$DRY_RUN" = "false" ]; then
  KB_BASES="$(dirname "$0")/kb-bases"
  if [ -x "$KB_BASES" ]; then
    echo ""
    echo "📊 生成 Obsidian Bases 视图..."
    for s in "${SCOPES[@]}"; do
      "$KB_BASES" --scope "$s" --vault-out 2>&1 | sed 's|^|  |'
    done
    echo "   在 Obsidian 里打开 vault/知识库/<scope>/.bases/*.base 即可使用"
  else
    echo "⚠️  未找到 kb-bases，跳过 --with-bases" >&2
  fi
fi
