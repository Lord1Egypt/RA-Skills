# Internet Outage Warlord

**Skill:** `internet-outage-warlord` · v1.0.0 · MIT · ClawHub `@voronindenis5/internet-outage-warlord`

## The real-world problem

Home internet goes down 1–3× a month in a typical household, and every time it does, the same scene: everyone blames the router, someone factory-resets something at 9PM and loses the PPPoE password, and if it's actually the ISP's fault, nobody has evidence — so the SLA credit that the contract owes you never gets claimed. UK Ofcom data: the major ISPs paid out £54M+ in automatic compensation in a single year, and that's only the scheme members, only the people who persisted.

The failure can live in seven layers (device → Wi-Fi → LAN → router-WAN → DNS → ISP last-mile → the one platform you actually need), and each has a different fix and a different owner. Guessing wrong wastes an evening; documenting nothing forfeits the claim.

## What it does

Pure-stdlib Python, log in a local JSONL:

- **`diagnose`** — layered probe sequence (local IP → gateway ping → DNS × 3 domains → anycast IPs 1.1.1.1/8.8.8.8/9.9.9.9 → HTTP HEAD × 3), stops at the first broken layer, prints a scoped verdict (`DEVICE / WIFI-OR-LAN / ROUTER-WAN / DNS / ISP / PLATFORM / UPSTREAM-OK`) **plus the exact action sequence** — including what NOT to do (no factory resets). Falls back to DNS+HTTP verdicts where ICMP is filtered (clouds, carriers) so it doesn't cry wolf.
- **`monitor --interval N`** — cron/silent mode: logs only state changes (DOWN with verdict / RECOVERED with duration), optional notify command. This is the 3AM-outage catcher — and the evidence machine: every outage gets real timestamps the ISP's own monitoring "can't see".
- **`report`** — the evidence package: outage windows with durations, equipment inventory (modem/router/serial — pre-empts "it's your router"), fault-time line stats, and a ready-to-paste ISP complaint letter with the SLA math and the escalation path for your jurisdiction (US: FCC complaint; UK: Ofcom automatic compensation £9.76/day; EU: national regulator under EECC).
- **`diagnose --simulate X`** — demo each verdict type without breaking anything (also how I tested it).

## Who needs this

- **Any household** that loses an evening to "is it just us?" — scoping takes 30 seconds
- **Remote workers** deciding whether to head to a café or wait out the ISP window
- **Home-server / Raspberry Pi / NAS owners** — deploy `monitor` from cron and accumulate claimable evidence passively
- **Smart-home households** — know in advance which devices are cloud-hostage during outages
- **Anyone with an SLA** — "99.5% availability" allows 3h39m/month; your log showing 11h is a 3× breach and a credit claim

## Example

```bash
python3 scripts/outage_warlord.py diagnose
# VERDICT: ISP  (gateway ok, 100% loss to 1.1.1.1/8.8.8.8, DNS dead)
#   actions: 1. check ISP status via mobile data  2. report once, get ticket
#            3. start monitor — this outage is now evidence  4. SLA credit accruing
python3 scripts/outage_warlord.py monitor --interval 120 --notify "curl -s -d 'NET DOWN' ntfy.sh/home >/dev/null"
# ...next day...
python3 scripts/outage_warlord.py report --sla-credit --contract "100Mbps, SLA 99.5%"
# OUTAGE WINDOWS (2): 16:02->16:49 [ISP]  18:02->18:50 [ISP]
# total logged downtime: 96 minutes (1.6 h)  + complaint letter, ready to paste
```

## License

MIT © Denis Voronin. Probes run on your own equipment against your own connection; no telemetry, no cloud.
