#!/usr/bin/env bash
# Helper functions for reading agent configuration
# DEPRECATED: Use secure-creds.sh instead for credential handling

# Get script directory
SCRIPT_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source secure credential handling
source "${SCRIPT_LIB_DIR}/secure-creds.sh"

get_default_provider() {
    local config_file="${1:-.agent-config.json}"
    
    if [ ! -f "$config_file" ]; then
        echo "easydns"  # Fallback default
        return
    fi
    
    python3 -c "import json; print(json.load(open('$config_file'))['default_provider'])" 2>/dev/null || echo "easydns"
}

get_credentials_path() {
    local config_file="${1:-.agent-config.json}"
    
    # Use secure-creds.sh function
    local skill_dir="$(cd "$(dirname "$config_file")" && pwd)"
    get_credentials_dir "$skill_dir"
}

load_provider_credentials() {
    local provider="$1"
    local config_file="${2:-.agent-config.json}"
    
    # Use secure credential loading from secure-creds.sh
    local skill_dir="$(cd "$(dirname "$config_file")" && pwd)"
    load_provider_credentials_to_env "$provider" "$skill_dir"
}
