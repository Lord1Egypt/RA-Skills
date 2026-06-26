#!/usr/bin/env bash
set -euo pipefail

# Publish the Hookaido skill to ClawHub.
#
# Prerequisites:
#   npx clawhub@latest login   (one-time, opens browser for GitHub OAuth)
#   npx clawhub@latest whoami  (verify auth)
#
# The --slug flag is required because the repository folder name
# (claw-skill-hookaido) differs from the skill slug on ClawHub (hookaido).
# The --name flag sets the display name shown in the ClawHub UI.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Extract version from SKILL.md frontmatter
VERSION="$(sed -n 's/^version: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "$SKILL_DIR/SKILL.md")"

if [[ -z "$VERSION" ]]; then
  echo "Error: could not extract version from SKILL.md" >&2
  exit 1
fi

echo "Publishing hookaido@${VERSION} from ${SKILL_DIR}"

npx clawhub@latest publish "$SKILL_DIR" \
  --slug hookaido \
  --name "Hookaido Webhook Integration" \
  --version "$VERSION" \
  "$@"
