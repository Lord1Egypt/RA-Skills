---
name: mikrotik-encyclopedia
description: >-
  MikroTik RouterOS documentation-first workflow for MikroTik-specific
  questions, troubleshooting, command planning, live CLI/API work, config
  review, log analysis, security review, performance tuning, and diagnostics.
  Use when the request is clearly about MikroTik or RouterOS: MikroTik
  devices, RouterOS, RouterBOARD, CAPsMAN, WinBox, RouterOS CLI/API/SSH
  access, or networking topics specifically in a MikroTik context such as
  firewall, NAT, filter/raw/mangle, bridge, switch, VLAN, DHCP, DNS, queues,
  wireless/WiFi, routing, packet flow, connection tracking, or device
  management. Do not use for generic networking theory, generic firewall
  design, or generic Linux router/admin work unless the MikroTik/RouterOS
  context is explicit.
metadata: {"openclaw":{"emoji":"📡","homepage":"https://help.mikrotik.com/docs/"}}
---

# MikroTik Encyclopedia

## Overview

Use a docs-first workflow for MikroTik work. Prefer the official MikroTik documentation at `https://help.mikrotik.com/docs/`, consult cached local copies under `.MikroTik-Encyclopedia/` before re-fetching, and record useful official-doc excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for the **MikroTik RouterOS/device layer**. It should trigger for real RouterOS behavior, configuration, and device-management questions — not for generic networking advice or generic Linux firewall/router administration.

## Workflow

1. **Classify the task**
   - Decide whether the task is a MikroTik question, troubleshooting task, command-planning task, config review, or live SSH/API task.
   - Use this skill when the request is clearly about MikroTik hardware, RouterOS behavior, or a networking/admin task in a MikroTik context.
   - Do not use this skill for generic networking theory, vendor-neutral firewall design, or generic Linux firewall/admin work unless the MikroTik/RouterOS context is explicit.

2. **Check local cache first**
   - Use `.MikroTik-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`
     - `.MikroTik-Encyclopedia/notes/devices/...`
     - `.MikroTik-Encyclopedia/notes/patterns/...`
     - `.MikroTik-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult official MikroTik docs before answering or touching devices**
   - Before answering direct or indirect MikroTik questions that depend on RouterOS behavior, syntax, feature boundaries, security posture, or version-sensitive details, consult the official docs unless the answer is already well-supported by the local cache.
   - Before performing direct SSH/API access against a MikroTik device, consult the relevant docs first when:
     - the exact command path matters
     - feature semantics are easy to misremember
     - the action could affect routing, switching, bridge behavior, VLANs, CAPsMAN, DHCP, firewalling, or management reachability
   - Do not improvise high-impact MikroTik commands from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult a MikroTik doc page, save a normalized markdown/text cache copy under `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate official documentation from local observations**
   - Store official-doc-derived material under `.MikroTik-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.MikroTik-Encyclopedia/notes/devices/`
     - `.MikroTik-Encyclopedia/notes/patterns/`
     - `.MikroTik-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - official documented behavior
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - device roles and naming
     - management-access methods
     - discovered topology relationships
     - CAPsMAN/controller placement
     - repeated gotchas or RouterOS command patterns
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same topology later.

## Live Access Rules

- Treat official docs lookup as the default preflight for non-trivial MikroTik work.
- Prefer read/inspect first when entering a device you have not recently reviewed.
- Treat edge routers/firewalls, bridge/VLAN changes, CAPsMAN changes, and management-service changes as high-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed device state.

## Data Root

Use this workspace-local root for cache and notes:

- `.MikroTik-Encyclopedia/`

Expected structure:

- `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`
- `.MikroTik-Encyclopedia/notes/devices/...`
- `.MikroTik-Encyclopedia/notes/patterns/...`
- `.MikroTik-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Device-specific observations → `.MikroTik-Encyclopedia/notes/devices/<device-name>.md`
- Reusable RouterOS patterns/gotchas → `.MikroTik-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide topology/access info → `.MikroTik-Encyclopedia/inventory/*.md`
- Cached official docs → `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.MikroTik-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official MikroTik docs page under `.MikroTik-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.MikroTik-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful MikroTik topic groupings for faster doc lookup.

## Good Outcomes

- Answer a MikroTik question using cached or freshly checked official docs instead of guesswork.
- Inspect a live MikroTik device after checking the relevant docs and record any new local topology knowledge.
- Build a growing local MikroTik knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off RouterOS discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering RouterOS-specific questions purely from memory when docs are easy to consult.
- Treating local observed behavior as if it were guaranteed official documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing device-specific observations into the official-doc cache tree.
- Making high-impact live changes before checking the relevant docs when exact behavior matters.
