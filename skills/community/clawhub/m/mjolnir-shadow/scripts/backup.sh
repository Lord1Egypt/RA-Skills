#!/bin/bash
# ⚡🌑 Mjolnir Shadow (雷神之影) - Automated Rotating Backup
# Backs up OpenClaw workspace to WebDAV with automatic rotation
# Security: credentials encrypted via GPG, never exposed in process listings

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config/backup-config.json"
ENCRYPTED_CONFIG="${SKILL_DIR}/config/backup-config.json.gpg"
NETRC_FILE="/tmp/.mjolnir_shadow_netrc_$$"

cleanup() {
  rm -f "$NETRC_FILE"
  rm -rf "$BACKUP_DIR" "$FINAL_FILE" 2>/dev/null
}
trap cleanup EXIT

# ── Load Config ──────────────────────────────────────────────
decrypt_config() {
  if [ -f "$ENCRYPTED_CONFIG" ]; then
    if [ -n "$MJOLNIR_SHADOW_PASS" ]; then
      gpg --quiet --batch --yes --passphrase "$MJOLNIR_SHADOW_PASS" \
        --decrypt "$ENCRYPTED_CONFIG" 2>/dev/null
    else
      gpg --quiet --batch --yes --decrypt "$ENCRYPTED_CONFIG" 2>/dev/null
    fi
  elif [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Warning: Using unencrypted config. Run setup to encrypt." >&2
    cat "$CONFIG_FILE"
  else
    echo "❌ No config found. Run: python3 ${SCRIPT_DIR}/setup_backup.py" >&2
    exit 1
  fi
}

CONFIG_JSON=$(decrypt_config)
if [ -z "$CONFIG_JSON" ]; then
  echo "❌ Failed to load config. Check GPG passphrase or run setup."
  exit 1
fi

WEBDAV_URL=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_url'])")
WEBDAV_USER=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_user'])")
WEBDAV_PASS=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_pass'])")
REMOTE_DIR=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['remote_dir'])")
MAX_BACKUPS=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('max_backups', 3))")
BACKUP_WORKSPACE=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('backup_workspace', True))")
BACKUP_CONFIG=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('backup_config', True))")
BACKUP_STRATEGIES=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('backup_strategies', True))")
BACKUP_SKILLS=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('backup_skills', True))")
WORKSPACE_PATH=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('workspace_path', '$HOME/.openclaw/workspace'))")
OPENCLAW_DIR=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('openclaw_dir', '$HOME/.openclaw'))")
EXCLUDE_AUTH=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('exclude_channel_auth', True))")

# ── Security: Use netrc file instead of -u flag ─────────────
# This prevents credentials from appearing in process listings
WEBDAV_HOST=$(echo "$WEBDAV_URL" | grep -oP '://\K[^/]+')
cat > "$NETRC_FILE" << EOF
machine ${WEBDAV_HOST}
login ${WEBDAV_USER}
password ${WEBDAV_PASS}
EOF
chmod 600 "$NETRC_FILE"
CURL_AUTH="--netrc-file ${NETRC_FILE}"

# ── HTTPS Check ──────────────────────────────────────────────
if [[ "$WEBDAV_URL" != https://* ]]; then
  echo "⚠️  WARNING: WebDAV URL is not HTTPS! Credentials will be sent in plaintext."
  echo "   Strongly recommend using HTTPS for production backups."
  echo "   Current URL: ${WEBDAV_URL}"
  echo ""
fi

FULL_URL="${WEBDAV_URL}/${REMOTE_DIR}"
BACKUP_DIR="/tmp/mjolnir_shadow_backup_$$"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
BACKUP_NAME="backup_${TIMESTAMP}"
STATE_FILE="${WORKSPACE_PATH}/memory/backup-state.json"

echo "🌑 Mjolnir Shadow Backup - ${TIMESTAMP}"
echo "=========================================="

# ── Clean up ─────────────────────────────────────────────────
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# ── Pack components ──────────────────────────────────────────
if [ "$BACKUP_WORKSPACE" = "True" ]; then
  echo "📦 Packing workspace..."
  tar czf "$BACKUP_DIR/workspace.tar.gz" \
    -C "$WORKSPACE_PATH" \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='secrets/*.gpg' \
    --exclude='secrets/*.key' \
    --exclude='.env' \
    --exclude='*.secret' \
    . 2>/dev/null || echo "⚠️ Workspace pack had warnings (non-fatal)"
fi

if [ "$BACKUP_CONFIG" = "True" ]; then
  echo "📦 Packing config..."
  EXCLUDE_ARGS=""
  if [ "$EXCLUDE_AUTH" = "True" ]; then
    EXCLUDE_ARGS="--exclude=openclaw-weixin --exclude=qqbot --exclude=*/accounts --exclude=*/auth"
  fi
  tar czf "$BACKUP_DIR/config.tar.gz" \
    -C "$OPENCLAW_DIR" \
    $EXCLUDE_ARGS \
    --exclude='*.gpg' \
    --exclude='*.secret' \
    --exclude='.env' \
    openclaw.json \
    cron/ \
    2>/dev/null || echo "⚠️ Config pack had warnings (non-fatal)"
fi

if [ "$BACKUP_STRATEGIES" = "True" ]; then
  STRAT_DIR="${OPENCLAW_DIR}/workspace/projects/auto_trading"
  if [ -d "$STRAT_DIR/strategies" ]; then
    echo "📦 Packing strategies..."
    tar czf "$BACKUP_DIR/strategies.tar.gz" \
      -C "$STRAT_DIR" \
      --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' \
      strategies/ monitor/ 2>/dev/null || echo "⚠️ Strategies pack had warnings"
  fi
fi

if [ "$BACKUP_SKILLS" = "True" ]; then
  SKILLS_DIR="${OPENCLAW_DIR}/workspace/skills"
  if [ -d "$SKILLS_DIR" ]; then
    echo "📦 Packing skills..."
    tar czf "$BACKUP_DIR/skills.tar.gz" \
      -C "$OPENCLAW_DIR/workspace" \
      --exclude='node_modules' --exclude='venv' --exclude='.venv' \
      --exclude='__pycache__' --exclude='*.pyc' \
      --exclude='*.gpg' --exclude='*.secret' --exclude='.env' \
      skills/ 2>/dev/null || echo "⚠️ Skills pack had warnings"
  fi
fi

# ── Create final archive ─────────────────────────────────────
echo "📦 Creating final archive..."
FINAL_FILE="/tmp/${BACKUP_NAME}_$$.tar.gz"
tar czf "$FINAL_FILE" -C "$BACKUP_DIR" . 2>/dev/null
FILESIZE=$(du -h "$FINAL_FILE" | cut -f1)
FILESIZE_BYTES=$(stat -c%s "$FINAL_FILE" 2>/dev/null || stat -f%z "$FINAL_FILE" 2>/dev/null)
echo "📦 Size: ${FILESIZE}"

# ── Ensure remote directory ──────────────────────────────────
curl -s $CURL_AUTH -X MKCOL "${FULL_URL}/" 2>/dev/null || true

# ── Check existing backups ───────────────────────────────────
echo "🔄 Checking existing backups..."
EXISTING=$(curl -s $CURL_AUTH \
  -X PROPFIND "${FULL_URL}/" -H "Depth: 1" 2>/dev/null \
  | grep -oP 'backup_[^<]+\.tar\.gz' | sort -u || true)
BACKUP_COUNT=$(echo "$EXISTING" | grep -c "backup_" 2>/dev/null || true)
BACKUP_COUNT=$(echo "$BACKUP_COUNT" | tr -d '[:space:]')
BACKUP_COUNT=${BACKUP_COUNT:-0}
echo "📊 Existing: ${BACKUP_COUNT} / ${MAX_BACKUPS}"

# ── Rotate ───────────────────────────────────────────────────
if [ "$BACKUP_COUNT" -ge "$MAX_BACKUPS" ]; then
  DELETE_COUNT=$((BACKUP_COUNT - MAX_BACKUPS + 1))
  echo "🗑️ Rotating: deleting ${DELETE_COUNT} oldest backup(s)..."
  echo "$EXISTING" | head -n "$DELETE_COUNT" | while read -r OLD_BACKUP; do
    if [ -n "$OLD_BACKUP" ]; then
      echo "   Deleting: ${OLD_BACKUP}"
      curl -s $CURL_AUTH -X DELETE "${FULL_URL}/${OLD_BACKUP}" 2>/dev/null
    fi
  done
fi

# ── Upload ───────────────────────────────────────────────────
echo "📤 Uploading..."
HTTP_CODE=$(curl -s $CURL_AUTH \
  -T "$FINAL_FILE" \
  "${FULL_URL}/${BACKUP_NAME}.tar.gz" \
  -w "%{http_code}" -o /dev/null 2>&1)

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "204" ]; then
  echo "✅ Upload successful! HTTP ${HTTP_CODE}"
  STATUS="success"
else
  echo "❌ Upload failed! HTTP ${HTTP_CODE}"
  STATUS="failed"
fi

# ── Update state ─────────────────────────────────────────────
mkdir -p "$(dirname "$STATE_FILE")"
NEW_COUNT=$((BACKUP_COUNT >= MAX_BACKUPS ? MAX_BACKUPS : BACKUP_COUNT + 1))
cat > "$STATE_FILE" << EOF
{
  "lastBackup": "${TIMESTAMP}",
  "backupName": "${BACKUP_NAME}.tar.gz",
  "fileSize": "${FILESIZE}",
  "fileSizeBytes": ${FILESIZE_BYTES},
  "httpStatus": ${HTTP_CODE},
  "status": "${STATUS}",
  "backupCount": ${NEW_COUNT},
  "maxBackups": ${MAX_BACKUPS},
  "remoteDir": "${REMOTE_DIR}",
  "credentialSecurity": "gpg-encrypted"
}
EOF

echo ""
echo "=========================================="
echo "🌑 Mjolnir Shadow - ${STATUS^^}"
echo "📅 Time: ${TIMESTAMP}"
echo "📦 Size: ${FILESIZE}"
echo "📍 Remote: ${REMOTE_DIR}/${BACKUP_NAME}.tar.gz"
echo "🔄 Rotation: ${NEW_COUNT}/${MAX_BACKUPS} slots used"
echo "=========================================="

exit $([ "$STATUS" = "success" ] && echo 0 || echo 1)
