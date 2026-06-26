# Net Detective — Diagnostic Guide

## What Each Test Measures

### Ping
Sends ICMP echo packets to a host and measures round-trip time (RTT). Reports:
- **avg_ms** — average round-trip latency. Under 20ms is excellent; 20–60ms is normal; over 150ms is noticeable.
- **packet_loss_pct** — percentage of probes that got no reply. Any loss above 1% is abnormal; above 5% causes noticeable issues.
- **min/max** — spread reveals jitter. A large gap (e.g., min 10ms, max 400ms) means unstable connection.

### DNS Resolution
Sends an A-record query for each test domain to multiple DNS servers. Measures:
- **latency_ms** — how long the resolver took to respond. Under 30ms is fast; over 200ms is slow.
- **success/failure** — if a resolver fails entirely, it may be down, blocked, or unreachable.
- Compare **system resolver** vs **Google 8.8.8.8** vs **Cloudflare 1.1.1.1**. If the system resolver is much slower than 1.1.1.1, the ISP's DNS is the bottleneck.

### Traceroute
Sends probes with increasing TTL to map the path to a destination. Each line is one router hop. Reveals:
- **Where packet loss starts** — if hop 4 drops all probes but hop 3 doesn't, the issue is between those routers.
- **Hop count** — more hops generally means more latency. Over 20 hops to a common destination is unusual.
- **`* * *` lines** — the router didn't respond. This isn't necessarily a problem; many routers silently drop TTL-exceeded packets. Only meaningful if the destination also becomes unreachable.
- **Latency jumps** — a sudden increase at one hop (e.g., 10ms → 120ms) indicates a slow link at that point.

### MTU Detection
Finds the largest packet that travels end-to-end without fragmentation. Standard Ethernet MTU is 1500 bytes. A lower path MTU means:
- **VPN or tunneling** — IPsec/WireGuard/OpenVPN add overhead, reducing effective MTU.
- **Older ISP equipment** — some DSL providers use PPPoE (MTU 1492).
- Fragmentation causes TCP performance problems, especially with large downloads or video streams.

### Speed Test
Downloads fixed-size payloads from Cloudflare's speed endpoint and measures throughput. Provides a rough estimate of available bandwidth. Not a substitute for a proper speed test service but good for trend comparison.

---

## Common Failure Patterns

### Pattern: Websites unreachable, but `ping 8.8.8.8` works
**Cause:** DNS resolution failure. The network is up but domain names aren't resolving.  
**Diagnosis:** dns_check.py will show failures or very high latency on the system resolver.  
**Fix:** Change DNS to 1.1.1.1 or 8.8.8.8. On macOS: System Preferences → Network → DNS. On Linux: edit `/etc/resolv.conf` or your NetworkManager config.

### Pattern: Packet loss starting at hop 1–2
**Cause:** Local network problem — bad cable, failing NIC, overloaded router, or flaky Wi-Fi.  
**Diagnosis:** Traceroute shows first timeout at hop 1 or 2; ping to gateway also shows loss.  
**Fix:** Try a wired connection. Restart the router. Check for cable damage.

### Pattern: Packet loss starting at hop 3–6
**Cause:** ISP's network is dropping packets. This is outside your control.  
**Diagnosis:** Traceroute shows clean first 1–2 hops (your equipment), then loss begins in the ISP's address ranges.  
**Fix:** Contact your ISP. Document the traceroute output as evidence.

### Pattern: High latency everywhere, no packet loss
**Cause:** Congestion — either local (overloaded Wi-Fi, maxed-out bandwidth) or upstream (ISP peak-time congestion).  
**Diagnosis:** Ping to gateway is also slow (local issue) vs. gateway fast but remote hosts slow (upstream issue).  
**Fix:** Check for other devices consuming bandwidth. If gateway ping is also slow, reboot router.

### Pattern: Speed much lower than subscribed tier
**Cause:** Could be Wi-Fi signal, ISP throttling, in-home interference, or a faulty modem/router.  
**Diagnosis:** Run speed test both wired and wireless. Compare to ISP plan speed.  
**Fix:** Try a wired connection first. If wired speed is still low, contact ISP.

### Pattern: MTU below 1472 (fragmentation)
**Cause:** Usually a VPN, PPPoE DSL connection, or ISP equipment that doesn't support full 1500-byte frames.  
**Diagnosis:** MTU probe returns estimated MTU of 1452 or similar.  
**Fix:** Set your MTU to match the path MTU. For VPNs, configure MSS clamping. For PPPoE, set MTU to 1492.

### Pattern: DNS fast, ping fast, speed slow
**Cause:** Likely ISP throttling specific traffic types (especially streaming or large transfers) rather than all traffic.  
**Diagnosis:** Speed test shows low throughput but latency looks normal.  
**Fix:** This is hard to fix without changing ISPs. A VPN sometimes bypasses throttling.

---

## Interpreting History Comparisons

A single reading means nothing without context. history.py stores results over time and flags anomalies using Z-score deviation from the baseline.

- **Z-score > 2** = unusual (top 5% of historical values)
- **Z-score > 4** = very unusual (worth investigating)
- **Speed drop > 50%** = significant throughput change
- **Packet loss appearing when baseline was 0** = definite problem

After 5+ runs, the baseline becomes meaningful. Run diagnostics periodically (daily or weekly when things are normal) to build a good baseline before problems occur.
