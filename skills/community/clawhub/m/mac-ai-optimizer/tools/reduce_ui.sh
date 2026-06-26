#!/bin/bash
# reduce_ui.sh - Reduce macOS UI overhead (GPU + RAM)
# Expected savings: 200~500MB RAM + reduced GPU load

set -e

echo "=============================="
echo "  UI Optimization"
echo "=============================="
echo ""

# 1. Reduce transparency
echo "[1/5] Enabling reduce transparency..."
defaults write com.apple.universalaccess reduceTransparency -bool true 2>/dev/null
echo "  -> Transparency reduced"

# 2. Reduce motion
echo "[2/5] Enabling reduce motion..."
defaults write com.apple.universalaccess reduceMotion -bool true 2>/dev/null
echo "  -> Motion reduced"

# 3. Speed up Dock (remove animation delay)
echo "[3/5] Optimizing Dock..."
defaults write com.apple.dock autohide-delay -float 0 2>/dev/null
defaults write com.apple.dock autohide-time-modifier -float 0.3 2>/dev/null
defaults write com.apple.dock launchanim -bool false 2>/dev/null
defaults write com.apple.dock expose-animation-duration -float 0.1 2>/dev/null
# Minimize to application to reduce Dock memory
defaults write com.apple.dock minimize-to-application -bool true 2>/dev/null
echo "  -> Dock animations minimized"

# 4. Disable window animations
echo "[4/5] Reducing window animations..."
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false 2>/dev/null
defaults write -g QLPanelAnimationDuration -float 0 2>/dev/null
echo "  -> Window animations disabled"

# 5. Disable Finder animations and previews
echo "[5/5] Optimizing Finder..."
defaults write com.apple.finder DisableAllAnimations -bool true 2>/dev/null
defaults write com.apple.finder QLEnableTextSelection -bool false 2>/dev/null
echo "  -> Finder animations disabled"

# Apply Dock changes
killall Dock 2>/dev/null || true

# Apply Finder changes
killall Finder 2>/dev/null || true

echo ""
echo "=============================="
echo "  UI optimization complete"
echo "  Estimated savings: ~300-500MB RAM + GPU"
echo "=============================="
echo ""
echo "To revert all UI changes, run:"
echo "  defaults delete com.apple.universalaccess reduceTransparency"
echo "  defaults delete com.apple.universalaccess reduceMotion"
echo "  defaults delete com.apple.dock autohide-delay"
echo "  defaults delete com.apple.dock autohide-time-modifier"
echo "  defaults delete com.apple.dock launchanim"
echo "  killall Dock"
