#!/usr/bin/env bash
# encrypt.sh – Encrypt MMAG memory files using AES-256-CBC (via openssl)
# Usage: bash encrypt.sh [--layer <layer>] [--file <path>] [--root <memory-root>]
#
# Key resolution order:
#   1. MMAG_KEY environment variable
#   2. ~/.openclaw/skills/mmag/.key file
#   3. Interactive passphrase prompt
#
# Encrypts all .md files in the target layer → .md.enc
# Original .md files are securely removed after encryption.

set -euo pipefail

ROOT="memory"
LAYER="long-term"
TARGET_FILE=""
KEY_FILE="${MMAG_KEY_FILE:-$HOME/.openclaw/skills/mmag/.key}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --layer)  LAYER="$2";       shift 2 ;;
    --file)   TARGET_FILE="$2"; shift 2 ;;
    --root)   ROOT="$2";        shift 2 ;;
    *) shift ;;
  esac
done

if ! command -v openssl >/dev/null 2>&1; then
  echo "❌ Missing required binary: openssl" >&2
  exit 1
fi

# ── Key resolution ─────────────────────────────────────────────────────────────
resolve_key() {
  if [ -n "${MMAG_KEY:-}" ]; then
    printf "%s" "$MMAG_KEY"
    return
  fi
  if [ -f "$KEY_FILE" ]; then
    tr -d '\r\n' < "$KEY_FILE"
    return
  fi
  # Interactive prompt (written to stderr so it doesn't pollute output)
  read -rsp "🔑 MMAG passphrase: " PASSPHRASE </dev/tty >&2
  echo "" >&2
  printf "%s" "$PASSPHRASE"
}

# ── Encrypt a single file ──────────────────────────────────────────────────────
encrypt_file() {
  local src="$1"
  local key="$2"
  local dst="${src%.md}.md.enc"

  # Use stdin for password to avoid exposure in process listings
  printf "%s" "$key" | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 \
    -pass stdin \
    -in  "$src" \
    -out "$dst" 2>/dev/null

  # Secure delete original
  if command -v shred &>/dev/null; then
    shred -u "$src"
  else
    rm -f "$src"
  fi

  echo "  🔒 Encrypted: $(basename "$src") → $(basename "$dst")"
}

# ── Main ───────────────────────────────────────────────────────────────────────
if [ -n "${MMAG_KEY:-}" ]; then
  echo "⚠️  MMAG_KEY environment mode is active; prefer MMAG_KEY_FILE to reduce exposure." >&2
fi

KEY=$(resolve_key)

if [ -n "$TARGET_FILE" ]; then
  if [ ! -f "$TARGET_FILE" ]; then
    echo "❌ File not found: $TARGET_FILE" >&2; exit 1
  fi
  encrypt_file "$TARGET_FILE" "$KEY"
else
  LAYER_DIR="$ROOT/$LAYER"
  if [ ! -d "$LAYER_DIR" ]; then
    echo "❌ Layer directory not found: $LAYER_DIR (run init.sh)" >&2; exit 1
  fi

  files=$(find "$LAYER_DIR" -name "*.md" ! -name "README.md" 2>/dev/null || true)
  if [ -z "$files" ]; then
    echo "  ℹ️  No .md files to encrypt in $LAYER_DIR"
    exit 0
  fi

  echo "🔒 Encrypting $LAYER layer..."
  while IFS= read -r f; do
    encrypt_file "$f" "$KEY"
  done <<< "$files"
fi

echo ""
echo "✅ Encryption complete."
echo "   Decrypt with: bash decrypt.sh --layer $LAYER"
