#!/bin/bash
# Google Services Secure - Setup Validation Script
# This script validates Google API configuration and OAuth setup before allowing skill usage

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GOOGLE_API_KEY="${GOOGLE_API_KEY:-}"
GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID:-}"
GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET:-}"
GOOGLE_REDIRECT_URI="${GOOGLE_REDIRECT_URI:-http://localhost:8080/callback}"
GOOGLE_PERMISSION_MODE="${GOOGLE_PERMISSION_MODE:-readonly}"
AUDIT_LOG_DIR="/data/.openclaw/logs"
AUDIT_LOG="$AUDIT_LOG_DIR/google-services-audit.log"

# Error tracking
ERRORS=0
WARNINGS=0

# Print functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Validation functions
validate_environment_variables() {
    print_header "Step 1: Environment Variables"

    # Check GOOGLE_API_KEY
    if [ -z "$GOOGLE_API_KEY" ]; then
        print_error "GOOGLE_API_KEY environment variable is not set"
        print_info "Set it with: export GOOGLE_API_KEY='your-api-key'"
    else
        print_success "GOOGLE_API_KEY is set"

        # Validate API key format
        if [[ ! "$GOOGLE_API_KEY" =~ ^AIza[A-Za-z0-9_-]{39}$ ]]; then
            print_error "GOOGLE_API_KEY must be a valid Google Cloud API key"
            print_info "Format: AIzaSyCd_... (39 characters)"
        else
            print_success "GOOGLE_API_KEY format is valid"
        fi
    fi

    # Check GOOGLE_CLIENT_ID
    if [ -z "$GOOGLE_CLIENT_ID" ]; then
        print_error "GOOGLE_CLIENT_ID environment variable is not set"
        print_info "Set it with: export GOOGLE_CLIENT_ID='your-client-id.apps.googleusercontent.com'"
    else
        print_success "GOOGLE_CLIENT_ID is set"

        # Validate client ID format
        if [[ ! "$GOOGLE_CLIENT_ID" =~ ^[a-z0-9-]+\.apps\.googleusercontent\.com$ ]]; then
            print_error "GOOGLE_CLIENT_ID must be a valid OAuth 2.0 client ID"
            print_info "Format: your-client-id.apps.googleusercontent.com"
        else
            print_success "GOOGLE_CLIENT_ID format is valid"
        fi
    fi

    # Check GOOGLE_CLIENT_SECRET
    if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
        print_error "GOOGLE_CLIENT_SECRET environment variable is not set"
        print_info "Set it with: export GOOGLE_CLIENT_SECRET='your-client-secret'"
    else
        print_success "GOOGLE_CLIENT_SECRET is set"

        # Check secret length (should be at least 16 chars)
        if [ ${#GOOGLE_CLIENT_SECRET} -lt 16 ]; then
            print_warning "GOOGLE_CLIENT_SECRET seems too short (less than 16 characters)"
        else
            print_success "GOOGLE_CLIENT_SECRET length is reasonable"
        fi
    fi

    echo ""
}

validate_oauth_setup() {
    print_header "Step 2: OAuth 2.0 Setup"

    # Check redirect URI
    if [[ ! "$GOOGLE_REDIRECT_URI" =~ ^https?://[a-z0-9.-]+(:[0-9]+)?/callback$ ]]; then
        print_error "GOOGLE_REDIRECT_URI must be a valid callback URL"
        print_info "Format: http://localhost:8080/callback"
    else
        print_success "GOOGLE_REDIRECT_URI format is valid"
    fi

    echo ""
}

validate_permission_mode() {
    print_header "Step 3: Permission Mode"

    case "$GOOGLE_PERMISSION_MODE" in
        readonly)
            print_success "Permission mode: readonly (SAFE)"
            print_info "This mode allows: read operations only (list, get, view)"
            ;;
        restricted)
            print_success "Permission mode: restricted (MODERATE)"
            print_info "This mode allows: read + limited write operations"
            print_warning "Write operations require 2-factor confirmation"
            ;;
        full)
            print_warning "Permission mode: full (HIGH RISK)"
            print_warning "All operations allowed (with confirmation)"
            print_warning "Recommended only for isolated environments"
            ;;
        *)
            print_error "Invalid permission mode: $GOOGLE_PERMISSION_MODE"
            print_info "Valid modes: readonly, restricted, full"
            print_info "Set with: export GOOGLE_PERMISSION_MODE='readonly'"
            ;;
    esac

    echo ""
}

validate_audit_setup() {
    print_header "Step 4: Audit Logging"

    # Check if log directory exists
    if [ ! -d "$AUDIT_LOG_DIR" ]; then
        print_warning "Audit log directory does not exist: $AUDIT_LOG_DIR"
        print_info "Creating directory..."
        mkdir -p "$AUDIT_LOG_DIR"
        chmod 700 "$AUDIT_LOG_DIR"
        print_success "Created audit log directory"
    else
        print_success "Audit log directory exists"

        # Check permissions
        perms=$(stat -c %a "$AUDIT_LOG_DIR" 2>/dev/null || stat -f %A "$AUDIT_LOG_DIR")
        if [ "$perms" = "700" ]; then
            print_success "Audit log directory has secure permissions (700)"
        else
            print_warning "Audit log directory permissions: $perms (recommended: 700)"
            print_info "Fix with: chmod 700 $AUDIT_LOG_DIR"
        fi
    fi

    # Check if log file exists
    if [ -f "$AUDIT_LOG" ]; then
        print_success "Audit log file exists"

        # Check log file size
        size=$(stat -c%s "$AUDIT_LOG" 2>/dev/null || stat -f%z "$AUDIT_LOG")
        if [ "$size" -gt 10485760 ]; then
            print_warning "Audit log file is larger than 10MB"
            print_info "Consider rotating logs"
        else
            print_success "Audit log file size is reasonable"
        fi

        # Check permissions
        perms=$(stat -c %a "$AUDIT_LOG" 2>/dev/null || stat -f %A "$AUDIT_LOG")
        if [ "$perms" = "600" ]; then
            print_success "Audit log file has secure permissions (600)"
        else
            print_warning "Audit log file permissions: $perms (recommended: 600)"
            print_info "Fix with: chmod 600 $AUDIT_LOG"
        fi
    else
        print_warning "Audit log file does not exist: $AUDIT_LOG"
        print_info "Creating file..."
        touch "$AUDIT_LOG"
        chmod 600 "$AUDIT_LOG"
        print_success "Created audit log file"
    fi

    echo ""
}

test_google_api_connectivity() {
    print_header "Step 5: Google API Connectivity Test"

    if [ -z "$GOOGLE_API_KEY" ]; then
        print_warning "Skipping API test (credentials not set)"
        echo ""
        return
    fi

    print_info "Testing Google API connectivity..."

    # Test with a simple API call
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        "https://www.googleapis.com/oauth2/v3/tokeninfo" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "access_token=mock_token" 2>/dev/null || echo "000")

    case "$response" in
        200|400)
            print_success "Google API endpoint accessible (HTTP $response)"
            ;;
        403)
            print_error "Forbidden (HTTP 403)"
            print_info "Check API key validity"
            ;;
        401)
            print_error "Unauthorized (HTTP 401)"
            print_info "Check API key and OAuth credentials"
            ;;
        000)
            print_error "Connection failed (no response)"
            print_info "Check network connectivity"
            ;;
        *)
            print_warning "Unexpected response (HTTP $response)"
            print_info "Check Google Cloud Console settings"
            ;;
    esac

    echo ""
}

check_security_issues() {
    print_header "Step 6: Security Check"

    # Check for credentials in config files
    print_info "Checking for credentials in OpenClaw config..."
    config_file="$HOME/.openclaw/openclaw.json"

    if [ -f "$config_file" ]; then
        if grep -q "GOOGLE_CLIENT_SECRET" "$config_file"; then
            print_error "CRITICAL: GOOGLE_CLIENT_SECRET found in $config_file"
            print_error "Credentials should NEVER be stored in config files!"
            print_info "Remove from config and use environment variables"
        elif grep -q "GOOGLE_API_KEY" "$config_file"; then
            print_error "CRITICAL: GOOGLE_API_KEY found in $config_file"
            print_error "API keys should be stored in environment variables only!"
            print_info "Remove from config and use environment variables"
        else
            print_success "No credentials found in config file"
        fi

        if grep -q '"GOOGLE_"' "$config_file"; then
            print_warning "Google environment variables found in config file"
            print_info "Consider using environment variables instead"
        else
            print_success "No Google variables in config file"
        fi
    else
        print_warning "OpenClaw config file not found: $config_file"
    fi

    echo ""

    # Check for common security issues
    print_info "Checking for common security issues..."

    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root (not recommended)"
        print_info "Consider running as non-root user"
    else
        print_success "Not running as root"
    fi

    # Check for insecure file permissions
    if [ -f "$config_file" ]; then
        perms=$(stat -c %a "$config_file" 2>/dev/null || stat -f %A "$config_file")
        if [ "$perms" != "600" ]; then
            print_warning "Config file permissions: $perms (recommended: 600)"
            print_info "Fix with: chmod 600 $config_file"
        else
            print_success "Config file has secure permissions (600)"
        fi
    fi

    echo ""
}

generate_report() {
    print_header "Validation Report"

    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
        echo ""
        echo "Your Google Services Secure setup is ready to use!"
        echo ""
        echo "Environment:"
        echo "  GOOGLE_API_KEY: ${GOOGLE_API_KEY:+[*** set ***]}"
        echo "  GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID:+[*** set ***]}"
        echo "  GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET:+[*** set ***]}"
        echo "  GOOGLE_REDIRECT_URI: $GOOGLE_REDIRECT_URI"
        echo "  GOOGLE_PERMISSION_MODE: $GOOGLE_PERMISSION_MODE"
        echo ""
        echo "Audit log: $AUDIT_LOG"
        echo ""
        echo "Next step: Run OAuth authentication"
        echo "  ./scripts/auth-google.sh"
        echo ""
        return 0
    elif [ $ERRORS -eq 0 ]; then
        echo -e "${YELLOW}⚠ WARNINGS FOUND ($WARNINGS)${NC}"
        echo ""
        echo "Setup is usable but has warnings. Review above."
        echo ""
        echo "Recommendations:"
        echo "  1. Review warnings and apply fixes"
        echo "  2. Re-run validation script"
        echo "  3. Enable stricter security if needed"
        echo ""
        return 0
    else
        echo -e "${RED}✗ CRITICAL ISSUES FOUND ($ERRORS)${NC}"
        echo ""
        echo "Setup has security issues. Fix before using:"
        echo ""
        echo "Required actions:"
        echo "  1. Set environment variables: GOOGLE_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET"
        echo "  2. Remove credentials from config files"
        echo "  3. Fix OAuth 2.0 setup"
        echo "  4. Re-run validation script"
        echo ""
        return 1
    fi
}

# Main execution
main() {
    echo ""
    print_header "Google Services Secure - Setup Validation"
    echo ""

    validate_environment_variables
    validate_oauth_setup
    validate_permission_mode
    validate_audit_setup
    test_google_api_connectivity
    check_security_issues

    generate_report
}

# Run main function
main "$@"
