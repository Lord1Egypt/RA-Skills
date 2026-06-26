#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/nasplycc/clawra-selfie.git"
TARGET_DIR="${1:-$HOME/.openclaw/skills/clawra-selfie}"
PARENT_DIR="$(dirname "$TARGET_DIR")"

printf '\n==> Installing clawra-selfie\n'
printf 'Repo: %s\n' "$REPO_URL"
printf 'Target: %s\n\n' "$TARGET_DIR"

mkdir -p "$PARENT_DIR"

if [ -d "$TARGET_DIR/.git" ]; then
  printf '==> Existing install found, pulling latest changes...\n'
  git -C "$TARGET_DIR" pull --ff-only
else
  if [ -e "$TARGET_DIR" ]; then
    echo "Target exists but is not a git repository: $TARGET_DIR" >&2
    echo "Please move/remove it, or pass a different target path." >&2
    exit 1
  fi
  printf '==> Cloning repository...\n'
  git clone "$REPO_URL" "$TARGET_DIR"
fi

cat <<EOF

✅ clawra-selfie is ready.

Next steps:
1. Ensure dependencies exist: bash, curl, jq, git
2. Set your Hugging Face token, for example:

   export HF_TOKEN=your_huggingface_token

3. Put your face reference image into your agent workspace, e.g.:

   references/raya-official-face-current.jpg

4. If needed, adapt SOUL.md / role settings for your own character.

Installed at:
  $TARGET_DIR
EOF
