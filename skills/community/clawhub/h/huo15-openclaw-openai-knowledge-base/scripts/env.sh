#!/bin/bash
# env.sh — 加载知识库环境变量
# 用法: source env.sh [--scope agent|shared]
# 或: KB_SCOPE=shared source env.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# shellcheck disable=SC1091
source "$SCRIPT_DIR/kb-scope.sh"
kb_parse_scope "$@"

export KB_ROOT="$SKILL_ROOT"
export KB_RAW_DIR="${KB_DATA_DIR}/raw"
export KB_WIKI_DIR="${KB_DATA_DIR}/wiki"
export KB_CACHE_DIR="${KB_DATA_DIR}/cache"

# 读取全局配置（Obsidian + shared_kb）
KB_CONFIG="$SKILL_ROOT/config.json"
if [ -f "$KB_CONFIG" ]; then
  OBSIDIAN_ENABLED=$(python3 -c "
import json
with open('$KB_CONFIG') as f:
    cfg = json.load(f)
v = cfg.get('obsidian', {}).get('enabled', False)
print('true' if v else 'false')
" 2>/dev/null || echo "false")
  OBSIDIAN_VAULT=$(python3 -c "
import json
with open('$KB_CONFIG') as f:
    cfg = json.load(f)
v = cfg.get('obsidian', {}).get('vault_path', '')
print(v if v else '')
" 2>/dev/null || echo "")
  SHARED_KB_ENABLED=$(python3 -c "
import json
with open('$KB_CONFIG') as f:
    cfg = json.load(f)
print('true' if cfg.get('shared_kb', {}).get('enabled', True) else 'false')
" 2>/dev/null || echo "true")
  export OBSIDIAN_ENABLED OBSIDIAN_VAULT SHARED_KB_ENABLED
fi

export PATH="$SCRIPT_DIR:$PATH"

echo "✅ 知识库环境已加载（scope=$KB_SCOPE）"
echo "   KB_DATA_DIR: $KB_DATA_DIR"
echo "   KB_RAW_DIR:  $KB_RAW_DIR"
echo "   KB_WIKI_DIR: $KB_WIKI_DIR"
echo "   SHARED_KB:   ${SHARED_KB_ENABLED:-true}  (${HOME}/.openclaw/kb/shared)"
echo "   OBSIDIAN:    ${OBSIDIAN_ENABLED:-false} ${OBSIDIAN_VAULT:+→ vault: $OBSIDIAN_VAULT}"
