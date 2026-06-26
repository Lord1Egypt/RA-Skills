#!/usr/bin/env python3
"""
iKuai 流量报表生成器
从 ikuai-cli 收集真实数据，替换 template.html 中的硬编码假数据，
输出 /tmp/ikuai-report.html
"""

import subprocess, json, re, shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATE  = SKILL_DIR / "assets" / "template.html"
OUTPUT    = Path("/tmp/ikuai-report.html")

# ── auto-detect ikuai-cli ────────────────────────────────────
CLI = shutil.which("ikuai-cli") or (Path.home() / ".local" / "bin" / "ikuai-cli").as_posix()

# ── check auth ────────────────────────────────────────────────
def check_auth():
    r = subprocess.run([CLI, "auth", "status"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"❌ ikuai-cli 执行失败: {r.stderr.strip()}")
        return False
    try:
        j = json.loads(r.stdout)
        has_url    = bool(j.get("base_url") or j.get("url"))
        has_cred   = bool(j.get("source") == "token" or j.get("token"))
        if not has_url or not has_cred:
            print("❌ ikuai-cli 未完成认证配置，请先运行:")
            print(f"   ikuai-cli auth set-url  <路由器IP>   # 例如: ikuai-cli auth set-url http://10.10.10.253")
            print(f"   ikuai-cli auth set-token <token>      # 在路由器 Web UI 获取")
            return False
        return True
    except Exception:
        pass
    # Fallback: try a simple API call to verify connectivity
    r2 = subprocess.run([CLI, "monitor", "system", "--format", "json"],
                        capture_output=True, text=True)
    if r2.returncode != 0 or not r2.stdout.strip():
        print("❌ ikuai-cli 连接失败，请检查 auth 配置")
        return False
    return True

# ── helpers ───────────────────────────────────────────────────

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        return j.get("results", j)
    except:
        return {}


def fmtB(b):
    try:
        b = int(b)
        if b >= 1e12: return f"{b/1e12:.2f} TB"
        if b >= 1e9:  return f"{b/1e9:.2f} GB"
        if b >= 1e6:  return f"{b/1e6:.2f} MB"
        if b >= 1e3:  return f"{b/1e3:.2f} KB"
        return f"{b} B"
    except:
        return "—"


def fmtK(b):
    try:
        b = int(b)
        if b >= 1e6: return f"{b/1e6:.2f} Mbps"
        if b >= 1e3: return f"{b/1e3:.1f} Kbps"
        return f"{b} bps"
    except:
        return "—"

def uptime_fmt(s):
    try:
        s = int(s)
        d, r = divmod(s, 86400)
        h, r = divmod(r, 3600)
        m, _ = divmod(r, 60)
        if d > 0: return f"{d}d {h}h {m}m"
        if h > 0: return f"{h}h {m}m"
        return f"{m}m"
    except:
        return "—"

def js_str(s):
    return json.dumps(str(s), ensure_ascii=False)


# ── collect data ──────────────────────────────────────────────

if not check_auth():
    raise SystemExit(1)

print(f"📡 正在收集 iKuai 路由器数据...")
print(f"   CLI: {CLI}")

system    = run([CLI, "monitor", "system",                "--format", "json"])
trafSum   = run([CLI, "monitor", "traffic-summary",       "--format", "json"])
appTraf   = run([CLI, "monitor", "app-traffic-summary",  "--format", "json"])
protocols = run([CLI, "monitor", "protocols",            "--format", "json"])
clients   = run([CLI, "monitor", "clients-online",       "--format", "json"])
phy       = run([CLI, "monitor", "interfaces-physical",  "--format", "json"])
wan_list  = run([CLI, "network", "wan",                  "--format", "json"])
lan_list  = run([CLI, "network", "lan", "list",         "--format", "json"])
dns_get   = run([CLI, "network", "dns", "get",           "--format", "json"])
acl_list  = run([CLI, "security", "acl", "list",         "--format", "json"])
qos_list  = run([CLI, "qos", "ip", "list",               "--format", "json"])
log_list  = run([CLI, "log", "system", "list",           "--format", "json", "--human-time"])
dnat_list = run([CLI, "network", "dnat", "list",         "--format", "json"])

# ── parse ────────────────────────────────────────────────────

si         = system.get("sysinfo", {})
hostname   = si.get("hostname", "iKuai")
version    = si.get("verstring", si.get("version", "未知"))
uptime_s   = int(si.get("uptime", 0))
cpu_list   = si.get("cpu", [])
mem_info   = si.get("memory", {})
online_cnt = si.get("online_user", {}).get("count", 0)
stream     = si.get("stream", {})
total_down = int(stream.get("total_down", 0))
total_up   = int(stream.get("total_up", 0))
conn_num   = stream.get("connect_num", 0)
down_rate  = float(stream.get("download", 0))
up_rate    = float(stream.get("upload", 0))
total_flow = total_down + total_up

terms = trafSum.get("terminal", [])
terms.sort(key=lambda x: int(x.get("sum_total", 0)), reverse=True)

proto3_day        = appTraf.get("proto3_day", [])
proto3_flow_total = int(appTraf.get("proto3_day_total_flow", 0))
proto3_day.sort(key=lambda x: int(x.get("total", 0)), reverse=True)

proto_data = protocols.get("data", [])
proto_data.sort(key=lambda x: int(x.get("total", 0)), reverse=True)

client_list  = clients.get("data", [])
client_total = int(clients.get("total", 0))

wan  = wan_list.get("data", [{}])[0] if wan_list.get("data") else {}
lan  = lan_list.get("data", [{}])[0] if lan_list.get("data") else {}
dnsd = dns_get.get("data", [{}])[0] if dns_get.get("data") else {}

wan_ip   = wan.get("dhcp_ip_addr", wan.get("pppoe_ip_addr", "—"))
wan_gw   = wan.get("dhcp_gateway", wan.get("pppoe_gateway", "—"))
wan_dns1 = wan.get("dhcp_dns1", "—")
wan_dns2 = wan.get("dhcp_dns2", "—")
wan_mtu  = wan.get("mtu", "—")
wan_type = {2: "DHCP"}.get(wan.get("dhcp_status"), "PPPoE" if wan.get("pppoe_status") else "—")
wan_link = "已连接" if wan.get("internet") == 1 else "未连接"

lan_ip   = lan.get("ip_mask", "?").split("/")[0] if lan.get("ip_mask") else "—"
lan_mask = lan.get("ip_mask", "?").split("/")[1] if "/" in lan.get("ip_mask", "") else "—"
dhcp_en  = "已启用" if lan.get("dhcp_server") == 1 else "未启用"
vlan_name = lan.get("vlan", "")

dns1     = dnsd.get("dns1", "—")
dns2     = dnsd.get("dns2", "—")
dns_fwd  = "已启用" if dnsd.get("enabled") == "yes" else "未启用"

acl_count  = acl_list.get("total", 0)
qos_count  = qos_list.get("total", 0)
dnat_rules = dnat_list.get("data", [])
dnat_count = len(dnat_rules)

log_items = log_list.get("data", [])[:20]
ether     = phy.get("ether_info", {})

proto_flow_total = sum(int(p.get("total", 0)) for p in proto_data) or 1

# ── build arrays ─────────────────────────────────────────────

def arr_proto():
    out = []
    for p in proto_data[:15]:
        out.append(f'{{name:{js_str(p.get("proto_name","?"))},total:{p.get("total",0)}}}')
    return "[" + ",".join(out) + "]"

def arr_apps():
    out = []
    for a in proto3_day[:20]:
        out.append(
            f'{{name:{js_str(a.get("appname","?"))},'
            f'cat:{js_str(a.get("appname_level1","?"))},'
            f'sub:{js_str(a.get("appname_level2","?"))},'
            f'down:{a.get("total_down",0)},'
            f'up:{a.get("total_up",0)},'
            f'total:{a.get("total",0)}}}'
        )
    return "[" + ",".join(out) + "]"

def arr_terminals():
    out = []
    for t in terms[:20]:
        out.append(
            f'{{ip:{js_str(t.get("ip_addr","?"))},'
            f'mac:{js_str(t.get("mac","?"))},'
            f'down:{t.get("sum_total_down",0)},'
            f'up:{t.get("sum_total_up",0)},'
            f'total:{t.get("sum_total",0)},'
            f'type:{js_str(t.get("client_type","Unknown"))}}}'
        )
    return "[" + ",".join(out) + "]"

def arr_online():
    out = []
    for c in client_list[:20]:
        out.append(
            f'{{ip:{js_str(c.get("ip_addr","?"))},'
            f'hostname:{js_str(c.get("hostname",c.get("termname","")))},'
            f'vendor:{js_str(c.get("client_vendor","Unknown"))},'
            f'conn:{c.get("connect_num",0)}}}'
        )
    return "[" + ",".join(out) + "]"

def arr_logs():
    out = []
    for l in log_items[:20]:
        content = l.get("content", "")
        ts      = l.get("timestamp", "")
        s = "warn" if ("关闭" in content or "断开" in content) else \
            "ok"  if ("启动" in content or "成功" in content or "连接" in content) else "info"
        out.append(f'{{t:{js_str(ts)},c:{js_str(content)},s:{js_str(s)}}}')
    return "[" + ",".join(out) + "]"

def arr_sources():
    out = []
    for item in [
        (f"{CLI} monitor system --format json",               system),
        (f"{CLI} monitor traffic-summary --format json",     trafSum),
        (f"{CLI} monitor app-traffic-summary --format json", appTraf),
        (f"{CLI} monitor protocols --format json",          protocols),
        (f"{CLI} monitor clients-online --format json",      clients),
        (f"{CLI} monitor interfaces-physical --format json",phy),
        (f"{CLI} network wan --format json",                wan),
        (f"{CLI} network lan list --format json",           lan),
        (f"{CLI} network dns get --format json",           dnsd),
        (f"{CLI} security acl list --format json",          acl_list),
        (f"{CLI} qos ip list --format json",              qos_list),
        (f"{CLI} log system list --format json --human-time",log_list),
    ]:
        out.append(f'{{cmd:{js_str(item[0])},out:{js_str(json.dumps(item[1])[:120])}}}')
    return "[" + ",".join(out) + "]"

print(f"✅ 数据收集完成: {hostname} | 在线{online_cnt}台 | 总流量{fmtB(total_flow)}")

# ── read template ─────────────────────────────────────────────

raw = TEMPLATE.read_text(encoding="utf-8")
lines = raw.split("\n")

# Find the line index for each array's [ line and its ]; line
# We detect "const NAME=[" lines and the nearest subsequent "]; " line
def find_array_range(arr_name):
    start = None
    for i, line in enumerate(lines):
        if f"const {arr_name}=[" in line:
            start = i
        elif start is not None and line.strip() == "];":
            return start, i
    return None, None

replacements = {}
for arr_name, fn in [
    ("protocols",      arr_proto),
    ("apps",          arr_apps),
    ("terminals",     arr_terminals),
    ("onlineClients", arr_online),
    ("logs",          arr_logs),
    ("sources",       arr_sources),
]:
    s, e = find_array_range(arr_name)
    if s is not None:
        replacements[arr_name] = (s, e)
        val = fn()
        print(f"  ✅ {arr_name}: lines {s+1}–{e+1} ({e-s} lines)")
    else:
        print(f"  [WARN] {arr_name}: not found in template")

# Build new lines list
new_lines = lines[:]
# Apply in reverse order so earlier indices stay valid
for arr_name, (s, e) in sorted(replacements.items(), key=lambda x: -x[1][0]):
    val = {
        "protocols":      arr_proto(),
        "apps":           arr_apps(),
        "terminals":      arr_terminals(),
        "onlineClients":  arr_online(),
        "logs":           arr_logs(),
        "sources":        arr_sources(),
    }[arr_name]
    indent = "  "
    # Build lines: "const NAME = DATA;" as one line
    new_array_line = f"const {arr_name}={val};"
    # Replace lines[s..e] (inclusive) with new_array_line
    new_lines = new_lines[:s] + [new_array_line] + new_lines[e+1:]

html = "\n".join(new_lines)

# ── fix scalar variables (const NAME=...; in JS section) ──────
# These appear in the <script> block as single-line declarations
scalar_patts = {
    "totalDown":      str(total_down),
    "totalUp":        str(total_up),
    "totalFlow":      str(total_down + total_up),
    "onlineCnt":      str(online_cnt),
    "termTotal":      str(len(terms)),
    "connectNum":     str(conn_num),
    "downRate":       str(down_rate),
    "upRate":         str(up_rate),
    "wanIP":          js_str(wan_ip),
    "wanGW":          js_str(wan_gw),
    "wanDNS1":        js_str(wan_dns1),
    "wanDNS2":        js_str(wan_dns2),
    "wanType":        js_str(wan_type),
    "wanLink":        js_str(wan_link),
    "lanIP":          js_str(lan_ip),
    "lanMask":        js_str(lan_mask),
    "dhcpEn":         js_str(dhcp_en),
    "vlanName":       js_str(vlan_name),
    "dns1":           js_str(dns1),
    "dns2":           js_str(dns2),
    "dnsForward":     js_str(dns_fwd),
    "aclCount":       str(acl_count),
    "qosCount":       str(qos_count),
    "dnatCount":      str(dnat_count),
    "protoFlowTotal": str(proto_flow_total),
    "appFlowTotal":   str(proto3_flow_total),
}
for name, val in scalar_patts.items():
    # Match "const NAME=...;" (without space before ;)
    pat = rf'(const {re.escape(name)}\s*=\s*)[^;]+;'
    repl = f'const {name}={val};'
    if re.search(pat, html):
        html = re.sub(pat, repl, html)
    else:
        pass  # template may not have this variable; skip silently

# ── fix HTML text placeholders ────────────────────────────────
cpu_avg = f"均值 {sum(float(c.strip('%')) for c in cpu_list if c.strip('%')) / max(len(cpu_list), 1):.2f}%"
for old, new in [
    ("4.0.210-beta x64",                     version),
    ("10.10.10.253",                        lan_ip),
    ("10.64.211.237",                       wan_ip),
    ("24 / 28",                             f"{client_total} / {len(terms)}"),
    ("28 台",                               f"{len(terms)} 台"),
    ("24 台",                               f"{online_cnt} 台"),
    ("4d 16h 0m",                           uptime_fmt(uptime_s)),
    ("均值 2.34%",                           cpu_avg),
    ("222.71 GB",                           fmtB(total_down)),
    ("26.83 GB",                            fmtB(total_up)),
    ("283.1K",                              fmtK(down_rate)),
    ("331",                                 str(conn_num)),
    ("38.89 GB",                            fmtB(proto3_flow_total)),
    ("20 个应用",                           f"{len(proto3_day)} 个应用"),
    ("20 台设备",                            f"{len(terms)} 台设备"),
    ("160 条",                              f"{len(log_items)} 条"),
    ("24台",                                f"{client_total}台"),
    ("共 160 条",                           f"共 {len(log_items)} 条"),
    ("4.0.210 Build 202604161034",           version),
    ("2026-04-16",                          str(si.get("verinfo", {}).get("build_date", ""))[:8] if si.get("verinfo", {}).get("build_date") else ""),
]:
    if old in html:
        html = html.replace(old, new)

OUTPUT.write_text(html, encoding="utf-8")
print(f"\n✅ 报表已生成: {OUTPUT}")
print(f"   浏览器打开: file:///{OUTPUT}")
