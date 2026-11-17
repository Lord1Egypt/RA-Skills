<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Routing Log — AI-FLO

**Created:** {date}
**Workspace:** Mode {1/2/3}
**Purpose:** Append-only audit trail of all routing events. Never edit or delete entries.

---

## Log Entries

| # | Timestamp | Project ID | From | To | Type | Trigger | Operator | Notes |
|---|-----------|------------|------|-----|------|---------|----------|-------|
| 1 | {ISO datetime} | — | — | — | Init | FLO configured | @{operator} | Mode {X}, {N} projects |

---

## Type Reference

| Type | Meaning | Spine Entry? |
|------|---------|:------------:|
| Init | FLO initialization/reconfiguration | ❌ |
| Hop | Normal routing from A to B | ❌ |
| Hold | Routing paused (fan-in wait or conflict) | ❌ |
| Skip | Package bypassed (profile or toggle) | ✅ FLO-D- |
| Override | Operator changed the default route | ✅ FLO-D- |
| Toggle | Package switched on/off | ✅ FLO-D- |
| Cancel | Project flow terminated | ✅ FLO-D- |
| Rework | Routed backward (quality gate failure) | ✅ FLO-D- |
| Dispatch | New project entered the flow | ✅ FLO-D- |
| Escalate | Conflict/issue escalated to PPM | ✅ FLO-I- |
| Auto-resolve | Timeout expired; fallback rule applied | ✅ FLO-D- |
| Roll-Up | Report generated for PPM | ❌ |
| Drift | Position drift detected on resume | ❌ |

---

*Append-only. Corrections are new entries with Type="Correction" referencing the original #.*
