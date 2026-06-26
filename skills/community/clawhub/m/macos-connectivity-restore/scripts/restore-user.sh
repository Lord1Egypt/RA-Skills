#!/bin/zsh
set -euo pipefail

/usr/bin/defaults write com.apple.sharingd DiscoverableMode -string "Contacts Only"
/usr/bin/defaults write com.apple.NetworkBrowser DisableAirDrop -bool false

killall sharingd >/dev/null 2>&1 || true
killall Finder >/dev/null 2>&1 || true
killall SystemUIServer >/dev/null 2>&1 || true
killall cfprefsd >/dev/null 2>&1 || true

echo "AirDrop discoverability set to Contacts Only"
