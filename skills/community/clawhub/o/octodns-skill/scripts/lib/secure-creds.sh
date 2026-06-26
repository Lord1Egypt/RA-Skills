#!/usr/bin/env bash
# Secure credential handling for octoDNS skill

# Find credentials directory relative to skill root
get_credentials_dir() {
    local skill_dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
    local agent_config="${skill_dir}/.agent-config.json"
    
    # Try to read from agent config
    if [ -f "$agent_config" ]; then
        local creds_path=$(python3 -c "
import json, os, sys
try:
    config = json.load(open('$agent_config'))
    path = config.get('credentials_path', '../.credentials')
    # Resolve relative to agent_config location
    abs_path = os.path.abspath(os.path.join(os.path.dirname('$agent_config'), path))
    print(abs_path)
except:
    sys.exit(1)
" 2>/dev/null)
        
        if [ -n "$creds_path" ] && [ -d "$creds_path" ]; then
            echo "$creds_path"
            return 0
        fi
    fi
    
    # Fallback: look for .credentials in parent directory
    local parent_creds="${skill_dir}/../.credentials"
    if [ -d "$parent_creds" ]; then
        echo "$(cd "$parent_creds" && pwd)"
        return 0
    fi
    
    echo "Error: Cannot find credentials directory" >&2
    return 1
}

# Verify credential file has safe permissions
check_credential_file_permissions() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: Credential file not found: $file" >&2
        return 1
    fi
    
    # Check if file is readable by others or group
    if [ "$(uname)" = "Darwin" ]; then
        # macOS stat format
        local perms=$(stat -f "%Lp" "$file")
    else
        # Linux stat format  
        local perms=$(stat -c "%a" "$file")
    fi
    
    # Warn if permissions are too open (should be 600 or 400)
    if [ "$perms" != "600" ] && [ "$perms" != "400" ]; then
        echo "⚠️  Warning: $file has insecure permissions: $perms" >&2
        echo "   Recommended: chmod 600 $file" >&2
    fi
    
    return 0
}

# Load credentials into a temp file (safer than environment variables)
create_temp_creds_config() {
    local provider="$1"
    local creds_dir="$2"
    local creds_file="${creds_dir}/${provider}.json"
    
    if [ ! -f "$creds_file" ]; then
        echo "Error: Credentials file not found: $creds_file" >&2
        return 1
    fi
    
    # Check permissions
    check_credential_file_permissions "$creds_file"
    
    # Create secure temp file
    local temp_file=$(mktemp -t octodns-creds.XXXXXX)
    chmod 600 "$temp_file"
    
    # Copy credentials to temp file
    cp "$creds_file" "$temp_file"
    
    # Return temp file path
    echo "$temp_file"
    return 0
}

# Clean up temp credentials file
cleanup_temp_creds() {
    local temp_file="$1"
    
    if [ -f "$temp_file" ]; then
        # Securely wipe and remove
        if command -v shred &> /dev/null; then
            shred -u "$temp_file" 2>/dev/null
        else
            # macOS doesn't have shred, use multiple overwrite
            dd if=/dev/zero of="$temp_file" bs=1k count=1 conv=notrunc 2>/dev/null
            rm -f "$temp_file"
        fi
    fi
}

# Load credentials as environment variables (legacy support)
# Better: use octoDNS config file with credential file paths
load_provider_credentials_to_env() {
    local provider="$1"
    local skill_dir="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
    
    local creds_dir=$(get_credentials_dir "$skill_dir")
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    local creds_file="${creds_dir}/${provider}.json"
    
    if [ ! -f "$creds_file" ]; then
        echo "Error: Credentials file not found: $creds_file" >&2
        echo "Run: ./scripts/setup.sh" >&2
        return 1
    fi
    
    # Check permissions before loading
    check_credential_file_permissions "$creds_file"
    
    # Load credentials based on provider
    if [ "$provider" = "easydns" ]; then
        export EASYDNS_TOKEN=$(python3 -c "import json; print(json.load(open('$creds_file'))['api_token'])" 2>/dev/null)
        export EASYDNS_API_KEY=$(python3 -c "import json; print(json.load(open('$creds_file'))['api_key'])" 2>/dev/null)
        export EASYDNS_PORTFOLIO=$(python3 -c "import json; print(json.load(open('$creds_file')).get('portfolio', ''))" 2>/dev/null)
        
        if [ -z "$EASYDNS_TOKEN" ] || [ -z "$EASYDNS_API_KEY" ]; then
            echo "Error: Failed to load easyDNS credentials" >&2
            return 1
        fi
    elif [ "$provider" = "route53" ]; then
        export AWS_ACCESS_KEY_ID=$(python3 -c "import json; print(json.load(open('$creds_file'))['access_key_id'])" 2>/dev/null)
        export AWS_SECRET_ACCESS_KEY=$(python3 -c "import json; print(json.load(open('$creds_file'))['secret_access_key'])" 2>/dev/null)
    elif [ "$provider" = "cloudflare" ]; then
        export CLOUDFLARE_TOKEN=$(python3 -c "import json; print(json.load(open('$creds_file'))['token'])" 2>/dev/null)
    fi
    
    echo "✓ Loaded credentials for $provider (from $creds_dir)" >&2
    return 0
}

# Verify credentials file exists and has content
verify_credentials_file() {
    local provider="$1"
    local skill_dir="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
    
    local creds_dir=$(get_credentials_dir "$skill_dir")
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    local creds_file="${creds_dir}/${provider}.json"
    
    if [ ! -f "$creds_file" ]; then
        echo "❌ Credentials file not found: $creds_file" >&2
        return 1
    fi
    
    check_credential_file_permissions "$creds_file"
    
    # Verify JSON is valid
    if ! python3 -c "import json; json.load(open('$creds_file'))" 2>/dev/null; then
        echo "❌ Invalid JSON in credentials file: $creds_file" >&2
        return 1
    fi
    
    echo "✓ Credentials file verified: $creds_file" >&2
    return 0
}
