#!/usr/bin/env python3
"""outage_warlord.py — scope home internet outages, log evidence, build ISP complaints.

Offline-friendly: stdlib only (socket, subprocess ping, urllib.request).
Log: outage_log.jsonl beside the script. Commands: diagnose | monitor | report | log-equip | log-linesn
Verdicts: DEVICE | WIFI | LAN | ROUTER-WAN | DNS | ISP | PLATFORM | UPSTREAM-OK
"""
import argparse
import json
import platform
import re
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG = Path(__file__).resolve().parent / "outage_log.jsonl"
DNS_TARGETS = ["example.com", "cloudflare.com", "gnu.org"]
ANYCAST = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]
HTTP_TARGETS = ["https://www.cloudflare.com", "https://www.gnu.org", "https://example.com"]
PING_TIMEOUT_S = 2


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_log(log, rec):
    with open(log, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ------------------------------------------------------------------ probes
def gateway_ip():
    """Default gateway from the OS routing table."""
    system = platform.system()
    try:
        if system == "Linux":
            out = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5).stdout
            m = re.search(r"via (\d+\.\d+\.\d+\.\d+)", out)
            return m.group(1) if m else None
        if system == "Darwin":
            out = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True, timeout=5).stdout
            m = re.search(r"gateway: (\d+\.\d+\.\d+\.\d+)", out)
            return m.group(1) if m else None
        out = subprocess.run(["powershell", "-c", "(Find-NetRoute -RemoteIPAddress 1.1.1.1).NextHop[0]"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        return out or None
    except Exception:
        return None


def ping(host, count=3, timeout=PING_TIMEOUT_S):
    """Returns (ok, avg_ms or None, loss_pct)."""
    system = platform.system()
    flag = "-c" if system != "Windows" else "-n"
    tflag = "-W" if system != "Windows" else "-w"
    tval = str(timeout * 1000) if system == "Windows" else str(timeout)
    try:
        cmd = ["ping", flag, str(count), tflag, tval, host]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * count + 5).stdout
        ok = ("ttl=" in out.lower()) or ("time=" in out.lower()) or (", 0% loss" in out.lower()) or ("(0% loss)" in out.lower())
        times = [float(x) for x in re.findall(r"time[=<]([\d.]+) ms", out)]
        loss_m = re.search(r"(\d+)% (?:packet )?loss", out)
        loss = int(loss_m.group(1)) if loss_m else (0 if ok else 100)
        return ok, (sum(times) / len(times) if times else None), loss
    except Exception:
        return False, None, 100


def resolve(name, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        return socket.gethostbyname(name)
    except Exception:
        return None


def http_head(url, timeout=5):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "outage-warlord/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False


def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ANYCAST[0], 53))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


# ------------------------------------------------------------------ diagnose
def diagnose(log, degrade=False, target=None, simulate=None, verbose=True):
    rec = {"ts": now_iso(), "type": "probe", "layers": {}, "verdict": None}
    if simulate:
        # demo/test mode: fabricate layer results for the given scenario
        scen = {
            "device": {"ip": False},
            "wifi": {"ip": True, "gw": False},
            "lan": {"ip": True, "gw": False},
            "router-wan": {"ip": True, "gw": True, "dns": False, "anycast": False},
            "dns": {"ip": True, "gw": True, "dns": False, "anycast": True, "http": False},
            "isp": {"ip": True, "gw": True, "dns": False, "anycast": False},
            "platform": {"ip": True, "gw": True, "dns": True, "anycast": True, "http": False, "target_only": True},
        }[simulate]
        rec["simulated"] = simulate
        rec["layers"] = scen
        verdict = simulate.upper()
        rec["verdict"] = verdict
        append_log(log, rec)
        if verbose:
            print_report_like(verdict, scen, simulated=True, target=target)
        return verdict

    # layer 1: device link
    ip = local_ip()
    rec["layers"]["ip"] = bool(ip and not ip.startswith("169.254"))
    if not rec["layers"]["ip"]:
        rec["verdict"] = "DEVICE"
        append_log(log, rec)
        if verbose:
            print_report_like("DEVICE", rec["layers"])
        return "DEVICE"

    # layer 2/3: gateway
    gw = gateway_ip()
    rec["layers"]["gw_ip"] = gw
    if gw:
        gw_ok, gw_ms, _ = ping(gw)
        rec["layers"]["gw"] = gw_ok
        if not gw_ok:
            rec["verdict"] = "WIFI-OR-LAN"
            append_log(log, rec)
            if verbose:
                print_report_like("WIFI-OR-LAN", rec["layers"], gw=gw)
            return "WIFI-OR-LAN"
    else:
        # gateway undeterminable (container/exotic env): skip layer, note it
        rec["layers"]["gw"] = None

    # layer 5: DNS
    dns_results = {d: resolve(d) for d in DNS_TARGETS}
    rec["layers"]["dns"] = {d: bool(v) for d, v in dns_results.items()}
    dns_any = any(dns_results.values())

    # layer 4/6: anycast IPs
    any_ok = False
    any_stats = {}
    for ipa in ANYCAST:
        ok, ms, loss = ping(ipa, count=10 if degrade else 3)
        any_stats[ipa] = {"ok": ok, "avg_ms": ms, "loss": loss}
        any_ok = any_ok or ok
    rec["layers"]["anycast"] = any_stats
    rec["layers"]["anycast_ok"] = any_ok

    # HTTP layer (works even where ICMP is filtered — clouds, some carriers)
    http_results = {u: http_head(u) for u in HTTP_TARGETS}
    rec["layers"]["http"] = http_results
    http_any = any(http_results.values())

    verdict = None
    if not any_ok and not dns_any and not http_any:
        verdict = "ISP"
    elif not dns_any and (any_ok or http_any):
        verdict = "DNS"
    elif http_any:
        if target:
            t_ok = bool(resolve(target)) or http_head(f"https://{target}")
            rec["layers"]["target"] = {target: t_ok}
            if not t_ok:
                verdict = "PLATFORM"
        if verdict is None:
            verdict = "UPSTREAM-OK"
            if not any_ok:
                rec["layers"]["note"] = "ICMP filtered on this network; verdict from DNS+HTTP"
    else:
        # ping ok or dns ok, but no HTTP: middlebox/MTU/CGNAT symptoms
        verdict = "ROUTER-WAN"
    rec["verdict"] = verdict
    append_log(log, rec)
    if verbose:
        print_report_like(verdict, rec["layers"], gw=gw, degrade=degrade, target=target)
    return verdict


def print_report_like(verdict, layers, gw=None, degrade=False, target=None, simulated=False):
    print(f"VERDICT: {verdict}" + ("  [simulated]" if simulated else ""))
    print(f"  layers: " + json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()}) for k, v in layers.items()}, default=str)[:300])
    presc = {
        "DEVICE": ["check cable / Wi-Fi toggle / airplane mode", "ip a  (Linux) or ipconfig (Win) — look for a real IP, not 169.254.x.x"],
        "WIFI-OR-LAN": ["toggle Wi-Fi off/on, forget+rejoin the network", "if wired: try another cable/port", "check another device — if it works, it's THIS device's path"],
        "ROUTER-WAN": ["power-cycle MODEM first: unplug 60-120s, plug, wait for solid link light", "then ROUTER: unplug 30s, plug, wait 2 min", "log into router: check WAN/Internet status page; capture line stats if visible", "DO NOT factory reset"],
        "DNS": ["switch DNS to 1.1.1.1 and 8.8.8.8 (on the router, so all devices inherit)", "flush local cache: systemd-resolve --flush-caches / dscacheutil -flushcache / ipconfig /flushdns", "REVERT after the outage — you want ISP defaults long-term for CDN locality"],
        "ISP": ["check ISP status page / Downdetector via MOBILE DATA", "report once, get a ticket number", "start monitor mode: this outage is now evidence", "if contractual SLA exists — you are accumulating a credit claim"],
        "PLATFORM": [f"check {target or 'the platform'}'s status page from mobile data", "do NOT touch your network — everything else is fine", "set a 30-min re-check reminder"],
        "UPSTREAM-OK": ["everything probes fine — problem is app-specific or intermittent", "if it recurs: run monitor --interval 120 to catch it in the act"],
    }.get(verdict, ["re-run diagnose"])
    print("  actions:")
    for i, p in enumerate(presc, 1):
        print(f"    {i}. {p}")
    print()


# ------------------------------------------------------------------ monitor
def monitor(log, interval, notify=None, duration=None):
    print(f"monitoring (interval {interval}s) — Ctrl-C to stop; log {log}")
    state = None
    started = time.time()
    while True:
        v = diagnose(log, verbose=False)
        down = v not in ("UPSTREAM-OK", "PLATFORM")
        cur = "DOWN" if down else "UP"
        if cur != state:
            ts = now_iso()
            rec = {"ts": ts, "type": "state", "state": cur, "verdict": v}
            append_log(log, rec)
            print(f"{ts}  {cur}  ({v})")
            if notify and cur == "DOWN":
                try:
                    subprocess.run(notify, shell=True, timeout=15)
                except Exception:
                    pass
            state = cur
        if duration and time.time() - started > duration:
            break
        time.sleep(interval)


# ------------------------------------------------------------------ report
def read_log(log):
    if not Path(log).exists():
        return []
    out = []
    for line in Path(log).read_text().splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def cmd_report(log, sla_credit=False, contract=None):
    recs = read_log(log)
    probes = [r for r in recs if r.get("type") == "probe"]
    states = [r for r in recs if r.get("type") == "state"]
    equip = [r for r in recs if r.get("type") == "equipment"]
    linesn = [r for r in recs if r.get("type") == "linesn"]
    if not probes and not states:
        sys.exit("log empty — run diagnose/monitor first")

    # outage windows from state records
    windows = []
    open_w = None
    for r in states:
        if r["state"] == "DOWN":
            if open_w is None:
                open_w = {"start": r["ts"], "verdicts": {r.get("verdict", "?")}}
            else:
                open_w["verdicts"].add(r.get("verdict", "?"))
        elif r["state"] == "UP" and open_w is not None:
            open_w["end"] = r["ts"]
            windows.append(open_w)
            open_w = None
    if open_w is not None:
        open_w["end"] = None
        windows.append(open_w)

    def _dur_min(w):
        if not w.get("end"):
            return 0.0
        try:
            return (datetime.fromisoformat(w["end"]) - datetime.fromisoformat(w["start"])).total_seconds() / 60
        except ValueError:
            return 0.0

    total_down = sum(_dur_min(w) for w in windows)
    print("=" * 62)
    print("INTERNET OUTAGE EVIDENCE REPORT")
    print(f"generated: {now_iso()}   log records: {len(recs)}")
    print("=" * 62)
    if equip:
        e = equip[-1]
        print(f"equipment: {e.get('modem', '?')} modem | {e.get('router', '?')} router | serials on file")
    if linesn:
        print("fault-time line stats captured:")
        for r in linesn[-5:]:
            print(f"  {r['ts']}  SNR={r.get('snr')} dB  power={r.get('power')} dBmV  uncorrectables={r.get('uncorr', '?')}")
    print(f"\nOUTAGE WINDOWS ({len(windows)}):")
    for w in windows:
        d = _dur_min(w)
        durs = f"  {d:.0f} min" if d else ""
        end = w.get("end") or "(ongoing at log end)"
        v = ",".join(sorted(w["verdicts"])) if w["verdicts"] else "?"
        print(f"  {w['start']} -> {end}{durs}  [{v}]")
    print(f"\ntotal logged downtime: {total_down:.0f} minutes ({total_down / 60:.1f} h)")

    if sla_credit and windows:
        print("\n" + "-" * 62)
        print("COMPLAINT LETTER (edit [brackets]) — paste into ISP web form/email")
        print("-" * 62)
        print(f"""Subject: Repeated service interruptions — [account #] — request SLA credit

To whom it may concern,

My service has been interrupted repeatedly. My own monitoring (timestamps below,
UTC/local as logged) shows {len(windows)} outages totalling {total_down:.0f} minutes this log period:

{chr(10).join('  ' + w['start'] + ' -> ' + (w.get('end') or '(ongoing)') for w in windows[:10])}

During these windows my equipment was verified and power-cycled per support guidance:
gateway reachable, 100% loss to public endpoints (1.1.1.1/8.8.8.8), affecting all
devices in the household — i.e. the fault is outside my premises.
{f"Contract: {contract}." if contract else ""}
I request: (1) availability credit per the service agreement for the downtime shown,
(2) escalation to the line/network team, and (3) written confirmation of the fault cause.

Regards, [name], [address], [account #], [phone]""")
        print("\nEscalation paths if unresolved: US: FCC informal complaint (consumercomplaints.fcc.gov);")
        print("UK: Ofcom automatic compensation scheme (£/day for loss of service);")
        print("EU: national regulator (EECC arts. 84-86) + consumer-protection price-reduction claim.")


def cmd_log_equip(log, args):
    rec = {"ts": now_iso(), "type": "equipment", "modem": args.modem, "router": args.router, "serial": args.serial}
    append_log(log, rec)
    print(f"equipment on file: modem={args.modem} router={args.router}")


def cmd_log_linesn(log, args):
    rec = {"ts": now_iso(), "type": "linesn", "snr": args.snr, "power": args.power, "uncorr": args.uncorr}
    append_log(log, rec)
    print(f"line stats logged: SNR={args.snr} power={args.power} uncorr={args.uncorr}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log", default=str(DEFAULT_LOG))
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diagnose")
    d.add_argument("--degrade", action="store_true")
    d.add_argument("--target", help="specific host to test (platform check)")
    d.add_argument("--simulate", choices=["device", "wifi", "lan", "router-wan", "dns", "isp", "platform"])
    m = sub.add_parser("monitor")
    m.add_argument("--interval", type=int, default=120)
    m.add_argument("--notify", help="shell command on DOWN")
    m.add_argument("--duration", type=int, help="stop after N seconds (tests)")
    r = sub.add_parser("report")
    r.add_argument("--sla-credit", action="store_true")
    r.add_argument("--contract", help='e.g. "100Mbps, SLA 99.5%"')
    e = sub.add_parser("log-equip")
    e.add_argument("--modem")
    e.add_argument("--router")
    e.add_argument("--serial")
    ln = sub.add_parser("log-linesn")
    ln.add_argument("--snr", type=float)
    ln.add_argument("--power", type=float)
    ln.add_argument("--uncorr", type=int)
    a = p.parse_args()
    if a.cmd == "diagnose":
        diagnose(a.log, degrade=a.degrade, target=a.target, simulate=a.simulate)
    elif a.cmd == "monitor":
        monitor(a.log, a.interval, a.notify, a.duration)
    elif a.cmd == "report":
        cmd_report(a.log, sla_credit=a.sla_credit, contract=a.contract)
    elif a.cmd == "log-equip":
        cmd_log_equip(a.log, a)
    elif a.cmd == "log-linesn":
        cmd_log_linesn(a.log, a)


if __name__ == "__main__":
    main()
