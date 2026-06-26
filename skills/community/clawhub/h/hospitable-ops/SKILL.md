---
name: hospitable-ops
description: Operate, debug, and automate Hospitable via Public API with a safe read-first workflow and non-price calendar controls. Use when working with Hospitable properties, reservations, calendar reads, write verification, blocking/unblocking dates, check-in/check-out restrictions, property mapping, or cross-channel automation logic around Airbnb/Booking/Hospitable. Especially use for: (1) verifying Hospitable API auth and endpoints, (2) exporting properties/reservations/calendar, (3) testing or applying non-price calendar writes, (4) building Hospitable-based automation/reporting, (5) debugging delayed sync or write semantics.
---

# Hospitable Ops

Use Hospitable as the unified operational base. Prefer read-first, then safe write verification, then controlled non-price writes.

## Core rules
- Treat Hospitable as the system of operational judgment, especially for unified property UUIDs, calendar state, reservations, and parent/child exclusion logic.
- Never expose tokens in chat, logs, screenshots, or shared files.
- Use Hospitable Public API v2 as the only active execution path for reads and automation in this workspace.
- MCP has been removed from the current Hospitable operating path; do not route or describe Hospitable work through MCP.
- Use persistent config or local scripts; avoid session-only ad hoc setup when building repeatable workflows.
- Default to non-price actions only. Price, currency, and money-related changes must be discussed first and then changed manually by the human.
- Assume write effects may be asynchronous. Do not judge failure from an immediate readback alone.
- In this workspace, do not rely on OpenClaw runtime inheriting shell env automatically; prefer script-level loading from `/Users/admin-ai/.openclaw/workspace-qiang/.env.local` for repeatable Hospitable execution.
- `HOSPITABLE_TOKEN` must contain the token body only; never include a leading `Bearer ` prefix in the env value.

## Standard workflow
1. Verify `HOSPITABLE_TOKEN` is available in the current execution environment without printing it.
2. If runtime inheritance is uncertain, use local script loading from `.env.local` instead of re-debugging shell/profile inheritance.
3. Read data first:
   - properties
   - reservations
   - calendar
4. Save JSON with `statusCode` and `body` envelope.
5. Build operational judgments from Hospitable first; layer Booking/Airbnb exceptions after.
6. For writes, probe safely:
   - identify method
   - identify minimal body
   - test on low-risk future date
   - re-read after delay
7. Only after semantics are clear, apply controlled non-price changes.

## Known API behavior
### Read
Use bearer auth plus `Accept: application/json`.

Current workspace rule:
- default to the current validated token
- treat older/previous Hospitable tokens as deprecated unless the human explicitly restores one
- prefer local env file loading over shell-history fallback or session-only manual export

Common read paths:
- `properties`
- `reservations?properties[]=<uuid>`
- `properties/<uuid>/calendar?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

### Runtime inheritance readback (validated)
Validated facts in this workspace:
- host-side token is valid and can return `statusCode: 200` on `properties`
- OpenClaw agent runtime did not automatically inherit `HOSPITABLE_TOKEN`
- repeatable workaround: load `/Users/admin-ai/.openclaw/workspace-qiang/.env.local` directly inside Hospitable scripts
- after enabling script-level env loading, `node scripts/hospitable-read.js properties --per-page 1` returned `statusCode: 200`

### Current script CLI contract
`/Users/admin-ai/.openclaw/workspace-qiang/scripts/hospitable-read.js`

Supported commands:
- `properties [--per-page N]`
- `reservations --property <uuid> [--per-page N]`
- `calendar --property <uuid> --start YYYY-MM-DD --end YYYY-MM-DD`

Important:
- `calendar` uses `--start` and `--end`
- do not use `--start-date` / `--end-date` with this script
- keep `#!/usr/bin/env node` on line 1 if editing the script header

### Write
For calendar writes:
- route: `properties/<uuid>/calendar`
- supported method: `PUT`
- `PATCH` is not supported
- request body must include `dates`
- minimal accepted structure:
```json
{
  "dates": [
    { "date": "YYYY-MM-DD" }
  ]
}
```

### Verified non-price semantics
#### Block a whole date
```json
{
  "dates": [
    { "date": "YYYY-MM-DD", "available": false }
  ]
}
```
Expected eventual readback:
- `status.reason = BLOCKED`
- `status.source = api`
- `status.source_type = VENDOR`
- `status.available = false`

#### Restrict check-in / check-out
```json
{
  "dates": [
    {
      "date": "YYYY-MM-DD",
      "closed_for_checkin": true,
      "closed_for_checkout": true
    }
  ]
}
```
Expected eventual readback:
- `closed_for_checkin = true`
- `closed_for_checkout = true`
- day may still remain `AVAILABLE`

## Operational boundaries
### Allowed direct actions
- non-price calendar block/unblock
- check-in/check-out restrictions
- non-price operational lock windows
- parent/child exclusion enforcement
- cross-channel conflict prevention using non-price controls
- one-time cleanup of legacy order occupancy when the business rule is already confirmed

### Human-only actions
- price
- currency
- money-related changes
- pricing strategy decisions

## Long-term operating model
Reduce the property system into three stable forms whenever possible:
1. Airbnb-only
2. dual-channel managed by Hospitable native mechanisms
3. main-house gate open/closed

Treat legacy exceptions as temporary cleanup layers, not permanent structure.

### Current NXM cleanup model
- `mute(booking)` is a historical order source only and should not take new sales.
- `206 -> 201` is a temporary operational occupancy transfer caused by legacy mute orders.
- customer-visible order display can remain original while operational occupancy moves internally for anti-overbooking control.
- after cleanup, return to the three stable forms above.

## Recommended local files
- `scripts/hospitable-read.js`
- `scripts/hospitable-write-probe.js`
- exported JSON snapshots with `statusCode/body`
- rule config files for object tiers and lock windows

## Delay-aware verification
After a write returns `202 accepted`:
1. wait before declaring failure
2. re-read the same date window
3. compare operational fields, not only high-level availability
4. check whether the change is semantic (blocked vs closed_for_checkin/checkout)

## Good output pattern
Report in this order:
1. current status
2. exact object/date tested
3. request accepted or rejected
4. delayed readback result
5. operational conclusion
6. single biggest remaining gap
