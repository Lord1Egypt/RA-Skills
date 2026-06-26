#!/bin/bash
# validate_skill.sh - Validate the NVS skill structure and content

echo "=== NVS Skill Validation ==="

SKILL_DIR=".lingma/skills/nvs-node-version-switcher"
ERRORS=0

# Check if skill directory exists
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Skill directory not found: $SKILL_DIR"
    exit 1
fi

echo "✓ Skill directory exists"

# Check required files
REQUIRED_FILES=("SKILL.md" "REFERENCE.md" "EXAMPLES.md" "README.md")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✓ $file exists"
    else
        echo "❌ Missing required file: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check scripts directory
if [ -d "$SKILL_DIR/scripts" ]; then
    echo "✓ Scripts directory exists"
    
    # Check script files
    SCRIPTS=("check_nvs_status.sh" "install_nvs.sh")
    for script in "${SCRIPTS[@]}"; do
        if [ -f "$SKILL_DIR/scripts/$script" ]; then
            echo "✓ Script $script exists"
        else
            echo "❌ Missing script: $script"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo "❌ Scripts directory missing"
    ERRORS=$((ERRORS + 1))
fi

# Check SKILL.md frontmatter
if grep -q "^---$" "$SKILL_DIR/SKILL.md" && \
   grep -q "^name:" "$SKILL_DIR/SKILL.md" && \
   grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
    echo "✓ SKILL.md has proper frontmatter"
else
    echo "❌ SKILL.md missing proper frontmatter"
    ERRORS=$((ERRORS + 1))
fi

# Check SKILL.md line count
LINE_COUNT=$(wc -l < "$SKILL_DIR/SKILL.md")
if [ "$LINE_COUNT" -le 500 ]; then
    echo "✓ SKILL.md is concise ($LINE_COUNT lines)"
else
    echo "⚠️  SKILL.md is too long ($LINE_COUNT lines, should be ≤500)"
fi

# Check description quality
DESCRIPTION=$(grep "^description:" "$SKILL_DIR/SKILL.md" | sed 's/^description: //')
if [ ${#DESCRIPTION} -gt 50 ] && [ ${#DESCRIPTION} -lt 1024 ]; then
    echo "✓ Description length is appropriate (${#DESCRIPTION} chars)"
else
    echo "⚠️  Description length may need adjustment (${#DESCRIPTION} chars)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 All validations passed! NVS skill is ready to use."
else
    echo "❌ Found $ERRORS issues. Please fix them before using the skill."
fi

exit $ERRORS
