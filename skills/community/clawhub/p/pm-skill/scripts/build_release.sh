#!/bin/bash
set -eo pipefail

DIST_DIR="dist"

echo "Building release to $DIST_DIR..."

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

if [ ! -f .release_ignore ]; then
  echo "Warning: .release_ignore not found in $(pwd). Creating default."
  cat <<EOF > .release_ignore
.git/
.sdlc/
docs/
tests/
*.log
*.diff
.review_count
memory/
EOF
fi

rsync -av --exclude-from='.release_ignore' --exclude="$DIST_DIR/" ./ "$DIST_DIR/"

echo "Build complete."
