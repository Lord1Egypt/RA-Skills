---
name: printer-hostage-rescue
description: "Use when a printer refuses to print: 'ink low' / 'cartridge error' / 'non-genuine chip' / 'paper jam' with no paper / WiFi printing broken. Diagnoses by failure class, unlocks region/cartridge DRM tricks legally, configures driverless AirPrint/Mopria printing, and replaces subscription-ink trap behavior."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [printer, ink, drivers, ipp-everywhere, airprint, troubleshooting]
---

# Printer Hostage Rescue

## Overview
Printers fail in well-known, well-documented ways, and most "errors" are business
models, not hardware faults: ink-level chips that report empty while ink remains,
region locks after moving countries, "non-genuine cartridge" refusals for legally
refilled cartridges, driver CDs from 2009, and spooler states that wedge after one
failed job. This skill walks the failure class → real cause → concrete fix, including
the legal reset paths (consumers' right to use refills is protected in many
jurisdictions; the *printer* must not refuse third-party consumables in the EU/UK
unless it warns honestly), and modern driverless setup (IPP Everywhere / AirPrint /
Mopria) that makes 90% of driver downloads unnecessary.

## When to Use
- Any "won't print" situation: error on panel, job stuck in queue, blank pages
- After moving countries (region lock) or refilling / using third-party cartridges
- Setting up a printer on a new network / new computer without the vendor driver stack
- Ink subscription traps ("HP Instant Ink blocks printing if the card expires")
- **Don't use for:** enterprise managed print servers (contact IT), dye-sub photo
  printers with ribbon errors (different failure class).

## Failure Classes → Fixes (summary table; full detail in references/)
| # | Symptom | Real cause | Fix |
|---|---|---|---|
| 1 | "Ink low/empty" but prints fine / new cart "empty" | chip estimate, not measurement | override/disable ink monitoring; plan real replacement by print quality, not the chip |
| 2 | "Non-genuine cartridge detected", refuses | cartridge DRM | firmware: accept-and-warn path; EU: consumer law; downgrade FW if vendor pulled override |
| 3 | Cartridge error LED / blinking, no message | contact/comm failure | reseat, clean contacts w/ isopropyl, check plastic shipping tape, try old cart to isolate |
| 4 | Region lock after moving | regionalization DRM | vendor reset tool / service mode; many vendors reset free with proof of local cart purchase |
| 5 | Job stuck "Printing…" forever | wedged spooler | cancel all, restart spooler service (Win) / `cancel -a` (CUPS), clear stuck .SHD/.SPL |
| 6 | Prints blank pages | clogged nozzles | 2–3 head cleanings max, then 8h pause (saturation), manual soak for removable heads; don't burn ink in cleaning loops |
| 7 | WiFi says connected, nothing prints | mDNS/Bonjour broken, IPv6 vs IPv4, AP isolation | wired/IP setup via web UI (port 80/443 on printer IP), static DHCP reservation, driverless IPP |
| 8 | New computer can't find printer | vendor driver stack hell | skip drivers: IPP Everywhere / AirPrint / Mopria — Windows 10+/macOS/Linux/Android/iOS all support it |
| 9 | Ink subscription hostage | Instant Ink / PrintPlans card expiry | cancel per flow; printer resumes with own cartridges (some vendors pause days after) |
| 10 | "Paper jam" with zero paper | fragment deep in path / sensor flag stuck | flashlight + inspection ports, rear access panel, Duplex unit reseat; strip of cardstock to feel path |
| 11 | Ghosting / repeating marks | drum/fuser life or toner spill | drum replacement vs fuser; count pages since last service |
| 12 | Scanner works, printer dead (or reverse) | single-function chip lock | power-nuke: unplug 60 s, hold power; NVRAM reset per model |

## Steps
1. Classify the failure using the table (or `scripts/print_rescue.py diagnose`).
2. Run the tool for model-family-specific unlock paths:
   ```bash
   python3 scripts/print_rescue.py diagnose --symptom "non-genuine cartridge"
   python3 scripts/print_rescue.py spooler --fix          # clears wedged queues
   python3 scripts/print_rescue.py discover               # find printers, test driverless IPP
   ```
3. Network path: `discover` finds the printer IP, probes TCP 631 (IPP), 9100
   (raw JetDirect), 80/443 (web admin), and prints a test page via driverless IPP
   — proving the hardware works without any vendor driver.
4. Escalation order per class: user-level fix → service menu → firmware path →
   consumer-law route (EU/UK: vendor must not disable refills silently; US:
   Magnuson-Moss warranty implications) → replacement economics (see below).
5. Replacement economics: repair estimate (drum ~$60–90, printhead ~$70–120,
   WiFi board ≈ printer value) vs. cheap laser for text ($120–180, toner
   1,500–3,000 pages vs inkjet page-cost 5–10× higher).

## Worked Example
HP inkjet, refilled cartridge, panel: "Non-HP cartridge detected — printing blocked".
1. `print_rescue.py diagnose --symptom "non-genuine"` → class 2: check firmware
   version against the vendor's "optional" updates that re-enable blocking; use the
   accept-and-warn menu if present (Settings → Supplies → Override).
2. EU/UK route: refusal to function with refills without disclosure at purchase can
   breach consumer law — cite in support chat; vendors commonly supply unlock steps.
3. Meanwhile `discover` + driverless IPP test page proves the print path itself is
   healthy, isolating the issue to cartridge DRM.
4. Long-term: printing volume < 100 pages/mo → mono laser recommendation computed
   (toner $0.02–0.04/page vs inkjet $0.10–0.25/page incl. cleaning waste).

## Common Pitfalls
1. **Running head cleaning 10× in a row.** Each cleaning dumps ink into the waste
   pad; 3 in a row then STOP for hours (nozzles saturate); a soaked park pad floods.
2. **Installing vendor "full feature" software to fix a network issue.** It adds
   3 services and a cloud agent; use driverless IPP first — it's built into every
   modern OS.
3. **Fighting region locks by buying a 3rd-party "resetter".** The official vendor
   reset (with local-cartridge proof) is free and doesn't risk the formatter board.
4. **Ignoring the print queue when "the printer is broken".** Half of "dead"
   printers are a wedged spooler on one computer; test from a second device first.
5. **Replacing cartridges based on chip warnings.** Chips estimate; ink is visible
   in most carts — judge by print quality and keep a spare, not a panic.
6. **Subscription ink while card expired = hostage.** Cancel properly (vendor flow,
   not just removing the card) so the printer exits grace state cleanly.

## Verification Checklist
- [ ] Failure class identified and matched to the fix path
- [ ] Print path proven healthy via second device or driverless IPP test page
- [ ] Spooler cleared before declaring hardware dead
- [ ] Firmware version checked against blocking-update advisories
- [ ] Fix or replacement economics stated with page-cost math
