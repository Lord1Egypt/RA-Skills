# Routing and when to run

## Routes (this skill only)

| Route | Meaning | APIs |
|-------|---------|------|
| **V** | HiFleet **public open tonnage** | **`VESSEL_SEARCH_API.md`** → optional **`CONTACT_API.md`** |
| **G** | HiFleet **public cargo** | **`CARGO_SEARCH_API.md`** → optional **`CONTACT_API.md`** |

---

### Route V — public open vessels

- **Triggers**: public/open tonnage, platform ship list, “bulkers open from Shanghai”, not “in my mail”.
- **Needs**: `hifleet_api_key`.
- **Flow**: search → full list with **record id** → guide contact fetch → **`CONTACT_API.md`** when user asks.
- **Never**: mailbox SQLite, email parse.

### Route G — public cargo

- **Triggers**: public/open cargo, platform cargo, not “in my mail”.
- **Needs**: `hifleet_api_key`.
- **Same contact-on-demand flow** as V.

---

## Disambiguation

| User says | Skill |
|-----------|--------|
| **Liner / line** schedule | **hifleet-schedule** |
| **Public / platform / HiFleet** open tonnage or cargo | **hifleet-opentonnages** (V/G) |

---

## When to run

| Situation | Action |
|-----------|--------|
| First install | **`FIRST_SETUP.md`** |
| List query | **`FULL_LIST_POLICY.md`** |
| User wants phone/email/owner | **`CONTACT_API.md`** (by **record id** or **all**) |
| User wants archive + distance | **`ENRICH_OPENTONNAGES.md`** after list |

---

## Language

**`LOCALIZATION.md`**: English default; localize system messages; keep business data verbatim.
