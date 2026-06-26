#!/bin/bash
# Pre-deployment backup hook
# Add to .git/hooks/pre-push or CI/CD pipeline

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

# Get current git commit hash
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Create pre-deployment backup
node scripts/backup.mjs --name "pre-deploy-$COMMIT" --desc "Backup before deployment"

if [ $? -eq 0 ]; then
  echo "✅ Pre-deployment backup created: pre-deploy-$COMMIT"
  exit 0
else
  echo "❌ Pre-deployment backup failed"
  exit 1
fi
