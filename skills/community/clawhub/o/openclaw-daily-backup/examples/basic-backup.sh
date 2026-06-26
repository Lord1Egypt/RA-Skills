#!/bin/bash

# Example: Basic backup workflow

echo "Creating backup..."
node scripts/backup.mjs --name "example-backup" --desc "Example backup for demonstration"

echo ""
echo "Listing backups..."
node scripts/list.mjs

echo ""
echo "Validating backup..."
node scripts/validate.mjs --name example-backup

echo ""
echo "Preview restore (dry run)..."
node scripts/restore.mjs --name example-backup --dry-run

echo ""
echo "✅ Example complete!"
echo "To actually restore: node scripts/restore.mjs --name example-backup"
