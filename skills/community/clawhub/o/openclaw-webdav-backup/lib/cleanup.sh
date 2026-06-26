#!/usr/bin/env bash
# Shared cleanup utilities for openclaw-webdav-backup

# Array to track temp files for cleanup
declare -a _TEMP_FILES=()
declare -a _TEMP_DIRS=()

# Register a temp file for cleanup
register_temp_file() {
    local file="$1"
    _TEMP_FILES+=("$file")
}

# Register a temp directory for cleanup
register_temp_dir() {
    local dir="$1"
    _TEMP_DIRS+=("$dir")
}

# Cleanup function - call this in trap EXIT
cleanup_all() {
    local exit_code=$?
    
    # Clean up temp files
    for file in "${_TEMP_FILES[@]}"; do
        if [[ -f "$file" ]]; then
            rm -f "$file" 2>/dev/null || true
        fi
    done
    
    # Clean up temp directories
    for dir in "${_TEMP_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            rm -rf "$dir" 2>/dev/null || true
        fi
    done
    
    # Also clean up any leftover curl error files
    rm -f /tmp/webdav_error_$$.txt 2>/dev/null || true
    
    return $exit_code
}

# Set up cleanup trap
setup_cleanup_trap() {
    # Save any existing EXIT trap
    local existing_trap
    existing_trap=$(trap -p EXIT 2>/dev/null || true)
    
    if [[ -n "$existing_trap" ]]; then
        # Combine with existing trap
        trap 'cleanup_all; eval "${existing_trap#trap }"' EXIT
    else
        trap cleanup_all EXIT
    fi
}

# Export functions
export -f register_temp_file register_temp_dir cleanup_all setup_cleanup_trap
