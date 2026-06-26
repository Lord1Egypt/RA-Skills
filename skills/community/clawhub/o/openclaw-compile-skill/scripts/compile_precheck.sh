#!/bin/bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
INBOX_DIR="${COMPILE_INBOX_DIR:-}"
TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
STATE_DIR="${COMPILE_STATE_DIR:-$VAULT/.openclaw/state}"
RULE_VERSION="compile-v2.4"
SESSION_FILE="$STATE_DIR/compile_session.json"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --vault)
      VAULT="$2"
      INBOX_DIR="${COMPILE_INBOX_DIR:-}"
      TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
      RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      STATE_DIR="${COMPILE_STATE_DIR:-$VAULT/.openclaw/state}"
      SESSION_FILE="$STATE_DIR/compile_session.json"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      echo "用法: compile_precheck.sh [--vault <path>]"
      exit 2 ;;
  esac
done

if [ -z "$INBOX_DIR" ]; then
  echo "❌ COMPILE_INBOX_DIR 未配置；拒绝回退到通用 Inbox。"
  echo "请在 OpenClaw config 的 skills.entries.compile.env 中注入真实收件箱路径。"
  exit 2
fi

if [ ! -d "$INBOX_DIR" ]; then
  echo "❌ 收件箱不存在: $INBOX_DIR"
  echo "不会自动创建收件箱，避免把通用版默认目录误写进生产 Vault。"
  exit 2
fi

mkdir -p "$STATE_DIR"
SESSION_ID="$(date +%Y%m%d-%H%M%S)-$$"

auto_dirs=(
  "$TRANSIT_DIR"
  "$RAW_DIR"
)

required_paths=(
  "$SKILL_DIR/SKILL.md"
  "$SKILL_DIR/references/compile-template.md"
  "$SCRIPT_DIR/compile_check.sh"
)

missing=0

echo "=== compile_precheck ==="
echo "Vault: $VAULT"
echo "Rule version: $RULE_VERSION"

echo ""
echo "[基础目录]"
echo "✅ $INBOX_DIR"
for path in "${auto_dirs[@]}"; do
  if [ -d "$path" ]; then
    echo "✅ $path"
  else
    mkdir -p "$path"
    echo "🛠️ created: $path"
  fi
done

echo ""
echo "[必备文件]"
for path in "${required_paths[@]}"; do
  if [ -e "$path" ]; then
    echo "✅ $path"
  else
    echo "❌ missing: $path"
    missing=1
  fi
done

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

if [ "$missing" -ne 0 ]; then
  exit 1
fi

echo ""
echo "[待编译文件扫描]"
is_processed() {
  file="$1"
  frontmatter_status="$(
    awk '
      NR == 1 && $0 == "---" { in_fm = 1; next }
      in_fm && $0 == "---" { exit }
      in_fm && $0 ~ /^status:[[:space:]]*/ {
        sub(/^status:[[:space:]]*/, "")
        gsub(/^["'\''"]|["'\''"]$/, "")
        print
        exit
      }
    ' "$file"
  )"
  [ "$frontmatter_status" = "processed" ]
}

count=0
for file in "$INBOX_DIR"/*.md; do
  [ -f "$file" ] || continue
  if is_processed "$file"; then
    continue
  fi
  echo "📋 $(basename "$file")"
  count=$((count + 1))
done

if [ "$count" -eq 0 ]; then
  echo "✅ 收件箱没有待编译文件。"
  exit 0
fi

echo "共 $count 篇待编译"
exit 0
