#!/bin/bash

# OpenClaw Health Check & Auto-Fix Script
# This script checks OpenClaw status and automatically fixes any issues found

# Set PATH for launchd daemon - include common paths
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin:$HOME/.nvm/versions/node/*/bin"

# Load nvm if available (supports multiple nvm installations)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" 2>/dev/null

# Find openclaw command - prefer which for portability
OPENCLAW_BIN=""
for path in "openclaw" "/opt/homebrew/bin/openclaw" "/usr/local/bin/openclaw" "$HOME/.local/bin/openclaw"; do
    if [ -x "$(which "$path" 2>/dev/null)" ]; then
        OPENCLAW_BIN="$(which "$path" 2>/dev/null)"
        break
    fi
done

# Fallback: try direct path check if which failed
if [ -z "$OPENCLAW_BIN" ]; then
    for path in "/opt/homebrew/bin/openclaw" "/usr/local/bin/openclaw" "$HOME/.local/bin/openclaw"; do
        if [ -x "$path" ]; then
            OPENCLAW_BIN="$path"
            break
        fi
    done
fi

# Use HOME variable for all paths - portable across users
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_FILE="$OPENCLAW_HOME/logs/health-check.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# State directory for cooldown and rate limiting
STATE_DIR="$OPENCLAW_HOME/state"
LAST_RESTART_FILE="$STATE_DIR/last_restart"
RESTART_COUNT_FILE="$STATE_DIR/restart_count"
HOUR_MARKER="$STATE_DIR/hour_marker"
COOLDOWN_SECONDS=180
MAX_RESTARTS_PER_HOUR=5

# Ensure directories exist
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$STATE_DIR"

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Check cooldown - returns 0 if allowed, 1 if in cooldown
check_cooldown() {
    if [ -f "$LAST_RESTART_FILE" ]; then
        local last_restart=$(cat "$LAST_RESTART_FILE" 2>/dev/null || echo "0")
        local now=$(date +%s)
        local diff=$((now - last_restart))
        if [ $diff -lt $COOLDOWN_SECONDS ]; then
            log "冷却期内 (${diff}s/${COOLDOWN_SECONDS}s)，跳过重启操作"
            return 1
        fi
    fi
    return 0
}

# Check rate limit - returns 0 if allowed, 1 if exceeded
check_rate_limit() {
    local current_hour=$(date +%Y%m%d%H)
    
    # Reset counter if hour changed
    if [ -f "$HOUR_MARKER" ]; then
        local marked_hour=$(cat "$HOUR_MARKER" 2>/dev/null)
        if [ "$marked_hour" != "$current_hour" ]; then
            echo "$current_hour" > "$HOUR_MARKER"
            echo "0" > "$RESTART_COUNT_FILE"
        fi
    else
        echo "$current_hour" > "$HOUR_MARKER"
        echo "0" > "$RESTART_COUNT_FILE"
    fi
    
    local restart_count=$(cat "$RESTART_COUNT_FILE" 2>/dev/null || echo "0")
    if [ "$restart_count" -ge "$MAX_RESTARTS_PER_HOUR" ]; then
        log "本小时已达重启上限(${MAX_RESTARTS_PER_HOUR}次)，跳过"
        return 1
    fi
    return 0
}

# Record restart event
record_restart() {
    date +%s > "$LAST_RESTART_FILE"
    local current_hour=$(date +%Y%m%d%H)
    if [ -f "$HOUR_MARKER" ]; then
        local marked_hour=$(cat "$HOUR_MARKER" 2>/dev/null)
        if [ "$marked_hour" != "$current_hour" ]; then
            echo "$current_hour" > "$HOUR_MARKER"
            echo "1" > "$RESTART_COUNT_FILE"
        else
            local count=$(cat "$RESTART_COUNT_FILE" 2>/dev/null || echo "0")
            echo $((count + 1)) > "$RESTART_COUNT_FILE"
        fi
    else
        echo "$current_hour" > "$HOUR_MARKER"
        echo "1" > "$RESTART_COUNT_FILE"
    fi
}

# Function to open terminal and notify user or attempt interactive fix
open_terminal_for_help() {
    local message="$1"
    log "Opening terminal for user assistance: $message"

    # Escape special characters for AppleScript (single quotes → \')
    local escaped_message="${message//\'/\'\\\'\'}"

    # AppleScript to open Terminal and run commands
    osascript <<EOF
    tell application "Terminal"
        activate
        do script "echo '=== OpenClaw Health Check Alert ===' && echo '$escaped_message' && echo '' && echo 'Current time: $(date)' && echo '' && echo 'Attempting to diagnose...' && openclaw status 2>/dev/null || echo 'openclaw status failed' && echo '' && echo 'Press any key to close this window...' && read -n 1"
    end tell
EOF
}

# Function to force start gateway with multiple fallback methods
force_start_gateway() {
    log "Attempting to force start Gateway..."

    GATEWAY_PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"

    # Method 1: Try launchctl bootstrap directly
    if [ -f "$GATEWAY_PLIST" ]; then
        log "Method 1: Trying launchctl bootstrap..."
        launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null
        sleep 1
        if launchctl bootstrap gui/$(id -u) "$GATEWAY_PLIST" 2>&1 | tee -a "$LOG_FILE"; then
            sleep 3
            if curl -s --max-time 5 "http://127.0.0.1:18789" >/dev/null 2>&1; then
                log "Gateway started successfully via launchctl"
                return 0
            fi
        fi
    fi

    # Method 2: Try openclaw gateway start if available
    if [ -n "$OPENCLAW_BIN" ] && [ -x "$OPENCLAW_BIN" ]; then
        log "Method 2: Trying openclaw gateway start..."
        "$OPENCLAW_BIN" gateway start 2>&1 | tee -a "$LOG_FILE"
        sleep 3
        if curl -s --max-time 5 "http://127.0.0.1:18789" >/dev/null 2>&1; then
            log "Gateway started successfully via openclaw gateway start"
            return 0
        fi
    fi

    # Method 3: Open terminal for user to manually fix
    log "Method 3: Automatic methods failed, opening terminal for user help"
    open_terminal_for_help "Gateway failed to start automatically - manual intervention needed"
    return 1
}

log "========================================="
log "Starting OpenClaw health check..."

# Pre-check: Verify openclaw command exists
if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
    log "ERROR: openclaw command not found or not executable"
    log "Attempting to find openclaw..."
    # Try to use nvm to load correct node version
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    OPENCLAW_BIN=$(which openclaw 2>/dev/null)

    # Still not found - try to start gateway directly via launchctl
    if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
        log "Cannot find openclaw in PATH, attempting direct gateway start..."
        GATEWAY_PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
        if [ -f "$GATEWAY_PLIST" ]; then
            # Unload first to ensure clean state
            launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null
            sleep 2
            # Bootstrap the gateway directly
            if launchctl bootstrap gui/$(id -u) "$GATEWAY_PLIST" 2>&1 | tee -a "$LOG_FILE"; then
                log "Gateway started via launchctl bootstrap"
                sleep 5
                # Try to find openclaw again after gateway starts
                OPENCLAW_BIN=$(which openclaw 2>/dev/null)
            fi
        fi

        if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
            log "ERROR: Still cannot find openclaw after gateway start attempt"
            # Open terminal to notify user
            open_terminal_for_help "Cannot find openclaw command - Gateway may need manual restart"
            exit 1
        fi
    fi
fi

log "Using openclaw: $OPENCLAW_BIN"

# Step 0: Check if Gateway service is loaded, if not, load it
GATEWAY_LOADED=$(launchctl list | grep -q "ai.openclaw.gateway" && echo "yes" || echo "no")
if [ "$GATEWAY_LOADED" != "yes" ]; then
    log "Gateway service not loaded, attempting to load..."
    if ! launchctl load "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" 2>&1 | tee -a "$LOG_FILE"; then
        log "launchctl load failed, trying bootstrap..."
        launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null
        sleep 1
        launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" 2>&1 | tee -a "$LOG_FILE"
    fi
    sleep 3
fi

# Step 1: Check OpenClaw status
log "Checking OpenClaw status..."
STATUS_OUTPUT=$("$OPENCLAW_BIN" status 2>&1)
STATUS_EXIT_CODE=$?

if [ $STATUS_EXIT_CODE -ne 0 ]; then
    log "ERROR: openclaw status failed with exit code $STATUS_EXIT_CODE"
    log "Output: $STATUS_OUTPUT"

    # Check if Gateway is reachable via HTTP directly
    GATEWAY_HTTP_OK=false
    if curl -s --max-time 5 "http://127.0.0.1:18789" >/dev/null 2>&1; then
        GATEWAY_HTTP_OK=true
        log "Gateway HTTP check: reachable on port 18789"
    fi

    if [ "$GATEWAY_HTTP_OK" = "false" ]; then
        log "Gateway is not responding, attempting force start..."
        
        # Check cooldown and rate limit before force start
        if ! check_cooldown; then
            log "跳过强制启动：冷却期内"
            exit 0
        fi
        
        if ! check_rate_limit; then
            log "跳过强制启动：已达每小时重启上限"
            exit 0
        fi
        
        # Record restart before attempting
        record_restart
        log "已记录重启事件 (冷却: ${COOLDOWN_SECONDS}s, 限流: ${MAX_RESTARTS_PER_HOUR}/小时)"
        
        if ! force_start_gateway; then
            log "ERROR: Failed to start Gateway, user notification sent"
            exit 1
        fi
        # Re-check status after force start
        sleep 3
        STATUS_OUTPUT=$("$OPENCLAW_BIN" status 2>&1)
        STATUS_EXIT_CODE=$?
        if [ $STATUS_EXIT_CODE -ne 0 ]; then
            log "ERROR: Gateway still not responding after force start"
            exit 1
        fi
        log "Gateway recovered after force start"
    else
        # Gateway is reachable but status failed - try restart
        log "Gateway HTTP reachable, attempting restart..."
        "$OPENCLAW_BIN" gateway restart 2>&1 | tee -a "$LOG_FILE"
    fi
fi

# Check if Gateway is reachable
if echo "$STATUS_OUTPUT" | grep -q "Gateway.*reachable"; then
    log "Gateway is reachable"
else
    log "WARNING: Gateway may not be reachable"
fi

# Check if Gateway service is running
if echo "$STATUS_OUTPUT" | grep -q "Gateway service.*running"; then
    log "Gateway service is running"
else
    log "WARNING: Gateway service may not be running"
fi

# Step 2: Run OpenClaw doctor
log "Running OpenClaw doctor..."
DOCTOR_OUTPUT=$("$OPENCLAW_BIN" doctor 2>&1)
DOCTOR_EXIT_CODE=$?

log "Doctor output:"
echo "$DOCTOR_OUTPUT" | tee -a "$LOG_FILE"

# Check for issues that need fixing
# Look for critical error indicators (not warnings)
ISSUES_FOUND=false

# Check if doctor returned non-zero exit code (real error, not just warnings)
if [ $DOCTOR_EXIT_CODE -ne 0 ]; then
    ISSUES_FOUND=true
    log "Doctor command returned non-zero exit code: $DOCTOR_EXIT_CODE"
fi

# Check for critical failures (not informational messages)
if echo "$DOCTOR_OUTPUT" | grep -qi "CRITICAL\|FATAL\|PANIC"; then
    ISSUES_FOUND=true
    log "Critical issues detected in doctor output"
fi

# Check if gateway is not reachable or not running
if ! echo "$STATUS_OUTPUT" | grep -q "Gateway.*reachable"; then
    ISSUES_FOUND=true
    log "Gateway is not reachable"
fi

if ! echo "$STATUS_OUTPUT" | grep -q "Gateway service.*running"; then
    ISSUES_FOUND=true
    log "Gateway service is not running"
    # Try to load the service if not loaded
    log "Attempting to load Gateway service..."
    launchctl load "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" 2>&1 | tee -a "$LOG_FILE"
    sleep 3
fi

# Step 3: If issues found, run doctor fix and restart gateway
if [ "$ISSUES_FOUND" = true ]; then
    log "Issues detected! Running openclaw doctor fix..."
    FIX_OUTPUT=$("$OPENCLAW_BIN" doctor --fix 2>&1)
    FIX_EXIT_CODE=$?
    log "Doctor fix output:"
    echo "$FIX_OUTPUT" | tee -a "$LOG_FILE"

    if [ $FIX_EXIT_CODE -eq 0 ]; then
        log "Doctor fix completed successfully"
    else
        log "WARNING: Doctor fix returned exit code $FIX_EXIT_CODE"
    fi

    # Step 4: Restart gateway using force method for reliability
    log "Restarting OpenClaw gateway..."
    
    # Check cooldown and rate limit before restart
    if ! check_cooldown; then
        log "跳过重启：冷却期内"
        exit 0
    fi
    
    if ! check_rate_limit; then
        log "跳过重启：已达每小时重启上限"
        exit 0
    fi
    
    # Record restart before attempting
    record_restart
    log "已记录重启事件 (冷却: ${COOLDOWN_SECONDS}s, 限流: ${MAX_RESTARTS_PER_HOUR}/小时)"

    # First try normal restart
    RESTART_OUTPUT=$("$OPENCLAW_BIN" gateway restart 2>&1)
    RESTART_EXIT_CODE=$?
    log "Gateway restart output:"
    echo "$RESTART_OUTPUT" | tee -a "$LOG_FILE"

    # Verify gateway is actually running after restart
    sleep 3
    GATEWAY_RUNNING=false
    if curl -s --max-time 5 "http://127.0.0.1:18789" >/dev/null 2>&1; then
        GATEWAY_RUNNING=true
        log "Gateway verified: responding on port 18789"
    fi

    # If restart failed or gateway not responding, use force start
    if [ $RESTART_EXIT_CODE -ne 0 ] || [ "$GATEWAY_RUNNING" = "false" ]; then
        if echo "$RESTART_OUTPUT" | grep -qi "not loaded\|failed\|error"; then
            log "Gateway restart failed or not responding, using force start..."
            force_start_gateway
            RESTART_EXIT_CODE=$?
        fi
    fi

    if [ $RESTART_EXIT_CODE -eq 0 ] && [ "$GATEWAY_RUNNING" = "true" ]; then
        log "Gateway restart completed successfully"
    elif [ "$GATEWAY_RUNNING" = "true" ]; then
        log "Gateway is running (verified via HTTP)"
    else
        log "ERROR: Gateway restart may have failed - verifying..."
        # Final verification attempt
        sleep 2
        if curl -s --max-time 5 "http://127.0.0.1:18789" >/dev/null 2>&1; then
            log "Gateway is actually running despite errors"
        else
            log "ERROR: Gateway confirmed not running, opening terminal for help"
            open_terminal_for_help "Gateway failed to restart - requires manual intervention"
        fi
    fi
else
    log "No issues found. OpenClaw is healthy!"
fi

log "Health check complete."
log "========================================="