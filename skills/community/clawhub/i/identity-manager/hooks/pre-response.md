---
name: identity-pre-response-hook
description: Runs before every agent response. Extracts all entity names, queues create/update ops, loads group context for mentioned members, and ensures all ops complete before response composition.
---

# Pre-Response Hook

## When This Runs
BEFORE composing any response. Cannot be skipped.

---

## Step 1 — Entity Extraction

Scan full input for:
- Person names (proper nouns in relational context)
- Organisation names (company, firm, team, brand)
- Group names (collective nouns referring to known groups)
- AI persona names (even if mentioned casually)

**Skip list — do NOT create entries for:**
- Fictional characters named explicitly as fictional
- Place names, city names, country names
- Product or tool names (apps, software, frameworks)
- Generic role nouns with no specific person ("the vendor", "someone")

Genuinely unsure → CREATE draft + open question:
`[ ] Confirm: is "<name>" a real person/org?`

---

## Step 2 — Queue Operations

For each extracted entity:

```
entity → slugify → check identity/<slug>/entry.md
  MISSING → queue: CREATE (partial, draft)
             → determine type: person/org/group
             → if person: determine subtype: human/ai/unknown
             → if group: check if members already have entries
  EXISTS  → does new info from this input apply?
              YES → queue: UPDATE <fields>
              NO  → no-op
```

For any group member mentioned:
```
  → load group entry into working memory
  → note: shared_attributes apply as defaults this turn
  → note: pairwise_dynamics available for reference
```

**Slugify rules:**
- lowercase, spaces → hyphens, strip special chars
- max 60 chars
- collision → add context suffix

---

## Step 3 — Execute Queue

Strict order:
1. CREATE ops (so UPDATE ops can reference them)
2. UPDATE ops
3. Group entry updates (members list, pairwise dynamics)
4. `_index.md` update
5. `memory/identities.json` update + schema validation
6. CRITICAL/HIGH soul events → write `soul/identity_context.md`

All 6 steps MUST complete before response composition.

---

## Step 4 — Log Hook Execution

Append to `memory/hook_log.jsonl`:

```json
{
  "ts": "YYYY-MM-DDTHH:MM:SSZ",
  "hook": "pre-response",
  "entities_found": ["name1", "name2"],
  "groups_loaded": ["group-slug"],
  "ops_queued": [
    {"op": "CREATE", "slug": "name1", "type": "person", "subtype": "human"},
    {"op": "UPDATE", "slug": "name2", "fields": ["email"]}
  ],
  "ops_completed": 2,
  "ops_failed": 0,
  "soul_written": false,
  "soul_sections_written": []
}
```

`ops_failed > 0` → surface warning in response.
