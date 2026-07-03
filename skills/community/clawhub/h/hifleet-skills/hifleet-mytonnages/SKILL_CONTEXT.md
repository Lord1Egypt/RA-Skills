# Skill context

## Positioning

- **Route A**: User’s **mailbox** open tonnage / cargo → local SQLite + optional memory search.  
- **Route C**: **Pre-arrival** vessels at a port (HiFleet API); contacts on demand via **`CONTACT_API.md`**.  
- **Liner schedules** (bulk, Ro-Ro, container): skill **`hifleet-schedule`** (separate install).

## Requirements

| Capability | Needs |
|------------|--------|
| A (mailbox) | Email IMAP + optional memory-lancedb-pro |
| A enrich / C | `hifleet_api_key` |
| C contact fetch | `hifleet_liner_api_base` (unlock; see **`CONTACT_API.md`**) |

## One-liner

**A = my mail tonnage/cargo; C = pre-arrival at port; schedules = hifleet-schedule.**
