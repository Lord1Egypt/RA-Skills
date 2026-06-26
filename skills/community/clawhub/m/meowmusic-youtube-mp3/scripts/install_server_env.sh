#!/usr/bin/env bash
set -euo pipefail

# Bootstrap a Debian/Ubuntu-like server for the known-good MeowMusic YouTube fallback stack.
# Safe to re-run. Review before using on production hosts.

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y curl ca-certificates gnupg ffmpeg python3 python3-pip

if ! command -v node >/dev/null 2>&1 || ! node -v | grep -Eq '^v22\.'; then
  install -d -m 0755 /etc/apt/keyrings
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
  apt-get update
  apt-get install -y nodejs
fi

python3 -m pip install --break-system-packages -U yt-dlp || python3 -m pip install -U yt-dlp
npm install -g yt-dlp-ejs

cat <<'EOF'
Done.
Verify with:
  node -v
  yt-dlp --version
  ffmpeg -version | head -n 1
  yt-dlp-ejs --help || true

Recommended yt-dlp flags for the known-good setup:
  --extractor-args "youtube:player_client=tv,web;formats=missing_pot"
  --extractor-args "youtube:player_skip=webpage,configs"
EOF
