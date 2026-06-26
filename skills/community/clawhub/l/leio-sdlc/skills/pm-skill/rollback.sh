#!/bin/bash
set -e
SLUG="pm-skill"
HOME_DIR="${HOME_MOCK:-$HOME}"
RELEASES_DIR="$HOME_DIR/.openclaw/.releases/$SLUG"
PROD_DIR="$HOME_DIR/.openclaw/skills/$SLUG"

NO_RESTART=false
for arg in "$@"; do
    case $arg in
        --no-restart)
        NO_RESTART=true
        shift
        ;;
    esac
done

LATEST_BACKUP=$(ls -t "$RELEASES_DIR"/backup_*.tar.gz 2>/dev/null | head -n 1)
if [ -z "$LATEST_BACKUP" ]; then
    echo "No backup found for $SLUG."
    exit 1
fi

echo "Rolling back $SLUG from $LATEST_BACKUP..."
rm -rf "$PROD_DIR"
tar -xzf "$LATEST_BACKUP" -C "$HOME_DIR/.openclaw/skills/"

if [ -z "$HOME_MOCK" ] && [ "$NO_RESTART" != "true" ]; then
    openclaw gateway restart || true
fi
echo "✅ Rollback complete for $SLUG."
