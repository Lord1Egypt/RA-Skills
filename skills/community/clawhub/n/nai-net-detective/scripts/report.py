#!/usr/bin/env python3
"""
Generate a plain-English markdown diagnostic report from net-detective JSON output.
Usage: report.py <diag.json> [--history-compare <history_output.json>]
"""

import json
import sys
import os
from datetime import datetime, timezone


def load_json(path):
    with open(path) as f:
        return json.load(f)


def fmt_ms(ms):
    if ms is None:
        return "N/A"
    return f"{ms:.1f}ms"


def ping_quality(avg_ms, loss_pct):
    if avg_ms is None:
        return "unreachable"
    if loss_pct and loss_pct > 10:
        return "packet_loss"
    if avg_ms < 20:
        return "excellent"
    if avg_ms < 60:
        return "good"
    if avg_ms < 150:
        return "fair"
    return "poor"


def generate_report(diag, history_data=None):
    lines = []
    lines.append("# 🔍 Net Detective Diagnostic Report\n")
    ts = diag.get("timestamp", "unknown")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        ts_fmt = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        ts_fmt = ts
    lines.append(f"**Run at:** {ts_fmt}  ")
    local = diag.get("local", {})
    lines.append(f"**Host:** {local.get('hostname', 'unknown')}  ")
    lines.append(f"**Local IP:** {local.get('local_ip', 'unknown')}  ")
    lines.append(f"**Gateway:** {local.get('gateway', 'unknown')}  ")
    lines.append("")

    # -----------------------------------------------------------------------
    # FINDINGS SUMMARY (computed first, printed second)
    # -----------------------------------------------------------------------
    findings = []
    severity_order = []

    # --- Ping analysis ---
    ping = diag.get("ping", {})
    unreachable_hosts = []
    high_loss_hosts = []
    high_latency_hosts = []
    ok_pings = []

    for host, p in ping.items():
        if not isinstance(p, dict):
            continue
        avg_ms = p.get("avg_ms")
        loss = p.get("packet_loss_pct", 0) or 0
        reachable = p.get("reachable", False)
        if not reachable or avg_ms is None:
            unreachable_hosts.append(host)
        elif loss > 10:
            high_loss_hosts.append((host, loss, avg_ms))
        elif avg_ms and avg_ms > 150:
            high_latency_hosts.append((host, avg_ms))
        else:
            ok_pings.append(host)

    # Check if only IPs are reachable (DNS issue signal)
    ip_hosts = {"1.1.1.1", "8.8.8.8"}
    name_hosts = {"google.com", "cloudflare.com", "cdn.cloudflare.com"}
    names_unreachable = name_hosts.intersection(unreachable_hosts)
    ips_reachable = ip_hosts - set(unreachable_hosts)

    if names_unreachable and ips_reachable and not names_unreachable.issuperset(ip_hosts):
        findings.append({
            "severity": "high",
            "category": "DNS",
            "message": f"Named hosts ({', '.join(sorted(names_unreachable))}) are unreachable but IP addresses respond — this strongly suggests a **DNS resolution failure**.",
            "action": "Check your DNS settings. Try switching to 1.1.1.1 (Cloudflare) or 8.8.8.8 (Google).",
        })

    if unreachable_hosts and len(unreachable_hosts) == len(ping):
        findings.append({
            "severity": "critical",
            "category": "Connectivity",
            "message": "**No hosts are reachable.** You may have no internet connection at all.",
            "action": "Check your router/modem. Try unplugging and replugging the network cable or restarting your Wi-Fi router.",
        })
    elif unreachable_hosts:
        findings.append({
            "severity": "medium",
            "category": "Connectivity",
            "message": f"Some hosts are unreachable: {', '.join(unreachable_hosts)}.",
            "action": "Partial reachability may indicate routing issues or ISP filtering.",
        })

    for host, loss, avg_ms in high_loss_hosts:
        findings.append({
            "severity": "high",
            "category": "Packet Loss",
            "message": f"**{loss:.0f}% packet loss** to `{host}` (avg latency {fmt_ms(avg_ms)}).",
            "action": "Packet loss this high causes dropped calls, stuttering video, and slow transfers. This is likely an ISP or Wi-Fi issue.",
        })

    for host, avg_ms in high_latency_hosts:
        findings.append({
            "severity": "medium",
            "category": "Latency",
            "message": f"High latency to `{host}`: {fmt_ms(avg_ms)}.",
            "action": "Latency above 150ms will noticeably degrade real-time apps (video calls, gaming). Consider checking for ISP congestion.",
        })

    # --- DNS analysis ---
    dns = diag.get("dns", {})
    dns_summary = dns.get("summary", {})
    dns_failures = dns_summary.get("failures", 0)
    dns_slow = dns_summary.get("slow_queries", 0)
    server_avgs = dns_summary.get("server_avg_ms", {})

    if dns_failures > 0:
        findings.append({
            "severity": "high",
            "category": "DNS",
            "message": f"**{dns_failures} DNS lookup(s) failed** across tested servers.",
            "action": "DNS failures cause websites to appear down even when servers are up. Try flushing your DNS cache and switching to 1.1.1.1.",
        })
    elif dns_slow > 0:
        slowest_server = max(server_avgs, key=server_avgs.get) if server_avgs else "unknown"
        slowest_ms = server_avgs.get(slowest_server, 0)
        # Check if system resolver is unusually slow compared to alternatives
        system_ms = server_avgs.get("system")
        cf_ms = server_avgs.get("cloudflare")
        g_ms = server_avgs.get("google")
        if system_ms and cf_ms and system_ms > cf_ms * 5:
            findings.append({
                "severity": "medium",
                "category": "DNS",
                "message": f"Your system DNS is taking **{fmt_ms(system_ms)}** vs Cloudflare's **{fmt_ms(cf_ms)}** — your DNS server may be overloaded or misconfigured.",
                "action": "Switch your DNS to 1.1.1.1 (Cloudflare) or 8.8.8.8 (Google) for faster resolution.",
            })
        elif system_ms and g_ms and system_ms > g_ms * 5:
            findings.append({
                "severity": "medium",
                "category": "DNS",
                "message": f"Your system DNS is taking **{fmt_ms(system_ms)}** vs Google's **{fmt_ms(g_ms)}** — unusually slow.",
                "action": "Try switching your DNS resolver to 8.8.8.8 or 1.1.1.1.",
            })
        else:
            findings.append({
                "severity": "low",
                "category": "DNS",
                "message": f"{dns_slow} DNS lookup(s) were slower than expected (slowest server avg: {fmt_ms(slowest_ms)}).",
                "action": "DNS performance is slightly degraded but not critical.",
            })

    # --- Traceroute analysis ---
    trace = diag.get("traceroute", {})
    hops = trace.get("hops", [])
    first_timeout = trace.get("first_timeout_hop")
    if hops and first_timeout:
        # Try to characterize where loss starts
        if first_timeout <= 3:
            location = "your **local network or router**"
            action_hint = "Check your router settings, cables, or Wi-Fi signal."
        elif first_timeout <= 6:
            location = "your **ISP's network**"
            action_hint = "This is likely an ISP issue — contact your provider."
        else:
            location = "a **distant router or backbone**"
            action_hint = "The issue is far from your home — likely a transit or upstream problem outside your control."
        findings.append({
            "severity": "medium",
            "category": "Routing",
            "message": f"Packet loss/timeouts begin at **hop {first_timeout}** — located in {location}.",
            "action": action_hint,
        })

    # --- MTU analysis ---
    mtu = diag.get("mtu", {})
    if mtu.get("fragmentation_likely"):
        estimated = mtu.get("estimated_path_mtu", "unknown")
        findings.append({
            "severity": "low",
            "category": "MTU",
            "message": f"Path MTU is **{estimated} bytes** (below 1500) — packets are being fragmented.",
            "action": "Fragmentation can cause slow speeds and connection drops, especially with VPNs. Consider adjusting your MTU setting to match the path MTU.",
        })

    # --- Historical anomalies ---
    if history_data:
        anomalies = history_data.get("anomalies", [])
        for a in anomalies:
            findings.append({
                "severity": a.get("severity", "medium"),
                "category": "Historical Anomaly",
                "message": a.get("message", ""),
                "action": "",
            })

    # -----------------------------------------------------------------------
    # Print findings
    # -----------------------------------------------------------------------
    if not findings:
        lines.append("## ✅ Overall: Everything Looks Normal\n")
        lines.append("All tests passed within normal parameters. No issues detected.\n")
    else:
        critical = [f for f in findings if f["severity"] == "critical"]
        high = [f for f in findings if f["severity"] == "high"]
        medium = [f for f in findings if f["severity"] == "medium"]
        low = [f for f in findings if f["severity"] == "low"]

        if critical:
            lines.append("## 🚨 Overall: **Critical Issues Found**\n")
        elif high:
            lines.append("## ⚠️ Overall: **Significant Issues Found**\n")
        elif medium:
            lines.append("## 🟡 Overall: **Minor Issues Found**\n")
        else:
            lines.append("## 🟢 Overall: Mostly Fine (Minor Notes)\n")

        lines.append("### Findings\n")
        for f in critical + high + medium + low:
            icon = {"critical": "🚨", "high": "⚠️", "medium": "🟡", "low": "ℹ️"}.get(f["severity"], "•")
            lines.append(f"**{icon} {f['category']}:** {f['message']}")
            if f.get("action"):
                lines.append(f"> 💡 **Action:** {f['action']}")
            lines.append("")

    # -----------------------------------------------------------------------
    # Detail sections
    # -----------------------------------------------------------------------

    # Ping table
    lines.append("---\n")
    lines.append("## Ping Results\n")
    lines.append("| Host | Reachable | Loss % | Min | Avg | Max |")
    lines.append("|------|-----------|--------|-----|-----|-----|")
    for host, p in ping.items():
        if not isinstance(p, dict):
            continue
        reachable = "✅" if p.get("reachable") else "❌"
        loss = f"{p.get('packet_loss_pct', 0):.0f}%" if p.get('packet_loss_pct') is not None else "—"
        min_ms = fmt_ms(p.get("min_ms"))
        avg_ms = fmt_ms(p.get("avg_ms"))
        max_ms = fmt_ms(p.get("max_ms"))
        lines.append(f"| `{host}` | {reachable} | {loss} | {min_ms} | {avg_ms} | {max_ms} |")
    lines.append("")

    # DNS table
    lines.append("## DNS Resolution\n")
    dns_checks = dns.get("checks", {})
    if dns_checks:
        lines.append("| Server | Avg Latency | Failures | Slow Queries |")
        lines.append("|--------|-------------|----------|--------------|")
        for server, domains in dns_checks.items():
            latencies = [d["latency_ms"] for d in domains.values() if d.get("success")]
            failures = sum(1 for d in domains.values() if not d.get("success"))
            slow = sum(1 for d in domains.values() if d.get("slow"))
            avg = f"{sum(latencies)/len(latencies):.1f}ms" if latencies else "N/A"
            lines.append(f"| {server} | {avg} | {failures} | {slow} |")
    lines.append("")

    # Traceroute summary
    if hops:
        lines.append("## Traceroute to google.com\n")
        lines.append("| Hop | Host | IP | Avg Latency |")
        lines.append("|-----|------|----|-------------|")
        for h in hops[:20]:
            if h.get("timeout"):
                lines.append(f"| {h['hop']} | * | * | timeout |")
            else:
                lines.append(
                    f"| {h['hop']} | {h.get('host','*')} | {h.get('ip','*')} | {fmt_ms(h.get('avg_ms'))} |"
                )
        lines.append("")

    # MTU
    if mtu:
        lines.append("## MTU Detection\n")
        lines.append(f"- **Estimated Path MTU:** {mtu.get('estimated_path_mtu', 'unknown')} bytes")
        lines.append(f"- **Max payload without fragmentation:** {mtu.get('max_payload_bytes', 'unknown')} bytes")
        lines.append(f"- **Fragmentation likely:** {'Yes ⚠️' if mtu.get('fragmentation_likely') else 'No ✅'}")
        lines.append(f"- {mtu.get('note', '')}")
        lines.append("")

    # Speed (if available)
    speed = diag.get("speed")
    if speed:
        lines.append("## Speed Test\n")
        summary = speed.get("summary", {})
        lines.append(f"- **Headline speed:** {summary.get('headline_mbps', 'N/A')} Mbps ({summary.get('quality', 'unknown')})")
        for t in speed.get("tests", []):
            if t.get("success"):
                lines.append(f"  - {t['label']}: {t.get('speed_mbps', 'N/A')} Mbps")
        lines.append("")

    # Historical comparison
    if history_data:
        lines.append("## Historical Comparison\n")
        baseline = history_data.get("baseline", {})
        current = history_data.get("current_metrics", {})
        samples = history_data.get("history_samples", 0)
        lines.append(f"Comparing against {samples} historical run(s).\n")
        if baseline:
            lines.append("| Metric | Current | Baseline Avg |")
            lines.append("|--------|---------|--------------|")
            for key in sorted(set(list(current.keys()) + list(baseline.keys()))):
                cur_val = current.get(key, "—")
                base_val = baseline.get(key, {}).get("mean", "—")
                if isinstance(cur_val, float):
                    cur_val = f"{cur_val:.2f}"
                if isinstance(base_val, float):
                    base_val = f"{base_val:.2f}"
                lines.append(f"| {key} | {cur_val} | {base_val} |")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by net-detective*")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: report.py <diag.json> [--history-compare <history_output.json>]", file=sys.stderr)
        sys.exit(1)

    diag = load_json(sys.argv[1])
    history_data = None

    if "--history-compare" in sys.argv:
        idx = sys.argv.index("--history-compare")
        if idx + 1 < len(sys.argv):
            history_data = load_json(sys.argv[idx + 1])

    report = generate_report(diag, history_data)
    print(report)
