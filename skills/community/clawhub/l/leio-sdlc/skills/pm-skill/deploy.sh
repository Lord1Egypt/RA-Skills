#!/bin/bash
set -e
SLUG="pm-skill"
HOME_DIR="${HOME_MOCK:-$HOME}"
OPENCLAW_DIR="$HOME_DIR/.openclaw"
SKILLS_DIR="$OPENCLAW_DIR/skills"
RELEASES_DIR="$OPENCLAW_DIR/.releases/$SLUG"
PROD_DIR="$SKILLS_DIR/$SLUG"

NO_RESTART=false
for arg in "$@"; do
    case $arg in
        --no-restart)
        NO_RESTART=true
        shift
        ;;
    esac
done

echo "Deploying $SLUG..."
mkdir -p "$SKILLS_DIR"
mkdir -p "$RELEASES_DIR"
RELEASE_ID=$(date +"%Y%m%d_%H%M%S")

if [ -e "$PROD_DIR" ]; then
    if [ -L "$PROD_DIR" ]; then
        rm -f "$PROD_DIR"
    else
        tar -czf "$RELEASES_DIR/backup_${RELEASE_ID}.tar.gz" -C "$SKILLS_DIR" "$SLUG"
    fi
fi

TMP_DIR="$SKILLS_DIR/.tmp_$SLUG"
OLD_DIR="$SKILLS_DIR/.old_$SLUG"
rm -rf "$TMP_DIR" "$OLD_DIR"
mkdir -p "$TMP_DIR"

# Stage the skill directory
rsync -a --exclude=.git --exclude=__pycache__ skills/$SLUG/ "$TMP_DIR/"

# Package dependencies from monorepo root
mkdir -p "$TMP_DIR/scripts"
cp scripts/agent_driver.py "$TMP_DIR/scripts/"

if [ -e "$PROD_DIR" ]; then
    mv "$PROD_DIR" "$OLD_DIR"
fi
mv -T "$TMP_DIR" "$PROD_DIR"
rm -rf "$OLD_DIR"

ls -dt "$RELEASES_DIR"/backup_*.tar.gz 2>/dev/null | tail -n +4 | xargs -r rm -f

echo "✅ $SLUG deployed."
if [ -z "$HOME_MOCK" ] && [ "$NO_RESTART" != "true" ]; then
    openclaw gateway restart || true
fi
