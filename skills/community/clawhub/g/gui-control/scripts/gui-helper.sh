#!/usr/bin/env bash
# gui-helper.sh — Quick GUI operations on DISPLAY=:1
# Usage: gui-helper.sh <command> [args]
#
# Commands:
#   open <url>          Open Firefox with URL
#   close               Close Firefox
#   screenshot [path]   Take screenshot (default: /tmp/screenshot.png)
#   type <text>         Type text into active window
#   key <key>           Press a key (e.g., Return, Tab, Escape)
#   window              Get active window name
#   wait [seconds]      Wait N seconds (default: 5)

set -euo pipefail
DISPLAY=:1
export DISPLAY

cmd="${1:-help}"
shift || true

case "$cmd" in
  open)
    url="${1:-https://www.google.com}"
    nohup firefox "$url" > /dev/null 2>&1 &
    echo "Firefox opened: $url"
    ;;
  close)
    pkill firefox 2>/dev/null || true
    echo "Firefox closed"
    ;;
  screenshot)
    out="${1:-/tmp/screenshot.png}"
    scrot "$out"
    echo "Screenshot saved: $out"
    ;;
  type)
    text="${1:-}"
    xdotool type --delay 50 "$text"
    echo "Typed: $text"
    ;;
  key)
    key="${1:-Return}"
    xdotool key "$key"
    echo "Key pressed: $key"
    ;;
  window)
    xdotool getactivewindow getwindowname
    ;;
  wait)
    secs="${1:-5}"
    sleep "$secs"
    echo "Waited ${secs}s"
    ;;
  help|*)
    echo "Usage: gui-helper.sh <command> [args]"
    echo "Commands: open <url>, close, screenshot [path], type <text>, key <key>, window, wait [seconds]"
    ;;
esac
