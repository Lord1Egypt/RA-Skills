#!/usr/bin/env bash
# Verify octoDNS skill security configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔒 octoDNS Skill Security Verification"
echo ""

# Source secure credentials library
source "${SCRIPT_DIR}/lib/secure-creds.sh"

# 1. Check if credentials directory exists
echo "1. Checking credentials directory..."
CREDS_DIR=$(get_credentials_dir "$SKILL_DIR" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✓ Credentials directory found: $CREDS_DIR${NC}"
else
    echo -e "${RED}   ✗ Credentials directory not found${NC}"
    exit 1
fi

# 2. Check if credentials directory is in .gitignore
echo "2. Checking .gitignore protection..."
PARENT_DIR="$(dirname "$SKILL_DIR")"
if grep -q "\.credentials" "${PARENT_DIR}/.gitignore" 2>/dev/null; then
    echo -e "${GREEN}   ✓ .credentials is in .gitignore${NC}"
else
    echo -e "${YELLOW}   ⚠ .credentials not found in .gitignore${NC}"
    echo "     Add this line to ${PARENT_DIR}/.gitignore:"
    echo "     .credentials/"
fi

# 3. Check credentials directory permissions
echo "3. Checking directory permissions..."
if [ "$(uname)" = "Darwin" ]; then
    DIR_PERMS=$(stat -f "%Lp" "$CREDS_DIR")
else
    DIR_PERMS=$(stat -c "%a" "$CREDS_DIR")
fi

if [ "$DIR_PERMS" = "700" ] || [ "$DIR_PERMS" = "755" ]; then
    echo -e "${GREEN}   ✓ Directory permissions OK: $DIR_PERMS${NC}"
else
    echo -e "${YELLOW}   ⚠ Directory permissions: $DIR_PERMS (recommended: 700)${NC}"
fi

# 4. Check each credential file
echo "4. Checking credential files..."
FOUND_FILES=0
for creds_file in "$CREDS_DIR"/*.json; do
    if [ -f "$creds_file" ]; then
        FOUND_FILES=$((FOUND_FILES + 1))
        filename=$(basename "$creds_file")
        
        # Check permissions
        if [ "$(uname)" = "Darwin" ]; then
            FILE_PERMS=$(stat -f "%Lp" "$creds_file")
        else
            FILE_PERMS=$(stat -c "%a" "$creds_file")
        fi
        
        if [ "$FILE_PERMS" = "600" ] || [ "$FILE_PERMS" = "400" ]; then
            echo -e "${GREEN}   ✓ $filename (permissions: $FILE_PERMS)${NC}"
        else
            echo -e "${RED}   ✗ $filename (insecure permissions: $FILE_PERMS)${NC}"
            echo "     Fix with: chmod 600 $creds_file"
        fi
        
        # Check if valid JSON
        if python3 -c "import json; json.load(open('$creds_file'))" 2>/dev/null; then
            echo "     ✓ Valid JSON"
        else
            echo -e "${RED}     ✗ Invalid JSON${NC}"
        fi
    fi
done

if [ $FOUND_FILES -eq 0 ]; then
    echo -e "${YELLOW}   ⚠ No credential files found${NC}"
fi

# 5. Check if environment variables are exposed
echo "5. Checking for exposed credentials..."
if env | grep -E "(EASYDNS_TOKEN|EASYDNS_API_KEY|AWS_SECRET|CLOUDFLARE_TOKEN)" > /dev/null 2>&1; then
    echo -e "${YELLOW}   ⚠ Credentials found in environment variables${NC}"
    echo "     This is expected if a script just ran."
    echo "     Verify they're cleared after script completion."
else
    echo -e "${GREEN}   ✓ No credentials in environment variables${NC}"
fi

# 6. Check .agent-config.json
echo "6. Checking .agent-config.json..."
if [ -f "${SKILL_DIR}/.agent-config.json" ]; then
    if grep -q "credentials_path" "${SKILL_DIR}/.agent-config.json"; then
        echo -e "${GREEN}   ✓ credentials_path is configured${NC}"
    else
        echo -e "${YELLOW}   ⚠ credentials_path not found in config${NC}"
    fi
    
    # Check if it's in .gitignore
    if grep -q "^\.agent-config\.json$" "${SKILL_DIR}/.gitignore" 2>/dev/null; then
        echo -e "${GREEN}   ✓ .agent-config.json is in .gitignore${NC}"
    else
        echo -e "${YELLOW}   ⚠ .agent-config.json not in .gitignore${NC}"
    fi
else
    echo -e "${YELLOW}   ⚠ .agent-config.json not found${NC}"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Security Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Recommendations:"
echo "  • Keep credentials directory at 700 permissions"
echo "  • Keep credential files at 600 permissions"
echo "  • Never commit .credentials/ directory to git"
echo "  • Regularly rotate API tokens"
echo "  • Use environment-specific credentials (dev/prod)"
echo ""
echo "For more info, see: SAFETY.md"
echo ""
