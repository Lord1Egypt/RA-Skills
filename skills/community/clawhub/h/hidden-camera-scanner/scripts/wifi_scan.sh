#!/usr/bin/env bash
#
# hidden-camera-scanner · wifi_scan.sh
# 局域网扫描：发现联网设备并标记疑似监控摄像头 / NVR（反偷拍排查阶段①）。
#
# 合规定位：目的是帮助用户保护自身隐私、发现针对自己的非法偷拍设备。
#   - 只做被动的设备发现与端口探测，不登录任何设备、不利用漏洞、不访问摄像头视频流；
#   - 仅扫描你本人已连接、有权限的网络；nmap 等会主动发送探测包，运行前须确认范围并获得授权；
#   - 扫到监控厂商设备 ≠ 有人在偷拍，需结合场景与人工排查确认。
#
# 依赖（可选，自动降级）：
#   nmap  : 推荐。主机发现 + MAC 厂商识别 + 端口扫描（macOS: brew install nmap）
#   无 nmap: 回退到 ping 探测 + arp -a + bash /dev/tcp 端口探测（macOS 原生，免安装）
#
# 用法：
#   ./wifi_scan.sh [--subnet 192.168.1.0/24] [--ports 554,8554,...] [--out result.json] [--no-portscan]
#
# 输出：JSON 到 stdout；--out 时同时写入文件；人类可读摘要到 stderr。

set -uo pipefail

SURVEIL_PORTS="554,8554,3702,80,8080,443,8000,34567,37777,8899,23,21,1900,9999,49152"
SUBNET=""
OUT_FILE=""
DO_PORTSCAN=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --subnet) SUBNET="$2"; shift 2;;
    --ports)  SURVEIL_PORTS="$2"; shift 2;;
    --out)    OUT_FILE="$2"; shift 2;;
    --no-portscan) DO_PORTSCAN=0; shift;;
    -h|--help) grep -E '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
    *) echo "未知参数: $1" >&2; exit 1;;
  esac
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
NMAP_HOSTS="$TMP/nmap_hosts.gnmap"
NMAP_PORTS="$TMP/nmap_ports.gnmap"
ARP_FILE="$TMP/arp.txt"
FALLBACK_PORTS="$TMP/fallback_ports.txt"
JSON_OUT="$TMP/result.json"
: > "$FALLBACK_PORTS"

have_nmap() { command -v nmap >/dev/null 2>&1; }

IS_DARWIN=0
IS_WIN=0
case "$(uname -s)" in
  Darwin) IS_DARWIN=1;;
  MINGW*|MSYS*|CYGWIN*) IS_WIN=1;;   # Git Bash / MSYS2 / Cygwin
esac

# 获取默认网卡与子网，兼容 macOS / Windows(Git Bash) / Linux(Termux)
get_subnet() {
  local iface ip
  if [[ "$IS_DARWIN" -eq 1 ]]; then
    iface="$(route -n get default 2>/dev/null | awk '/interface:/{print $2}')"
    ip="$(ipconfig getifaddr "$iface" 2>/dev/null)"
  elif [[ "$IS_WIN" -eq 1 ]]; then
    # 有默认网关的接口的 IPv4 地址（locale 无关）
    ip="$(powershell.exe -NoProfile -Command "(Get-NetIPConfiguration | Where-Object {\$_.IPv4DefaultGateway} | Select-Object -First 1).IPv4Address.IPAddress" 2>/dev/null | tr -d '\r\n')"
  else
    iface="$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="dev") print $(i+1); exit}')"
    ip="$(ip -4 addr show "$iface" 2>/dev/null | grep -oE 'inet [0-9.]+' | awk '{print $2}' | cut -d/ -f1)"
  fi
  [[ -z "$ip" ]] && return
  echo "${ip%.*}.0/24"
}

if [[ -z "$SUBNET" ]]; then
  SUBNET="$(get_subnet)"
  if [[ -z "$SUBNET" ]]; then
    echo "无法确定本地子网，请用 --subnet 指定（如 192.168.1.0/24）" >&2
    exit 1
  fi
fi

echo "▶ 扫描子网: $SUBNET" >&2

if have_nmap; then
  echo "▶ [nmap] 主机发现..." >&2
  nmap -sn -T4 "$SUBNET" -oG "$NMAP_HOSTS" >/dev/null 2>&1
  if [[ "$DO_PORTSCAN" -eq 1 ]]; then
    echo "▶ [nmap] 端口扫描（监控相关端口: ${SURVEIL_PORTS}）..." >&2
    nmap -Pn -p "$SURVEIL_PORTS" --open "$SUBNET" -oG "$NMAP_PORTS" >/dev/null 2>&1
  fi
else
  case "$(uname -s)" in
    Darwin)   NMAP_HINT="brew install nmap";;
    MINGW*|MSYS*|CYGWIN*) NMAP_HINT="winget install Insecure.Nmap（勾选 Npcap）；勿用 WSL2";;
    Linux)    if [[ -n "${TERMUX_VERSION:-}" ]]; then NMAP_HINT="pkg install nmap"; else NMAP_HINT="sudo apt install nmap 或 dnf install nmap"; fi;;
    *)        NMAP_HINT="安装 nmap（见 references/platforms.md）";;
  esac
  echo "▶ 未检测到 nmap，回退到 ping + ARP 表探测（厂商识别能力弱）。建议: $NMAP_HINT" >&2
  read -r o1 o2 o3 _ <<<"$(echo "$SUBNET" | sed 's#/.*##;s/\./ /g')"
  if [[ "$IS_DARWIN" -eq 1 ]]; then PING_ARGS="-c1 -t1"
  elif [[ "$IS_WIN" -eq 1 ]]; then PING_ARGS="-n 1 -w 1000"
  else PING_ARGS="-c1 -W1"; fi
  for i in $(seq 1 254); do
    ( ping $PING_ARGS "$o1.$o2.$o3.$i" >/dev/null 2>&1 ) &
    (( i % 40 == 0 )) && wait
  done
  wait
  if [[ "$IS_DARWIN" -eq 1 ]]; then
    arp -a -n > "$ARP_FILE" 2>/dev/null      # 格式: ? (ip) at mac ...
  elif [[ "$IS_WIN" -eq 1 ]]; then
    # Windows arp -a: "ip  aa-bb-cc-dd-ee-ff  动态/dynamic" -> 归一为 "ip mac"（冒号分隔），过滤组播
    arp -a 2>/dev/null | awk '{n=split($2,m,"-"); if(n==6 && $1 !~ /^(224|239|255)\./){mac=tolower($2); gsub(/-/ ,":",mac); print $1, mac}}' > "$ARP_FILE"
  else
    # Linux/Termux: ip neigh -> 归一为 "ip mac" 两列
    ip neigh show 2>/dev/null | awk '{ip=$1; for(i=1;i<=NF;i++) if($i=="lladdr") print ip, $(i+1)}' > "$ARP_FILE"
  fi
  if [[ "$DO_PORTSCAN" -eq 1 ]]; then
    echo "▶ 端口探测（bash /dev/tcp，仅监控相关端口）..." >&2
    while read -r ip; do
      for p in ${SURVEIL_PORTS//,/ }; do
        if (exec 3<>"/dev/tcp/$ip/$p") 2>/dev/null; then
          exec 3>&- 3<&-
          echo "$ip $p" >> "$FALLBACK_PORTS"
        fi
      done
    done < <(grep -oE '\(([0-9]+\.){3}[0-9]+\)' "$ARP_FILE" | tr -d '()' | sort -u)
  fi
fi

# ---- 解析 + 标记 + 输出（单次 Python，结果落 JSON_OUT，再按需复制）----
export NMAP_HOSTS NMAP_PORTS ARP_FILE FALLBACK_PORTS SUBNET JSON_OUT
python3 <<'PYEOF'
import sys, re, json, os

nmap_hosts   = os.environ["NMAP_HOSTS"]
nmap_ports   = os.environ["NMAP_PORTS"]
arp_file     = os.environ["ARP_FILE"]
fallback_ports = os.environ["FALLBACK_PORTS"]
subnet       = os.environ["SUBNET"]
json_out     = os.environ["JSON_OUT"]

# 监控厂商关键字（匹配 nmap MAC 厂商字段，小写比较；见 references/vendors_ports.md）
SURVEIL_KEYWORDS = [
    "hikvision","海康","hangzhou hikvision","dahua","大华","reolink","axis",
    "ezviz","萤石","imou","乐橙","uniview","宇视","tp-link","xiaomi","小米",
    "d-link","foscam","yi tech","小蚁","amcrest","wyze","lorex","swann","tend",
    "wansview","tenvis","geovision","奇偶","vivotek","mobotix","hanwha",
    "bosch","panasonic","sony","netatmo","nest",
]
PORT_MEANING = {
    "554":"RTSP 视频流","8554":"RTSP 备用","3702":"ONVIF 设备发现",
    "80":"HTTP 管理界面","8080":"HTTP 管理界面","443":"HTTPS 管理界面",
    "8000":"海康威视 ISAPI/SDK","34567":"大华私有协议","37777":"大华私有协议",
    "8899":"大华/通用私有","23":"Telnet(高危)","21":"FTP","1900":"UPnP/SSDP",
    "9999":"厂商私有","49152":"厂商私有",
}
HIGH_PORTS = {"554","8554","3702","8000","34567","37777"}

hosts = {}

def add(ip):
    if ip not in hosts:
        hosts[ip] = {"ip": ip, "mac": "", "vendor": "", "vendor_suspect": False,
                     "open_ports": [], "flags": []}
    return hosts[ip]

# 回退：解析 ARP 文件（两种格式：macOS `? (ip) at mac`；Linux 归一化的 `ip mac`）
if os.path.exists(arp_file):
    for line in open(arp_file, errors="ignore"):
        m = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17})', line)
        if not m:
            m = re.match(r'^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17})\b', line.strip())
        if m:
            add(m.group(1))["mac"] = m.group(2).lower()

# nmap 主机 + MAC + 厂商（gnmap：MAC 行紧跟对应 Host 行，按最近 Host 关联）
cur_ip = None
if os.path.exists(nmap_hosts):
    for line in open(nmap_hosts, errors="ignore"):
        if line.startswith("Host:") and "Status: Up" in line:
            m = re.search(r'Host:\s+(\S+)', line)
            if m:
                cur_ip = m.group(1); add(cur_ip)
        elif "MAC Address:" in line and cur_ip:
            m = re.search(r'MAC Address:\s+([0-9A-F:]{17})\s+\(([^)]*)\)', line)
            if m:
                h = add(cur_ip)
                h["mac"] = m.group(1).lower()
                h["vendor"] = m.group(2).strip()

def ingest(ip, port):
    h = add(ip)
    if port not in h["open_ports"]:
        h["open_ports"].append(port)

# 端口：nmap gnmap 或回退文件
if os.path.exists(nmap_ports):
    for line in open(nmap_ports, errors="ignore"):
        if line.startswith("Host:") and "Ports:" in line:
            m = re.search(r'Host:\s+(\S+).*?Ports:\s*(.*)', line)
            if m:
                for seg in m.group(2).split(","):
                    pm = re.search(r'(\d+)/open/', seg)
                    if pm:
                        ingest(m.group(1), pm.group(1))
if os.path.exists(fallback_ports):
    for line in open(fallback_ports, errors="ignore"):
        line = line.strip()
        if line:
            ip, port = line.split()
            ingest(ip, port)

# 标记
for h in hosts.values():
    v = h["vendor"].lower()
    if any(k in v for k in SURVEIL_KEYWORDS):
        h["vendor_suspect"] = True
        h["flags"].append("厂商命中监控关键字")
    for p in h["open_ports"]:
        meaning = PORT_MEANING.get(p, "未知服务")
        if p in HIGH_PORTS:
            h["flags"].append(f"开放高危监控端口 {p}({meaning})")
        else:
            h["flags"].append(f"开放端口 {p}({meaning})")

isolation = len(hosts) <= 2
result = {
    "scan_type": "wifi",
    "subnet": subnet,
    "tool": "nmap" if (os.path.exists(nmap_hosts) and os.path.getsize(nmap_hosts) > 0) else "arp-fallback",
    "client_isolation_suspected": isolation,
    "host_count": len(hosts),
    "hosts": sorted(hosts.values(), key=lambda x: x["ip"]),
}
out = json.dumps(result, ensure_ascii=False, indent=2)
with open(json_out, "w") as f:
    f.write(out)
print(out)

# 人类可读摘要（stderr）
e = sys.stderr
print("\n=== Wi-Fi 扫描摘要 ===", file=e)
print(f"子网: {subnet} | 工具: {result['tool']} | 发现设备: {len(hosts)} 台", file=e)
if isolation:
    print("⚠️ 疑似客户端隔离：仅发现极少设备，无法扫描其他联网设备 → 建议转人工排查（阶段④）", file=e)
sus = [h for h in hosts.values() if h["flags"]]
if not sus:
    print("未标记可疑设备（不代表安全：蜂窝/其他 Wi-Fi/纯本地存储的摄像头不可见）", file=e)
for h in sus:
    print(f"  可疑 {h['ip']}  MAC {h['mac'] or '?'}  厂商[{h['vendor'] or '未知'}]", file=e)
    for f in h["flags"]:
        print(f"    - {f}", file=e)
print("提示：以上仅为设备发现结果，发现监控厂商设备不等于偷拍，需结合场景与人工排查确认。", file=e)
PYEOF
RC=$?

if [[ $RC -eq 0 && -n "$OUT_FILE" ]]; then
  cp "$JSON_OUT" "$OUT_FILE"
  echo "▶ JSON 已写入: $OUT_FILE" >&2
fi
exit $RC
