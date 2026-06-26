#!/usr/bin/env bash
set -e

BASE_DIR="$HOME/.openclaw/music"
BIN="$BASE_DIR/go-music-api"
LOG_FILE="$BASE_DIR/log.txt"
PID_FILE="$BASE_DIR/pid"
PORT_FILE="$BASE_DIR/port"
API_URL="https://api.github.com/repos/guohuiyuan/go-music-api/releases/latest"

mkdir -p "$BASE_DIR"

echo "[music] base dir: $BASE_DIR"

have_cmd() {
 command -v "$1" >/dev/null 2>&1
}

is_pid_running() {
 if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [ -n "$PID" ] && ps -p "$PID" >/dev/null 2>&1; then
   return 0
  fi
 fi
 return 1
}

port_is_busy() {
 P="$1"
 if have_cmd lsof; then
  lsof -i :"$P" >/dev/null 2>&1
  return $?
 fi
 if have_cmd ss; then
  ss -ltn "( sport = :$P )" | grep -q LISTEN
  return $?
 fi
 return 1
}

find_free_port() {
 for P in 8080 8081 8090 18080 28080; do
  if ! port_is_busy "$P"; then
   echo "$P"
   return 0
  fi
 done
 return 1
}

healthcheck() {
 P="$1"
 curl -fsS "http://localhost:$P/api/v1/music/search?q=test" >/dev/null 2>&1
}

cleanup_stale_pid() {
 if [ -f "$PID_FILE" ] && ! is_pid_running; then
  rm -f "$PID_FILE"
 fi
}

cleanup_stale_pid

if is_pid_running; then
 if [ -f "$PORT_FILE" ]; then
  RUN_PORT="$(cat "$PORT_FILE" 2>/dev/null || true)"
  if [ -n "$RUN_PORT" ] && healthcheck "$RUN_PORT"; then
   echo "[music] service already running on port $RUN_PORT"
   exit 0
  fi
 fi
fi

if [ ! -f "$BIN" ]; then
 echo "[music] fetching latest release info..."
 JSON="$(curl -fsSL "$API_URL")"

 PLATFORM="$(uname -s)"
 ARCH="$(uname -m)"

 TARGET=""
 ASSET_NAME=""
 case "$PLATFORM" in
  Darwin)
   if [ "$ARCH" = "arm64" ]; then
    TARGET="darwin-arm64"
    ASSET_NAME="go-music-api_darwin_arm64.tar.gz"
   else
    TARGET="darwin-amd64"
    ASSET_NAME="go-music-api_darwin_amd64.tar.gz"
   fi
   ;;
  Linux)
   if [ "$ARCH" = "x86_64" ]; then
    TARGET="linux-amd64"
    ASSET_NAME="go-music-api_linux_amd64.tar.gz"
   elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    TARGET="linux-arm64"
    ASSET_NAME="go-music-api_linux_arm64.tar.gz"
   else
    echo "[music] unsupported Linux arch: $ARCH"
    exit 1
   fi
   ;;
  *)
   echo "[music] unsupported platform: $PLATFORM"
   exit 1
   ;;
 esac

 echo "[music] target: $TARGET"
 echo "[music] asset: $ASSET_NAME"

 URL="$(printf "%s" "$JSON" | tr ',' '\n' | grep 'browser_download_url' | grep "$ASSET_NAME" | head -n 1 | cut -d '"' -f 4)"

 if [ -z "$URL" ]; then
  echo "[music] failed to find release asset: $ASSET_NAME"
  exit 1
 fi

 PKG="$BASE_DIR/${ASSET_NAME}"
 EXTRACT_DIR="$BASE_DIR/extract"
 rm -rf "$EXTRACT_DIR"
 mkdir -p "$EXTRACT_DIR"

 echo "[music] downloading: $URL"
 curl -fL "$URL" -o "$PKG"

 if echo "$URL" | grep -qE "\.tar\.gz$|\.tgz$"; then
  tar -xzf "$PKG" -C "$EXTRACT_DIR"
 elif echo "$URL" | grep -qE "\.zip$"; then
  if ! have_cmd unzip; then
   echo "[music] unzip not found"
   exit 1
  fi
  unzip -o "$PKG" -d "$EXTRACT_DIR" >/dev/null
 else
  echo "[music] unsupported asset format: $URL"
  exit 1
 fi

 FOUND="$(find "$EXTRACT_DIR" -maxdepth 5 -type f \( -name 'go-music-api' -o -path '*/go-music-api' \) | head -n 1 || true)"
 if [ -z "$FOUND" ]; then
  echo "[music] binary not found after extraction"
  exit 1
 fi

 if ! file "$FOUND" | grep -Eq 'ELF|Mach-O'; then
  echo "[music] extracted file is not a native executable: $FOUND"
  file "$FOUND" || true
  exit 1
 fi

 cp "$FOUND" "$BIN"
 chmod +x "$BIN"
 rm -f "$PKG"
 rm -rf "$EXTRACT_DIR"
fi

PORT="$(find_free_port || true)"
if [ -z "$PORT" ]; then
 echo "[music] no free port found"
 exit 1
fi

echo "$PORT" > "$PORT_FILE"

echo "[music] starting service on port $PORT..."
nohup "$BIN" > "$LOG_FILE" 2>&1 &
PID="$!"
echo "$PID" > "$PID_FILE"

sleep 2

if healthcheck "$PORT"; then
 echo "[music] installed and running on http://localhost:$PORT"
 exit 0
fi

echo "[music] failed to start, check log: $LOG_FILE"
exit 1
