---
name: internet-outage-warlord
description: "Use when a home internet connection drops or degrades and someone needs to figure out WHAT failed (modem, router, ISP, DNS, Wi-Fi, device), what to do right now, and how to prove it to the ISP. Runs layered diagnostics (gateway/DNS/public-IP probes), builds an evidence log with timestamps, and generates an ISP complaint package — turning 'the internet is down' from a guessing game into a scoped fault with a paper trail."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [internet, outage, diagnostics, isp, network, dns, evidence-log, complaint]
---

# Internet Outage Warlord

## Overview

Home internet goes down. The household revolts. Someone (you) is deputized to fix it. The failure can be in seven different places — your device, Wi-Fi radio, router LAN, router WAN, DNS resolver, ISP last-mile, or a regional/platform outage — and the difference between them is the difference between "reboot the router" and "call the ISP with evidence", or "do nothing, it's Cloudflare".

Internet Outage Warlord does three things:

1. **Scopes the fault** — a layered probe sequence that isolates WHERE connectivity died, from the laptop outward: link → gateway → DNS → public endpoint → ISP headend, plus known-platform-outage heuristics. The output is a scoped verdict (`WIFI`, `LAN`, `ROUTER-WAN`, `DNS`, `ISP`, `PLATFORM`, `UPSTREAM-COMPLETE`), not vibes.
2. **Prescribes** — the right first action per verdict: which box to power-cycle and in what order, what NOT to touch (don't factory-reset at 9PM), when to switch to mobile data or a phone hotspot, how to ride out an ISP outage with a downtime SLA credit claim.
3. **Builds the evidence log** — timestamped probe results persisted to disk. When the ISP says "we see no outage in your area", you paste the log: 47 minutes of 100% packet loss to the gateway at 19:02–19:49, with model/serial of your equipment, traceroute capture at fault time, and a ready-to-send complaint with statutory citation where applicable.

The core principle: **an outage you can't scope, you can't fix — and an outage you can't document, you can't claim.**

## When to Use

- "The internet is down" / "Wi-Fi is down" / "websites won't load"
- "Internet is slow / videos buffer constantly" → run `diagnose` in degrade mode (it logs latency/jitter/loss, not just up/down)
- "Is it just me or is everyone down?" → platform-outage heuristics + optional online check
- Preparing an ISP complaint / SLA credit claim after repeated outages
- Setting up the monitor before problems start (proactive monitoring on a home server / Raspberry Pi / NAS cron)
- Deciding whether to work from a café or wait it out (verdict + ETA heuristics)

**Don't use for:** enterprise networks with NOC teams (different tooling), fiber cuts you can physically see (call the ISP immediately), or suspected compromise/hacking of your network (different threat model — this is availability, not security).

## How It Works — Numbered Workflow

1. **Run `diagnose`** the moment connectivity degrades. The script probes in order, stopping at the first hard failure layer:
   link (interface up? IP?) → gateway ping → DNS resolution of a stable domain → ping a public anycast IP (1.1.1.1, 8.8.8.8) → HTTP HEAD to 2–3 majors. Each hop gets logged with a timestamp to `outage_log.jsonl`.
2. **Read the verdict** — a scoped fault label plus the confidence and the immediate prescription. The script prints the action sequence (power-cycle order: modem → wait 2 min → router → wait 2 min → re-probe), never a factory reset.
3. **If DNS:** the script tests alternate resolvers (1.1.1.1, 8.8.8.8, 9.9.9.9) and prescribes the temporary switch (and how to revert).
4. **If ISP/platform:** check the heuristics — can you reach anycast IPs but not HTTP? Are specific platforms failing while others work? The script optionally checks a public status aggregator (if you have any connectivity at all, e.g. via mobile data) and logs the result.
5. **After the outage, run `report`** — the evidence package: outage windows extracted from the log (≥2 consecutive failed probe sets), total downtime, per-window scope, equipment inventory, and a filled-in ISP complaint letter (with EU/UK/US regulatory hooks where relevant).
6. **Optional `monitor` mode** — run from cron every 1–5 min; silent while healthy, logs and (optionally) runs a notification command on state change. This is how the warlord catches the 3AM outages you sleep through and the intermittent degradation that never shows up when the technician visits.
7. **Restore your normal config** after any temporary DNS/workaround changes (the log records what changed).

## Verdicts & First Actions

| Verdict | Meaning | First action |
|---|---|---|
| `DEVICE` | your machine's link is down (no IP / airplane mode / cable) | fix NIC / Wi-Fi toggle / cable |
| `WIFI` | gateway unreachable from this device only (other devices fine per probe history) | toggle Wi-Fi, forget/rejoin network, check band steering |
| `LAN` | gateway reachable, but router's upstream dead from inside | log into router, check WAN status page |
| `ROUTER-WAN` | router up but no public connectivity, DNS ok via alternate | power-cycle modem → router (order matters), check coax/fiber/DSL line stats |
| `DNS` | IPs reachable, names don't resolve | switch resolver to 1.1.1.1/8.8.8.8 temporarily; flush local cache |
| `ISP` | line-side failure (gateway ok, public unreachable via all resolvers) | report to ISP with log; check ISP status page via mobile data; claim SLA credit if contractual |
| `PLATFORM` | one site/service down, rest of internet fine | wait it out; check the platform's status page; don't touch your network |
| `UPSTREAM-OK` | everything reachable — problem is app-specific or too brief to catch | run in monitor mode to catch intermittents |

## Quick Start

```bash
python3 scripts/outage_warlord.py diagnose          # scope the fault now
python3 scripts/outage_warlord.py diagnose --degrade   # slow-but-up mode: latency/loss stats
python3 scripts/outage_warlord.py report         # evidence log → ISP complaint package
python3 scripts/outage_warlord.py monitor --interval 120   # cron mode, logs state changes
python3 scripts/outage_warlord.py report --sla-credit --contract "100Mbps, SLA 99.5%"   # credit claim
```

Log: `outage_log.jsonl` beside the script (override `--log`). Network probes use only stdlib (socket, subprocess ping) — works on Linux/macOS; on Windows use WSL or the --no-ping fallback (HTTP-only probes).

## The ISP Complaint Package

`report` generates:

- **Outage table**: start, end, duration, verdict at each window, probes that failed
- **Equipment inventory**: modem/router model + serial (from `setup`, entered once) — proving it's not "your router" before the ISP blames it
- **Complaint letter** (plain text): dates/durations, statement that customer equipment was power-cycled per ISP instructions during windows (from your action log), reference to contractual availability (e.g. "99.5% monthly availability" = max 3h39m downtime/month; your log shows 11h), and the remedy requested (credit, escalation, fix commitment).
- Where relevant, cites: US — FCC complaints; EU — Art. 22 Universal Service Directive availability/quality obligations... see `references/isp-evidence-playbook.md` for jurisdiction specifics.

## Common Pitfalls

1. **Rebooting everything at once.** It "fixes" ~60% of outages and destroys the evidence: you lose the fault state the ISP needs to see (line stats at fault time), and if it's an ISP-side fault you've learned nothing. Scope first with `diagnose`, act second.
2. **Factory-resetting at night.** The 9PM panic reset wipes your PPPoE credentials, Wi-Fi names, port forwards. The warlord never recommends factory reset as a first-line action — power-cycle only, and only the scoped layer.
3. **Trusting the router's "Internet: Connected" light.** DHCP-lease-OK but no actual upstream happens constantly; the script probes public endpoints, not indicator LEDs.
4. **Blaming DNS for everything.** "Internet down" that's actually DNS is common but over-diagnosed; the layered probe distinguishes "names fail, IPs work" (DNS) from "everything fails from the gateway out" (ISP).
5. **No log = no claim.** ISP support scripts are designed to wear you down ("unplug for 30 seconds"). A timestamped log with durations and a letter citing the SLA percentage changes the conversation from support-tier roulette to a documented claim.
6. **Testing only one endpoint.** google.com down ≠ internet down. The script probes anycast IPs + multiple HTTP endpoints + DNS to separate platform vs general failures.
7. **Ignoring the modem's line stats.** Coax SNR/fiber RX power visible in modem UI are the ISP's own telemetry; the reference explains how to capture them into the log (manual entry command) as fault-time evidence.

## Verification Checklist

- [ ] `diagnose` on a healthy connection prints `UPSTREAM-OK` and appends to the log
- [ ] `diagnose` with network disconnected (or `--simulate isp`) prints a scoped verdict + prescription
- [ ] `report` after ≥2 logged failures prints outage windows + complaint letter
- [ ] `monitor --interval N` writes only on state change (healthy → failing → healthy = 2 lines)
- [ ] Simulate modes work: `--simulate dns|isp|platform|wifi` (for demos/tests without breaking anything)
- [ ] No non-stdlib imports (grep: requests|urllib3|scapy → empty; stdlib urllib.request IS used for HTTP probes)

## One-Shot Recipes

**"Internet is down" at home:**
```bash
python3 scripts/outage_warlord.py diagnose
# → VERDICT: ISP (gateway ok, 100% loss to 1.1.1.1 and 8.8.8.8)
# → actions: 1. mobile-data check of ISP status page 2. power-cycle modem only ...
python3 scripts/outage_warlord.py monitor --interval 120    # passive until it recovers
python3 scripts/outage_warlord.py report --sla-credit       # when it's back
```

**Chronic evening slowdowns:**
```bash
python3 scripts/outage_warlord.py diagnose --degrade --label evening
# latency/loss table for the evening window; congestion pattern = ISP capacity issue
python3 scripts/outage_warlord.py report   # trend: 20:00-23:00 latency 4x baseline
```

**Is Discord down or is it me?**
```bash
python3 scripts/outage_warlord.py diagnose --target discord.com
# PLATFORM verdict if everything else probes fine
```

## License

MIT (see LICENSE). No warranty; network probes run on your own equipment against your own connection.
