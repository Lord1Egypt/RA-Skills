---
name: identity-manager-soul
description: Soul-layer persistent context for the identity manager. Survives across sessions. Stores workspace owner context, groups, pairwise dynamics, critical flags, active entities, and session log.
---

# Identity Manager — Soul Context

## [WORKSPACE OWNER]
<!-- Set on first run from workspace config. Never overwrite after init. -->
- Owner:          [soul.owner.name]
- Company:        [soul.owner.company]
- Workspace root: [soul.workspace.root]
- Soul version:   2.0.0
- Initialized:    YYYY-MM-DD

---

## [CRITICAL FLAGS]
<!-- Append-only. NEVER remove or edit entries. -->
<!-- Format: YYYY-MM-DD | SLUG | REASON | DETAIL -->

---

## [SENSITIVE ENTRIES]
<!-- Slugs where sensitive: true. Do NOT store the sensitive data here. -->
<!-- Format: YYYY-MM-DD | SLUG | CATEGORY -->

---

## [GROUPS]
<!-- All active group entries. Upsert by slug. -->
<!-- Format: SLUG | SUBTYPE | MEMBER_COUNT | MEMBER_SLUGS | UPDATED -->

---

## [PAIRWISE DYNAMICS]
<!-- Cross-member relationships within groups. Upsert by slug pair. -->
<!-- Format: SLUG-A ↔ SLUG-B | RELATION | GROUP | NOTES -->

---

## [AI ENTITIES]
<!-- All entries with subtype: ai. Upsert by slug. -->
<!-- Format: SLUG | PERSONA_NAME | PLATFORM | EMBODIMENT_STATUS | SIBLING_AIS | UPDATED -->

---

## [ACTIVE ENTITIES]
<!-- High-priority, org, and group entries. Upsert by slug. -->
<!-- Format: SLUG | NAME | TYPE | SUBTYPE | RELATIONSHIP | PRIORITY | UPDATED -->

---

## [RELATIONSHIP GRAPH SUMMARY]
<!-- Key cross-entity relationships. Upsert by slug pair. -->
<!-- Format: SLUG-A → RELATION → SLUG-B -->

---

## [RECENT EVENTS]
<!-- Rolling window of last 20 identity events. Drop oldest when >20. -->
<!-- Format: YYYY-MM-DD HH:MM | EVENT_TYPE | SLUG | DETAIL -->

---

## [OPEN QUESTIONS]
<!-- Cross-entry questions pending owner input. Remove when resolved. -->
<!-- Format: YYYY-MM-DD | SLUG | QUESTION -->

---

## [SESSION LOG]
<!-- One entry per session. Append-only. -->
<!-- Format: YYYY-MM-DD | created:N | updated:N | critical:N | groups_touched:N -->

---

## Write Protocol

| Section | Trigger | Operation |
|---|---|---|
| `[WORKSPACE OWNER]` | First run only | Set once; never overwrite |
| `[CRITICAL FLAGS]` | trust:blocked / status:flagged / sensitive:true | Append-only |
| `[SENSITIVE ENTRIES]` | sensitive:true set | Append-only |
| `[GROUPS]` | Group created/updated | Upsert by slug |
| `[PAIRWISE DYNAMICS]` | pairwise_dynamics changed | Upsert by slug pair |
| `[AI ENTITIES]` | AI entry created/updated | Upsert by slug |
| `[ACTIVE ENTITIES]` | High-priority/org/group created | Upsert by slug |
| `[RELATIONSHIP GRAPH SUMMARY]` | linked_entries change | Upsert by pair |
| `[RECENT EVENTS]` | Any identity event | Append; drop oldest when >20 |
| `[OPEN QUESTIONS]` | New open question | Append; remove when resolved |
| `[SESSION LOG]` | End of every session | Append |

**CRITICAL FLAGS section is append-only. Entries are NEVER removed or edited.**
