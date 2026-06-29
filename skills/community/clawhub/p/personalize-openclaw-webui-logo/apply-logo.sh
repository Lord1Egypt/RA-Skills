#!/usr/bin/env bash
# Apply a named logo set as the OpenClaw control-ui website favicon.
#
# Usage:
#   bash apply-logo.sh [<set-name>]      (default: mac)
#
# Logo sets live in:  <skill>/logos/<set-name>/
#   - favicon-master.png  (raw, preferred if present)
#   - favicon-master.txt  (base64 of the PNG; shipped through hubs that reject raw .png)
#
# UI dist auto-discovery order (override anytime with OPENCLAW_UI_DIR=/abs/path):
#   1. $OPENCLAW_UI_DIR
#   2. $(npm root -g)/openclaw/dist/control-ui   (works for npm/pnpm/yarn-global)
#   3. dirname of `which openclaw` walked up to find ../lib/node_modules/openclaw/dist/control-ui
#   4. Common locations: ~/.npm-global, /usr/local, /opt/homebrew, /usr/lib, %APPDATA%/npm
#
# Image toolchain auto-discovery (first available wins):
#   sips (macOS) → magick/convert (ImageMagick, Linux/Win/mac) → python+Pillow → ffmpeg
#
# Runtime state (the .applied-state stamp + checker log) is written to
#   ${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/
# so the skill dir itself stays publish-clean (no user paths leak into hubs).
#
# Re-run after any openclaw update overwrites dist/control-ui/.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SET="${1:-mac}"
SETDIR="$SKILL_DIR/logos/$SET"

# ---------- 1. Locate control-ui dist ----------
find_ui_dir() {
  # 1. Explicit override
  if [ -n "${OPENCLAW_UI_DIR:-}" ]; then
    echo "$OPENCLAW_UI_DIR"; return 0
  fi

  local candidates=()

  # 2. npm root -g
  if command -v npm >/dev/null 2>&1; then
    local nr
    nr="$(npm root -g 2>/dev/null || true)"
    [ -n "$nr" ] && candidates+=("$nr/openclaw/dist/control-ui")
  fi

  # 3. which openclaw → walk up
  if command -v openclaw >/dev/null 2>&1; then
    local bin real dir
    bin="$(command -v openclaw)"
    # Resolve symlink if possible (readlink -f is GNU; fallback to python)
    if real="$(readlink -f "$bin" 2>/dev/null)"; then :; \
    elif command -v python3 >/dev/null 2>&1; then
      real="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$bin")"
    else
      real="$bin"
    fi
    dir="$(dirname "$real")"
    # Typical layouts: <prefix>/bin/openclaw → <prefix>/lib/node_modules/openclaw/dist/control-ui
    candidates+=("$dir/../lib/node_modules/openclaw/dist/control-ui")
    candidates+=("$dir/../../openclaw/dist/control-ui")
  fi

  # 4. Common install prefixes
  candidates+=(
    "$HOME/.npm-global/lib/node_modules/openclaw/dist/control-ui"
    "$HOME/.local/lib/node_modules/openclaw/dist/control-ui"
    "/usr/local/lib/node_modules/openclaw/dist/control-ui"
    "/opt/homebrew/lib/node_modules/openclaw/dist/control-ui"
    "/usr/lib/node_modules/openclaw/dist/control-ui"
  )
  # Windows (Git Bash / MSYS / WSL with /mnt/c)
  if [ -n "${APPDATA:-}" ]; then
    candidates+=("$APPDATA/npm/node_modules/openclaw/dist/control-ui")
  fi
  if [ -n "${USERPROFILE:-}" ]; then
    candidates+=("$USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/dist/control-ui")
  fi

  local c
  for c in "${candidates[@]}"; do
    # Normalize ../ segments
    if [ -d "$c" ]; then
      ( cd "$c" && pwd -P )
      return 0
    fi
  done
  return 1
}

UI="$(find_ui_dir || true)"
if [ -z "$UI" ] || [ ! -d "$UI" ]; then
  echo "ERROR: openclaw control-ui dist not found." >&2
  echo "Tried npm root -g, \$(which openclaw), and common install prefixes." >&2
  echo "Set OPENCLAW_UI_DIR=/abs/path/to/openclaw/dist/control-ui and re-run." >&2
  exit 1
fi

if [ ! -d "$SETDIR" ]; then
  echo "ERROR: logo set '$SET' not found at $SETDIR" >&2
  echo "Available sets:" >&2
  ls -1 "$SKILL_DIR/logos" 2>/dev/null | sed 's/^/  - /' >&2 || echo "  (none)" >&2
  exit 1
fi

# ---------- 2. Resolve master PNG ----------
MASTER=""
CLEANUP=""
TMPROOT="${TMPDIR:-/tmp}"

if [ -f "$SETDIR/favicon-master.png" ]; then
  MASTER="$SETDIR/favicon-master.png"
elif [ -f "$SETDIR/favicon-master.txt" ]; then
  MASTER="$(mktemp "$TMPROOT/logo-master.XXXXXX").png"
  CLEANUP="$MASTER"
  # GNU base64 → -d; BSD/mac → -D. Try both.
  if ! base64 -d "$SETDIR/favicon-master.txt" > "$MASTER" 2>/dev/null; then
    base64 -D -i "$SETDIR/favicon-master.txt" > "$MASTER"
  fi
else
  echo "ERROR: no favicon-master.png or favicon-master.txt in $SETDIR" >&2
  exit 1
fi

# ---------- 3. Image toolchain dispatcher ----------
# resize_png <src> <dst> <size>   — produce a square PNG at <size>x<size>
# write_ico  <src> <dst> <size>   — produce an .ico (falls back to PNG bytes if no ico encoder)
TOOL=""
if command -v sips >/dev/null 2>&1; then
  TOOL="sips"
elif command -v magick >/dev/null 2>&1; then
  TOOL="magick"
elif command -v convert >/dev/null 2>&1; then
  TOOL="convert"
elif command -v python3 >/dev/null 2>&1 && python3 -c "import PIL" 2>/dev/null; then
  TOOL="pillow"
elif command -v ffmpeg >/dev/null 2>&1; then
  TOOL="ffmpeg"
else
  echo "ERROR: need one of: sips (macOS), ImageMagick (magick/convert), python3+Pillow, or ffmpeg." >&2
  echo "  macOS:    built-in sips" >&2
  echo "  Linux:    sudo apt install imagemagick   # or: pip install Pillow" >&2
  echo "  Windows:  choco install imagemagick      # or: pip install Pillow" >&2
  exit 1
fi

resize_png() {
  local src="$1" dst="$2" size="$3"
  case "$TOOL" in
    sips)
      sips -s format png "$src" --out "$dst" --resampleHeightWidth "$size" "$size" >/dev/null 2>&1
      ;;
    magick)
      magick "$src" -resize "${size}x${size}" "$dst"
      ;;
    convert)
      convert "$src" -resize "${size}x${size}" "$dst"
      ;;
    pillow)
      python3 - "$src" "$dst" "$size" <<'PY'
import sys
from PIL import Image
src, dst, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGBA")
im = im.resize((size, size), Image.LANCZOS)
im.save(dst, "PNG")
PY
      ;;
    ffmpeg)
      ffmpeg -y -i "$src" -vf "scale=${size}:${size}" "$dst" >/dev/null 2>&1
      ;;
  esac
}

write_ico() {
  local src="$1" dst="$2" size="$3"
  local tmp
  tmp="$(mktemp "$TMPROOT/fav.XXXXXX").png"
  resize_png "$src" "$tmp" "$size"
  case "$TOOL" in
    sips)
      sips -s format ico "$tmp" --out "$dst" >/dev/null 2>&1 || cp "$tmp" "$dst"
      ;;
    magick)
      magick "$tmp" "$dst" 2>/dev/null || cp "$tmp" "$dst"
      ;;
    convert)
      convert "$tmp" "$dst" 2>/dev/null || cp "$tmp" "$dst"
      ;;
    pillow)
      python3 - "$tmp" "$dst" <<'PY' || cp "$tmp" "$dst"
import sys
from PIL import Image
Image.open(sys.argv[1]).save(sys.argv[2], "ICO", sizes=[(64,64),(32,32),(16,16)])
PY
      ;;
    *)
      cp "$tmp" "$dst"
      ;;
  esac
  rm -f "$tmp"
}

# ---------- 4. Apply to dist ----------
# 1) favicon-32.png
resize_png "$MASTER" "$UI/favicon-32.png" 32
# 2) apple-touch-icon.png (180x180)
resize_png "$MASTER" "$UI/apple-touch-icon.png" 180
# 3) favicon.svg slot - browsers prefer it; wrap PNG as image-in-SVG
B64="$(base64 < "$MASTER" | tr -d '\n')"
cat > "$UI/favicon.svg" <<SVGEOF
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><image width="400" height="400" href="data:image/png;base64,$B64"/></svg>
SVGEOF
# 4) favicon.ico (64x64)
write_ico "$MASTER" "$UI/favicon.ico" 64

[ -n "$CLEANUP" ] && rm -f "$CLEANUP"

# ---------- 5. Write applied-state stamp to STATE_DIR (publish-safe) ----------
# State lives outside the skill dir so the skill stays clean for skillhub/clawhub publish.
STATE_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true
STAMP="$STATE_DIR/applied-state"

if command -v sha256sum >/dev/null 2>&1; then
  STAMP_HASH="$(sha256sum "$UI/favicon-32.png" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  STAMP_HASH="$(shasum -a 256 "$UI/favicon-32.png" | awk '{print $1}')"
else
  STAMP_HASH=""
fi
if [ -n "$STAMP_HASH" ]; then
  cat > "$STAMP" <<STAMPEOF
set=$SET
favicon32_sha256=$STAMP_HASH
ui_dir=$UI
skill_dir=$SKILL_DIR
applied_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
STAMPEOF
fi

echo "Applied logo set '$SET' to: $UI"
echo "Image tool: $TOOL"
ls -la "$UI"/favicon.svg "$UI"/favicon-32.png "$UI"/favicon.ico "$UI"/apple-touch-icon.png
echo "Hard-refresh the browser (Cmd+Shift+R / Ctrl+F5) to clear the cached old icon."
[ -n "$STAMP_HASH" ] && echo "State: $STAMP"
