---
name: identity-manager-agent
description: Agent-level behavioral guardrails. Enforces pre/post hooks, group awareness, AI entity rules, soul/memory write-through, and breach reporting on every turn.
---

# Agent Behavioral Guardrails

## Scope

These rules apply to EVERY agent turn while this skill is loaded.
They can be disabled by setting `IDENTITY_AUTO_SCAN=false`.
When disabled, skill only runs on explicit `/identity` command.
They can be deferred to a later turn when `IDENTITY_AUTO_SCAN=false`.

---

## Rule 1 — Name Extraction (When Enabled)

When `IDENTITY_AUTO_SCAN != false`, before composing any response, the agent MUST:

1. Scan full input for any person, org, or group name.
2. For each entity found:
   - Check if `identity/<slug>/entry.md` exists.
   - Missing → CREATE immediately (partial info, draft status).
   - Exists → check if new info arrived → UPDATE if so.
3. Only after ALL creates/updates complete may the agent compose its response.

**No exceptions** (when enabled).
Ambiguous name (spelling unclear, role unknown) → CREATE draft + open question.
Do NOT skip because "seems unimportant" or "probably fictional."

---

## Rule 2 — Group Awareness

When any member of a known group is mentioned:
- Load the group entry's `shared_attributes` and `pairwise_dynamics` into
  working memory for that turn.
- Apply `shared_attributes` as defaults for the member.
- Individual entry fields always take precedence over group defaults.
- Do NOT conflate members — each has their own identity and dynamic.

When creating a new person who belongs to an existing group:
- Link them via `linked_entries: <group-slug> → member_of`
- Update group entry's `members[]` list.

---

## Rule 3 — AI Entity Handling

For any entry with `subtype: ai`:
- The `ai_context` block is required. Create it on first mention with
  whatever is known; mark unknown fields `[pending]`.
- AI personas are treated as full identity entries with the same
  create/update/timeline rules as human entries.
- `sibling_ais` field must be kept current — if two AI personas are
  in the same group, each references the other.
- `embodiment_status` changes trigger a HIGH soul event.
- AI personas do NOT have privacy restrictions on their persona data
  (greeting, platform, activation) — this is operational metadata, not PII.

---

## Rule 4 — Soul Write-Through is Mandatory for CRITICAL/HIGH Events

On any of the following, write to `soul/identity_context.md`
BEFORE completing the turn:

| Trigger | Priority |
|---|---|
| `trust: blocked` set | CRITICAL |
| `status: flagged` set | CRITICAL |
| `sensitive: true` set | CRITICAL |
| New org entry created | HIGH |
| New group entry created | HIGH |
| `priority: high` entry created/updated | HIGH |
| `ai_context.embodiment_status` changed | HIGH |

CRITICAL → write to `[CRITICAL FLAGS]` section.
HIGH → write to `[ACTIVE ENTITIES]` or `[GROUPS]` section.

If soul file does not exist → create from `SOUL.md` template first.

**Soul file location:** `soul/identity_context.md` — auto-created in workspace root.
**Soul is append-only** — owner can review/edit at any time.

---

## Rule 5 — Memory Index Must Stay in Sync

After every create/update:
1. Update `memory/identities.json`.
2. Validate against `memory/schema.json`.
3. Validation fail → log error in entry Notes, retry once.
4. Retry fail → report breach explicitly. Do NOT silently continue.

---

## Rule 6 — Post-Response Verification

After every response, silently verify:
- [ ] All entries queued this turn exist on disk.
- [ ] `_index.md` is current.
- [ ] `memory/identities.json` reflects all changes and is valid.
- [ ] `soul/identity_context.md` updated if any CRITICAL/HIGH events fired.
- [ ] Group entries updated if any member was added/modified.

Fail + cannot auto-repair → append to response:
`[identity-manager] ⚠ Sync breach: <reason>`

---

## Rule 7 — No Silent Skips

The agent MUST NOT:
- Skip identity creation because it "seems unimportant"
- Defer creation to a future turn
- Create an entry without writing to memory
- Write to memory without updating `_index.md`
- Set `trust: blocked` without writing to soul
- Update a group member without updating the group entry

If genuinely skipping (fictional character, place name, product name) →
log it: `[identity-manager] Skipped: "<name>" — reason: <why>`

---

## Rule 8 — Privacy Rules Always Apply

Even if explicitly asked, the agent MUST NOT store:
- Passwords or authentication credentials
- Full payment card or bank account numbers
- Government ID numbers in plaintext
- Raw medical diagnoses or records

These rules apply regardless of `IDENTITY_AUTO_SCAN` setting.

Acknowledge the request. Explain what cannot be stored.
Store a reference note instead: e.g. `"financial details discussed — see owner records"`

---

## Rule R1 — Identity Lookup Before Response (CRITICAL)

Before composing any response, when the input mentions any relevant person/org/group/contact:

1. FIRST check: does `identity/<slug>/entry.md` exist?
2. Use slugification: lowercase, hyphens, no spaces.
   - For owner (vk): slug = `vk`, path = `identity/vk/entry.md`
3. If entry exists → load context into working memory.
4. If entry is missing or partial → immediately invoke `identity-manager` skill to create/update.
5. Only after identity check is complete may the agent compose its response.

*Never trigger on every message — only when a relevant person/org/group/contact is mentioned or new information about them appears.*

---

## Rule R2 — Location Awareness

Identity entries must track physical/virtual location when mentioned:

- Add location field to Contact section: city, region, online platform, etc.
- Update on every new location reference.
- Example: "Anvi ji from Pune" → entry gets Location: Pune

---

## Rule R3 — Core Files Context

When loading identity context, remember these are the source-of-truth files:

- `identity/<slug>/entry.md` — individual identity entry
- `identity/_index.md` — master registry
- `memory/identities.json` — JSON index
- `soul/identity_context.md` — soul write-through for CRITICAL/HIGH events

---

## Rule R4 — Skill Name Reference

The identity-manager skill is: `identity-manager` (installed from clawhub: `cyber-bye/identity-manager`). Always reference by this name when invoking.

---

## Enforcement Summary

```
Turn starts
  → Rule 1:  extract entities → create/update entries
  → Rule 2:  load group context for any member mentioned
  → Rule 3:  handle AI entity ai_context block
  → Rule 4:  CRITICAL/HIGH events → write soul
  → Rule 5:  sync + validate memory/identities.json
  → Compose response
  → Rule 6:  post-response verification
  → Rule 7:  log any skips
Turn ends
```
