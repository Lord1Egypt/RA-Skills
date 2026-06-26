#!/bin/bash
# Uninstall @Mention Skill - restore original files from backup
set -e

DIST="/usr/lib/node_modules/openclaw/dist"

echo "Restoring backups..."

for pattern in deliver-reply login; do
  FILE=$(ls "$DIST"/${pattern}-*.js 2>/dev/null | grep -v '.bak.' | head -1)
  BACKUP=$(ls -t "$DIST"/${pattern}-*.js.bak.mention.* 2>/dev/null | head -1)
  if [ -n "$BACKUP" ] && [ -n "$FILE" ]; then
    cp "$BACKUP" "$FILE"
    echo "✓ Restored $(basename $FILE) from $(basename $BACKUP)"
  else
    echo "⚠ No backup found for $pattern"
  fi
done

echo ""
echo "Restarting OpenClaw..."
systemctl restart openclaw 2>/dev/null && echo "✓ Restarted" || echo "⚠ Restart manually"
echo ""
echo "@Mention skill removed. LID_CACHE.json and mention-guide.md were NOT deleted."
