# ISP Evidence Playbook — Reference

## 1. Where home outages actually live (the failure stack)

Layered from your fingertips outward. Each layer has its own failure modes and its own fix. Scoping = finding the lowest broken layer.

| # | Layer | Typical failures | Probe | Fix owner |
|---|---|---|---|---|
| 1 | Device link | airplane mode, dead NIC, bad cable, DHCP fail (no IP) | interface status, APIPA 169.254.x.x | you |
| 2 | Wi-Fi | radio interference, band-steering gone wrong, AP overload | gateway ping from multiple devices | you |
| 3 | Router LAN | router hung, LAN port dead, IP conflict | ping gateway from wired client | you |
| 4 | Router WAN / modem | PPPoE session drop, DHCP lease loss, modem lockup | router WAN status + public probe | you + reboot |
| 5 | DNS | resolver outage (ISP DNS is chronically fragile), hijack | resolve name vs ping IP | you (switch resolver) |
| 6 | ISP last-mile | line fault, congestion, maintenance, modem-sync loss (SNR/RX power) | all public probes fail from gateway out | ISP |
| 7 | Platform | the one site you need is down | other sites fine, target fails | nobody — wait |

Key diagnostic asymmetries:

- **Gateway reachable + everything else dead** → look at layers 4–6. If the modem's line stats are bad (coax SNR < 33 dB, uncorrectable codewords climbing, fiber RX power out of spec), it's layer 6 with proof.
- **IPs ping, names don't resolve** → layer 5. Switch to 1.1.1.1/8.8.8.9 temporarily; this fixes "the internet" for 80% of DNS-outage cases in 30 seconds.
- **One site down, everything else fine** → layer 7. Check the site's status page from mobile data; don't touch your network.
- **Everything fine from the wired desktop, Wi-Fi devices suffering** → layer 2. 2.4GHz congestion, or a mesh node that "helpfully" steered everyone to a dead backhaul.

## 2. Probe design (what the script does and why)

- **Gateway**: derived from the OS routing table (the `default` route) — not hardcoded, survives network changes. Ping it (subprocess ping, 3 packets). Gateway responds = LAN/Wi-Fi path to router OK.
- **DNS**: resolve 3 domains of differing infrastructure (`example.com`, `cloudflare.com`, `gnu.org`). All fail while IPs ping = resolver layer. Mixed results = DNS or partial upstream — degrade mode disambiguates.
- **Anycast IPs**: ping 1.1.1.1 and 8.8.8.8 (and 9.9.9.9). These are anycast — a nearby instance answers unless your upstream is truly dead. Reachable while HTTP fails suggests filtering, MTU, or platform issues; combined with DNS OK, strongly suggests the problem is above L3.
- **HTTP**: HEAD requests (stdlib urllib, 5s timeout) to 3 majors. HTTP failing while ICMP works happens with CGNAT issues, IPv6 breakage (happy-eyeballs timeout), or middlebox corruption.
- **Degrade mode**: 10 pings per target, reports min/avg/max latency and loss %. Evening latency 3–5× morning baseline with 2–8% loss is the classic ISP congestion signature (oversubscribed CMTS/DSLAM), and it's claimable evidence — SLAs speak of "availability" but chronic congestion violates "service description" clauses.

## 3. Evidence: what makes ISPs pay attention

Support tier-1 is a funnel designed to exhaust you. What escapes the funnel:

1. **Timestamped log with durations** — "outage 19:02–19:49, 21:10–22:03, and 14 for September" beats "it goes down every night".
2. **Equipment proof** — modem model + serial, showing CPE (customer premises equipment) is yours and was power-cycled per script. Pre-empts "it's your router".
3. **Fault-time line stats** — cable: SNR, power level, uncorrectables; DSL: attenuation, SNR margin, CRC errors; fiber: RX power. Screenshot or manual transcription from modem UI at fault time (the script logs manual entries: `log-linesn --sn 33.2 --power -6.8`).
4. **Scope proof** — "gateway reachable throughout, 100% loss to 1.1.1.1/8.8.8.8, DNS via 1.1.1.1 also failed" removes every "have you tried restarting" branch from their script.
5. **The ask** — credit per SLA, escalation to tier-2/line-team, or a fix commitment date. A complaint that asks for nothing gets nothing.

## 4. Regulatory hooks (complaint escalation paths)

When the ISP stonewalls:

- **US**: FCC Informal Complaint (consumercomplaints.fcc.gov) — ISPs must respond within 30 days; state utility commissions for some states; also the ISP's own exec-email carpet bomb (CEO email + support escalation address, politely, with the log attached) works embarrassingly well.
- **EU**: national regulators (NRAs) under the EECC; Art. 22 of the old Universal Service Directive (availability/quality obligations) transitions into EECC Arts. 84–86 (service quality, outage information, compensation schemes where offered). Consumer-protection law: the 2011 EU Directive 2011/83 (consumer rights) and national implementations let you claim price reduction for non-conforming service.
- **UK**: Ofcom's 2022 Automatic Compensation scheme — £9.76/day (indexed) for total loss of service, £5.04/day for missed repair appointments, £26.24 per missed appointment — automatic for the major ISPs (BT, Sky, TalkTalk, Virgin Media, etc.). If your ISP is in the scheme, the claim letter just cites the dates; the money is owed regardless of you noticing.
- **Anywhere**: the contract's own SLA. "99.5% monthly availability" = 3h39m allowed downtime/month; your log showing 11h is a 3× breach. Even without a formal SLA, chronic non-performance = material breach argument for exit-without-ETF (early termination fee) claims.

## 5. Monitor deployment (the 3AM catcher)

Cron on any always-on box (Raspberry Pi, NAS, home server):

```
*/2 * * * *  /usr/bin/python3 /path/to/outage_warlord.py monitor --interval 120 --notify "curl -s -d 'NET DOWN at $(date)' ntfy.sh/yourhome >/dev/null"
```

- Silent while healthy (one heartbeat line per hour by default — tunable).
- State-change lines: `DOWN` (with verdict) and `RECOVERED` (with duration).
- The log then contains every outage with real timestamps — including the ones the ISP's own monitoring "doesn't see" (many access-network faults are invisible to central monitoring; only CPE-side logs prove them).
- Storage: ~1–2 KB/day. A year of logs is nothing; rotate when `report` gets slow.

Battery/cost note: run probes at ≥60s intervals; more aggressive probing adds nothing (most last-mile faults don't flap faster) and can trip ISP rate-limits on their DNS resolvers.

## 6. Working around an outage (triage for the household)

1. **Scope it** (`diagnose`) — 30 seconds, tells everyone whether to wait or act.
2. **Mobile data / hotspot** for the machines that matter (work laptop first). Enable low-data mode on family devices; warn streaming.
3. **If DNS-only**: switch resolver on the router (not per-device) so phones/TVs inherit it.
4. **If platform-only**: status page via mobile data; set a reminder to re-check in 30 min; don't let anyone "fix" the network.
5. **If ISP**: report once (get a ticket number — the report letter includes a placeholder), then stop calling; the monitor log is the claim.
6. **Smart-home caveat**: most IoT devices die without WAN (cloud-dependent). Local-control hubs (Home Assistant with local integrations) keep lights/heat working; note which of your devices are cloud-hostage in the reference inventory (`setup --equip`) so you know what to expect during outages.

## 7. What NOT to do (the panic catalogue)

- Don't factory-reset any equipment at night (you'll lose PPPoE creds, Wi-Fi config, port forwards; at 9PM with no internet you can't look up how to reconfigure).
- Don't unplug the modem for "a while" — modems need 60–120s to fully discharge capacitors and re-register on the CMTS/OLT; 10-second plugs teach nothing.
- Don't run speed tests during a partial outage as "proof" — server load contaminates them; ping/loss/latency to stable anycast is cleaner evidence.
- Don't change DNS to some random "fast" resolver list from a forum; stick to 1.1.1.1/8.8.8.8/9.9.9.9 and revert after.
- Don't buy a "better router" in the first week of an ISP fault — the warlord's verdict tells you which layer is broken; buying layer-2 gear for a layer-6 problem wastes the money and the return window.
