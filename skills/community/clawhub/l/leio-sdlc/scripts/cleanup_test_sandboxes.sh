#!/bin/bash
set -e

# Target directory
TARGET_DIR="tests"

# Defensive check: Ensure we are operating from the project root and the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist."
    exit 1
fi

echo "Cleaning up legacy test sandboxes..."

# Safely remove planner sandboxes
for dir in "$TARGET_DIR"/planner_sandbox_* "$TARGET_DIR"/manager_sandbox_*; do
    if [[ -d "$dir" ]]; then
        echo "Deleting legacy sandbox: $dir"
        # Attempt to git rm if tracked, otherwise rm -rf
        if git ls-files --error-unmatch "$dir" > /dev/null 2>&1; then
            git rm -r -q "$dir"
        else
            rm -rf "$dir"
        fi
    fi
done

echo "Cleanup complete."
exit 0
