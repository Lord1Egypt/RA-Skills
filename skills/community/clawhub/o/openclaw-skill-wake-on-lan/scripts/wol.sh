#!/bin/bash

# Wake-on-LAN script for OpenClaw
# Supports waking devices by MAC address or name from config

set -e

# Config file location
CONFIG_DIR="$HOME/.config/openclaw"
CONFIG_FILE="$CONFIG_DIR/wol-devices.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Ensure config directory exists
ensure_config() {
    mkdir -p "$CONFIG_DIR"
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo '[]' > "$CONFIG_FILE"
    fi
}

# Check for required tools
check_dependencies() {
    local missing=0
    
    if ! command -v wakeonlan &> /dev/null; then
        echo -e "${RED}Error: 'wakeonlan' command not found.${NC}"
        echo "Install with: brew install wakeonlan"
        missing=1
    fi
    
    if ! command -v ping &> /dev/null; then
        echo -e "${RED}Error: 'ping' command not found.${NC}"
        missing=1
    fi
    
    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
}

# Get broadcast address (default to 255.255.255.255)
get_broadcast() {
    local broadcast="${1:-255.255.255.255}"
    echo "$broadcast"
}

# Wake a device by MAC address
wake_by_mac() {
    local mac="$1"
    local broadcast="${2:-255.255.255.255}"
    
    if [[ -z "$mac" ]]; then
        echo -e "${RED}Error: MAC address required${NC}"
        echo "Usage: wol.sh wake <MAC address> [broadcast IP] [ping IP]"
        exit 1
    fi
    
    echo -e "${CYAN}Waking device ${mac}...${NC}"
    wakeonlan -i "$broadcast" "$mac"
    echo -e "${GREEN}Wake-on-LAN packet sent to ${mac}${NC}"
}

# Get device from config by name
get_device_by_name() {
    local name="$1"
    local devices
    devices=$(cat "$CONFIG_FILE")
    
    # Use Python to parse JSON for compatibility
    python3 -c "
import json
import sys
name = sys.argv[1]
config_file = sys.argv[2]
devices = json.load(open(config_file))
for d in devices:
    if d.get('name', '').lower() == name.lower():
        print(json.dumps(d))
        sys.exit(0)
sys.exit(1)
" "$name" "$CONFIG_FILE" 2>/dev/null
}

# Wake a device by name
wake_by_name() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}Error: Device name required${NC}"
        echo "Usage: wol.sh wake-name <device name>"
        exit 1
    fi
    
    ensure_config
    
    local device
    device=$(get_device_by_name "$name")
    
    if [[ -z "$device" ]]; then
        echo -e "${RED}Error: Device '${name}' not found in config${NC}"
        echo "Use 'wol.sh list' to see saved devices"
        echo "Use 'wol.sh add <name> <MAC> [broadcast]' to add a device"
        exit 1
    fi
    
    local mac broadcast
    mac=$(echo "$device" | python3 -c "import json,sys; print(json.load(sys.stdin).get('mac',''))")
    broadcast=$(echo "$device" | python3 -c "import json,sys; print(json.load(sys.stdin).get('broadcast','255.255.255.255'))")
    
    echo -e "${CYAN}Waking device '${name}' (${mac})...${NC}"
    wakeonlan -i "$broadcast" "$mac"
    echo -e "${GREEN}Wake-on-LAN packet sent to '${name}'${NC}"
}

# List all saved devices
list_devices() {
    ensure_config
    
    local devices
    devices=$(cat "$CONFIG_FILE")
    
    local count
    count=$(echo "$devices" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    if [[ "$count" -eq 0 ]]; then
        echo -e "${YELLOW}No devices saved yet.${NC}"
        echo "Use 'wol.sh add <name> <MAC> [broadcast]' to add a device"
        return
    fi
    
    echo -e "${BLUE}Saved devices:${NC}"
    echo "$devices" | python3 -c "
import json
import sys

devices = json.load(sys.stdin)
print()
for i, d in enumerate(devices, 1):
    name = d.get('name', 'Unknown')
    mac = d.get('mac', 'N/A')
    broadcast = d.get('broadcast', '255.255.255.255')
    print(f'  {i}. {name}')
    print(f'     MAC: {mac}')
    print(f'     Broadcast: {broadcast}')
    ip = d.get('ip', '')
    if ip:
        print(f'     IP: {ip}')
    print()
"
}

# Add a device to config
add_device() {
    local name="$1"
    local mac="$2"
    local broadcast="${3:-255.255.255.255}"
    local ip="${4:-}"
    
    if [[ -z "$name" || -z "$mac" ]]; then
        echo -e "${RED}Error: Name and MAC address required${NC}"
        echo "Usage: wol.sh add <name> <MAC> [broadcast IP] [ping IP]"
        exit 1
    fi
    
    # Validate MAC address format
    if ! [[ "$mac" =~ ^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$ ]]; then
        echo -e "${RED}Error: Invalid MAC address format${NC}"
        echo "Expected format: XX:XX:XX:XX:XX:XX"
        exit 1
    fi
    
    ensure_config
    
    # Read existing devices
    local devices
    devices=$(cat "$CONFIG_FILE")
    
    # Check if device with same name exists
    local existing
    existing=$(echo "$devices" | python3 -c "
import json
import sys
name = sys.argv[1]
devices = json.load(sys.stdin)
for d in devices:
    if d.get('name', '').lower() == name.lower():
        print('yes')
        sys.exit(0)
print('no')
" "$name" 2>/dev/null)
    
    if [[ "$existing" == "yes" ]]; then
        echo -e "${YELLOW}Warning: Device '${name}' already exists. Updating...${NC}"
        # Remove existing device with same name
        devices=$(echo "$devices" | python3 -c "
import json
import sys
name = sys.argv[1]
devices = json.load(sys.stdin)
devices = [d for d in devices if d.get('name', '').lower() != name.lower()]
print(json.dumps(devices))
" "$name")
    fi
    
    # Add new device
    local new_device
    new_device=$(python3 -c "
import json
import sys
name = sys.argv[1]
mac = sys.argv[2]
broadcast = sys.argv[3]
ip = sys.argv[4] if len(sys.argv) > 4 else ''
device = {
    'name': name,
    'mac': mac,
    'broadcast': broadcast,
    'ip': ip
}
print(json.dumps(device))
" "$name" "$mac" "$broadcast" "$ip")
    
    # Merge and save
    echo "$devices" | python3 -c "
import json
import sys
new_device = json.loads(sys.argv[1])
devices = json.load(sys.stdin)
devices.append(new_device)
print(json.dumps(devices, indent=2))
" "$new_device" > "$CONFIG_FILE"
    
    echo -e "${GREEN}Device '${name}' added successfully!${NC}"
    if [[ -n "$ip" ]]; then
        echo "  IP for ping: $ip"
    fi
    echo "  MAC: $mac"
    echo "  Broadcast: $broadcast"
}

# Remove a device from config
remove_device() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}Error: Device name required${NC}"
        echo "Usage: wol.sh remove <device name>"
        exit 1
    fi
    
    ensure_config
    
    local devices
    devices=$(cat "$CONFIG_FILE")
    
    # Check if device exists
    local exists
    exists=$(echo "$devices" | python3 -c "
import json
import sys
name = sys.argv[1]
devices = json.load(sys.stdin)
for d in devices:
    if d.get('name', '').lower() == name.lower():
        print('yes')
        sys.exit(0)
print('no')
" "$name" 2>/dev/null)
    
    if [[ "$exists" == "no" ]]; then
        echo -e "${RED}Error: Device '${name}' not found in config${NC}"
        exit 1
    fi
    
    # Remove device
    echo "$devices" | python3 -c "
import json
import sys
name = sys.argv[1]
devices = json.load(sys.stdin)
devices = [d for d in devices if d.get('name', '').lower() != name.lower()]
print(json.dumps(devices, indent=2))
" "$name" > "$CONFIG_FILE"
    
    echo -e "${GREEN}Device '${name}' removed successfully!${NC}"
}

# Query device status (ping)
query_status() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}Error: Device name required${NC}"
        echo "Usage: wol.sh status <device name>"
        exit 1
    fi
    
    ensure_config
    
    local device
    device=$(get_device_by_name "$name")
    
    if [[ -z "$device" ]]; then
        echo -e "${RED}Error: Device '${name}' not found in config${NC}"
        exit 1
    fi
    
    local ip
    ip=$(echo "$device" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ip',''))")
    
    if [[ -z "$ip" ]]; then
        echo -e "${YELLOW}Warning: No IP configured for '${name}'${NC}"
        echo "Use 'wol.sh add <name> <MAC> <broadcast> <IP>' to set an IP address"
        exit 1
    fi
    
    echo -e "${CYAN}Pinging ${ip}...${NC}"
    
    if ping -c 3 -t 5 "$ip" &> /dev/null; then
        echo -e "${GREEN}Device '${name}' is ONLINE${NC}"
    else
        echo -e "${RED}Device '${name}' is OFFLINE or unreachable${NC}"
    fi
}

# Broadcast to all saved devices
broadcast_all() {
    ensure_config
    
    local devices
    devices=$(cat "$CONFIG_FILE")
    
    local count
    count=$(echo "$devices" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    if [[ "$count" -eq 0 ]]; then
        echo -e "${YELLOW}No devices to wake.${NC}"
        return
    fi
    
    echo -e "${CYAN}Broadcasting wake signal to all ${count} device(s)...${NC}"
    echo "$devices" | python3 -c "
import json
import sys

devices = json.load(sys.stdin)
for d in devices:
    name = d.get('name', 'Unknown')
    mac = d.get('mac', '')
    broadcast = d.get('broadcast', '255.255.255.255')
    if mac:
        print(f'Waking {name} ({mac})...')
" >&2
    
    # Send wake signals
    echo "$devices" | python3 -c "
import json
import subprocess
import sys

devices = json.load(sys.stdin)
for d in devices:
    mac = d.get('mac', '')
    broadcast = d.get('broadcast', '255.255.255.255')
    if mac:
        subprocess.run(['wakeonlan', '-i', broadcast, mac], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
" 2>/dev/null
    
    echo -e "${GREEN}Broadcast complete!${NC}"
}

# Show help
show_help() {
    cat << EOF
Wake-on-LAN for OpenClaw

Usage: wol.sh <command> [options]

Commands:
    wake <MAC> [broadcast]     Wake a device by MAC address
    wake-name <name>            Wake a device by name from config
    list                        List all saved devices
    add <name> <MAC> [broadcast]  Add a device to config
    remove <name>              Remove a device from config
    status <name>               Query device status (ping)
    broadcast                   Wake all saved devices
    help                        Show this help message

Examples:
    wol.sh wake 00:11:22:33:44:55
    wol.sh wake 00:11:22:33:44:55 192.168.1.255
    wol.sh wake-name desktop
    wol.sh add desktop 00:11:22:33:44:55 192.168.1.255
    wol.sh list
    wol.sh status desktop
    wol.sh broadcast

Config file: $CONFIG_FILE
EOF
}

# Main
main() {
    check_dependencies
    
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        wake)
            wake_by_mac "$@"
            ;;
        wake-name)
            wake_by_name "$@"
            ;;
        list)
            list_devices
            ;;
        add)
            add_device "$@"
            ;;
        remove|rm)
            remove_device "$@"
            ;;
        status|ping)
            query_status "$@"
            ;;
        broadcast|all)
            broadcast_all
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: ${command}${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
