#!/bin/bash
set -e

echo "Running static analysis for legacy backgrounding commands..."

FILES=(
    "projects/docs/TEMPLATES/AgentSkill_Archetype/SKILL.md.template"
    "SKILL.md"
    "skills/pm-skill/SKILL.md"
    "skills/issue_tracker/SKILL.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "nohup" "$file"; then
            echo "❌ Error: nohup found in $file"
            exit 1
        fi
        if grep -q "&[[:space:]]*$" "$file"; then
            echo "❌ Error: & found in $file"
            exit 1
        fi
        echo "✅ $file is clean."
    fi
done

echo "✅ All tests pass."
