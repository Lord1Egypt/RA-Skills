#!/bin/bash
# Pre-flight check for Nebius CLI
# Verifies installation, authentication, and project configuration
# Supports both interactive and non-interactive (CI/CD) environments

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

echo "=== Nebius CLI Pre-flight Check ==="
echo ""

# Detect environment
if [ -t 0 ] && [ -t 1 ]; then
    INTERACTIVE=true
else
    INTERACTIVE=false
    echo -e "${YELLOW}[INFO]${NC} Non-interactive environment detected"
    echo ""
fi

# 1. Check CLI installed
if command -v nebius &> /dev/null; then
    VERSION=$(nebius version 2>/dev/null || echo "unknown")
    echo -e "${GREEN}[OK]${NC} nebius CLI installed (${VERSION})"
else
    echo -e "${RED}[FAIL]${NC} nebius CLI not found"
    echo "  Install with: curl -sSL https://storage.eu-north1.nebius.cloud/cli/install.sh | bash"
    echo "  Then run: exec -l \$SHELL"
    ERRORS=$((ERRORS + 1))
fi

# 2. Check config file exists
if [ -f "$HOME/.nebius/config.yaml" ]; then
    echo -e "${GREEN}[OK]${NC} Config file exists (~/.nebius/config.yaml)"
else
    echo -e "${YELLOW}[WARN]${NC} No config file found (~/.nebius/config.yaml)"
    if [ "$INTERACTIVE" = true ]; then
        echo "  Run: nebius profile create"
    else
        echo "  Create config manually:"
        echo "    mkdir -p ~/.nebius"
        echo "    Write config.yaml with profile, endpoint, and parent-id"
        echo "  See: https://docs.nebius.com/cli/configure"
    fi
    WARNINGS=$((WARNINGS + 1))
fi

# 3. Check authentication
if command -v nebius &> /dev/null; then
    if nebius iam whoami --format json &> /dev/null; then
        USER_NAME=$(nebius iam whoami --format json 2>/dev/null | jq -r '.user_profile.attributes.name // "unknown"' 2>/dev/null || echo "authenticated")
        echo -e "${GREEN}[OK]${NC} Authenticated as: ${USER_NAME}"
    else
        echo -e "${RED}[FAIL]${NC} Not authenticated"
        if [ "$INTERACTIVE" = true ]; then
            echo "  Run: nebius profile create  (interactive setup)"
            echo "  Or:  nebius profile create   (re-authenticate)"
        else
            echo "  For CI/CD, use service account auth:"
            echo "    1. Create service account: nebius iam service-account create"
            echo "    2. Generate key: nebius iam auth-public-key generate"
            echo "    3. Configure profile with service account credentials"
            echo "  See: https://docs.nebius.com/cli/configure"
        fi
        ERRORS=$((ERRORS + 1))
    fi
fi

# 4. Check profile
if command -v nebius &> /dev/null; then
    PROFILE=$(nebius config get profile 2>/dev/null || echo "")
    if [ -n "$PROFILE" ]; then
        echo -e "${GREEN}[OK]${NC} Active profile: ${PROFILE}"
    else
        echo -e "${YELLOW}[WARN]${NC} No active profile configured"
        echo "  Run: nebius profile create"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 5. Check project ID
if command -v nebius &> /dev/null; then
    PARENT_ID=$(nebius config get parent-id 2>/dev/null || echo "")
    if [ -n "$PARENT_ID" ]; then
        echo -e "${GREEN}[OK]${NC} Project ID: ${PARENT_ID}"
    else
        echo -e "${YELLOW}[WARN]${NC} No parent-id (project) configured"
        echo "  Run: nebius config set parent-id <PROJECT_ID>"
        echo "  Find your project ID:"
        echo "    nebius iam project list --format json | jq -r '.items[].metadata.id'"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 6. Quick connectivity test (only if authenticated)
if command -v nebius &> /dev/null && [ $ERRORS -eq 0 ]; then
    if nebius ai endpoint list --format json &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} API connectivity verified"
    else
        echo -e "${YELLOW}[WARN]${NC} Could not reach Nebius API (may be a permissions issue)"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 7. Check optional tools
echo ""
echo "--- Optional Tools ---"
for tool in docker kubectl helm jq; do
    if command -v "$tool" &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} ${tool} installed"
    else
        echo -e "${YELLOW}[SKIP]${NC} ${tool} not found (optional)"
    fi
done

# Summary
echo ""
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}Pre-flight check failed with ${ERRORS} error(s) and ${WARNINGS} warning(s)${NC}"
    echo ""
    echo "Documentation: https://docs.nebius.com/cli/configure"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Pre-flight check passed with ${WARNINGS} warning(s)${NC}"
    exit 0
else
    echo -e "${GREEN}Pre-flight check passed${NC}"
    exit 0
fi
