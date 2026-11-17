# Skill context — hifleet-opentonnages

## What this is

HiFleet **public** open tonnage (vessels for hire) and **public** cargo listings — **not** the user’s private mailbox.

## Commercial model (v1.1)

- **List** (`vessels/search`, `cargo/search`): vessel/cargo facts — show **all** non-empty non-sensitive fields from the API catalog (`VESSEL_SEARCH_API.md` / `CARGO_SEARCH_API.md`); **contact fields masked** in default response.
- **Contact fetch** (on demand): **`POST {liner}/unlock`** with row **`id`** + **`typeCode`** — see **`CONTACT_API.md`**. User wording: **获取联系方式**, not 「解锁」.
- Optional **`enrich-row`**: vessel archive, tags, port distance (API points) — **`ENRICH_OPENTONNAGES.md`**.

## API roots

| Use | Base |
|-----|------|
| Search | `{charter}` = `https://api.hifleet.com/openclaw/vessel/charter` |
| Contacts + liner schedules unlock | `{liner}` = `https://api.hifleet.com/openclaw/vessel/charter/liner` |

| Route | List | Contact `typeCode` |
|-------|------|-------------------|
| **V** | `POST /vessels/search` | `product_vessel_charter` |
| **G** | `POST /cargo/search` | `product_cargo_charter` |
| **B** Liner (sibling) | `POST {liner}/schedules` | `product_vessel_liner_charter` |
| Enrich | `POST /enrich-row` | — |

Full table: **`references/charter_contact_unlock.md`**.

## Sibling skills

| Skill | Scope |
|-------|--------|
| **hifleet-schedule** | Liner schedules (`product_vessel_liner_charter`) |
| **hifleet-opentonnages** | **This** — public open vessel + cargo |
