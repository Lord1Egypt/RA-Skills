#!/bin/bash
# Bootstrap a new wiki — creates structure, installs MkDocs, inits git, sets up static server.
# Usage: bash scripts/bootstrap.sh [--remote <git-remote-url>] [--serve-port 8300]

set -euo pipefail

WIKI_DIR="${HOME}/wiki"
SERVE_PORT="${2:-8300}"
REMOTE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --remote) REMOTE="$2"; shift 2 ;;
    --serve-port) SERVE_PORT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "📚 Bootstrapping wiki at ${WIKI_DIR}..."

# Create directory structure
mkdir -p "${WIKI_DIR}/docs/raw/processed"
mkdir -p "${WIKI_DIR}/docs/topics"

# Master index
if [[ ! -f "${WIKI_DIR}/docs/index.md" ]]; then
  cat > "${WIKI_DIR}/docs/index.md" << 'EOF'
# Personal Wiki

Knowledge base maintained by your AI assistant.

## Topics

*No topics yet. Start a conversation and say "wiki this" to begin building your knowledge base.*

## How This Works

- **Your assistant maintains everything** — articles are written and updated from conversations
- **`raw/`** — drop links, PDFs, or articles here and ask to compile them
- **Ask** — "what does my wiki say about X?" works anytime
EOF
fi

# MkDocs config
if [[ ! -f "${WIKI_DIR}/mkdocs.yml" ]]; then
  cat > "${WIKI_DIR}/mkdocs.yml" << EOF
site_name: Personal Wiki
site_description: LLM-maintained personal knowledge base
dev_addr: 127.0.0.1:${SERVE_PORT}
theme:
  name: material
  palette:
    scheme: slate
    primary: black
  features:
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight
    - content.code.copy

plugins:
  - search

nav:
  - Home: index.md

markdown_extensions:
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
EOF
fi

# Gitignore
if [[ ! -f "${WIKI_DIR}/.gitignore" ]]; then
  echo "site/" > "${WIKI_DIR}/.gitignore"
fi

# Install MkDocs if not present
if ! command -v mkdocs &>/dev/null; then
  echo "Installing MkDocs..."
  if command -v pipx &>/dev/null; then
    pipx install mkdocs
    pipx inject mkdocs mkdocs-material
  elif command -v pip3 &>/dev/null; then
    pip3 install --user mkdocs mkdocs-material 2>/dev/null || \
    pip3 install --break-system-packages mkdocs mkdocs-material
  else
    echo "❌ No pip3 or pipx found. Install MkDocs manually."
    exit 1
  fi
fi

# Init git
if [[ ! -d "${WIKI_DIR}/.git" ]]; then
  cd "${WIKI_DIR}"
  git init
  git branch -m main
  git add -A
  git commit -m "Initial wiki bootstrap"
  if [[ -n "${REMOTE}" ]]; then
    git remote add origin "${REMOTE}"
    git push -u origin main
  fi
fi

# Build static site
cd "${WIKI_DIR}"
mkdocs build 2>/dev/null || true

# Create LaunchAgent (macOS) or systemd service (Linux) for static serving
if [[ "$(uname)" == "Darwin" ]]; then
  PLIST="${HOME}/Library/LaunchAgents/dev.wiki.server.plist"
  if [[ ! -f "${PLIST}" ]]; then
    PYTHON_PATH=$(which python3)
    cat > "${PLIST}" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>dev.wiki.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>-m</string>
        <string>http.server</string>
        <string>${SERVE_PORT}</string>
        <string>--bind</string>
        <string>127.0.0.1</string>
        <string>--directory</string>
        <string>${WIKI_DIR}/site</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/wiki-server.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/wiki-server.log</string>
</dict>
</plist>
EOF
    launchctl load "${PLIST}"
    echo "✅ Static server running on port ${SERVE_PORT}"
  fi
elif command -v systemctl &>/dev/null; then
  SERVICE="${HOME}/.config/systemd/user/wiki-server.service"
  if [[ ! -f "${SERVICE}" ]]; then
    mkdir -p "$(dirname "${SERVICE}")"
    cat > "${SERVICE}" << EOF
[Unit]
Description=Wiki Static Server
After=network.target

[Service]
ExecStart=$(which python3) -m http.server ${SERVE_PORT} --bind 127.0.0.1 --directory ${WIKI_DIR}/site
Restart=always

[Install]
WantedBy=default.target
EOF
    systemctl --user daemon-reload
    systemctl --user enable --now wiki-server
    echo "✅ Static server running on port ${SERVE_PORT}"
  fi
fi

echo "📚 Wiki bootstrapped at ${WIKI_DIR}"
echo "   Browse: http://127.0.0.1:${SERVE_PORT}/"
echo "   Expose via Tailscale: tailscale serve --bg --set-path /wiki http://127.0.0.1:${SERVE_PORT}"
