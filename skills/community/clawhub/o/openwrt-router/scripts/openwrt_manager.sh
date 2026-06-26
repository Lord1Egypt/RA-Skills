#!/bin/bash
# OpenWRT Router Manager - LuCI RPC API 工具
# 用法: ./openwrt_manager.sh <router_ip> <password> <action>
#        ./openwrt_manager.sh <name> <action>     (从 TOOLS.md 读取配置)
# Action: devices, leases, wifi, arp, uptime, all, packages, install:<pkg>

ROUTER_IP="${1}"
PASSWORD="${2}"
ACTION="${3:-all}"
COOKIE_FILE="/tmp/luci_cookies_$$.txt"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

cleanup() { rm -f "$COOKIE_FILE"; }
trap cleanup EXIT

# 登录
login() {
    local resp=$(curl -s -m 10 -X POST "http://${ROUTER_IP}/cgi-bin/luci/" \
        -d "luci_username=root&luci_password=${PASSWORD}" \
        -c "$COOKIE_FILE" -w "%{http_code}" -o /dev/null)
    # 新版 LuCI 返回 302 Found 表示登录成功
    [[ "$resp" == "302" ]] && return 0 || return 1
}

# 获取 sysauth token（兼容 sysauth 和 sysauth_http）
get_token() {
    grep sysauth "$COOKIE_FILE" 2>/dev/null | awk '{print $NF}'
}

# 执行远程命令（参数通过环境变量传递，避免 shell 转义问题）
rpc() {
    local token=$(get_token)
    [[ -z "$token" ]] && { echo "ERROR: not logged in"; return 1; }
    ROUTER_IP="$ROUTER_IP" RPC_AUTH="$token" RPC_CMD="$1" \
    python3 -c '
import os, json, urllib.request
req = urllib.request.Request(
    f"http://{os.environ[\"ROUTER_IP\"]}/cgi-bin/luci/rpc/sys?auth={os.environ[\"RPC_AUTH\"]}",
    data=json.dumps({"method": "exec", "params": [os.environ["RPC_CMD"]]}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read().decode())
print(data.get("result", "") or "")
' 2>/dev/null
}

show_leases() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}📋 DHCP 租约列表${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    
    # 动态租约
    local dhcp_data=$(rpc "cat /tmp/dhcp.leases 2>/dev/null")
    echo -e "${GREEN}  动态租约（DHCP自动分配）:${NC}"
    if [[ -n "$dhcp_data" ]]; then
        echo "$dhcp_data" | while IFS=' ' read -r expire mac ip name; do
            printf "  %-20s %-17s %s\n" "$ip" "$mac" "${name:-<未知>}"
        done
    else
        echo -e "  ${YELLOW}无动态租约数据${NC}"
    fi
    echo
    
    # 静态租约
    local uci_data=$(rpc "uci show dhcp 2>/dev/null | grep -E 'dhcp\\.@host\\[[0-9]+\\]\\.(name|ip|mac)='")
    echo -e "${GREEN}  静态租约（手动绑定）:${NC}"
    if [[ -n "$uci_data" ]]; then
        # 解析 UCI 数据，按 host 块分组输出
        echo "$uci_data" | awk -F'=' '
            /\.name=/ {
                gsub(/\047/, "", $2);
                name=$2;
                match($1, /\[[0-9]+\]/);
                idx=substr($1, RSTART, RLENGTH);
                names[idx]=name;
            }
            /\.ip=/ {
                gsub(/\047/, "", $2);
                ip=$2;
                match($1, /\[[0-9]+\]/);
                idx=substr($1, RSTART, RLENGTH);
                ips[idx]=ip;
            }
            /\.mac=/ {
                gsub(/\047/, "", $2);
                mac=$2;
                match($1, /\[[0-9]+\]/);
                idx=substr($1, RSTART, RLENGTH);
                macs[idx]=mac;
            }
            END {
                for (i in names) {
                    printf "  %-20s %-17s %s\n", ips[i], macs[i], names[i];
                }
            }
        '
    else
        echo -e "  ${YELLOW}无静态租约数据${NC}"
    fi
    echo
}

show_wifi() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}📶 WiFi 连接设备${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    local iface_data=$(rpc "iwinfo 2>/dev/null | grep ESSID" | head -5)
    local use_iw=false
    if [[ -z "$iface_data" ]]; then
        iface_data=$(rpc "iw dev 2>/dev/null | grep Interface | awk '{print \$2}'")
        use_iw=true
    fi
    if [[ -z "$iface_data" ]]; then
        echo -e "${YELLOW}  未能获取无线接口信息${NC}"
        echo
        return
    fi

    # 收集接口名到列表（$NF 兼容 iwinfo 和 iw dev 两种输出格式）
    local ifaces=()
    while IFS= read -r line; do
        ifaces+=("$(echo "$line" | awk '{print $NF}')")
    done <<< "$iface_data"

    # 打印接口信息
    if ! $use_iw; then
        while IFS= read -r line; do
            local iface=$(echo "$line" | awk '{print $1}')
            local ssid=$(echo "$line" | awk -F'"' '/ESSID/{print $2}')
            echo -e "  ${GREEN}接口:${NC} $iface  ${GREEN}SSID:${NC} ${ssid:-N/A}"
        done <<< "$iface_data"
    else
        for iface in "${ifaces[@]}"; do
            echo -e "  ${GREEN}接口:${NC} $iface"
        done
    fi

    # 获取关联设备（遍历所有接口）
    local assoc=""
    for iface in "${ifaces[@]}"; do
        assoc+=$(rpc "iwinfo $iface assoclist 2>/dev/null")
    done
    if [[ -z "$assoc" ]]; then
        echo -e "${YELLOW}  无 WiFi 设备连接或命令不支持${NC}"
    else
        echo "$assoc"
    fi
    echo
}

show_arp() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}🌐 ARP 活跃设备（有线+本地网络）${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    local data=$(rpc "cat /proc/net/arp")
    if [[ -z "$data" ]]; then
        echo -e "${YELLOW}  无活跃设备数据${NC}"
    else
        # 过滤掉标题行和无效MAC，在本地处理
        echo "$data" | grep -v 'IP address' | grep -v '00:00:00:00:00:00' | \
        while IFS=' ' read -r ip hw type flags mask mac; do
            printf "  %-20s %s\n" "$ip" "$mac"
        done
    fi
    echo
}

show_uptime() {
    local data=$(rpc "uptime")
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}⏱ 路由器运行状态${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "  $data"
    local conns=$(rpc "cat /proc/net/nf_conntrack 2>/dev/null | wc -l")
    echo -e "  当前活跃连接数: ${conns:-N/A}"
    echo
}

show_devices() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}📱 所有联网设备（综合查询）${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    
    # 获取各数据源
    local dhcp_data=$(rpc "cat /tmp/dhcp.leases")
    local uci_data=$(rpc "uci show dhcp")
    local arp_data=$(rpc "cat /proc/net/arp")
    local neigh_data=$(rpc "ip neigh show 2>/dev/null")
    local wifi_ifaces=$(rpc "iwinfo 2>/dev/null | grep ESSID | awk '{print \$1}'")
    local wifi_data=""
    for wiface in $wifi_ifaces; do
        wifi_data+=$(rpc "iwinfo $wiface assoclist 2>/dev/null")
    done
    
    # 通过环境变量传递给 Python，避免 shell 转义问题
    export DEV_DHCP="$dhcp_data"
    export DEV_UCI="$uci_data"
    export DEV_ARP="$arp_data"
    export DEV_NEIGH="$neigh_data"
    export DEV_WIFI="$wifi_data"
    
    python3 << 'PYEOF'
import os, re
from collections import OrderedDict

devices = OrderedDict()

# 1. 解析 ARP 表（获取所有已知设备的 IP→MAC）
arp_raw = os.environ.get("DEV_ARP", "")
for line in arp_raw.split("\n"):
    parts = line.split()
    if len(parts) >= 4 and parts[1] == "0x1":
        ip, mac = parts[0], parts[3]
        if mac != "00:00:00:00:00:00":
            devices[ip] = {"mac": mac.upper(), "name": "<未知>", "signal": "", "status": "不在线"}

# 2. 解析 ip neigh 表（准确在线状态）
neigh_raw = os.environ.get("DEV_NEIGH", "")
for line in neigh_raw.split("\n"):
    parts = line.split()
    if len(parts) >= 4 and parts[1] == "dev":
        ip = parts[0]
        state = parts[-1]  # 最后一个字段是状态
        if ip in devices and state in ("REACHABLE", "DELAY", "PROBE"):
            devices[ip]["status"] = "在线"

# 3. 解析 DHCP 动态租约
dhcp_raw = os.environ.get("DEV_DHCP", "")
for line in dhcp_raw.split("\n"):
    parts = line.split()
    if len(parts) >= 4:
        mac, ip, name = parts[1].upper(), parts[2], parts[3]
        if ip in devices and devices[ip]["name"] == "<未知>":
            devices[ip]["name"] = name
        elif ip not in devices:
            devices[ip] = {"mac": mac, "name": name, "signal": "", "status": "不在线"}

# 4. 解析 DHCP 静态租约（最高优先级）
uci_raw = os.environ.get("DEV_UCI", "")
host_data = {}
for line in uci_raw.split("\n"):
    m = re.match(r"dhcp\.@host\[(\d+)]\.(\w+)='(.*)'", line)
    if m:
        idx, key, val = m.groups()
        host_data.setdefault(idx, {})[key] = val
for entry in host_data.values():
    name = entry.get("name", "<未知>")
    ip = entry.get("ip", "")
    mac = entry.get("mac", "").upper()
    if ip:
        if ip in devices:
            devices[ip]["name"] = name
            if mac:
                devices[ip]["mac"] = mac
        else:
            devices[ip] = {"mac": mac, "name": name, "signal": "", "status": "不在线"}

# 5. 解析 WiFi 关联设备（WiFi 连接的设备必然在线）
wifi_signals = {}
wifi_raw = os.environ.get("DEV_WIFI", "")
for line in wifi_raw.split("\n"):
    m = re.match(r"([0-9A-Fa-f:]{17})\s+(-\d+ dBm)", line)
    if m:
        wifi_signals[m.group(1).upper()] = m.group(2)

for info in devices.values():
    mac = info.get("mac", "").upper()
    if mac in wifi_signals:
        info["signal"] = wifi_signals[mac]
        info["status"] = "在线"  # WiFi 设备一定在线

# 输出
count = 1
for ip, info in devices.items():
    name = info["name"]
    mac = info["mac"]
    signal = info["signal"]
    status = info["status"]
    wifi_flag = "\U0001f4f6" if signal else "  "

    if signal:
        print(f"  {count:2d}. {wifi_flag} {status}  {ip:20s}  {mac:17s}  {name:30s}  {signal}")
    else:
        print(f"  {count:2d}. {wifi_flag} {status}  {ip:20s}  {mac:17s}  {name:30s}")
    count += 1

if count == 1:
    print("  (无设备数据)")
PYEOF
    
    echo -e "\n${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}💡 状态判断: WiFi连接=在线 | ip neigh REACHABLE/DELAY/PROBE=在线 | 其他=不在线${NC}"
    echo -e "${CYAN}   (不依赖 arp_flags，已弃用旧规则)${NC}"
    echo -e "${CYAN}💰 名称来源: 静态租约 > 动态租约${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo
}

# Main
echo ""
echo -e "${GREEN}🔐 正在登录 ${ROUTER_IP} ...${NC}"
if login; then
    echo -e "${GREEN}✅ 登录成功！${NC}\n"
    
    case "$ACTION" in
        devices) show_devices ;;
        leases) show_leases ;;
        wifi)   show_wifi ;;
        arp)    show_arp ;;
        uptime) show_uptime ;;
        all|*)
            show_uptime
            show_devices
            show_leases
            show_arp
            show_wifi
            ;;
    esac
else
    echo -e "${RED}❌ 登录失败！请检查 IP 地址和密码${NC}"
    exit 1
fi
