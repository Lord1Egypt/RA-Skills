#!/bin/bash
# common.sh - OpenClaw Gateway Manager shared helpers

detect_os() {
    case "$(uname -s 2>/dev/null)" in
        Darwin*) echo "macOS" ;;
        Linux*) echo "Linux" ;;
        CYGWIN*|MINGW*|MSYS*) echo "Windows" ;;
        *) echo "Unknown" ;;
    esac
}

CURRENT_OS="${CURRENT_OS:-$(detect_os)}"

script_dir() {
    CDPATH= cd -- "$(dirname -- "$0")" && pwd
}

manager_root() {
    CDPATH= cd -- "$(script_dir)/.." && pwd
}

print_repo_usage_hint() {
    local base
    base="$(manager_root)"
    echo "提示：脚本仓库可以放在任意目录，例如：$base"
}

service_kind() {
    case "$CURRENT_OS" in
        macOS) echo "launchagent" ;;
        Linux) echo "systemd-user" ;;
        *) echo "manual" ;;
    esac
}

instance_service_name() {
    local instance="$1"
    case "$instance" in
        local-shrimp) echo "ai.openclaw.gateway" ;;
        *) echo "ai.openclaw.gateway-$instance" ;;
    esac
}

service_file_for_instance() {
    local instance="$1"
    local service_name
    service_name="$(instance_service_name "$instance")"

    case "$(service_kind)" in
        launchagent) echo "$HOME/Library/LaunchAgents/$service_name.plist" ;;
        systemd-user) echo "$HOME/.config/systemd/user/$service_name.service" ;;
        *) echo "" ;;
    esac
}

resolve_instance() {
    local raw="$1"

    case "$raw" in
        local-shrimp|本地虾|18789|local)
            INSTANCE_KEY="local-shrimp"
            INSTANCE_NAME="本地虾"
            CONFIG_DIR="$HOME/.jvs/.openclaw"
            ;;
        feishu|飞书|18790|fly)
            INSTANCE_KEY="feishu"
            INSTANCE_NAME="飞书机器人"
            CONFIG_DIR="$HOME/.openclaw"
            ;;
        qclaw|腾讯|28789)
            INSTANCE_KEY="qclaw"
            INSTANCE_NAME="QClaw"
            CONFIG_DIR="$HOME/.qclaw"
            ;;
        *)
            INSTANCE_KEY="$raw"
            INSTANCE_NAME="$raw"
            if [ -d "$HOME/.openclaw-$raw" ] || [ ! -d "$HOME/.config/openclaw-$raw" ]; then
                CONFIG_DIR="$HOME/.openclaw-$raw"
            else
                CONFIG_DIR="$HOME/.config/openclaw-$raw"
            fi
            ;;
    esac

    SERVICE_FILE="$(service_file_for_instance "$INSTANCE_KEY")"
}

list_candidate_dirs() {
    local seen=""
    local dir

    for dir in \
        "$HOME/.openclaw" \
        "$HOME/.jvs/.openclaw" \
        "$HOME/.qclaw" \
        "$HOME/.claw-cloud" \
        "$HOME/.openclaw-cloud" \
        "$HOME/.config/openclaw" \
        "$HOME"/.openclaw-* \
        "$HOME"/.config/openclaw-* \
        "/opt/openclaw"
    do
        [ -d "$dir" ] || continue
        case " $seen " in
            *" $dir "*) continue ;;
        esac
        seen="$seen $dir"
        echo "$dir"
    done
}

read_gateway_port() {
    local config_file="$1"
    [ -f "$config_file" ] || return 1
    jq -r '.gateway.port // empty' "$config_file" 2>/dev/null
}

read_primary_channel() {
    local config_file="$1"
    [ -f "$config_file" ] || return 1
    jq -r '.channels | keys[0] // empty' "$config_file" 2>/dev/null
}

port_pid() {
    local port="$1"

    if command -v lsof >/dev/null 2>&1; then
        lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $2; exit}'
        return 0
    fi

    if command -v ss >/dev/null 2>&1; then
        ss -lntp 2>/dev/null | awk -v port=":$port" '$4 ~ port {gsub(/.*pid=/, "", $NF); gsub(/,.*/, "", $NF); print $NF; exit}'
        return 0
    fi

    if command -v netstat >/dev/null 2>&1; then
        netstat -tlnp 2>/dev/null | awk -v port=":$port" '$4 ~ port {split($7, a, "/"); print a[1]; exit}'
    fi
}

port_is_listening() {
    local port="$1"
    local pid
    pid="$(port_pid "$port")"
    [ -n "$pid" ]
}

ensure_port_free() {
    local port="$1"
    if port_is_listening "$port"; then
        return 1
    fi
    return 0
}

restart_instance_process() {
    local config_dir="$1"
    if ! command -v openclaw >/dev/null 2>&1; then
        return 1
    fi
    OPENCLAW_HOME="$config_dir" openclaw gateway restart
}

restart_service() {
    local instance_key="$1"
    local config_dir="$2"
    local service_file="$3"
    local service_name
    service_name="$(instance_service_name "$instance_key")"

    case "$(service_kind)" in
        launchagent)
            if [ -f "$service_file" ]; then
                launchctl kickstart -k "gui/$(id -u)/$service_name" >/dev/null 2>&1 && return 0
            fi
            ;;
        systemd-user)
            if command -v systemctl >/dev/null 2>&1 && [ -f "$service_file" ]; then
                systemctl --user daemon-reload >/dev/null 2>&1
                systemctl --user restart "$service_name" >/dev/null 2>&1 && return 0
            fi
            ;;
    esac

    restart_instance_process "$config_dir"
}

stop_service() {
    local instance_key="$1"
    local service_file="$2"
    local service_name
    service_name="$(instance_service_name "$instance_key")"

    case "$(service_kind)" in
        launchagent)
            [ -f "$service_file" ] || return 1
            launchctl bootout "gui/$(id -u)" "$service_file" >/dev/null 2>&1 || launchctl unload "$service_file" >/dev/null 2>&1
            ;;
        systemd-user)
            command -v systemctl >/dev/null 2>&1 || return 1
            systemctl --user disable --now "$service_name" >/dev/null 2>&1
            ;;
        *)
            return 1
            ;;
    esac
}

delete_service_file() {
    local service_file="$1"
    [ -n "$service_file" ] && [ -f "$service_file" ] && rm -f "$service_file"
}

create_service_file() {
    local instance_key="$1"
    local config_dir="$2"
    local port="$3"
    local service_file="$4"
    local service_name
    local node_path

    service_name="$(instance_service_name "$instance_key")"
    node_path="$(command -v node 2>/dev/null || true)"

    case "$(service_kind)" in
        launchagent)
            mkdir -p "$(dirname "$service_file")" "$config_dir/logs"
            cat > "$service_file" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$service_name</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
        <string>${node_path:-node}</string>
        <string>-e</string>
        <string>require('child_process').execSync('openclaw gateway --port $port', {cwd: '$config_dir', stdio: 'inherit', env: {...process.env, OPENCLAW_HOME: '$config_dir'}})</string>
    </array>
    <key>StandardOutPath</key>
    <string>$config_dir/logs/gateway.log</string>
    <key>StandardErrorPath</key>
    <string>$config_dir/logs/gateway.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>$HOME</string>
        <key>OPENCLAW_HOME</key>
        <string>$config_dir</string>
        <key>OPENCLAW_GATEWAY_PORT</key>
        <string>$port</string>
    </dict>
</dict>
</plist>
EOF
            ;;
        systemd-user)
            mkdir -p "$(dirname "$service_file")" "$config_dir/logs"
            cat > "$service_file" <<EOF
[Unit]
Description=OpenClaw Gateway ($instance_key)
After=network.target

[Service]
Type=simple
WorkingDirectory=$config_dir
Environment=OPENCLAW_HOME=$config_dir
Environment=OPENCLAW_GATEWAY_PORT=$port
ExecStart=/bin/sh -lc 'openclaw gateway --port $port'
Restart=always
RestartSec=2
StandardOutput=append:$config_dir/logs/gateway.log
StandardError=append:$config_dir/logs/gateway.err.log

[Install]
WantedBy=default.target
EOF
            ;;
        *)
            return 1
            ;;
    esac
}

enable_service() {
    local instance_key="$1"
    local service_file="$2"
    local service_name
    service_name="$(instance_service_name "$instance_key")"

    case "$(service_kind)" in
        launchagent)
            launchctl bootstrap "gui/$(id -u)" "$service_file" >/dev/null 2>&1 || launchctl load "$service_file" >/dev/null 2>&1
            ;;
        systemd-user)
            systemctl --user daemon-reload >/dev/null 2>&1
            systemctl --user enable --now "$service_name" >/dev/null 2>&1
            ;;
        *)
            return 1
            ;;
    esac
}
