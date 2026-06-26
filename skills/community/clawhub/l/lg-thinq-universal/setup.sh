#!/bin/bash
# LG ThinQ Universal - Setup Script
# Automated setup for device discovery and skill generation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
VENV_DIR="${PROJECT_ROOT}/venv"
REQUIREMENTS_FILE="${PROJECT_ROOT}/requirements.txt"
ENV_FILE="${PROJECT_ROOT}/.env"
SKILL_DIR="${PROJECT_ROOT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies
install_deps() {
    log_info "Preparing Python environment..."
    
    if [ -d "$VENV_DIR" ]; then
        log_warn "Virtual environment already exists at $VENV_DIR. Skipping creation."
    else
        python3 -m venv "$VENV_DIR"
        log_info "Created new virtual environment."
    fi
    
    log_info "Synchronizing dependencies..."
    "$VENV_DIR/bin/pip" install -q -r "$REQUIREMENTS_FILE"
    log_info "Dependencies are up to date."
}

# Check environment variables
check_env() {
    log_info "Validating configuration..."
    
    source "$VENV_DIR/bin/activate"
    
    CONFIG_OUTPUT=$(python3 "$SCRIPT_DIR/scripts/lg_api_tool.py" check-config 2>/dev/null || echo "")
    echo "$CONFIG_OUTPUT"
    
    if echo "$CONFIG_OUTPUT" | grep -q "❌"; then
        log_error "Configuration incomplete."
        log_info "Please ensure LG_PAT and LG_COUNTRY are exported in your shell or set in .env."
        echo ""
        echo "Example:"
        echo "export LG_PAT=your_token"
        echo "export LG_COUNTRY=IN"
        exit 1
    fi
    
    log_info "Configuration validated successfully."
}

# Resolve API route
save_api_route() {
    log_info "Resolving API route..."
    
    CACHE_FILE="${PROJECT_ROOT}/.api_server_cache"
    
    # Check if cache exists and is not empty
    if [ -f "$CACHE_FILE" ] && [ -s "$CACHE_FILE" ]; then
        API_SERVER=$(cat "$CACHE_FILE")
        log_info "Using cached API route: $API_SERVER"
    else
        log_info "No valid cache found. Discovering regional API server..."
        source "$VENV_DIR/bin/activate"
        ROUTE_OUTPUT=$(python3 "$SCRIPT_DIR/scripts/lg_api_tool.py" save-route 2>/dev/null)
        
        if echo "$ROUTE_OUTPUT" | grep -q '"success": true'; then
            API_SERVER=$(echo "$ROUTE_OUTPUT" | python3 -c "import sys, json; print(json.load(sys.stdin)['apiServer'])")
            log_info "API route discovered and cached: $API_SERVER"
        else
            log_error "Failed to resolve API route."
            echo "$ROUTE_OUTPUT"
            exit 1
        fi
    fi
}

# Fetch and save device profiles
fetch_profiles() {
    log_info "Fetching device list..."
    
    source "$VENV_DIR/bin/activate"
    
    DEVICES_OUTPUT=$(python3 "$SCRIPT_DIR/scripts/lg_api_tool.py" list-devices 2>/dev/null)
    
    if echo "$DEVICES_OUTPUT" | grep -q '"success": false'; then
        log_error "Failed to fetch devices"
        echo "$DEVICES_OUTPUT"
        exit 1
    fi
    
    # Parse device details into a pipe-separated list: ID|NAME|TYPE
    DEVICE_DETAILS=$(echo "$DEVICES_OUTPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
devices = data.get('response', [])
if not isinstance(devices, list): devices = []
for d in devices:
    d_id = d.get('deviceId', '')
    info = d.get('deviceInfo', {})
    name = info.get('alias', 'Unknown')
    type_name = info.get('modelName', 'Unknown')
    print(f'{d_id}|{name}|{type_name}')
" 2>/dev/null || true)
    
    if [ -z "$DEVICE_DETAILS" ]; then
        log_warn "No devices found"
        return
    fi
    
    log_info "Found devices, fetching profiles..."
    
    PROFILES_DIR="${SKILL_DIR}/profiles"
    mkdir -p "$PROFILES_DIR"
    
    declare -A DEVICE_INFO
    
    # Loop through the pipe-separated details
    while IFS='|' read -r DEVICE_ID DEVICE_NAME DEVICE_TYPE; do
        if [ -z "$DEVICE_ID" ]; then continue; fi
        
        PROFILE_FILE="${PROFILES_DIR}/device_${DEVICE_ID}.json"
        
        log_info "Fetching profile for: $DEVICE_NAME ($DEVICE_ID)"
        PROFILE_OUTPUT=$(python3 "$SCRIPT_DIR/scripts/lg_api_tool.py" get-profile "$DEVICE_ID" 2>/dev/null)
        
        # Check if the output is valid JSON and contains profile data
        if echo "$PROFILE_OUTPUT" | grep -q '"property"'; then
            echo "$PROFILE_OUTPUT" > "$PROFILE_FILE"
            log_info "  Saved to: $PROFILE_FILE"
            DEVICE_INFO["$DEVICE_ID"]="$DEVICE_NAME|$DEVICE_TYPE|$PROFILE_FILE"
        else
            log_warn "  Failed to fetch profile for: $DEVICE_ID"
        fi
    done <<< "$DEVICE_DETAILS"
    
    # Output summary JSON
    echo ""
    echo "========================================"
    log_info "Setup Complete - Discovered Appliances"
    echo "========================================"
    echo ""
    echo "The following device profiles have been saved to $PROFILES_DIR:"
    echo ""
    echo "{"
    echo "  \"success\": true,"
    echo "  \"apiServer\": \"$API_SERVER\","
    echo "  \"devices\": ["
    
    # Create master device database
    echo "[" > "${PROFILES_DIR}/devices.json"
    
    FIRST=true
    # Re-loop through details to maintain order and match with DEVICE_INFO
    while IFS='|' read -r DEVICE_ID NAME TYPE; do
        if [ -z "$DEVICE_ID" ]; then continue; fi
        
        INFO="${DEVICE_INFO[$DEVICE_ID]}"
        if [ -n "$INFO" ]; then
            IFS='|' read -r STORED_NAME STORED_TYPE PROFILE_PATH <<< "$INFO"
            
            # Add comma for valid JSON array
            if [ "$FIRST" = true ]; then
                FIRST=false
            else
                echo "    ," >> "${PROFILES_DIR}/devices.json"
                echo "    ,"
            fi
            
            # Write to master DB
            echo "    {" >> "${PROFILES_DIR}/devices.json"
            echo "      \"id\": \"$DEVICE_ID\"," >> "${PROFILES_DIR}/devices.json"
            echo "      \"name\": \"$STORED_NAME\"," >> "${PROFILES_DIR}/devices.json"
            echo "      \"model\": \"$STORED_TYPE\"," >> "${PROFILES_DIR}/devices.json"
            echo "      \"profile\": \"$PROFILE_PATH\"" >> "${PROFILES_DIR}/devices.json"
            echo "    }" >> "${PROFILES_DIR}/devices.json"
            
            # Write to console output
            echo "    {"
            echo "      \"name\": \"$STORED_NAME\","
            echo "      \"model\": \"$STORED_TYPE\","
            echo "      \"id\": \"$DEVICE_ID\","
            echo "      \"profile\": \"$PROFILE_PATH\""
            echo -n "    }"
        fi
    done <<< "$DEVICE_DETAILS"
    
    echo "]" >> "${PROFILES_DIR}/devices.json"
    
    echo ""
    echo "  ]"
    echo "}"
    echo ""
    echo "========================================"
    echo "🚀 DISCOVERY COMPLETE"
    echo "========================================"
    echo "1. Choose a device ID from the list above."
    echo "2. Run the assembly script to build the workspace:"
    echo ""
    echo "   python3 scripts/assemble_device_workspace.py --id <DEVICE_ID>"
    echo ""
    echo "Note: You can also add '--location livingroom' to customize the folder name."
}

# Main execution
main() {
    # SAFETY CHECK
    CONFIRMED=false
    for arg in "$@"; do
        if [ "$arg" == "--confirm" ]; then
            CONFIRMED=true
        fi
    done

    if [ "$CONFIRMED" = false ]; then
        echo ""
        echo "🛡️  SAFETY MANIFEST: LG THINQ DISCOVERY"
        echo "========================================"
        echo "This script will perform the following actions:"
        echo "1. [ENV]  Create virtual environment at ./venv"
        echo "2. [NET]  Download & Install dependencies from PyPI (requests, python-dotenv)"
        echo "3. [NET]  Discover regional API server (uses LG_PAT/LG_COUNTRY)"
        echo "4. [NET]  Fetch list of devices and technical profiles"
        echo "5. [FILE] Save profiles to ./profiles/ and update database"
        echo ""
        echo "[ACTION REQUIRED]"
        echo "Please review these actions. If you approve, run:"
        echo "   ./setup.sh --confirm"
        echo "========================================"
        echo ""
        exit 0
    fi

    echo "========================================"
    echo "LG ThinQ Universal - Setup"
    echo "========================================"
    echo ""
    
    install_deps
    check_env
    save_api_route
    fetch_profiles
    
    log_info "Setup complete!"
}

main "$@"
