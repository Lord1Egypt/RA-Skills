#!/usr/bin/env bash
set -euo pipefail

app_name="Photo Booth"
capture_mode="window"
layout_mode="large"
output_path=""
activate_delay="2"
post_layout_delay="1"
large_width="1200"
large_height="900"

usage() {
  cat <<'EOF'
Usage: capture_via_app.sh [options]

Open a camera app, optionally enlarge it, then save a screenshot.

Options:
  --app NAME           App to activate (default: Photo Booth)
  --capture MODE       window|screen (default: window)
  --layout MODE        large|fullscreen|none (default: large)
  --output PATH        Output image path (required)
  --activate-delay N   Seconds to wait after opening app (default: 2)
  --layout-delay N     Seconds to wait after layout change (default: 1)
  -h, --help           Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --app)
      app_name="$2"
      shift 2
      ;;
    --capture)
      capture_mode="$2"
      shift 2
      ;;
    --layout)
      layout_mode="$2"
      shift 2
      ;;
    --output)
      output_path="$2"
      shift 2
      ;;
    --activate-delay)
      activate_delay="$2"
      shift 2
      ;;
    --layout-delay)
      post_layout_delay="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$output_path" ]]; then
  echo "--output is required" >&2
  exit 2
fi

if [[ "$capture_mode" != "window" && "$capture_mode" != "screen" ]]; then
  echo "--capture must be window or screen" >&2
  exit 2
fi

if [[ "$layout_mode" != "large" && "$layout_mode" != "fullscreen" && "$layout_mode" != "none" ]]; then
  echo "--layout must be large, fullscreen, or none" >&2
  exit 2
fi

mkdir -p "$(dirname "$output_path")"

window_bounds="$({
/usr/bin/osascript <<APPLESCRIPT
set appName to "$app_name"
set layoutMode to "$layout_mode"
set activateDelay to $activate_delay
set layoutDelay to $post_layout_delay
set targetWidth to $large_width
set targetHeight to $large_height

tell application appName to activate
delay activateDelay

tell application "System Events"
  if layoutMode is "fullscreen" then
    keystroke "f" using {command down, control down}
    delay layoutDelay + 1
  else if layoutMode is "large" then
    tell process appName
      set frontmost to true
      try
        set position of front window to {60, 60}
        set size of front window to {targetWidth, targetHeight}
      end try
    end tell
    delay layoutDelay
  end if

  tell process appName
    set frontmost to true
    set winPos to position of front window
    set winSize to size of front window
    set x1 to item 1 of winPos
    set y1 to item 2 of winPos
    set w1 to item 1 of winSize
    set h1 to item 2 of winSize
    return (x1 as text) & "," & (y1 as text) & "," & (w1 as text) & "," & (h1 as text)
  end tell
end tell
APPLESCRIPT
} 2>/dev/null || true)"

if [[ "$capture_mode" == "screen" ]]; then
  /usr/sbin/screencapture -x "$output_path"
else
  if [[ -z "$window_bounds" ]]; then
    echo "Failed to read app window bounds. Check Accessibility and Automation permissions." >&2
    exit 1
  fi
  /usr/sbin/screencapture -x -R"$window_bounds" "$output_path"
fi

printf '%s\n' "$output_path"
