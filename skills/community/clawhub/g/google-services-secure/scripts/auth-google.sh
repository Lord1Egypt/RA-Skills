#!/bin/bash
# Google Services Secure - OAuth 2.0 Authentication Script
# This script handles OAuth 2.0 flow for Google services authentication

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID:-}"
GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET:-}"
GOOGLE_REDIRECT_URI="${GOOGLE_REDIRECT_URI:-http://localhost:8080/callback}"
AUDIT_LOG_DIR="/data/.openclaw/logs"
AUDIT_LOG="$AUDIT_LOG_DIR/google-services-audit.log"
TOKEN_FILE="$HOME/.google-oauth-token"

# OAuth scopes (can be customized)
SCOPES="https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/calendar.events.readonly"

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
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Log action to audit
log_action() {
    local action="$1"
    local status="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    
    local log_entry="{\"timestamp\":\"$timestamp\",\"service\":\"google-auth\",\"action\":\"$action\",\"status\":\"$status\"}"
    
    echo "$log_entry" >> "$AUDIT_LOG"
    
    # Redact client secret in logs
    sed -i "s/$GOOGLE_CLIENT_SECRET/REDACTED_SECRET/g" "$AUDIT_LOG"
}

# Validation functions
validate_environment() {
    print_header "Step 1: Validate Environment"

    if [ -z "$GOOGLE_CLIENT_ID" ]; then
        print_error "GOOGLE_CLIENT_ID not set"
        print_info "Set with: export GOOGLE_CLIENT_ID='your-client-id.apps.googleusercontent.com'"
        return 1
    fi

    if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
        print_error "GOOGLE_CLIENT_SECRET not set"
        print_info "Set with: export GOOGLE_CLIENT_SECRET='your-client-secret'"
        return 1
    fi

    print_success "Environment variables validated"
    echo ""
    
    return 0
}

# Generate OAuth 2.0 Authorization URL
generate_auth_url() {
    print_header "Step 2: Generate Authorization URL"
    
    # URL encode the redirect URI
    local encoded_redirect=$(echo -n "$GOOGLE_REDIRECT_URI" | od -An -tx1 | tr 'a-f\n' '0-:a-f' | tr '\n' '=' | tr -d ' ')
    
    local auth_url="https://accounts.google.com/o/oauth2/v2/auth?client_id=$GOOGLE_CLIENT_ID&redirect_uri=$GOOGLE_REDIRECT_URI&response_type=code&scope=$SCOPES&access_type=offline"
    
    echo ""
    print_info "Authorization URL:"
    print_success "$auth_url"
    echo ""
    
    # Copy to clipboard if possible
    if command -v xclip; then
        echo -n "$auth_url" | xclip -selection clipboard
        print_info "URL copied to clipboard"
    elif command -v pbcopy; then
        echo -n "$auth_url" | pbcopy
        print_info "URL copied to clipboard"
    fi
    
    # Log to audit
    log_action "GENERATE_AUTH_URL" "success"
    
    return 0
}

# Exchange authorization code for access token
exchange_code_for_token() {
    print_header "Step 3: Exchange Authorization Code"
    
    echo ""
    print_info "Paste the authorization code from browser:"
    read -p "Authorization Code: " auth_code
    
    if [ -z "$auth_code" ]; then
        print_error "Authorization code cannot be empty"
        log_action "EXCHANGE_CODE" "failed"
        return 1
    fi
    
    print_info "Exchanging code for access token..."
    
    # Make POST request to token endpoint
    local response=$(curl -s -X POST \
        "https://oauth2.googleapis.com/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "client_id=$GOOGLE_CLIENT_ID" \
        -d "client_secret=$GOOGLE_CLIENT_SECRET" \
        -d "code=$auth_code" \
        -d "redirect_uri=$GOOGLE_REDIRECT_URI" \
        -d "grant_type=authorization_code")
    
    # Parse response
    if echo "$response" | grep -q '"access_token"'; then
        local access_token=$(echo "$response" | grep -oP '"access_token":\s*"\K[^"]*' | head -1)
        local refresh_token=$(echo "$response" | grep -oP '"refresh_token":\s*"\K[^"]*' | head -1)
        local expires_in=$(echo "$response" | grep -oP '"expires_in":\s*\K[^,]*' | head -1)
        
        print_success "Access token received"
        print_info "Token expires in: ${expires_in}s (${expires_in} seconds)"
        
        # Save tokens securely
        echo "$response" > "$TOKEN_FILE"
        chmod 600 "$TOKEN_FILE"
        print_success "Tokens saved to: $TOKEN_FILE"
        
        # Log to audit (redact tokens)
        log_action "EXCHANGE_CODE" "success"
        
        # Export for current session
        export ACCESS_TOKEN="$access_token"
        export REFRESH_TOKEN="$refresh_token"
        
        echo ""
        print_info "Access token exported to environment for current session"
        print_info "Use: echo \$ACCESS_TOKEN"
        echo ""
        
        return 0
    else
        print_error "Failed to exchange code for token"
        print_error "Response: $response"
        log_action "EXCHANGE_CODE" "failed"
        return 1
    fi
}

# Refresh access token using refresh token
refresh_token_func() {
    print_header "Step 4: Refresh Access Token"
    
    if [ ! -f "$TOKEN_FILE" ]; then
        print_error "Token file not found: $TOKEN_FILE"
        print_info "Please run authentication first"
        return 1
    fi
    
    print_info "Refreshing access token..."
    
    # Read refresh token from file
    local refresh_token=$(grep -oP '"refresh_token":\s*"\K[^"]*' "$TOKEN_FILE" | head -1)
    
    if [ -z "$refresh_token" ]; then
        print_error "Refresh token not found"
        return 1
    fi
    
    # Make POST request to refresh
    local response=$(curl -s -X POST \
        "https://oauth2.googleapis.com/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "client_id=$GOOGLE_CLIENT_ID" \
        -d "client_secret=$GOOGLE_CLIENT_SECRET" \
        -d "refresh_token=$refresh_token" \
        -d "grant_type=refresh_token")
    
    # Parse response
    if echo "$response" | grep -q '"access_token"'; then
        local access_token=$(echo "$response" | grep -oP '"access_token":\s*"\K[^"]*' | head -1)
        local new_refresh_token=$(echo "$response" | grep -oP '"refresh_token":\s*"\K[^"]*' | head -1)
        local expires_in=$(echo "$response" | grep -oP '"expires_in":\s*\K[^,]*' | head -1)
        
        print_success "Access token refreshed"
        print_info "New token expires in: ${expires_in}s"
        
        # Update token file
        echo "$response" > "$TOKEN_FILE"
        chmod 600 "$TOKEN_FILE"
        
        # Log to audit
        log_action "REFRESH_TOKEN" "success"
        
        # Export for current session
        export ACCESS_TOKEN="$access_token"
        export REFRESH_TOKEN="$new_refresh_token"
        
        echo ""
        print_info "New access token exported to environment"
        print_info "Use: echo \$ACCESS_TOKEN"
        echo ""
        
        return 0
    else
        print_error "Failed to refresh token"
        print_error "Response: $response"
        log_action "REFRESH_TOKEN" "failed"
        return 1
    fi
}

# Revoke access token
revoke_token() {
    print_header "Step 5: Revoke Access Token"
    
    if [ ! -f "$TOKEN_FILE" ]; then
        print_error "Token file not found: $TOKEN_FILE"
        return 1
    fi
    
    print_info "Revoking access token..."
    
    # Read access token from file
    local access_token=$(grep -oP '"access_token":\s*"\K[^"]*' "$TOKEN_FILE" | head -1)
    
    if [ -z "$access_token" ]; then
        print_error "Access token not found"
        return 1
    fi
    
    # Revoke token
    local response=$(curl -s -X POST \
        "https://oauth2.googleapis.com/revoke" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "token=$access_token")
    
    # Google returns 200 on success
    if [ "$response" = "" ]; then
        print_success "Access token revoked successfully"
        
        # Remove token file
        rm -f "$TOKEN_FILE"
        print_success "Token file removed"
        
        # Log to audit
        log_action "REVOKE_TOKEN" "success"
        
        # Unset environment variables
        unset ACCESS_TOKEN
        unset REFRESH_TOKEN
        
        echo ""
        print_info "Tokens revoked and removed from environment"
        return 0
    else
        print_error "Failed to revoke token"
        log_action "REVOKE_TOKEN" "failed"
        return 1
    fi
}

# Main function
main() {
    local action="${1:-auth}"
    
    case "$action" in
        auth)
            validate_environment || return 1
            generate_auth_url || return 1
            exchange_code_for_token || return 1
            ;;
        refresh)
            refresh_token_func
            ;;
        revoke)
            revoke_token
            ;;
        status)
            print_header "OAuth Token Status"
            
            if [ -f "$TOKEN_FILE" ]; then
                print_success "Token file exists: $TOKEN_FILE"
                
                # Check if token is expired
                # This is a simplified check - in production you'd parse the expires_at field
                print_info "To check expiry, use the 'refresh' action"
            else
                print_warning "No active token found"
                print_info "Run './auth-google.sh auth' to authenticate"
            fi
            ;;
        help|--help|-h)
            echo "Google Services Secure - OAuth 2.0 Authentication"
            echo ""
            echo "Usage: $0 [action]"
            echo ""
            echo "Actions:"
            echo "  auth     - Authenticate with OAuth 2.0 (default)"
            echo "  refresh  - Refresh access token using refresh token"
            echo "  revoke   - Revoke and remove access token"
            echo "  status   - Show OAuth token status"
            echo "  help     - Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  GOOGLE_CLIENT_ID       - OAuth 2.0 client ID"
            echo "  GOOGLE_CLIENT_SECRET   - OAuth 2.0 client secret"
            echo "  GOOGLE_REDIRECT_URI    - OAuth 2.0 redirect URI"
            echo ""
            echo "Example:"
            echo "  export GOOGLE_CLIENT_ID='your-client-id.apps.googleusercontent.com'"
            echo "  export GOOGLE_CLIENT_SECRET='your-client-secret'"
            echo "  ./auth-google.sh auth"
            ;;
        *)
            print_error "Unknown action: $action"
            echo ""
            echo "Run '$0 help' for usage information"
            return 1
            ;;
    esac
}

# Run main function
main "$@"
