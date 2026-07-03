---
name: hifleet-schedule
version: 1.0.0
description: >
  HiFleet liner schedules: general/bulk cargo, Ro-Ro, and container sailings.
  Requires hifleet_api_key. Full list policy applies. Prefer English replies; localize UI text per user locale (LOCALIZATION.md).
metadata:
  openclaw:
    homepage: https://mytonnages.hifleet.com
    requires:
      anyBins:
        - python
        - python3
---

## Read first (do not skip)

Before any schedule query: **`read_file` `SKILL_CONTEXT.md`**, **`read_file` `ROUTING_AND_WHEN.md`**.

**User-facing language**: **`read_file` `LOCALIZATION.md`** — default **English**; translate system prompts/errors to the user’s agent locale; **never translate** vessel names, port names, cargo names, or API field values.

**First install / missing API Key**: **`read_file` `FIRST_SETUP.md`**.

**Full list (mandatory)**: **`read_file` `FULL_LIST_POLICY.md`** — paginate until `total` is exhausted.

---

## Query steps (agent internal)

### 0. Ready

1. Route check: **`ROUTING_AND_WHEN.md`** (schedule types: bulk/general, Ro-Ro, container).  
2. If `hifleet_api_key` missing → **`FIRST_SETUP.md`**.  
3. Execute **`SCHEDULE_API.md`** (port suggest → `POST /schedules` → contact fetch on user request via **`/unlock`**, `typeCode=product_vessel_liner_charter`; batch **全部** supported). Unlock table: **`references/charter_contact_unlock.md`**.

### 1. Output

**`WORKFLOW_OUTPUT.md`**, **`USER_WORDING.md`**.

---

## Package index

```text
hifleet-skills/hifleet-schedule/
├── SKILL.md
├── SKILL_CONTEXT.md
├── LOCALIZATION.md
├── ROUTING_AND_WHEN.md
├── FIRST_SETUP.md
├── SCHEDULE_API.md
├── FULL_LIST_POLICY.md
├── WORKFLOW_OUTPUT.md
├── USER_WORDING.md
├── CONFIG.example.md
├── scripts/i18n_messages.py
└── PUBLISH.md
```

Publish notes: **`PUBLISH.md`**.
