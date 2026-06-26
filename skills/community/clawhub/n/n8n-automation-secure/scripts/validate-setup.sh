#!/bin/bash
# N8N Automation Secure - Setup Validation Script
# This script validates the security configuration before allowing skill usage

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
N8N_URL="${N8N_URL:-}"
N8N_API_KEY="${N8N_API_KEY:-}"
N8N_PERMISSION_MODE="${N8N_PERMISSION_MODE:-readonly}"
AUDIT_LOG_DIR="/data/.openclaw/logs"
AUDIT_LOG="$AUDIT_LOG_DIR/n8n-audit.log"

# Error tracking
ERRORS=0
WARNINGS=0

# Print functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
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

    # Check N8N_URL
    if [ -z "$N8N_URL" ]; then
        print_error "N8N_URL environment variable is not set"
        print_info "Set it with: export N8N_URL='https://your-n8n-instance.com'"
    else
        print_success "N8N_URL is set"

        # Validate URL format
        if [[ ! "$N8N_URL" =~ ^https://[a-z0-9.-]+(\.[a-z0-9.-]+)+$ ]]; then
            print_error "N8N_URL must be a valid HTTPS URL"
            print_info "Example: https://n8n.example.com"
        else
            print_success "N8N_URL format is valid (HTTPS)"
        fi

        # Check for credentials in URL
        if [[ "$N8N_URL" =~ @|:|key|token|secret ]]; then
            print_error "N8N_URL must not contain credentials or secret keywords"
        else
            print_success "N8N_URL does not contain credentials"
        fi
    fi

    # Check N8N_API_KEY
    if [ -z "$N8N_API_KEY" ]; then
        print_error "N8N_API_KEY environment variable is not set"
        print_info "Set it with: export N8N_API_KEY='your-api-key'"
    else
        print_success "N8N_API_KEY is set"

        # Check if API key looks reasonable
        if [ ${#N8N_API_KEY} -lt 16 ]; then
            print_warning "N8N_API_KEY seems too short (less than 16 characters)"
        else
            print_success "N8N_API_KEY length is reasonable"
        fi
    fi

    echo ""
}

validate_permission_mode() {
    print_header "Step 2: Permission Mode"

    case "$N8N_PERMISSION_MODE" in
        readonly)
            print_success "Permission mode: readonly (SAFE)"
            print_info "This mode allows: list, view, execute (with confirmation)"
            ;;
        restricted)
            print_success "Permission mode: restricted (MODERATE)"
            print_info "This mode allows: list, view, execute, create"
            print_warning "Update/delete operations require 2-factor confirmation"
            ;;
        full)
            print_warning "Permission mode: full (HIGH RISK)"
            print_warning "All operations allowed (with confirmation)"
            print_warning "Recommended only for isolated environments"
            ;;
        *)
            print_error "Invalid permission mode: $N8N_PERMISSION_MODE"
            print_info "Valid modes: readonly, restricted, full"
            print_info "Set with: export N8N_PERMISSION_MODE='readonly'"
            ;;
    esac

    echo ""
}

validate_audit_setup() {
    print_header "Step 3: Audit Logging"

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

test_api_connectivity() {
    print_header "Step 4: API Connectivity Test"

    if [ -z "$N8N_URL" ] || [ -z "$N8N_API_KEY" ]; then
        print_warning "Skipping API test (credentials not set)"
        echo ""
        return
    fi

    print_info "Testing connection to $N8N_URL..."

    # Test with curl
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        "$N8N_URL/api/v1/workflows" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" 2>/dev/null || echo "000")

    case "$response" in
        200)
            print_success "API connection successful (HTTP 200)"
            ;;
        401)
            print_error "Authentication failed (HTTP 401)"
            print_info "Check N8N_API_KEY validity"
            ;;
        403)
            print_error "Forbidden (HTTP 403)"
            print_info "Check API key permissions"
            ;;
        404)
            print_warning "Not found (HTTP 404)"
            print_info "API endpoint may be incorrect"
            ;;
        000)
            print_error "Connection failed (no response)"
            print_info "Check N8N_URL and network connectivity"
            ;;
        *)
            print_warning "Unexpected response (HTTP $response)"
            print_info "Check n8n instance status"
            ;;
    esac

    echo ""
}

check_security_issues() {
    print_header "Step 5: Security Check"

    # Check for credentials in config files
    print_info "Checking for credentials in OpenClaw config..."
    config_file="$HOME/.openclaw/openclaw.json"

    if [ -f "$config_file" ]; then
        if grep -q "N8N_API_KEY" "$config_file"; then
            print_error "CRITICAL: N8N_API_KEY found in $config_file"
            print_error "Credentials should NEVER be stored in config files!"
            print_info "Remove from config and use environment variables"
        else
            print_success "No credentials found in config file"
        fi

        if grep -q '"N8N_URL"' "$config_file"; then
            print_warning "N8N_URL found in config file"
            print_info "Consider using environment variables instead"
        else
            print_success "No N8N_URL in config file"
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
        echo "Your N8N Automation Secure setup is ready to use!"
        echo ""
        echo "Environment:"
        echo "  N8N_URL: ${N8N_URL:-[not set]}"
        echo "  N8N_API_KEY: ${N8N_API_KEY:+[*** set ***]}"
        echo "  N8N_PERMISSION_MODE: $N8N_PERMISSION_MODE"
        echo ""
        echo "Audit log: $AUDIT_LOG"
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
        echo "  1. Set environment variables: N8N_URL and N8N_API_KEY"
        echo "  2. Remove credentials from config files"
        echo "  3. Fix URL format (must be HTTPS)"
        echo "  4. Re-run validation script"
        echo ""
        return 1
    fi
}

# Main execution
main() {
    echo ""
    print_header "N8N Automation Secure - Setup Validation"
    echo ""

    validate_environment_variables
    validate_permission_mode
    validate_audit_setup
    test_api_connectivity
    check_security_issues

    generate_report
}

# Run main function
main "$@"
