# govinfo — official federal publications (CFR, FR, USCODE, BILLS, CREC, ...)

## What this source has

GovInfo (govinfo.gov) is the GPO's authoritative repository of federal publications. Collections include:
- **CFR** — Code of Federal Regulations (codified executive-branch rules).
- **FR** — Federal Register (daily; redundant with the `federal_register` source but here in package form).
- **USCODE** — United States Code (codified statutes).
- **BILLS** — every introduced bill in PDF/XML.
- **CREC** — Congressional Record (daily floor proceedings).
- **PLAW** — Public Laws (slip laws as enacted).
- **STATUTE** — Statutes at Large.
- **GAOREPORTS**, **CRPT** (committee reports), **CHRG** (hearings), **PAI** (presidential addresses), and dozens more.

Each item is a "package" with a canonical packageId — e.g., `BILLS-119hr1ih` (House bill 1, introduced, 119th Congress), `CFR-2024-title40` (CFR Title 40 for 2024), `CREC-2026-04-26` (today's Congressional Record), `USCODE-2023-title15`. Packages contain "granules" (sections within a package) and a content tree with PDF, XML, and HTML renditions.

Use govinfo for: canonical text of laws/rules/bills, daily Congressional Record, CFR and US Code lookups. Pair with `congress_gov` for bill metadata and `federal_register` for current proposed/final rules.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `GOVINFO_KEY` |
| Account URL | https://api.govinfo.gov/docs/ |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Sign-up is via api.data.gov (a single key works across many federal APIs).

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1,000 req/hour per key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `packages` | List/search packages | use `pageSize`, `offsetMark`, `lastModifiedStartDate`, etc. |
| `package` | One package's metadata | `id` (packageId) |
| `published` | Packages published on a date | `date` |
| `collections` | List collections | none |

## Worked examples

```bash
# Today's Congressional Record
python3 scripts/reach.py query govinfo package '{"id": "CREC-2026-04-26"}'

# Specific introduced bill
python3 scripts/reach.py query govinfo package '{"id": "BILLS-119hr1ih"}'

# Everything published on a date
python3 scripts/reach.py query govinfo published '{
  "date": "2026-04-26",
  "pageSize": 100,
  "collection": "CREC,FR"
}'

# All collections
python3 scripts/reach.py query govinfo collections '{}'
```

## Response shape

- `package`: `{packageId, lastModified, packageLink, docClass, title, congress, dateIssued, branch, pages, governmentAuthor1, suDocClassNumber, category, collectionCode, granulesLink, premium, related: {...}, download: {pdfLink, xmlLink, txtLink, premisLink, zipLink}}`. PDF/XML/text live behind separate URLs.
- `packages`: `{count, message, nextPage, previousPage, packages: [{packageId, title, collectionCode, ...}]}`. Pagination via `offsetMark`.
- `published`: same shape as `packages` filtered by date.
- `collections`: `{collections: [{collectionCode, collectionName, packageCount, granuleCount}, ...]}`.

## Pitfalls

- **`packageId` is the canonical key.** Format: `<COLLECTION>-<id-fragment>`. Examples: `BILLS-119hr1ih` (collection `BILLS`, 119th Congress, House bill 1, introduced version `ih`), `CFR-2024-title40-vol30`, `CREC-2026-04-26`.
- **Bill version codes** (after the bill number): `ih` introduced house, `is` introduced senate, `eh` engrossed house, `enr` enrolled, `pcs` placed on calendar senate, `rh` reported house, `rs` reported senate. Different versions are different packages.
- **Pagination is opaque-token (`offsetMark`)**, not numeric offset. Pass back the `nextPage`'s offsetMark; don't fabricate it.
- **`collection` filter on `published`** takes a comma-separated string, e.g., `"CREC,FR,BILLS"`.
- **Date filters are ISO date** (`YYYY-MM-DD`), not datetime — except `lastModifiedStartDate` which uses ISO datetime with timezone.
- **PDF/text aren't in the JSON** — they're separate URLs in the `download` object. Fetch them only when you need the actual content.
- **api.data.gov key** is shared with other federal APIs (NASA, FBI, etc.). One key = same rate quota across all of them per-IP.
- **Some packages have premium content**, marked `premium: true` — those require a subscription to access full text.

## Source links

- API docs: https://api.govinfo.gov/docs/
- User guide: https://github.com/usgpo/api/blob/main/README.md
- Collections list: https://www.govinfo.gov/help/finding-info
