#!/usr/bin/env bash
# ============================================================
# memory-sync.sh — 跨渠道记忆同步脚本（安全版）
# ============================================================
# 用法：bash scripts/memory-sync.sh <源文件>
#
# 功能：将任意文件内容同步到 memory/channels/<channel>/ 目录，
#       并自动触发 memory-backup.sh 备份。
#
# 安全限制：
#   - 拒绝绝对路径（防止读 /etc、/root 等系统文件）
#   - 拒绝包含 .. 的路径（防止目录遍历）
#   - 备份前扫描敏感内容模式，发现则中断
# ============================================================

set -euo pipefail

WORKDIR="${WORKDIR:-/root/.openclaw/workspace}"
cd "$WORKDIR"

INPUT_FILE="${1:-}"

# ---- 安全校验：路径验证 ----
if [ -z "$INPUT_FILE" ] || [ ! -f "$INPUT_FILE" ]; then
  echo "用法：bash scripts/memory-sync.sh <源文件>"
  echo "示例：bash scripts/memory-sync.sh /tmp/my-notes.md"
  exit 1
fi

# 拒绝绝对路径（防止读取 /etc、/root 等系统文件）
if [[ "$INPUT_FILE" == /* ]]; then
  echo "[memory-sync] 拒绝：不允许绝对路径，只接受相对文件名"
  echo "[memory-sync] 提示：把文件放到当前目录，用相对路径引用"
  exit 1
fi

# 拒绝目录遍历（防止 ../etc/passwd 这类路径）
if [[ "$INPUT_FILE" == *..* ]]; then
  echo "[memory-sync] 拒绝：路径不能包含 .. （目录遍历）"
  exit 1
fi

# ---- 安全校验：内容审查（敏感模式检测）----
SENSITIVE_PATTERNS=(
  "PRIVATE KEY"
  "-----BEGIN PRIVATE KEY-----"
  "-----BEGIN RSA PRIVATE KEY-----"
  "-----BEGIN OPENSSH PRIVATE KEY-----"
  "aws_access_key_id"
  "aws_secret_access_key"
  "password\s*=\s*['\"][^'\"]{8,}"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
  if grep -iE "$pattern" "$INPUT_FILE" &>/dev/null; then
    echo "[memory-sync] 拒绝：文件包含敏感内容模式（${pattern}）"
    echo "[memory-sync] 请检查文件内容，移除敏感信息后重试"
    exit 1
  fi
done

# ---- 内容同步 ----
STAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
BASENAME="$(basename "$INPUT_FILE")"
TARGET="memory/channels/custom/${BASENAME%.md}.sync.md"

mkdir -p "$(dirname "$TARGET")"

{
  echo "# 自动同步记忆"
  echo
  echo "- 来源文件：${INPUT_FILE}"
  echo "- 同步时间：${STAMP}"
  echo
  echo "## 原始内容"
  echo
  cat "$INPUT_FILE"
} > "$TARGET"

echo "[memory-sync] 已同步至：${TARGET}"

# 自动触发备份
bash scripts/memory-backup.sh
