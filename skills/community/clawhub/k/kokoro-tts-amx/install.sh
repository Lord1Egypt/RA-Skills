#!/usr/bin/env bash
# Install kokoro-tts-amx skill.
# Two ways to invoke:
#   1) Inside a clone:    bash install.sh
#   2) Remote one-liner:  curl -fsSL <raw-url>/install.sh | REPO_URL=https://github.com/Wray151/xeontts bash
# Override skill location:
#   TARGET=openclaw  -> ~/.openclaw/workspace/skills/   (default)
#   TARGET=claude    -> ~/.claude/skills/
set -euo pipefail

TARGET="${TARGET:-openclaw}"
case "$TARGET" in
  openclaw) DEST="$HOME/.openclaw/workspace/skills/kokoro-tts-amx" ;;
  claude)   DEST="$HOME/.claude/skills/kokoro-tts-amx" ;;
  *) echo "TARGET must be 'openclaw' or 'claude'"; exit 1 ;;
esac

# Locate the repo: if this script ran from a clone, use that; otherwise clone.
if [ -f "${BASH_SOURCE[0]:-}" ] && [ -f "$(dirname "${BASH_SOURCE[0]}")/tts.py" ]; then
  REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  : "${REPO_URL:?set REPO_URL=https://github.com/Wray151/xeontts when piping}"
  REPO_DIR="$HOME/.local/share/kokoro-tts-amx"
  [ -d "$REPO_DIR/.git" ] || git clone --depth 1 "$REPO_URL" "$REPO_DIR"
fi
echo "repo at: $REPO_DIR"

# 1. system dep
if command -v apt-get >/dev/null; then
  sudo apt-get install -y espeak-ng
elif command -v brew >/dev/null; then
  brew install espeak-ng
fi

# 2. venv + pip
python3 -m venv "$REPO_DIR/.venv"
# shellcheck disable=SC1091
source "$REPO_DIR/.venv/bin/activate"
pip install -r "$REPO_DIR/requirements.txt"
python -c "from kokoro import KPipeline; KPipeline(lang_code='z', repo_id='hexgrad/Kokoro-82M')"

# 3. register as skill (symlink)
mkdir -p "$(dirname "$DEST")"
[ -e "$DEST" ] && rm -rf "$DEST"
ln -s "$REPO_DIR" "$DEST"
echo "✓ skill installed at $DEST -> $REPO_DIR"
echo "  在 agent 里 /reset 或开新会话即可使用。"
