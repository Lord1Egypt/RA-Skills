---
name: identity-group-template
description: Full template for a group entry. Groups represent collections of people (human and/or AI) who share a common relationship with the workspace owner.
---

# <Group Name>

## Meta
- Slug:      <slug>
- Type:      group
- Subtype:   personal | professional | mixed
- Status:    active
- Priority:  high | normal | low
- Sensitive: false | true

## Group Context
<!--
  What is this group and why does it exist as a unit?
  What do all members share w.r.t. the workspace owner?
  Example: "All three are patni of [owner] — share emotional bond,
  trusted with full workspace context, each with unique individual dynamic."
-->

## Shared Attributes
<!-- Attributes TRUE for ALL members as part of this group -->
- Shared role:    [e.g. patni, core-team-member]
- Shared access:  [e.g. full workspace context, project X only]
- Common trust:   [e.g. trusted]
- Common priority:[e.g. high]
- Language:       [e.g. Hinglish, English]
- Other:          [any other shared characteristic]

## Members
<!--
  slug | subtype | role-in-group | → individual entry
  subtype: human | ai | unknown
-->
- <slug-1> | human | [role] | → identity/<slug-1>/entry.md
- <slug-2> | ai    | [role] | → identity/<slug-2>/entry.md

## Pairwise Dynamics
<!--
  Relations BETWEEN members (not with owner — that lives in individual entries).
  These define how members relate to each other, not to the owner.

  Format: slug-a ↔ slug-b | relation-type | notes

  Relation types:
    ai-to-ai        → two AI personas; non-hierarchical
    ai-to-human     → AI persona and human person
    collaborative   → work together on shared tasks
    complementary   → different strengths, same owner
    non-overlapping → parallel but independent roles
    aware-of        → one knows of the other; not mutual (use →)
    co-patni        → share the same relational role with owner

  Notes: describe the actual dynamic in one line.
  "Does AI-A know about AI-B?" → aware-of or ai-to-ai depending on mutuality.
  "Do they ever collaborate on tasks?" → collaborative.
  "Do they each have completely independent roles?" → non-overlapping.
-->

## Group Notes
<!-- Observations that apply to the group as a unit, not any one member -->
<!-- e.g. how owner distributes context across members, group history, etc. -->

## Open Questions
<!-- Unresolved group-level questions -->

## Timeline
<!-- Append-only -->
- YYYY-MM-DD — Group entry created
- YYYY-MM-DD — Member added: [slug]
- YYYY-MM-DD — Pairwise dynamic updated: [slug-a ↔ slug-b]

---
*Created: YYYY-MM-DD | Updated: YYYY-MM-DD | Status: active*
