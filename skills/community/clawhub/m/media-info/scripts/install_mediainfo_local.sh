#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/vendor"
SRC_DIR="$VENDOR_DIR/mediainfo-src"
OUT_DIR="$VENDOR_DIR/mediainfo"

MEDIAINFO_VERSION="${MEDIAINFO_VERSION:-0.7.94}"
MEDIAINFO_URL="${MEDIAINFO_URL:-https://mediaarea.net/download/binary/mediainfo/${MEDIAINFO_VERSION}/MediaInfo_CLI_${MEDIAINFO_VERSION}_GNU_FromSource.tar.bz2}"

BIN="$OUT_DIR/MediaInfo/Project/GNU/CLI/mediainfo"

if [[ -x "$BIN" ]]; then
  echo "[ok] mediainfo already exists: $BIN"
  "$BIN" --Version || true
  exit 0
fi

mkdir -p "$SRC_DIR" "$OUT_DIR"
ARCHIVE="$SRC_DIR/mediainfo-${MEDIAINFO_VERSION}.tar.bz2"
EXTRACTED="$SRC_DIR/MediaInfo_CLI_GNU_FromSource"

if [[ ! -f "$ARCHIVE" ]]; then
  echo "[info] downloading $MEDIAINFO_URL"
  curl -fL "$MEDIAINFO_URL" -o "$ARCHIVE"
fi

rm -rf "$EXTRACTED"
mkdir -p "$EXTRACTED"
tar -xjf "$ARCHIVE" -C "$SRC_DIR"

pushd "$EXTRACTED" >/dev/null
bash ./CLI_Compile.sh
popd >/dev/null

rm -rf "$OUT_DIR"
mkdir -p "$VENDOR_DIR"
cp -a "$EXTRACTED" "$OUT_DIR"

if [[ ! -x "$BIN" ]]; then
  echo "[error] build completed but binary not found: $BIN" >&2
  exit 1
fi

echo "[ok] installed mediainfo: $BIN"
"$BIN" --Version || true
