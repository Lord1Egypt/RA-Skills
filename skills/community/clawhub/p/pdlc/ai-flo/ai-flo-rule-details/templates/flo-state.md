<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Flow State — AI-FLO

---
package: AI-FLO
version: 1.0.0
topology_mode: {1 / 2 / 3}
created: {ISO date}
last_updated: {ISO date}
---

## Configuration

| Parameter | Value |
|-----------|-------|
| Hold Timeout | {N} business days |
| Optional-Feed Wait | {N} business days |
| Stall Threshold | {N} days |
| Auto-Resolve Rule | {upstream-wins / latest-wins / always-escalate / custom} |
| Roll-Up Schedule | {on-demand / session-start / weekly} |

---

## Project: {Project Name}

| Field | Value |
|-------|-------|
| Project ID | {PRJ-ABBREV-YYYY-NNN} |
| Workspace Ref | {./ or /absolute/path/} |
| Current Package | {AI-ADLC / AI-UXD / AI-POLC / AI-DWG / etc.} |
| Current Status | {In Progress / Complete / Blocked / Cancelled / Dispatched} |
| Next Hop | {next package / waiting-for-fan-in / end-of-chain} |
| Priority | {#N} |
| Dispatched | {ISO date} |
| Last Activity | {ISO date} |
| Profile | {Full / skip: [list]} |
| Rework Count | {N} |

### Active Toggles

| Package | Status | Toggled | Reason | Operator |
|---------|--------|---------|--------|----------|
| {AI-UXD} | {on/off} | {date or —} | {reason} | {name} |

### Position History

| Date | From | To | Trigger | Operator |
|------|------|----|---------|----------|
| {date} | — | {first package} | Dispatch DA-{ID} | Auto |
| {date} | {pkg A} | {pkg B} | {marker trigger} | {Auto/name} |

---

<!-- Repeat "## Project:" block for each tracked project -->
