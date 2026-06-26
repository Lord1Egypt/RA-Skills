#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scaffold.sh <source-project-dir> <skill-name>

Generate a standard skill directory from an existing project:
  - Creates skill-name/ with standard structure
  - Copies core files (excludes .git, node_modules, .env, logs/, etc.)
  - Generates SKILL.md skeleton from source README
  - Generates references/checklist.md

Output: path to generated skill directory.
EOF
  exit 1
}

[[ $# -lt 2 ]] && usage
SRC_DIR="$1"
SKILL_NAME="$2"
[[ ! -d "$SRC_DIR" ]] && echo "ERROR: '$SRC_DIR' is not a directory" && exit 1

DEST_DIR="./${SKILL_NAME}"
if [[ -d "$DEST_DIR" ]]; then
  echo "ERROR: '$DEST_DIR' already exists" && exit 1
fi

echo "Scaffolding skill '$SKILL_NAME' from $SRC_DIR ..."

mkdir -p "$DEST_DIR"/{scripts,references}

# Copy core files, excluding noise
rsync -a --exclude='.git' --exclude='node_modules' \
  --exclude='.env' --exclude='.env.*' \
  --exclude='logs/' --exclude='*.log' \
  --exclude='__pycache__' --exclude='.venv' \
  --exclude='.DS_Store' --exclude='Thumbs.db' \
  --exclude='dist/' --exclude='build/' \
  --exclude='.towow/' --exclude='.wow-harness/' \
  "$SRC_DIR/" "$DEST_DIR/"

# Extract description from README if available
DESC=""
for readme in "$SRC_DIR/README.md" "$SRC_DIR/readme.md" "$SRC_DIR/README"; do
  if [[ -f "$readme" ]]; then
    DESC=$(awk 'NR>1 && /^[^#]/ && NF>0 {print; exit}' "$readme")
    break
  fi
done
[[ -z "$DESC" ]] && DESC="TODO: Write a clear description with trigger keywords (e.g. verbs/nouns that match user intent) for when this skill should be activated"

# Generate SKILL.md if not already copied from source
if [[ ! -f "$DEST_DIR/SKILL.md" ]]; then
  cat > "$DEST_DIR/SKILL.md" <<SKILLEOF
---
name: ${SKILL_NAME}
description: ${DESC}
---

# ${SKILL_NAME}

${DESC}

## Usage

TODO: document usage steps.
SKILLEOF
  echo "  Created SKILL.md"
fi

# Generate checklist
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKLIST_SRC="$SCRIPT_DIR/../references/checklist.md"
if [[ -f "$CHECKLIST_SRC" ]]; then
  mkdir -p "$DEST_DIR/references"
  cp "$CHECKLIST_SRC" "$DEST_DIR/references/checklist.md"
  echo "  Copied references/checklist.md"
fi

# Remove .git if rsync somehow included it
rm -rf "$DEST_DIR/.git"

echo ""
echo "Done. Skill scaffolded at: $DEST_DIR"
echo "Next: run scan.sh and validate.sh before publishing."
