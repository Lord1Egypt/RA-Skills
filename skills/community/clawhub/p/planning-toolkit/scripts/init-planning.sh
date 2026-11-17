#!/bin/bash
# init-planning.sh — Initialize a planning directory with templates
# Usage: bash init-planning.sh "task-slug"
#
# Creates: .planning/YYYY-MM-DD-task-slug/
#   ├── task_plan.md
#   ├── findings.md
#   └── progress.md

set -e

# Check arguments
if [ -z "$1" ]; then
  echo "Usage: bash init-planning.sh <task-slug>"
  echo "Example: bash init-planning.sh 'refactor-auth-module'"
  exit 1
fi

# Get script directory (works regardless of where script is called from)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(dirname "$SCRIPT_DIR")/templates"

# Validate templates exist
if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "Error: Templates directory not found at $TEMPLATES_DIR"
  exit 1
fi

# Generate planning directory name
DATE=$(date +%Y-%m-%d)
SLUG="$1"
PLAN_DIR=".planning/${DATE}-${SLUG}"

# Check if directory already exists
if [ -d "$PLAN_DIR" ]; then
  echo "Warning: Planning directory already exists: $PLAN_DIR"
  read -p "Overwrite? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
  fi
fi

# Create directory
mkdir -p "$PLAN_DIR"

# Copy templates
cp "$TEMPLATES_DIR/task_plan.md" "$PLAN_DIR/"
cp "$TEMPLATES_DIR/findings.md" "$PLAN_DIR/"
cp "$TEMPLATES_DIR/progress.md" "$PLAN_DIR/"

# Replace placeholders with task slug
TASK_NAME=$(echo "$SLUG" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

# Update task_plan.md
sed -i.bak "s/\[TASK_NAME\]/$TASK_NAME/g" "$PLAN_DIR/task_plan.md"
rm -f "$PLAN_DIR/task_plan.md.bak"

# Update findings.md
sed -i.bak "s/\[TASK_NAME\]/$TASK_NAME/g" "$PLAN_DIR/findings.md"
rm -f "$PLAN_DIR/findings.md.bak"

# Update progress.md
sed -i.bak "s/\[TASK_NAME\]/$TASK_NAME/g" "$PLAN_DIR/progress.md"
rm -f "$PLAN_DIR/progress.md.bak"

# Update timestamps
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
sed -i.bak "s/\[YYYY-MM-DD HH:MM\]/$TIMESTAMP/g" "$PLAN_DIR/task_plan.md"
sed -i.bak "s/\[YYYY-MM-DD HH:MM\]/$TIMESTAMP/g" "$PLAN_DIR/findings.md"
sed -i.bak "s/\[YYYY-MM-DD HH:MM\]/$TIMESTAMP/g" "$PLAN_DIR/progress.md"
rm -f "$PLAN_DIR/"*.bak

# Create .active_plan pointer
echo "$PLAN_DIR" > .planning/.active_plan

echo "✅ Planning directory initialized: $PLAN_DIR"
echo ""
echo "Files created:"
echo "  ├── task_plan.md   (phase tracking)"
echo "  ├── findings.md    (research storage)"
echo "  └── progress.md    (session logging)"
echo ""
echo "Active plan pointer: .planning/.active_plan → $PLAN_DIR"
echo ""
echo "Next steps:"
echo "  1. Edit task_plan.md to define your goal and phases"
echo "  2. Start working through phases"
echo "  3. Update findings.md and progress.md as you go"
