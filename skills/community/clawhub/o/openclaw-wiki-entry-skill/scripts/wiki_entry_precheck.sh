#!/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VAULT="${OPENCLAW_VAULT:-}"
TRANSIT_DIR="${WIKI_ENTRY_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
DOMAIN_DIR="${WIKI_ENTRY_DOMAIN_DIR:-$VAULT/Knowledge/领域}"
GRADUATED_DIR="${WIKI_ENTRY_GRADUATED_DIR:-$VAULT/Knowledge/已入库}"
INDEX_FILE="${WIKI_ENTRY_INDEX_FILE:-$VAULT/Knowledge/_INDEX.md}"
STATE_DIR="${WIKI_ENTRY_STATE_DIR:-$VAULT/.openclaw/state}"
RULE_VERSION="wiki-entry-skill-c-v7"
INIT_MODE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --vault)
      VAULT="$2"
      TRANSIT_DIR="${WIKI_ENTRY_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
      DOMAIN_DIR="${WIKI_ENTRY_DOMAIN_DIR:-$VAULT/Knowledge/领域}"
      GRADUATED_DIR="${WIKI_ENTRY_GRADUATED_DIR:-$VAULT/Knowledge/已入库}"
      INDEX_FILE="${WIKI_ENTRY_INDEX_FILE:-$VAULT/Knowledge/_INDEX.md}"
      STATE_DIR="${WIKI_ENTRY_STATE_DIR:-$VAULT/.openclaw/state}"
      shift 2 ;;
    --init)
      INIT_MODE=1
      shift ;;
    *)
      echo "未知参数: $1"
      echo "用法: wiki_entry_precheck.sh --vault <path> [--init]"
      exit 2 ;;
  esac
done

if [ -z "$VAULT" ]; then
  echo "❌ OPENCLAW_VAULT 未配置，且未传入 --vault。"
  echo "请显式指定评委/用户自己的 vault 根目录；运行门禁不会把当前目录当作隐式 vault。"
  exit 2
fi

if [ ! -d "$VAULT" ]; then
  echo "❌ Vault 根目录不存在: $VAULT"
  exit 2
fi

if [ "$INIT_MODE" -eq 1 ]; then
  mkdir -p "$TRANSIT_DIR" "$DOMAIN_DIR" "$GRADUATED_DIR" "$STATE_DIR" "$(dirname "$INDEX_FILE")"
  if [ ! -f "$INDEX_FILE" ]; then
    cat > "$INDEX_FILE" <<'EOF'
---
topics_count: 0
---
# Knowledge Index

## 主题目录

| Wiki | 路径 | 来源数 | 更新 | 状态 |
|---|---|---:|---|---|
EOF
    echo "🛠️ created index: $INDEX_FILE"
  fi
  echo "✅ wiki-entry 初始化完成"
  exit 0
fi

if [ ! -d "$STATE_DIR" ]; then
  echo "❌ 状态目录不存在: $STATE_DIR"
  echo "如需初始化通用目录，请先运行: wiki_entry_precheck.sh --vault <path> --init"
  exit 2
fi

SESSION_ID="$(date +%Y%m%d-%H%M%S)-$$"
SESSION_FILE="$STATE_DIR/wiki_entry_session.json"

MISSING=0

auto_dirs=(
  "$TRANSIT_DIR"
  "$DOMAIN_DIR"
  "$GRADUATED_DIR"
)

required_paths=(
  "$INDEX_FILE"
  "$SKILL_DIR/SKILL.md"
  "$SKILL_DIR/references/workflow.md"
)

echo "=== wiki_entry_precheck ==="
echo "Vault: $VAULT"
echo "Rule version: $RULE_VERSION"

echo ""
echo "[基础目录]"
for p in "${auto_dirs[@]}"; do
  if [ -d "$p" ]; then
    echo "✅ $p"
  else
    echo "❌ missing: $p"
    echo "   通用版支持任意配置路径，但运行门禁不会自动创建业务目录；请配置路径或先执行 --init。"
    MISSING=1
  fi
done

if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ missing index: $INDEX_FILE"
  echo "   如需创建空索引，请先执行 --init；正式运行必须使用已确认的 index。"
  MISSING=1
fi

echo ""
echo "[必备文件]"
for p in "${required_paths[@]}"; do
  if [ -e "$p" ]; then
    echo "✅ $p"
  else
    echo "❌ missing: $p"
    MISSING=1
  fi
done

grad_count=0
echo ""
echo "[graduating 文档扫描]"
for f in "$TRANSIT_DIR"/*.md; do
  [ -f "$f" ] || continue
  if grep -q '^status:[[:space:]]*graduating' "$f" 2>/dev/null; then
    echo "⚠️  $(basename "$f")"
    grad_count=$((grad_count + 1))
  fi
done
[ "$grad_count" -eq 0 ] && echo "✅ 无"

cat > "$SESSION_FILE" <<EOF
{
  "session_id": "$SESSION_ID",
  "started_at": "$(date '+%Y-%m-%d %H:%M:%S')",
  "vault": "$VAULT",
  "rule_version": "$RULE_VERSION"
}
EOF

echo ""
echo "Session file: $SESSION_FILE"

if [ "$MISSING" -ne 0 ]; then
  exit 1
fi

if [ "$grad_count" -gt 0 ]; then
  exit 2
fi

# 检查中转站是否有 waiting 文档
waiting_count=0
echo ""
echo "[waiting 文档扫描]"
for f in "$TRANSIT_DIR"/*.md; do
  [ -f "$f" ] || continue
  if grep -q '^status:[[:space:]]*waiting' "$f" 2>/dev/null; then
    echo "📋 $(basename "$f")"
    waiting_count=$((waiting_count + 1))
  fi
done

if [ "$waiting_count" -eq 0 ]; then
  echo "✅ 中转站无待入库文档，跳过入库。"
  exit 3
fi

echo "共 $waiting_count 篇待入库"
exit 0
