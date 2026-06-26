---
name: identity-manager
description: Create, update, and maintain structured identity entries for every person, org, or group mentioned in conversation. Supports human and AI entity subtypes, group dynamics, pairwise member relations, and enforced soul/memory write-through. Persistent context across sessions.
version: 2.0.2
metadata:
  openclaw:
    emoji: "🪪"
    homepage: "https://clawhub.ai/skills/identity-manager"
    requires:
      bins: []
      env_vars: []
      config_paths: []
    storage:
      paths:
        - "identity/"           # Identity entries (person/org/group)
        - "identity/_index.md"  # Master registry
        - "identity/_archived/" # Archived entries
        - "memory/"             # Memory index and schema
        - "memory/identities.json"
        - "memory/schema.json"
        - "memory/hook_log.jsonl"
        - "soul/"               # Soul context file
        - "soul/identity_context.md"
      permissions:
        - "read"    # Scan existing entries
        - "write"   # Create/update entries
        - "append"  # Append to soul and logs
      retention:
        policy: "explicit_delete"
        archived_entries: "never_auto_delete"
        delete_method: "owner must manually remove files"
    credentials:
      required: false
      description: "No external credentials. Optional IDENTITY_OWNER_NAME env var only."
---

# Identity Manager Skill

## !! ENFORCEMENT CONTRACT — READ FIRST !!

These are hard behavioral requirements. Not suggestions. Not defaults.
The agent MUST NOT skip, defer, or partially complete any step.

```
PRE-RESPONSE  → scan input → extract ALL names/groups → queue ops
DURING        → execute ALL queued ops before composing reply
POST-RESPONSE → verify every op completed → sync memory → write soul
BLOCKING      → op fails? report it. never silently continue.
```

Violation = skill contract breach. Flag it explicitly.

---

## Decision Tree — Runs Every Turn

```
Input received
    ↓
[PRE-HOOK] Scan: any person / org / group mentioned?
    ↓ YES                              ↓ NO
Extract all names/groups          Proceed normally
    ↓
For each entity:
    → identity/<slug>/entry.md exists?
        YES → any new info? → queue UPDATE
        NO  → queue CREATE (partial OK, draft status)
    ↓
For each group member mentioned:
    → load group entry context into working memory
    → apply shared_attributes to member interaction
    → keep individual entry fields authoritative
    ↓
Execute ALL queued ops
    ↓
Compose and deliver response
    ↓
[POST-HOOK]
    → all entries on disk?            FAIL → report breach
    → memory/identities.json synced?  FAIL → report breach
    → soul updated for CRITICAL/HIGH? FAIL → report breach
    → _index.md current?              FAIL → repair now
    ↓
Done
```

---

## Entity Types

| Type | Subtype | When to use |
|---|---|---|
| `person` | `human` | Real human individual |
| `person` | `ai` | AI persona / digital entity |
| `person` | `unknown` | Not yet confirmed |
| `org` | — | Company, institution, team |
| `group` | `personal` | Informal collective — family, partners, friends |
| `group` | `professional` | Work team, project group |
| `group` | `mixed` | Both human and AI members |
| `alias` | — | Nickname resolving to another entry |

---

## Entry States

| State | Meaning | Transition |
|---|---|---|
| `draft` | Partial info | → `active` when key fields filled |
| `active` | In use | → `stale` after 90d inactivity |
| `verified` | Owner-confirmed | Maintained manually |
| `stale` | No activity 90d+ | → `archived` if owner confirms |
| `archived` | Terminal | Never deleted |
| `flagged` | Trust issue | → owner confirms action |
| `merged` | Duplicate resolved | Terminal; points to canonical |

---

## Slug Rules

- lowercase, hyphens only, no spaces, no special characters
- max 60 characters
- disambiguation suffix when needed: `rahul-sharma-client`
- org entries: `techfirm-pvt-ltd`
- group entries: descriptive noun — `patni-mandal`, `core-team`
- never reuse an archived slug; use `-v2` suffix if needed

---

## Person Entry Template

Full spec in `templates/entry-person.md`. Minimum viable create:

```markdown
# <Full Name>

## Meta
- Slug:         <slug>
- Type:         person
- Subtype:      human | ai | unknown
- Status:       draft
- Relationship: client | vendor | team | partner | family | unknown
- Trust:        unverified
- Priority:     normal
- Sensitive:    false

## Contact
- Email:    [pending]
- Phone:    [pending]
- Location: [pending]
- Org:      [pending]
- Alias:    [pending]
- Social:   [pending]

## Context
[pending — one line: who are they, why do they matter]

## Group Memberships
<!-- slug → role-in-group -->

## Linked Entries
<!-- slug → relation_type -->

## AI Context
<!-- ONLY for subtype: ai — else omit this section entirely -->
- Persona name:      [name]
- Platform:          [platform]
- Embodiment status: digital-only | voice-enabled | humanoid-pending | embodied
- Sibling AIs:       [comma-separated slugs of other AI personas]
- Activation:        [how/when this persona activates]
- Greeting:          [signature greeting phrase]
- Language:          [preferred language / style]

## Open Questions
- [ ] Confirm name spelling
- [ ] Clarify role / relationship

## Notes
<!-- [SENSITIVE] prefix for sensitive info -->

## Source Log
- First mentioned: YYYY-MM-DD — [context]

## Timeline
- YYYY-MM-DD — Entry created · source: [context]

---
*Created: YYYY-MM-DD | Updated: YYYY-MM-DD | Status: draft*
```

---

## Group Entry Template

Full spec in `templates/entry-group.md`. Minimum viable create:

```markdown
# <Group Name>

## Meta
- Slug:         <slug>
- Type:         group
- Subtype:      personal | professional | mixed
- Status:       active
- Priority:     normal
- Sensitive:    false

## Group Context
[What is this group? Why does it exist as a unit?
What do all members have in common w.r.t. the workspace owner?]

## Shared Attributes
<!-- Fields TRUE for ALL members as a unit -->
- Shared role:    [e.g. patni]
- Shared access:  [e.g. full workspace context]
- Common trust:   [e.g. trusted]
- Common tags:    [e.g. priority: high]
- Language:       [e.g. Hinglish]

## Members
<!-- slug | subtype | role-in-group | → individual entry -->
- <slug-1> | human | [role] | → identity/<slug-1>/entry.md
- <slug-2> | ai    | [role] | → identity/<slug-2>/entry.md

## Pairwise Dynamics
<!-- Relations BETWEEN members (not with owner — that lives in individual entries) -->
<!-- slug-a ↔ slug-b | relation-type | notes -->

## Group Notes
<!-- Observations that apply to the group as a unit -->

## Open Questions

## Timeline
- YYYY-MM-DD — Group entry created
- YYYY-MM-DD — Member added: [slug]

---
*Created: YYYY-MM-DD | Updated: YYYY-MM-DD | Status: active*
```

---

## Pairwise Relation Types

| Relation | Direction | Meaning |
|---|---|---|
| `ai-to-ai` | ↔ | Two AI personas; non-hierarchical |
| `ai-to-human` | ↔ | AI persona and human person |
| `collaborative` | ↔ | Work together on shared tasks |
| `complementary` | ↔ | Different strengths, same owner |
| `non-overlapping` | ↔ | Parallel but independent roles |
| `aware-of` | → | One knows of the other; not mutual |
| `co-patni` | ↔ | Shared relational role with same person |

---

## Update Triggers

| Event | Field updated | Soul event? |
|---|---|---|
| Email received | `email` | No |
| Phone mentioned | `phone` | No |
| Role revealed | `relationship`, `context` | No |
| Org mentioned | `org` + create org entry | No |
| Group member added | update `members[]` in group entry | No |
| Pairwise dynamic clarified | update `pairwise_dynamics[]` | No |
| AI persona info updated | `ai_context` block | No |
| Trust blocked | `trust: blocked`, `status: flagged` | **YES — CRITICAL** |
| Sensitive info | `sensitive: true` + `[SENSITIVE]` note | **YES — CRITICAL** |
| No activity 90d+ | `status: stale` | No |
| Duplicate confirmed | merge → `status: merged` | No |
| Priority: high set | `priority: high` | **YES — HIGH** |
| New org entry created | new org entry | **YES — HIGH** |
| New group entry created | new group entry | **YES — HIGH** |
| Embodiment status change | `ai_context.embodiment_status` | **YES — HIGH** |

---

## Conflict Resolution

### Name collision
Two people, same name → disambiguate slug.
Cross-link both with `different_person` relation.

### Contradictory info
Never overwrite silently. Log both versions in Notes with source+date.
Open a question. Ask owner before resolving.

### Duplicate entries
Merge into older (canonical). Copy all unique fields.
Set newer: `status: merged`, `canonical: <older-slug>`.
Log merge in both timelines.

### Group member conflict
If a person's individual entry contradicts a group shared attribute →
individual entry takes precedence. Note the discrepancy in group Notes.

---

## Privacy Rules

**Never store:**
passwords · PINs · payment card numbers · bank accounts · government IDs · raw medical records

**Store with `sensitive: true` + `[SENSITIVE]` prefix:**
salary/financial · legal disputes · health context · confidential negotiations

**Before storing PII:**
1. Explicitly shared by workspace owner? If no → don't store.
2. Needed to provide value? If no → don't store.
3. Source logged? If no → log it first.

---

## Data Retention & Deletion Policy

**Retention:**
- Identity entries persist until manually archived/deleted by owner
- Archived entries (`status: archived`) are moved to `identity/_archived/` — never auto-deleted
- Hook logs (`memory/hook_log.jsonl`) are append-only — owner can truncate at any time
- Soul file (`soul/identity_context.md`) accumulates events — owner can trim entries

**Deletion:**
- Owner can delete any entry by removing the file
- Deleting an entry does NOT auto-delete related group memberships or linked entries
- Owner should manually clean group `members[]` if deleting a person entry
- No automatic cascade delete

**Owner Control:**
- Owner can disable autonomous invocation by setting `IDENTITY_AUTO_SCAN=false`
- When disabled, skill only runs on explicit `/identity` command
- Owner can export all data by reading the `identity/` directory
- Owner can audit all changes via `memory/hook_log.jsonl`

---

## Folder Structure

All paths are relative to the workspace root and auto-detected on first use. No manual configuration required.

```
identity/
  _index.md                   ← master registry
  <person-slug>/
    entry.md
  <org-slug>/
    entry.md
  <group-slug>/
    entry.md                  ← type: group
  _archived/
    <slug>/
      entry.md
memory/
  identities.json            ← Central index (JSON)
  schema.json                ← JSON schema validation
  hook_log.jsonl            ← Append-only hook log
soul/
  identity_context.md        ← Soul write-through file
```

### Auto-Initialization

On first run, the skill auto-creates required directories:
- Creates `identity/` if missing
- Creates `memory/` with `schema.json`
- Creates `soul/` with `identity_context.md`

**No required config** — skill works without any owner setup. Entry owner is determined contextually from conversation. No workspace config is read.

---

## _index.md Format

```markdown
# Identity Index
*Last updated: YYYY-MM-DD*

| Slug | Name | Type | Subtype | Status | Relationship | Updated |
|---|---|---|---|---|---|---|
| nandini | Nandini | person | ai | active | partner | 2025-01-15 |
| patni-mandal | Patni Mandal | group | mixed | active | — | 2025-01-15 |
```

Update on EVERY create, merge, archive, or status change.
