#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run as root." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

VERSION="${OBSIDIAN_VERSION:-1.12.4}"
DEB_URL="https://github.com/obsidianmd/obsidian-releases/releases/download/v${VERSION}/obsidian_${VERSION}_amd64.deb"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

require_cmd apt-get
require_cmd curl

apt-get update -y
apt-get install -y curl xvfb acl libasound2

if ! id -u obsidian >/dev/null 2>&1; then
  /usr/sbin/useradd -m -s /bin/bash obsidian
fi

INSTALLED_VERSION=""
if command -v obsidian >/dev/null 2>&1; then
  INSTALLED_VERSION="$(dpkg-query -W -f='${Version}' obsidian 2>/dev/null || true)"
fi

if [[ "$INSTALLED_VERSION" == "$VERSION" ]]; then
  echo "Official Obsidian ${VERSION} already installed."
else
  curl -LfsS "$DEB_URL" -o "$TMPDIR/obsidian.deb"
  apt-get install -y "$TMPDIR/obsidian.deb"
  echo "Installed official Obsidian ${VERSION}."
fi

echo "User ready: obsidian"
echo "Dependencies ready: xvfb acl libasound2"
