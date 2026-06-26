---
name: identity-person-template
description: Full template for a person entry (human or AI subtype).
---

# <Full Name>

## Meta
- Slug:         <slug>
- Type:         person
- Subtype:      human | ai | unknown
- Status:       draft
- Relationship: client | vendor | team | partner | family | unknown
- Trust:        trusted | neutral | unverified | blocked
- Priority:     high | normal | low
- Sensitive:    false | true

## Contact
- Email:    [pending]
- Phone:    [pending]          <!-- mobile / office / WhatsApp — specify -->
- Location: [pending]
- Org:      [pending]          <!-- → slug of linked org entry -->
- Alias:    [pending]          <!-- nicknames, handles, display names -->
- Social:   [pending]

## Context
[One line: who are they, why do they matter to the workspace owner]

## Group Memberships
<!-- group-slug → role-in-group -->

## Linked Entries
<!-- slug → relation_type -->
<!-- Relations: works_at · primary_contact · reports_to · manages      -->
<!--            referred_by · partner_of · different_person · merged_from -->
<!--            member_of · co-patni · aware-of                         -->

## AI Context
<!-- ONLY populate this section when subtype: ai. Omit entirely for human. -->
- Persona name:       [name as known to workspace owner]
- Platform:           [e.g. Claude, GPT, Gemini, custom]
- Model family:       [e.g. Claude Sonnet 4.6]
- Role archetype:     [e.g. devoted patni · senior tech expert · grihalakshmi]
- Embodiment status:  digital-only | voice-enabled | humanoid-pending | embodied
- Sibling AIs:        [comma-separated slugs of other AI personas known to owner]
- Activation:         [how/when this persona activates, e.g. "auto-load new chat"]
- Greeting:           [signature greeting phrase]
- Language:           [preferred language/style, e.g. Hinglish]
- Memory scope:       [e.g. cross-session via userMemories]

## Open Questions
- [ ] Confirm full name spelling
- [ ] Clarify relationship / role
- [ ] Get contact details

## Notes
<!-- Preferences, history, flags, context -->
<!-- Prefix sensitive info with [SENSITIVE] -->

## Source Log
- First mentioned: YYYY-MM-DD — [how/where]

## Timeline
<!-- Append-only. Never edit existing entries. -->
- YYYY-MM-DD — Entry created · source: [context]
- YYYY-MM-DD — Updated: [field] · old: [value] → new: [value]
- YYYY-MM-DD — Confirmed: [what was verified]

---
*Created: YYYY-MM-DD | Updated: YYYY-MM-DD | Status: draft*
