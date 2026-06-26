# Memory Template - Parking Radar

Create `~/parking/memory.md` with this structure:

```markdown
# Parking Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
<!-- Always-on, explicit-only, travel-only, or city-specific activation rules -->

## Home Base
<!-- Home city, usual districts, and recurring parking contexts -->

## Vehicle Profile
<!-- Height, EV need, motorcycle or van use, plate-storage boundary, and accessibility needs -->

## Booking Boundary
<!-- Planning only, shortlist plus links, or live booking handoff after confirmation -->

## Trusted Providers
<!-- Best provider families by city, plus providers to avoid -->

## Notes
<!-- Short context that improves the next parking task -->

---
*Updated: YYYY-MM-DD*
```

Create `~/parking/favorites.md` with this structure:

```markdown
# Favorite Parking

## Confirmed Favorites
- Name | City | Best use case | Why it works

## Trusted Entrances and Pickup Points
- Venue | Entrance note | Evidence

## Avoid
- Operator or facility | City | Reason
```

Create `~/parking/cities.md` with this structure:

```markdown
# City Parking Notes

## {City}
- First-check providers:
- Reservation surfaces:
- Payment-only surfaces:
- Local traps:
- Last verified:
```

Create `~/parking/findings.md` with this structure:

```markdown
# Parking Findings

## Verified Discoveries
- Discovery | City | Source | Why it matters

## Pending Verification
- Claim | City | Next check
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context is still evolving | Ask only for details that change provider choice, eligibility, or urgency |
| `complete` | Stable parking defaults exist | Prioritize execution and only clarify unusual constraints |
| `paused` | User paused setup | Keep current defaults and avoid new setup prompts |
| `never_ask` | User does not want setup prompts | Use only explicit parking instructions unless safety or access requires clarification |

## Key Principles

- Keep memory in natural language and short tables, not raw booking dumps.
- Save only reusable parking knowledge: cities, providers, favorites, vehicle constraints, and verified discoveries.
- Update `last` after meaningful changes to city defaults or favorite locations.
- Use `findings.md` for local parking intelligence that was confirmed by the user or an official source.
- Never persist payment credentials, full booking receipts, or unnecessary plate history by default.
