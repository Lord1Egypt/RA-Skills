#!/bin/bash
set -euo pipefail

# HiLink LTE Modem CLI
# Usage: hilink.sh <command> [args]

# Config
CONFIG_FILE="${HOME}/.config/hilink/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi
GATEWAY="${HILINK_GATEWAY:-192.168.200.1}"
GATEWAY_SUBNET="${HILINK_SUBNET:-192.168.200.0/24}"
STATIC_IP="${HILINK_STATIC_IP:-192.168.200.100/24}"
SIM_PIN="${HILINK_PIN:-}"  # Set in config or pass via 'pin enter'
API="http://${GATEWAY}/api"

# --- Interface Management ---

# Find the HiLink USB interface (Huawei cdc_ether)
find_interface() {
    # Try known name first
    if [ -d "/sys/class/net/lte0" ]; then
        echo "lte0"
        return
    fi
    # Find Huawei USB network interface (enx* that isn't the main LAN)
    local main_mac
    main_mac=$(cat /sys/class/net/enp*/address 2>/dev/null || echo "")
    for iface in /sys/class/net/enx*; do
        [ -d "$iface" ] || continue
        local name=$(basename "$iface")
        local mac=$(cat "$iface/address" 2>/dev/null)
        [ "$mac" != "$main_mac" ] && echo "$name" && return
    done
    echo ""
}

# Ensure interface is up with correct IP
ensure_interface() {
    local iface
    iface=$(find_interface)
    if [ -z "$iface" ]; then
        echo "ERROR: No HiLink USB interface found. Is the stick plugged in?" >&2
        return 1
    fi

    local state=$(cat "/sys/class/net/${iface}/operstate" 2>/dev/null)
    local has_ip=$(ip -4 addr show "$iface" 2>/dev/null | grep -c "inet ")

    if [ "$state" != "up" ] || [ "$has_ip" -eq 0 ]; then
        echo "Bringing up ${iface}..." >&2
        sudo ip addr add "$STATIC_IP" dev "$iface" 2>/dev/null || true
        sudo ip link set "$iface" up 2>/dev/null
        sleep 2
    fi

    # Verify gateway is reachable
    if ! ping -c1 -W2 "$GATEWAY" > /dev/null 2>&1; then
        echo "ERROR: Gateway ${GATEWAY} not reachable via ${iface}" >&2
        return 1
    fi
}

# Ensure SIM is registered (enter PIN if needed)
ensure_sim() {
    local resp state
    get_tokens
    resp=$(api_get "/pin/status")
    state=$(xml_val "SimState" "$resp")

    case "$state" in
        257) return 0 ;;  # Ready
        260|256)  # PIN required
            if [ -n "$SIM_PIN" ]; then
                echo "Entering SIM PIN..." >&2
                get_tokens
                resp=$(api_post "/pin/operate" "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><OperateType>0</OperateType><CurrentPin>${SIM_PIN}</CurrentPin><NewPin></NewPin><PukCode></PukCode></request>")
                if echo "$resp" | grep -q "<response>OK</response>"; then
                    echo "PIN accepted, waiting for network..." >&2
                    sleep 5
                    return 0
                else
                    echo "ERROR: PIN rejected!" >&2
                    return 1
                fi
            else
                echo "ERROR: SIM needs PIN. Set HILINK_PIN in config or run: $0 pin enter <PIN>" >&2
                return 1
            fi
            ;;
        255) echo "ERROR: No SIM card detected" >&2; return 1 ;;
        258) echo "ERROR: PUK required!" >&2; return 1 ;;
        *) echo "WARNING: Unknown SIM state ${state}" >&2 ;;
    esac
}

# Full initialization: interface + PIN + verify
cmd_init() {
    echo "=== HiLink LTE Init ==="
    
    # Step 1: Interface
    ensure_interface || return 1
    local iface=$(find_interface)
    echo "✅ Interface: ${iface}"
    
    # Step 2: SIM PIN
    ensure_sim || return 1
    echo "✅ SIM: registered"
    
    # Step 3: Status
    get_tokens
    local signal=$(api_get "/device/signal")
    local rsrp=$(xml_val "rsrp" "$signal" | sed 's/dBm//')
    local band=$(xml_val "band" "$signal")
    echo "✅ Signal: RSRP ${rsrp} dBm, Band ${band}"
    
    # Step 4: Remove any default route from LTE
    sudo ip route del default via "$GATEWAY" dev "$iface" 2>/dev/null || true
    echo "✅ Routes: clean (no LTE default route)"
    
    echo "=== Ready ==="
}

# --- Auth ---
get_tokens() {
    local resp
    resp=$(curl -s --connect-timeout 5 "${API}/webserver/SesTokInfo" 2>/dev/null)
    SESSION=$(echo "$resp" | grep -oP '(?<=<SesInfo>).*(?=</SesInfo>)')
    TOKEN=$(echo "$resp" | grep -oP '(?<=<TokInfo>).*(?=</TokInfo>)')
    if [ -z "$SESSION" ] || [ -z "$TOKEN" ]; then
        echo "ERROR: HiLink API not reachable at ${GATEWAY}" >&2
        exit 1
    fi
}

api_post() {
    local endpoint="$1" data="$2"
    curl -s --connect-timeout 10 -X POST "${API}${endpoint}" \
        -H "Cookie: ${SESSION}" \
        -H "__RequestVerificationToken: ${TOKEN}" \
        -H "Content-Type: application/xml" \
        -d "${data}" 2>/dev/null
}

api_get() {
    local endpoint="$1"
    curl -s --connect-timeout 10 "${API}${endpoint}" \
        -H "Cookie: ${SESSION}" \
        -H "__RequestVerificationToken: ${TOKEN}" 2>/dev/null
}

xml_val() {
    local tag="$1" xml="$2"
    echo "$xml" | grep -oP "(?<=<${tag}>)[^<]+" || echo ""
}

# --- Commands ---

cmd_sms_send() {
    local number="$1" message="${*:2}"
    local date length
    date=$(date "+%Y-%m-%d %H:%M:%S")
    length=${#message}
    ensure_interface || return 1
    ensure_sim || return 1
    get_tokens
    local resp
    resp=$(api_post "/sms/send-sms" "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><Index>-1</Index><Phones><Phone>${number}</Phone></Phones><Sca></Sca><Content>${message}</Content><Length>${length}</Length><Reserved>1</Reserved><Date>${date}</Date><SendType>0</SendType></request>")
    if echo "$resp" | grep -q "<response>OK</response>"; then
        echo "SMS sent to ${number}"
    else
        local code
        code=$(xml_val "code" "$resp")
        echo "ERROR sending SMS (code: ${code:-unknown})" >&2
        [ "$code" = "113018" ] && echo "Hint: SIM not registered. Check PIN and signal." >&2
        return 1
    fi
}

cmd_sms_list() {
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_post "/sms/sms-list" '<?xml version="1.0" encoding="UTF-8"?><request><PageIndex>1</PageIndex><ReadCount>20</ReadCount><BoxType>1</BoxType><SortType>0</SortType><Ascending>0</Ascending><UnreadPreferred>1</UnreadPreferred></request>')
    local count
    count=$(xml_val "Count" "$resp")
    echo "=== Inbox (${count:-0} SMS) ==="
    echo "$resp" | python3 -c "
import sys, xml.etree.ElementTree as ET
try:
    tree = ET.parse(sys.stdin)
    for msg in tree.findall('.//Message'):
        idx = msg.findtext('Index', '?')
        stat = msg.findtext('Smstat', '1')
        phone = msg.findtext('Phone', '?')
        date = msg.findtext('Date', '?')
        content = msg.findtext('Content', '')[:60]
        flag = 'NEW' if stat == '0' else '   '
        print(f'[{idx}] {flag} {date:<20} {phone:<15} {content}')
except: pass
" 2>/dev/null
}

cmd_sms_read() {
    local index="$1"
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_post "/sms/sms-list" '<?xml version="1.0" encoding="UTF-8"?><request><PageIndex>1</PageIndex><ReadCount>50</ReadCount><BoxType>1</BoxType><SortType>0</SortType><Ascending>0</Ascending><UnreadPreferred>0</UnreadPreferred></request>')
    echo "$resp" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
for msg in tree.findall('.//Message'):
    if msg.findtext('Index') == '${index}':
        print(f'From: {msg.findtext(\"Phone\")}')
        print(f'Date: {msg.findtext(\"Date\")}')
        print('---')
        print(msg.findtext('Content', ''))
        break
else:
    print('SMS ${index} not found')
" 2>/dev/null
}

cmd_sms_delete() {
    local index="$1"
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_post "/sms/delete-sms" "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><Index>${index}</Index></request>")
    if echo "$resp" | grep -q "<response>OK</response>"; then
        echo "SMS ${index} deleted"
    else
        echo "ERROR deleting SMS ${index}" >&2
        return 1
    fi
}

cmd_status() {
    ensure_interface || return 1
    get_tokens
    local signal info
    signal=$(api_get "/device/signal")
    info=$(api_get "/monitoring/status")
    local rsrp rssi sinr band unread net_type
    rsrp=$(xml_val "rsrp" "$signal" | sed 's/dBm//')
    rssi=$(xml_val "rssi" "$signal" | sed 's/dBm//')
    sinr=$(xml_val "sinr" "$signal" | sed 's/dB//')
    band=$(xml_val "band" "$signal")
    unread=$(xml_val "UnreadMessage" "$info")
    net_type=$(xml_val "CurrentNetworkType" "$info")
    local net_name="Unknown"
    case "$net_type" in
        19) net_name="LTE" ;;
        9|10|11) net_name="3G" ;;
        1|2|3) net_name="2G" ;;
        0) net_name="No Service" ;;
    esac
    echo "=== LTE Status ==="
    echo "Network: ${net_name} (type ${net_type})"
    echo "Signal:  RSRP ${rsrp} dBm | RSSI ${rssi} dBm | SINR ${sinr} dB"
    echo "Band:    ${band}"
    echo "Unread:  ${unread:-0} SMS"
}

cmd_signal() {
    ensure_interface || return 1
    get_tokens
    local signal
    signal=$(api_get "/device/signal")
    echo "$signal" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
r = tree.getroot()
for child in r:
    val = child.text
    if val: print(f'{child.tag}: {val}')
" 2>/dev/null
}

cmd_pin_enter() {
    local pin="$1"
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_post "/pin/operate" "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><OperateType>0</OperateType><CurrentPin>${pin}</CurrentPin><NewPin></NewPin><PukCode></PukCode></request>")
    if echo "$resp" | grep -q "<response>OK</response>"; then
        echo "PIN accepted"
    else
        echo "PIN rejected" >&2
        return 1
    fi
}

cmd_pin_disable() {
    local pin="$1"
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_post "/pin/operate" "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><OperateType>2</OperateType><CurrentPin>${pin}</CurrentPin><NewPin></NewPin><PukCode></PukCode></request>")
    if echo "$resp" | grep -q "<response>OK</response>"; then
        echo "PIN disabled"
    else
        echo "ERROR disabling PIN" >&2
        return 1
    fi
}

cmd_pin_status() {
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_get "/pin/status")
    local state pin_times puk_times
    state=$(xml_val "SimState" "$resp")
    pin_times=$(xml_val "SimPinTimes" "$resp")
    puk_times=$(xml_val "SimPukTimes" "$resp")
    local state_name="Unknown"
    case "$state" in
        255) state_name="No SIM" ;;
        256) state_name="PIN locked" ;;
        257) state_name="Ready" ;;
        258) state_name="PUK required" ;;
        260) state_name="PIN required" ;;
    esac
    echo "SIM State: ${state_name} (${state})"
    echo "PIN attempts remaining: ${pin_times}"
    echo "PUK attempts remaining: ${puk_times}"
}

cmd_balance() {
    ensure_interface || return 1
    get_tokens
    api_post "/ussd/send" '<?xml version="1.0" encoding="UTF-8"?><request><content>*#100#</content><codeType>CodeType</codeType><timeout></timeout></request>' > /dev/null
    sleep 3
    get_tokens
    local resp
    resp=$(api_get "/ussd/get")
    xml_val "content" "$resp" || echo "No response (try again)"
}

cmd_info() {
    ensure_interface || return 1
    get_tokens
    local resp
    resp=$(api_get "/device/information")
    echo "=== Device Info ==="
    echo "Model:    $(xml_val 'DeviceName' "$resp")"
    echo "Serial:   $(xml_val 'SerialNumber' "$resp")"
    echo "IMEI:     $(xml_val 'Imei' "$resp")"
    echo "Firmware: $(xml_val 'SoftwareVersion' "$resp")"
    echo "WebUI:    $(xml_val 'WebUIVersion' "$resp")"
    echo "MAC:      $(xml_val 'MacAddress1' "$resp")"
}

# --- Main ---
case "${1:-help}" in
    sms)
        case "${2:-help}" in
            send)   [ $# -lt 4 ] && echo "Usage: $0 sms send <number> <message>" && exit 1; cmd_sms_send "$3" "${@:4}" ;;
            list)   cmd_sms_list ;;
            read)   [ $# -lt 3 ] && echo "Usage: $0 sms read <index>" && exit 1; cmd_sms_read "$3" ;;
            delete) [ $# -lt 3 ] && echo "Usage: $0 sms delete <index>" && exit 1; cmd_sms_delete "$3" ;;
            *)      echo "Usage: $0 sms {send|list|read|delete}" ;;
        esac ;;
    status)  cmd_status ;;
    signal)  cmd_signal ;;
    balance) cmd_balance ;;
    info)    cmd_info ;;
    pin)
        case "${2:-help}" in
            enter)   [ $# -lt 3 ] && echo "Usage: $0 pin enter <PIN>" && exit 1; cmd_pin_enter "$3" ;;
            disable) [ $# -lt 3 ] && echo "Usage: $0 pin disable <PIN>" && exit 1; cmd_pin_disable "$3" ;;
            status)  cmd_pin_status ;;
            *)       echo "Usage: $0 pin {enter|disable|status}" ;;
        esac ;;
    init)    cmd_init ;;
    help|*)
        cat << USAGE
HiLink LTE Modem CLI

Usage: $0 <command> [args]

Commands:
  sms send <number> <text>   Send SMS
  sms list                   List inbox
  sms read <index>           Read SMS
  sms delete <index>         Delete SMS
  status                     LTE signal & network status
  signal                     Detailed signal info
  balance                    Prepaid balance (USSD *#100#)
  info                       Device information
  pin enter <PIN>            Enter SIM PIN
  pin disable <PIN>          Disable SIM PIN
  pin status                 Show PIN/SIM state
  init                       Full init (interface + PIN + verify)

Gateway: ${GATEWAY}
USAGE
        ;;
esac
