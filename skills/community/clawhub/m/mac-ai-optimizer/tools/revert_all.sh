#!/bin/bash
# revert_all.sh - Revert all optimizations back to macOS defaults
# Safe to run anytime

echo "=============================="
echo "  Reverting All Optimizations"
echo "=============================="
echo ""

# 1. Re-enable Spotlight
echo "[1/5] Re-enabling Spotlight..."
sudo mdutil -a -i on 2>/dev/null && echo "  -> Spotlight enabled" || echo "  -> Skipped (needs sudo)"

# 2. Re-enable Siri
echo "[2/5] Re-enabling Siri..."
defaults write com.apple.assistant.support "Assistant Enabled" -bool true 2>/dev/null || true
echo "  -> Siri re-enabled"

# 3. Revert UI changes
echo "[3/5] Reverting UI optimizations..."
defaults delete com.apple.universalaccess reduceTransparency 2>/dev/null || true
defaults delete com.apple.universalaccess reduceMotion 2>/dev/null || true
defaults delete com.apple.dock autohide-delay 2>/dev/null || true
defaults delete com.apple.dock autohide-time-modifier 2>/dev/null || true
defaults delete com.apple.dock launchanim 2>/dev/null || true
defaults delete com.apple.dock expose-animation-duration 2>/dev/null || true
defaults delete com.apple.dock minimize-to-application 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticWindowAnimationsEnabled 2>/dev/null || true
defaults delete -g QLPanelAnimationDuration 2>/dev/null || true
defaults delete com.apple.finder DisableAllAnimations 2>/dev/null || true
defaults delete com.apple.CrashReporter DialogType 2>/dev/null || true
killall Dock 2>/dev/null || true
killall Finder 2>/dev/null || true
echo "  -> UI settings reverted to defaults"

# 4. Re-enable crash reporter
echo "[4/5] Restoring crash reporter..."
defaults delete com.apple.CrashReporter DialogType 2>/dev/null || true
echo "  -> Crash reporter restored"

# 5. Note about SSH
echo "[5/5] SSH status..."
echo "  -> SSH was not disabled (you may want to keep it)"
echo "  -> To disable: sudo systemsetup -setremotelogin off"

echo ""
echo "=============================="
echo "  All optimizations reverted"
echo "  Restart your Mac for full effect"
echo "=============================="
