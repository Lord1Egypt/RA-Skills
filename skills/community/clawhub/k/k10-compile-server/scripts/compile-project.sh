#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────
# K10 Compile Server - Project Compile Helper
# Usage:
#   export COMPILE_SERVER=https://your-k10-compile-server.example.com:8900    # 设一次即可
#   bash k10-compile-server/scripts/compile-project.sh \
#     --server $COMPILE_SERVER \
#     --dir /path/to/k10-project \
#     --output ./firmware.bin
#
#   # Recommended client-side upload with no local tools:
#   bash k10-compile-server/scripts/compile-project.sh \
#     --server $COMPILE_SERVER \
#     --dir /path/to/k10-project \
#     --web-serial
#
#   # With server-side flash:
#   bash k10-compile-server/scripts/compile-project.sh \
#     --server $COMPILE_SERVER \
#     --dir /path/to/k10-project \
#     --flash
#
#   # With local client-side USB upload:
#   bash k10-compile-server/scripts/compile-project.sh \
#     --server $COMPILE_SERVER \
#     --dir /path/to/k10-project \
#     --upload-local \
#     --port /dev/cu.usbmodemXXXX
# ──────────────────────────────────────────────────────────────

# Default: use COMPILE_SERVER env var; do not guess a server URL.
SERVER="${COMPILE_SERVER:-}"
PROJECT_DIR=""
OUTPUT=""
FLASH=false
UPLOAD_LOCAL=false
WEB_SERIAL=false
PORT=""
BAUD=921600
POLL_INTERVAL=3
COMPILE_TIMEOUT=300

usage() {
  echo "Usage: $0 --server <url> --dir <project-dir> [--output <path>] [--web-serial] [--flash] [--upload-local] [--port <port>] [--baud <baud>]"
  echo ""
  echo "  --server       Compile server URL (or set \$COMPILE_SERVER)"
  echo "  --dir          K10 PlatformIO project directory"
  echo "  --output       Output path for firmware.bin (default: ./firmware-<build_id>.bin)"
  echo "  --web-serial   Open browser Web Serial flash page after compile (recommended client upload)"
  echo "  --flash        Flash to board via server-side USB after compile"
  echo "  --upload-local Flash to K10 connected to this client machine after compile"
  echo "  --port         Local serial port for --upload-local (auto-detect if omitted)"
  echo "  --baud         Local upload baud rate (default: 921600)"
  echo "  --help         Show this help"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)   SERVER="${2:-}"; shift 2 ;;
    --dir)      PROJECT_DIR="${2:-}"; shift 2 ;;
    --output)   OUTPUT="${2:-}"; shift 2 ;;
    --web-serial) WEB_SERIAL=true; shift ;;
    --flash)    FLASH=true;    shift ;;
    --upload-local) UPLOAD_LOCAL=true; shift ;;
    --port)      PORT="${2:-}"; shift 2 ;;
    --baud)      BAUD="${2:-}"; shift 2 ;;
    --help|-h)  usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# ── Validate ──────────────────────────────────────────────────

if [[ -z "$SERVER" || -z "$PROJECT_DIR" ]]; then
  echo "❌ --server and --dir are required. You can also set COMPILE_SERVER for the server URL."
  usage
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "❌ Project directory does not exist: $PROJECT_DIR"
  exit 1
fi

if [[ ! -f "$PROJECT_DIR/platformio.ini" ]]; then
  echo "❌ No platformio.ini found in $PROJECT_DIR"
  exit 1
fi

UPLOAD_MODE_COUNT=0
[[ "$FLASH" == true ]] && UPLOAD_MODE_COUNT=$((UPLOAD_MODE_COUNT + 1))
[[ "$UPLOAD_LOCAL" == true ]] && UPLOAD_MODE_COUNT=$((UPLOAD_MODE_COUNT + 1))
[[ "$WEB_SERIAL" == true ]] && UPLOAD_MODE_COUNT=$((UPLOAD_MODE_COUNT + 1))
if [[ "$UPLOAD_MODE_COUNT" -gt 1 ]]; then
  echo "❌ Use only one upload mode: --web-serial for browser upload, --flash for server-side USB, or --upload-local for local esptool"
  exit 1
fi

for CMD in curl python3 mktemp stat zip; do
  if ! command -v "$CMD" >/dev/null 2>&1; then
    echo "❌ Required command not found: $CMD"
    echo "   On Windows, prefer k10-compile-server/scripts/compile-project.ps1 to avoid WSL/Git Bash tool gaps."
    exit 1
  fi
done

# Remove trailing slash
SERVER="${SERVER%/}"

# Resolve relative output before changing into the project directory.
if [[ -n "$OUTPUT" && "$OUTPUT" != /* ]]; then
  OUTPUT="$(pwd)/$OUTPUT"
fi

# ── Step 1: Health check ──────────────────────────────────────

echo "🔍 Checking server health..."
if ! HEALTH=$(curl -skf --connect-timeout 5 "$SERVER/api/health" 2>/dev/null); then
  echo "❌ Cannot connect to server at $SERVER"
  echo "   Check if the server is running and reachable."
  exit 1
fi

K10_READY=$(echo "$HEALTH" | python3 -c "import sys,json;print(json.load(sys.stdin).get('k10_toolchain_ready',False))" 2>/dev/null || echo "unknown")
echo "   Server OK (K10 toolchain: $K10_READY)"

find_local_port() {
  local candidates=()
  case "$(uname -s)" in
    Darwin*)
      for tty in /dev/cu.usbmodem* /dev/cu.usbserial* /dev/cu.SLAB* /dev/cu.wchusb*; do
        [[ -e "$tty" ]] && candidates+=("$tty")
      done
      ;;
    Linux*)
      for tty in /dev/ttyACM* /dev/ttyUSB*; do
        [[ -e "$tty" ]] && candidates+=("$tty")
      done
      ;;
    CYGWIN*|MINGW*|MSYS*)
      mapfile -t candidates < <(powershell.exe -NoProfile -Command "Get-PnpDevice -Class Ports -ErrorAction SilentlyContinue | Where-Object { \$_.FriendlyName -match 'USB|UART|Serial|CP210|CH340|ESP|UNIHIKER|K10' -and \$_.FriendlyName -match 'COM\\d+' } | ForEach-Object { [regex]::Match(\$_.FriendlyName, 'COM\\d+').Value }" 2>/dev/null | tr -d '\r')
      ;;
  esac
  if [[ "${#candidates[@]}" -eq 1 ]]; then
    echo "${candidates[0]}"
    return 0
  fi
  if [[ "${#candidates[@]}" -gt 1 ]]; then
    echo "Multiple local serial ports found:" >&2
    printf '   %s\n' "${candidates[@]}" >&2
  fi
  return 1
}

run_esptool() {
  if command -v esptool.py >/dev/null 2>&1; then
    esptool.py "$@"
  elif command -v esptool >/dev/null 2>&1; then
    esptool "$@"
  elif command -v esptool.exe >/dev/null 2>&1; then
    esptool.exe "$@"
  elif python3 -c "import esptool" >/dev/null 2>&1; then
    python3 -m esptool "$@"
  else
    echo "❌ esptool not found. Install it on the client machine:"
    echo "   python3 -m pip install esptool"
    return 1
  fi
}

open_url() {
  local url="$1"
  case "$(uname -s)" in
    Darwin*)
      open "$url" >/dev/null 2>&1 || return 1
      ;;
    Linux*)
      xdg-open "$url" >/dev/null 2>&1 || return 1
      ;;
    CYGWIN*|MINGW*|MSYS*)
      powershell.exe -NoProfile -Command "Start-Process '$url'" >/dev/null 2>&1 || return 1
      ;;
    *)
      return 1
      ;;
  esac
}

# ── Step 2: Create zip ────────────────────────────────────────

ZIP_FILE=$(mktemp /tmp/k10-compile-XXXXXX.zip)
trap "rm -f $ZIP_FILE" EXIT

echo "📦 Zipping project: $PROJECT_DIR"
cd "$PROJECT_DIR"
zip -r "$ZIP_FILE" . -x ".pio/*" ".git/*" "build/*" "__pycache__/*" "*.pyc" >/dev/null 2>&1
ZIP_SIZE=$(stat --printf="%s" "$ZIP_FILE" 2>/dev/null || stat -f%z "$ZIP_FILE" 2>/dev/null)
echo "   Zip size: $((ZIP_SIZE/1024)) KB"

# ── Step 3: Submit compile ────────────────────────────────────

echo "🚀 Submitting compile job..."
SUBMIT=$(curl -skf -X POST "$SERVER/api/compile" \
  -F "file=@$ZIP_FILE" 2>/dev/null)

BUILD_ID=$(echo "$SUBMIT" | python3 -c "import sys,json;print(json.load(sys.stdin)['build_id'])" 2>/dev/null || echo "")
if [[ -z "$BUILD_ID" ]]; then
  echo "❌ Failed to submit compile:"
  echo "$SUBMIT"
  exit 1
fi
echo "   Build ID: $BUILD_ID"

# ── Step 4: Poll for completion ───────────────────────────────

echo "⏳ Compiling (polling every ${POLL_INTERVAL}s, timeout ${COMPILE_TIMEOUT}s)..."
START_TIME=$SECONDS

while true; do
  ELAPSED=$((SECONDS - START_TIME))
  if [[ $ELAPSED -gt $COMPILE_TIMEOUT ]]; then
    echo "❌ Compile timed out after ${COMPILE_TIMEOUT}s"
    exit 1
  fi

  STATUS=$(curl -sk "$SERVER/api/build/$BUILD_ID/status" 2>/dev/null || echo '{"status":"unknown"}')
  STATE=$(echo "$STATUS" | python3 -c "import sys,json;print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unknown")

  case "$STATE" in
    done)
      SIZE=$(echo "$STATUS" | python3 -c "import sys,json;print(json.load(sys.stdin).get('bin_size',''))" 2>/dev/null || echo "")
      if [[ "$SIZE" =~ ^[0-9]+$ ]]; then
        echo "✅ Compile complete! ($((SIZE/1024)) KB, ${ELAPSED}s)"
      else
        echo "✅ Compile complete! (${ELAPSED}s)"
      fi
      break
      ;;
    error)
      ERR=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('error',''))" 2>/dev/null)
      LOG=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('log','')[-300:])" 2>/dev/null)
      echo "❌ Compile failed: $ERR"
      if [[ -n "$LOG" ]]; then
        echo "   Last log lines:"
        echo "$LOG" | sed 's/^/   /'
      fi
      exit 1
      ;;
    compiling)
      echo "   ⏳ Compiling... (${ELAPSED}s)"
      ;;
    queued)
      POS=$(echo "$STATUS" | python3 -c "import sys,json;print(json.load(sys.stdin).get('queue_position','?'))" 2>/dev/null)
      echo "   ⏳ Queued (position: $POS)..."
      ;;
    *)
      echo "   Status: $STATE"
      ;;
  esac

  sleep "$POLL_INTERVAL"
done

# ── Step 5: Download firmware ────────────────────────────────

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="./firmware-$BUILD_ID.bin"
fi

echo "💾 Downloading firmware to $OUTPUT"
if ! curl -skf -o "$OUTPUT" "$SERVER/api/build/$BUILD_ID/download" 2>/dev/null; then
  echo "❌ Firmware download failed"
  exit 1
fi
if [[ ! -s "$OUTPUT" ]]; then
  echo "❌ Firmware download produced an empty file: $OUTPUT"
  exit 1
fi
ls -lh "$OUTPUT"

# Show flash manifest
echo "📋 Flash layout:"
curl -sk "$SERVER/api/build/$BUILD_ID/flash-files" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "   (manifest not available)"

# ── Step 6a: Optional browser Web Serial upload ────────────────

if [[ "$WEB_SERIAL" == true ]]; then
  WEB_SERIAL_URL="$SERVER/?build_id=$BUILD_ID"
  echo "🌐 Opening Web Serial flash page:"
  echo "   $WEB_SERIAL_URL"
  echo "   Use Chrome/Edge, click 浏览器烧录, and choose the K10 serial port."
  echo "   The page tries automatic bootloader entry first; use BOOT/RST only if prompted."
  if ! open_url "$WEB_SERIAL_URL"; then
    echo "⚠️  Could not open the browser automatically. Open this URL manually:"
    echo "   $WEB_SERIAL_URL"
  fi
fi

# ── Step 6b: Optional client-side local USB upload ─────────────

if [[ "$UPLOAD_LOCAL" == true ]]; then
  if [[ -z "$PORT" ]]; then
    echo "🔌 Detecting local K10 serial port..."
    PORT=$(find_local_port || true)
  fi
  if [[ -z "$PORT" ]]; then
    echo "❌ Could not auto-detect local K10 serial port."
    echo "   Re-run with --port <port>, e.g. COM3, /dev/cu.usbmodemXXXX, or /dev/ttyACM0."
    exit 1
  fi

  FLASH_DIR=$(mktemp -d /tmp/k10-flash-XXXXXX)
  trap "rm -f $ZIP_FILE; rm -rf $FLASH_DIR" EXIT
  echo "⬇️  Downloading flash files for local upload..."
  for FILE in bootloader partitions firmware; do
    if ! curl -skf -o "$FLASH_DIR/${FILE}.bin" "$SERVER/api/build/$BUILD_ID/file/${FILE}.bin" 2>/dev/null; then
      echo "❌ Failed to download ${FILE}.bin"
      exit 1
    fi
  done

  echo "⚡ Uploading to local K10 on $PORT..."
  echo "   If upload cannot enter bootloader automatically: hold BOOT, tap RST, then release BOOT."
  run_esptool \
    --chip esp32s3 \
    --port "$PORT" \
    --baud "$BAUD" \
    --before default_reset \
    --after hard_reset \
    write_flash -z \
    --flash_mode dio \
    --flash_freq 80m \
    --flash_size detect \
    0x0 "$FLASH_DIR/bootloader.bin" \
    0x8000 "$FLASH_DIR/partitions.bin" \
    0x10000 "$FLASH_DIR/firmware.bin"
  echo "✅ Local upload successful! K10 is rebooting..."
fi

# ── Step 6c: Optional server-side flash ────────────────────────

if [[ "$FLASH" == true ]]; then
  echo "⚡ Triggering server-side flash..."
  echo "   (Make sure K10 is connected via USB to the server machine)"
  FLASH_RESULT=$(curl -sk -X POST "$SERVER/api/flash/$BUILD_ID" 2>/dev/null)
  FLASH_STATUS=$(echo "$FLASH_RESULT" | python3 -c "import sys,json;print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null)
  if [[ "$FLASH_STATUS" == "success" ]]; then
    echo "✅ Flash successful! K10 is rebooting..."
  else
    echo "❌ Flash failed:"
    echo "$FLASH_RESULT"
    exit 1
  fi
fi

echo ""
echo "✅ Done! Build $BUILD_ID complete."
echo "   Firmware: $OUTPUT"
