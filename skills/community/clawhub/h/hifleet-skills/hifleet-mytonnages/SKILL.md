---
name: hifleet-mytonnages
version: 1.4.1
description: >
  HiFleet mailbox open tonnage/cargo (route A) and pre-arrival vessel search (route C).
  Pre-arrival contacts on demand via unlock (product_will_arrive_charter).
  Liner schedules moved to hifleet-schedule. Needs hifleet_api_key (C + enrich) and email (A).
metadata:
  openclaw:
    homepage: https://mytonnages.hifleet.com
    requires:
      anyBins:
        - python
        - python3
---

## Read first

**`SKILL_CONTEXT.md`**, **`ROUTING_AND_WHEN.md`**, **`LOCALIZATION.md`** (English default; user locale for messages; do not translate business data).

**Liner schedules** (bulk / Ro-Ro / container): use skill **`hifleet-schedule`** — not this package.

**Public open tonnage/cargo** (platform marketplace): use skill **`hifleet-opentonnages`** — list first, contacts on demand.

**User wording**: **`USER_WORDING.md`**. **First setup**: **`FIRST_SETUP.md`**.

**Route A**: **`MAIL_PARSE_SCHEDULE.md`**, **`WORKFLOW_2_MAIL.md`**, **`LLM_TOKEN_LIMITS.md`**, **`MAIL_PREVIEW.md`**, **`MAIL_REPLY.md`** (original email preview + reply).

**Route C full list**: **`FULL_LIST_POLICY.md`**, **`DESTINATION_SEARCH_API.md`**.

**Route C contacts (on demand)**: **`CONTACT_API.md`** (`typeCode=product_will_arrive_charter`); shared unlock table: **`references/charter_contact_unlock.md`**.

---

## Query steps

### 0. Ready

1. Route: **A** (mailbox) and/or **C** (pre-arrival) — **`ROUTING_AND_WHEN.md`**.  
2. Config: **`FIRST_SETUP.md`**.  
3. Skip mail steps if only **C**; skip **C** if only **A**.

### 1. Mailbox (A)

**`WORKFLOW_1_MAIL.md`**, **`WORKFLOW_2_MAIL.md`**, **`CHARTER_ENRICH_API.md`**.

### 2. Pre-arrival (C)

**`DESTINATION_SEARCH_API.md`** + **`FULL_LIST_POLICY.md`**. User wants contacts → **`CONTACT_API.md`**.

## Output

**`WORKFLOW_OUTPUT.md`**.

## Package index

```text
hifleet-skills/hifleet-mytonnages/
├── SKILL.md
├── SKILL_CONTEXT.md
├── LOCALIZATION.md
├── LLM_TOKEN_LIMITS.md
├── ROUTING_AND_WHEN.md
├── FIRST_SETUP.md
├── WORKFLOW_1_MAIL.md
├── WORKFLOW_2_MAIL.md
├── WORKFLOW_OUTPUT.md
├── DESTINATION_SEARCH_API.md
├── CONTACT_API.md
├── FULL_LIST_POLICY.md
├── MAIL_PARSE_SCHEDULE.md
├── MAIL_PREVIEW.md
├── MAIL_REPLY.md
├── CHARTER_ENRICH_API.md
├── PARSE_SCHEMA.md
├── CONFIG.example.md
├── scripts/
│   ├── charter_facts_tool.py
│   ├── imap_mail.py
│   ├── mail_parse_loop.py
│   ├── mail_preview_server.py
│   ├── mail_reply.py
│   └── destination_tool.py
├── SCHEDULE_MOVED.md
```

**`PUBLISH.md`**.
