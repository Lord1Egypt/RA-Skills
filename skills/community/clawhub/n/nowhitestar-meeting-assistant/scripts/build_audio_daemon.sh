#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$SCRIPT_DIR/AudioDaemon.app"
BIN="$SCRIPT_DIR/audio_daemon"
APP_BIN="$APP/Contents/MacOS/audio_daemon"
INFO="$APP/Contents/Info.plist"

cd "$SCRIPT_DIR"

swiftc -o "$BIN" audio_daemon.swift \
  -framework Cocoa \
  -framework ScreenCaptureKit \
  -framework AVFoundation \
  -framework CoreMedia \
  -framework CoreAudio

mkdir -p "$APP/Contents/MacOS"
cp "$BIN" "$APP_BIN"
chmod +x "$APP_BIN"

# Keep usage strings stable for TCC prompts.
/usr/libexec/PlistBuddy -c "Set :NSMicrophoneUsageDescription Meeting Assistant records microphone audio for meeting notes." "$INFO" >/dev/null 2>&1 || \
/usr/libexec/PlistBuddy -c "Add :NSMicrophoneUsageDescription string Meeting Assistant records microphone audio for meeting notes." "$INFO" >/dev/null 2>&1 || true
/usr/libexec/PlistBuddy -c "Set :NSScreenCaptureUsageDescription Meeting Assistant captures system audio for meeting notes." "$INFO" >/dev/null 2>&1 || \
/usr/libexec/PlistBuddy -c "Add :NSScreenCaptureUsageDescription string Meeting Assistant captures system audio for meeting notes." "$INFO" >/dev/null 2>&1 || true

IDENTITY="${MEETING_ASSISTANT_CODESIGN_IDENTITY:-}"
if [[ -z "$IDENTITY" ]]; then
  IDENTITY="$(security find-identity -v -p codesigning 2>/dev/null | awk -F'"' '/Apple Development: nowhitestar@gmail.com/ {print $2; exit}')"
fi
if [[ -z "$IDENTITY" ]]; then
  IDENTITY="$(security find-identity -v -p codesigning 2>/dev/null | awk -F'"' '/Developer ID Application|Apple Development|Mac Developer|PolyMeet Dev/ {print $2; exit}')"
fi
if [[ -z "$IDENTITY" ]]; then
  echo "⚠️ No fixed code-signing identity found; falling back to ad-hoc." >&2
  IDENTITY="-"
fi

codesign --force --deep --timestamp=none --sign "$IDENTITY" "$APP"
codesign --verify --deep --strict --verbose=2 "$APP"

echo "✅ Built and signed AudioDaemon.app"
echo "   identity: $IDENTITY"
codesign -dvvv "$APP" 2>&1 | grep -E 'Identifier|Authority|TeamIdentifier|CDHash|Signature' || true
