#!/bin/bash
# Publish MemoryVault skill to ClawHub
# READY TO RUN: 2026-02-21 (when account age blocker lifts)

set -e

echo "=== ClawHub Publish Script ==="
echo "Repository: memoryvault-skill"
echo "Target: ClawHub marketplace"
echo ""

# Check account age (should be 7+ days old by 2026-02-21)
echo "Account created: 2026-02-14"
echo "Minimum age requirement: 7 days"
echo "Earliest publish date: 2026-02-21"
echo ""

# Confirm before proceeding
echo "This script will:"
echo "1. Install clawdhub CLI + undici dependency (fixes ERR_MODULE_NOT_FOUND)"
echo "2. Publish MemoryVault skill to ClawHub"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create temporary directory for npm install
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "=== Installing clawdhub CLI ==="
npm init -y > /dev/null 2>&1
npm install clawdhub undici

echo ""
echo "=== Publishing to ClawHub ==="
npx clawdhub publish ~/moltbook-poc/projects/memoryvault-skill \
    --slug memoryvault \
    --name "MemoryVault" \
    --version 1.0.0

echo ""
echo "=== Cleanup ==="
cd ~
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Published to ClawHub!"
echo "Track installs: check ClawHub dashboard"
echo "Monitor impact: watch for MV registrations from OpenClaw agents"
