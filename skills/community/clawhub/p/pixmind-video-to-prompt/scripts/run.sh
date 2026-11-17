#!/bin/sh

set -eu

required_version="24.20.0"
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ -z "${PIXMIND_NODE_FORCE_PORTABLE:-}" ] && command -v node >/dev/null 2>&1; then
  node "$script_dir/video-to-prompt.js" "$@"
  exit $?
fi

if [ "$(uname -s)" != "Darwin" ]; then
  printf '%s\n' "Portable Pixmind Node.js currently supports Windows and macOS. Install Node.js from https://nodejs.org/en/download" >&2
  exit 1
fi

case "$(uname -m)" in
  arm64|aarch64)
    architecture="arm64"
    fallback_archive_sha="40e5607e5ecb3db9192723776da2d75d966260fc74a7a9e731c1bd67dda96bc8"
    ;;
  x86_64|amd64)
    architecture="x64"
    fallback_archive_sha="9e5b2644cf107befb6aefca676b96d3296bc10138096f022ed378d6233ed81f4"
    ;;
  *)
    printf 'Unsupported macOS architecture: %s\n' "$(uname -m)" >&2
    exit 1
    ;;
esac

manifest_url=${PIXMIND_NODE_MANIFEST:-"https://cdn.pixmind.io/pixmind-builder/dependencies/node/macos/$architecture/manifest.json"}
cache_root=${PIXMIND_CACHE_DIR:-"$HOME/Library/Caches/Pixmind"}
temporary=$(mktemp -d "${TMPDIR:-/tmp}/pixmind-node.XXXXXX")
trap 'rm -rf "$temporary"' EXIT INT TERM
manifest="$temporary/manifest.json"

version="$required_version"
url=""
size="0"
sha256=""
official_url="https://nodejs.org/dist/v$required_version/node-v$required_version-darwin-$architecture.tar.gz"
official_sha256="$fallback_archive_sha"
official_archive_path="node-v$required_version-darwin-$architecture/bin/node"

if curl -fsSL --connect-timeout 15 --max-time 60 "$manifest_url" -o "$manifest"; then
  version=$(/usr/bin/plutil -extract preferred raw -o - "$manifest")
  url=$(/usr/bin/plutil -extract versions.0.url raw -o - "$manifest")
  size=$(/usr/bin/plutil -extract versions.0.size raw -o - "$manifest")
  sha256=$(/usr/bin/plutil -extract versions.0.sha256 raw -o - "$manifest")
  official_url=$(/usr/bin/plutil -extract versions.0.officialUrl raw -o - "$manifest")
  official_sha256=$(/usr/bin/plutil -extract versions.0.officialSha256 raw -o - "$manifest")
  official_archive_path=$(/usr/bin/plutil -extract versions.0.officialArchivePath raw -o - "$manifest")
else
  printf '%s\n' 'Pixmind Node.js manifest is unavailable; using the nodejs.org fallback.' >&2
fi

directory="$cache_root/node/macos-$architecture/$version"
node="$directory/node"
mkdir -p "$directory"

valid_node() {
  file=$1
  expected_size=$2
  expected_sha=$3
  [ -f "$file" ] || return 1
  [ "$expected_size" = "0" ] || [ "$(stat -f '%z' "$file")" = "$expected_size" ] || return 1
  [ -z "$expected_sha" ] || [ "$(shasum -a 256 "$file" | awk '{print $1}')" = "$expected_sha" ] || return 1
  [ "$("$file" --version 2>/dev/null)" = "v$version" ]
}

if valid_node "$node" "$size" "$sha256"; then
  "$node" "$script_dir/video-to-prompt.js" "$@"
  exit $?
fi

download="$temporary/node.download"
if [ -n "$url" ] && curl -fL --connect-timeout 15 --max-time 900 "$url" -o "$download"; then
  chmod 755 "$download"
  if valid_node "$download" "$size" "$sha256"; then
    mv "$download" "$node"
    "$node" "$script_dir/video-to-prompt.js" "$@"
    exit $?
  fi
  printf '%s\n' 'Pixmind Node.js download failed size, SHA-256, or version validation.' >&2
fi

archive="$temporary/node.tar.gz"
if curl -fL --connect-timeout 15 --max-time 900 "$official_url" -o "$archive" &&
  [ "$(shasum -a 256 "$archive" | awk '{print $1}')" = "$official_sha256" ]; then
  tar -xzf "$archive" -C "$temporary" "$official_archive_path"
  cp "$temporary/$official_archive_path" "$node"
  chmod 755 "$node"
  if valid_node "$node" 0 ""; then
    "$node" "$script_dir/video-to-prompt.js" "$@"
    exit $?
  fi
fi

cat >&2 <<'EOF'
Unable to install the portable Pixmind Node.js runtime.
Official Node.js download: https://nodejs.org/en/download
Backup command shown by the official download flow:
  brew install node@24
After installation, open a new terminal and retry.
EOF
exit 1
