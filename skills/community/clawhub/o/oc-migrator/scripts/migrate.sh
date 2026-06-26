#!/bin/bash
# openclaw-migrator v1.0.0
# Full backup, restore, and migration for OpenClaw
set -uo pipefail

ACTION="${1:-help}"
shift 2>/dev/null || true

OC_HOME="$HOME/.openclaw"
OC_WORKSPACE="$OC_HOME/workspace"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
EXPORT_NAME="openclaw-export-${HOSTNAME}-${TIMESTAMP}"
ENCRYPT=true
DRY_RUN=false
ONLY=""

for arg in "$@"; do
  case "$arg" in
    --no-encrypt) ENCRYPT=false ;;
    --dry-run) DRY_RUN=true ;;
    --only=*) ONLY="${arg#--only=}" ;;
  esac
done

should_include() {
  [ -z "$ONLY" ] && return 0
  echo ",$ONLY," | grep -q ",$1," && return 0
  return 1
}

do_export() {
  TMPDIR=$(mktemp -d)
  EXPORT_DIR="$TMPDIR/$EXPORT_NAME"
  mkdir -p "$EXPORT_DIR"

  echo "📦 OpenClaw Migrator — Export"
  echo "   Host: $HOSTNAME | Date: $TIMESTAMP"
  echo ""

  # Config
  if should_include "config"; then
    echo "  → Global config"
    mkdir -p "$EXPORT_DIR/config"
    cp "$OC_HOME/openclaw.json" "$EXPORT_DIR/config/" 2>/dev/null && echo "    ✅ openclaw.json"
    if [ -d "$OC_HOME/agents" ]; then
      mkdir -p "$EXPORT_DIR/config/agents"
      # Only export agent configs, not session data
      for agent_dir in "$OC_HOME/agents"/*/; do
        [ -d "$agent_dir" ] || continue
        agent_name=$(basename "$agent_dir")
        if [ -d "$agent_dir/agent" ]; then
          mkdir -p "$EXPORT_DIR/config/agents/$agent_name/agent"
          cp "$agent_dir/agent/"*.json "$EXPORT_DIR/config/agents/$agent_name/agent/" 2>/dev/null
        fi
      done
      echo "    ✅ agents/ (configs only, sessions excluded)"
    fi
  fi

  # Workspace core files
  if should_include "workspace"; then
    echo "  → Workspace files"
    mkdir -p "$EXPORT_DIR/workspace"
    for f in MEMORY.md AGENTS.md SOUL.md TOOLS.md HEARTBEAT.md IDENTITY.md USER.md BOOTSTRAP.md; do
      [ -f "$OC_WORKSPACE/$f" ] && cp "$OC_WORKSPACE/$f" "$EXPORT_DIR/workspace/" && echo "    ✅ $f"
    done
  fi

  # Memory
  if should_include "memory"; then
    echo "  → Memory files"
    if [ -d "$OC_WORKSPACE/memory" ]; then
      mkdir -p "$EXPORT_DIR/workspace/memory"
      rsync -a --exclude='conversations/' --exclude='experiences/' "$OC_WORKSPACE/memory/" "$EXPORT_DIR/workspace/memory/" 2>/dev/null
      MEM_COUNT=$(find "$EXPORT_DIR/workspace/memory" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
      echo "    ✅ $MEM_COUNT memory files"
    fi
  fi

  # Knowledge
  if should_include "knowledge"; then
    if [ -d "$OC_WORKSPACE/knowledge" ]; then
      echo "  → Knowledge base"
      cp -R "$OC_WORKSPACE/knowledge" "$EXPORT_DIR/workspace/knowledge" 2>/dev/null
      echo "    ✅ knowledge/"
    fi
  fi

  # Learnings
  if should_include "learnings"; then
    if [ -d "$OC_WORKSPACE/.learnings" ]; then
      echo "  → Learnings"
      cp -R "$OC_WORKSPACE/.learnings" "$EXPORT_DIR/workspace/.learnings" 2>/dev/null
      echo "    ✅ .learnings/"
    fi
  fi

  # Scripts
  if should_include "scripts"; then
    if [ -d "$OC_WORKSPACE/scripts" ]; then
      echo "  → Scripts"
      mkdir -p "$EXPORT_DIR/workspace/scripts"
      rsync -a --exclude='node_modules/' "$OC_WORKSPACE/scripts/" "$EXPORT_DIR/workspace/scripts/" 2>/dev/null
      echo "    ✅ scripts/"
    fi
  fi

  # Skills
  if should_include "skills"; then
    if [ -d "$OC_WORKSPACE/skills" ]; then
      echo "  → Skills"
      mkdir -p "$EXPORT_DIR/workspace/skills"
      for skill_dir in "$OC_WORKSPACE/skills"/*/; do
        [ -d "$skill_dir" ] || continue
        skill_name=$(basename "$skill_dir")
        rsync -a --exclude='node_modules/' --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' "$skill_dir" "$EXPORT_DIR/workspace/skills/$skill_name/" 2>/dev/null
      done
      SKILL_COUNT=$(ls -d "$EXPORT_DIR/workspace/skills"/*/ 2>/dev/null | wc -l | tr -d ' ')
      echo "    ✅ $SKILL_COUNT skills"
    fi
  fi

  # Cron jobs
  if should_include "cron"; then
    echo "  → Cron jobs"
    openclaw cron list --json > "$EXPORT_DIR/cron-jobs.json" 2>/dev/null && echo "    ✅ cron-jobs.json"
  fi

  # Manifest
  echo "{\"version\":\"1.0.0\",\"host\":\"$HOSTNAME\",\"date\":\"$TIMESTAMP\",\"os\":\"$(uname -s)\"}" > "$EXPORT_DIR/manifest.json"

  if $DRY_RUN; then
    echo ""
    echo "🔍 Dry run — would export:"
    du -sh "$EXPORT_DIR" | awk '{print "   Total: " $1}'
    rm -rf "$TMPDIR"
    return
  fi

  # Pack
  OUTPUT_DIR="$HOME/backups/openclaw"
  mkdir -p "$OUTPUT_DIR"
  cd "$TMPDIR"

  if $ENCRYPT; then
    echo ""
    if [ -n "${MIGRATE_PASSWORD:-}" ]; then
      PASS="$MIGRATE_PASSWORD"
    else
      echo -n "  🔑 Enter encryption password: "
      read -s PASS
      echo ""
    fi
    tar -czf - "$EXPORT_NAME" | openssl enc -aes-256-cbc -salt -pbkdf2 -pass "pass:$PASS" -out "$OUTPUT_DIR/${EXPORT_NAME}.tar.gz.enc"
    OUTPUT_FILE="$OUTPUT_DIR/${EXPORT_NAME}.tar.gz.enc"
  else
    tar -czf "$OUTPUT_DIR/${EXPORT_NAME}.tar.gz" "$EXPORT_NAME"
    OUTPUT_FILE="$OUTPUT_DIR/${EXPORT_NAME}.tar.gz"
  fi

  SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
  rm -rf "$TMPDIR"

  echo ""
  echo "✅ Export complete: $OUTPUT_FILE ($SIZE)"
  echo "   Transfer this file to your new machine and run:"
  echo "   bash scripts/migrate.sh restore $(basename $OUTPUT_FILE)"
}

do_restore() {
  BACKUP_FILE="${1:-}"
  if [ -z "$BACKUP_FILE" ]; then
    echo "❌ Usage: migrate.sh restore <backup-file>"
    exit 1
  fi

  if [ ! -f "$BACKUP_FILE" ]; then
    # Try backups dir
    BACKUP_FILE="$HOME/backups/openclaw/$BACKUP_FILE"
    [ ! -f "$BACKUP_FILE" ] && echo "❌ File not found: $1" && exit 1
  fi

  echo "📥 OpenClaw Migrator — Restore"
  echo "   From: $(basename $BACKUP_FILE)"
  echo ""

  TMPDIR=$(mktemp -d)

  if echo "$BACKUP_FILE" | grep -q "\.enc$"; then
    if [ -n "${MIGRATE_PASSWORD:-}" ]; then
      PASS="$MIGRATE_PASSWORD"
    else
      echo -n "  🔑 Enter decryption password: "
      read -s PASS
      echo ""
    fi
    openssl enc -aes-256-cbc -d -salt -pbkdf2 -pass "pass:$PASS" -in "$BACKUP_FILE" | tar -xzf - -C "$TMPDIR"
  else
    tar -xzf "$BACKUP_FILE" -C "$TMPDIR"
  fi

  RESTORE_DIR=$(ls -d "$TMPDIR"/openclaw-export-* 2>/dev/null | head -1)
  if [ -z "$RESTORE_DIR" ]; then
    echo "❌ Invalid backup format"
    rm -rf "$TMPDIR"
    exit 1
  fi

  # Show manifest
  if [ -f "$RESTORE_DIR/manifest.json" ]; then
    echo "  📋 Backup from: $(cat "$RESTORE_DIR/manifest.json")"
  fi

  # Restore config
  if [ -d "$RESTORE_DIR/config" ]; then
    echo "  → Restoring config"
    cp "$RESTORE_DIR/config/openclaw.json" "$OC_HOME/openclaw.json" 2>/dev/null && echo "    ✅ openclaw.json"
    chmod 600 "$OC_HOME/openclaw.json"
    if [ -d "$RESTORE_DIR/config/agents" ]; then
      cp -R "$RESTORE_DIR/config/agents/"* "$OC_HOME/agents/" 2>/dev/null && echo "    ✅ agents/"
      find "$OC_HOME/agents" -name "*.json" -exec chmod 600 {} \;
    fi
  fi

  # Restore workspace
  if [ -d "$RESTORE_DIR/workspace" ]; then
    echo "  → Restoring workspace"
    for f in "$RESTORE_DIR/workspace"/*.md; do
      [ -f "$f" ] && cp "$f" "$OC_WORKSPACE/" && echo "    ✅ $(basename $f)"
    done
    for dir in memory knowledge .learnings scripts skills; do
      if [ -d "$RESTORE_DIR/workspace/$dir" ]; then
        mkdir -p "$OC_WORKSPACE/$dir"
        cp -R "$RESTORE_DIR/workspace/$dir/"* "$OC_WORKSPACE/$dir/" 2>/dev/null && echo "    ✅ $dir/"
      fi
    done
  fi

  rm -rf "$TMPDIR"

  echo ""
  echo "✅ Restore complete! Run: openclaw gateway restart"
}

case "$ACTION" in
  export) do_export ;;
  restore) do_restore "$@" ;;
  *)
    echo "OpenClaw Migrator v1.0.0"
    echo "Usage:"
    echo "  migrate.sh export [--no-encrypt] [--dry-run] [--only=config,memory,skills]"
    echo "  migrate.sh restore <backup-file>"
    ;;
esac
