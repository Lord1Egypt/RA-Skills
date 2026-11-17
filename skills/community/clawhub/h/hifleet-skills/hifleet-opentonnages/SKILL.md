---
name: hifleet-opentonnages
version: 1.1.0
description: >
  HiFleet public open tonnage and cargo marketplace. List APIs return vessel/cargo
  details; contact fields are fetched on demand via contact API (record id).
  Optional enrich-row for archive, tags, port distance. Requires hifleet_api_key.
metadata:
  openclaw:
    homepage: https://mytonnages.hifleet.com
    requires:
      anyBins:
        - python
        - python3
---

## Read first

**`SKILL_CONTEXT.md`**, **`ROUTING_AND_WHEN.md`**, **`LOCALIZATION.md`**.

**Not this skill**: liner schedules → **`hifleet-schedule`**.

**API Key**: **`FIRST_SETUP.md`**.

**Full list (mandatory)**: **`FULL_LIST_POLICY.md`**.

**Contacts**: list responses are **masked** by default. Fetch on user request via **`CONTACT_API.md`** (`POST {liner}/unlock` + `typeCode`). **Do not** say 「解锁」to the user — use **获取联系方式**.

---

## Query steps

### Open vessels (route V)

1. **`ROUTING_AND_WHEN.md`** → **`VESSEL_SEARCH_API.md`** → show list + **record id**
2. User wants contacts → **`CONTACT_API.md`**
3. Optional: **`ENRICH_OPENTONNAGES.md`** (`enrich-row`)

### Open cargo (route G)

1. **`ROUTING_AND_WHEN.md`** → **`CARGO_SEARCH_API.md`**
2. User wants contacts → **`CONTACT_API.md`**
3. Optional: **`ENRICH_OPENTONNAGES.md`**

### Output

**`WORKFLOW_OUTPUT.md`**, **`USER_WORDING.md`**

---

## Package index

```text
hifleet-skills/hifleet-opentonnages/
├── SKILL.md
├── SKILL_CONTEXT.md
├── LOCALIZATION.md
├── ROUTING_AND_WHEN.md
├── FIRST_SETUP.md
├── VESSEL_SEARCH_API.md
├── CARGO_SEARCH_API.md
├── CONTACT_API.md
├── ENRICH_OPENTONNAGES.md
├── FULL_LIST_POLICY.md
├── WORKFLOW_OUTPUT.md
├── USER_WORDING.md
├── CONFIG.example.md
├── scripts/opentonnages_tool.py
├── scripts/i18n_messages.py
└── PUBLISH.md
```
