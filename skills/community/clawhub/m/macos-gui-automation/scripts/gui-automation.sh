#!/bin/bash
# macOS GUI Automation Helper Script
# Usage: ./gui-automation.sh <command> [args]

set -e

SCREENSHOT_DIR="/tmp/gui-auto"
mkdir -p "$SCREENSHOT_DIR"

cmd="$1"
shift || true

case "$cmd" in
  capture)
    # Capture full screen or region
    # Usage: capture [x y w h]
    if [ $# -eq 4 ]; then
      screencapture -R "$1" "$2" "$3" "$4" "$SCREENSHOT_DIR/screen.png"
    else
      screencapture "$SCREENSHOT_DIR/screen.png"
    fi
    echo "$SCREENSHOT_DIR/screen.png"
    ;;
    
  ocr)
    # OCR from image or screen
    # Usage: ocr [image.png]
    img="${1:-$SCREENSHOT_DIR/screen.png}"
    if [ ! -f "$img" ]; then
      screencapture "$img"
    fi
    tesseract "$img" stdout
    ;;
    
  click)
    # Click at coordinates
    # Usage: click x y
    cliclick c:"$1,$2"
    ;;
    
  doubleclick)
    # Double click
    # Usage: doubleclick x y
    cliclick dc:"$1,$2"
    ;;
    
  rightclick)
    # Right click
    # Usage: rightclick x y
    cliclick rc:"$1,$2"
    ;;
    
  move)
    # Move mouse
    # Usage: move x y
    cliclick m:"$1,$2"
    ;;
    
  type)
    # Type text
    # Usage: type "text"
    cliclick t:"$*"
    ;;
    
  key)
    # Press key
    # Usage: key enter
    cliclick kp:"$1"
    ;;
    
  findtext)
    # Find text on screen and return coordinates
    # Usage: findtext "search text"
    # Returns: x,y or nothing if not found
    search="$*"
    screencapture "$SCREENSHOT_DIR/screen.png"
    ocr_result=$(tesseract "$SCREENSHOT_DIR/screen.png" stdout)
    
    # Simple line-by-line search (doesn't return coords, just confirms presence)
    if echo "$ocr_result" | grep -qi "$search"; then
      echo "found"
    else
      echo "not found"
    fi
    ;;
    
  listwindows)
    # List all application windows
    osascript -e 'tell application "System Events" to get name of every process'
    ;;
    
  frontwindow)
    # Get frontmost app window info
    osascript -e 'tell application "System Events"
      set frontApp to name of first application process whose frontmost is true
      return frontApp
    end tell'
    ;;
    
  help)
    echo "macOS GUI Automation Helper"
    echo ""
    echo "Commands:"
    echo "  capture [x y w h]     - Capture screen (full or region)"
    echo "  ocr [image.png]       - OCR from image or current screen"
    echo "  click x y             - Click at coordinates"
    echo "  doubleclick x y       - Double click"
    echo "  rightclick x y        - Right click"
    echo "  move x y              - Move mouse"
    echo "  type \"text\"          - Type text"
    echo "  key <keyname>         - Press key (enter, tab, escape, etc.)"
    echo "  findtext \"text\"       - Search for text on screen"
    echo "  listwindows           - List all apps"
    echo "  frontwindow           - Get frontmost app"
    echo ""
    echo "Examples:"
    echo "  ./gui-automation.sh capture"
    echo "  ./gui-automation.sh ocr"
    echo "  ./gui-automation.sh click 500 300"
    echo "  ./gui-automation.sh type \"hello world\""
    ;;
    
  *)
    echo "Unknown command: $cmd"
    echo "Run '$0 help' for usage"
    exit 1
    ;;
esac
