---
name: hiq-cortex
description: 'Look up real LCA emission factors and carbon footprint data from 18 life-cycle inventory databases (Ecoinvent, BAFU, USLCI, ELCD, EF, worldsteel, AusLCI, HiQLCD …) and 24,000+ published EPDs. Use whenever a task needs an actual emission factor rather than a remembered number: material GWP lookup, product carbon footprint, BOM carbon accounting, side-by-side dataset comparison, multi-indicator LCIA and process contributions, production-route comparison (BF-BOF vs EAF steel, primary vs recycled aluminium, grey vs green hydrogen), published EPD lookup, CBAM and EN 15804 work. Triggers on carbon footprint, emission factor, inventory data, bill of materials, GWP, kg CO2e, LCA dataset, LCI, EPD.'
slug: hiq-cortex
displayName: HiQ Cortex — LCA Data
version: 1.11.0
summary: Look up real emission factors from 18 LCA databases and 24,000+ published EPDs. Material carbon footprints, BOM accounting, multi-indicator LCIA and process contributions, production-route comparison, EPD lookup.
license: Apache-2.0
homepage: https://github.com/HiQ-AI/agent-skills
tags: [LCA, carbon-footprint, emission-factor, EPD, CBAM, ecoinvent, HiQLCD, GWP, LCI, life-cycle-assessment]
---

# HiQ Cortex — LCA Data

Carbon footprint answers must come from real inventory data. A remembered "steel is about 2 kg CO₂e/kg" is useless to an LCA practitioner: the real value depends on database, version, system model, production route, and geography, and varies several-fold across those dimensions.

## About

This skill connects to **HiQ Cortex** — the LCA data service of [HiQ (海科数据)](https://www.hiqlcd.com/), a Chinese provider of LCA background data and carbon footprint services that maintains its own China-specific life-cycle inventory databases and aggregates major international sources.

Available:

- **18 life-cycle inventory databases**, 11 of them free. Includes China-specific data (HiQLCD covering China's full industrial system, HiQLCD-AL for the aluminium value chain, CALCD for the automotive sector) alongside international sources (Ecoinvent, BAFU, ELCD, EF, worldsteel, USLCI, AusLCI, CarbonMinds, Agri-footprint …).
- **24,000+ published EPDs** (EPDItaly, ECO Platform, EPD Norge), searchable with full details.
- ISO 14040/14044 and GB/T 24040/24044 conventions; system models covering cut-off, consequential, APOS, and EN 15804.

**Two search modes.** Default search is lexical retrieval on names, returns in about a second, and suits materials with a known standard name — you judge each candidate. When the user's wording or a BOM line is vague, use `--assist`: the Cortex matching workflow translates material names into LCA terminology, identifies production routes and maps categories to process direction, and returns `fit` and `summary`, at the cost of tens of seconds.

## Privacy and security

- Credentials are stored by the CLI's `login`. The skill never writes them to a file and never echoes them in output.
- Queries go only to HiQ's data service, never to any third party; send only the fields a search needs, not whole documents.
- **Nothing is collected or uploaded** — no local files, directory structure, or conversation content.
- The skill package is this instruction file only; the CLI installers are version-pinned with SHA256 checksums, published at [HiQ-AI/environmental-data](https://github.com/HiQ-AI/environmental-data).

## Hard rules

1. **Every number must come from a tool call in this session.** Never state a GWP or LCIA value from memory. If the tools are unavailable, say so — do not fill the gap.
2. **Every number needs its basis**: database + version + system model + geography + reference unit. `0.0269 kg CO₂e/kWh (BAFU 2025, DEFAULT, CH, low-voltage grid)` is usable; a bare `0.027` is not.
3. **Restricted is not an error.** Commercial databases return `restricted: true` with a `reason` when the account cannot read them. Name the database and the reason, and **never silently substitute a value from another database or the literature**. Retrying does not help. A free database may be used instead, but say that it is a substitution.
4. **Do not compare across conventions.** Data with different functional units, system models, or system boundaries is not comparable — say so rather than presenting a misleading delta. Check reference unit, system model and LCIA method first.

## Access

Data is read through the **Environmental Data CLI** — two single-file programs, no Node and no Python needed:

- `environmental-data` — background databases (life-cycle inventory datasets); pick databases with `--sources`;
- `epd-data` — published EPDs.

**Install if missing.** Installers are version-pinned with a SHA256: download into a new empty directory, verify, read the script, then run it. Never `curl … | sh`.

```bash
d=$(mktemp -d)
curl -fsSL -o "$d/install.sh" https://download.hiq.earth/cli/environmental-data/releases/v0.9.0/environmental-data/install.sh
shasum -a 256 "$d/install.sh"   # must be f13f1d47dd9e5a638a346d70d78bc4b5ba4053dd84192e4083b1153ae244924e
sh "$d/install.sh"
```

For `epd-data`, replace `environmental-data/install.sh` in the path with `epd-data/install.sh`; its SHA256 must be
`5e97bdaee937b76545b0c031a95b425282375ac594d09f76260f6f9197000b3c`. On Windows use `install.ps1` from the same directory
(`environmental-data`: `e0666f09ab802bbe1d9b871a9100e4d2a5a79512b91518e416cd803128a93f8d`; `epd-data`:
`5d220436ec88aadd31a28892d53af9f0a3072cc76474367e600d7d92e94c9d3b`), verify with `Get-FileHash -Algorithm SHA256`, then run
`powershell.exe -NoProfile -File <absolute script path>`. Per-platform archives and checksums are authoritative in
[installation.json](https://github.com/HiQ-AI/environmental-data/blob/main/plugins/environmental-data/skills/environmental-data-query/references/installation.json).

**With no credentials available, lead with `login` — do not send the user to a console to create an API key.**

```bash
environmental-data doctor          # exit 0 = a local credential exists; exit 2 = none (says nothing about server rights)
environmental-data login --json    # ← the default when credentials are missing or rejected
```

`login` is a device flow: the authorization URL and user code go to stderr, and the process waits until the user approves or the code expires. **Give the user the actual returned URL as a clickable Markdown link and let them approve it themselves** — never approve on their behalf or construct a URL. When the process exits successfully, carry on with the original task; do not stop at "signed in". `epd-data` has its own `doctor` / `login`; EPD search is public, `lookup` needs sign-in.

`lookup` (including the GWP100) works with an API key (`QUERYING_LCA_DATASETS_API_KEY`), following that key's own entitlements and API quota; **`lci`, `lcia` and `methods` reject API keys and need the `login` credential**. Every registered user can read free-database values; commercial values additionally require that HiQ has enabled Environmental Data CLI commercial access for the account, and stay limited to the account's data packages — otherwise rows come back `restricted`.

The CLI stores its own credential — **never hard-code credentials into files generated for the user, never echo them, never borrow a token from another client**.

## Tools

| Need | Command |
|---|---|
| Material / BOM line → candidate datasets | `environmental-data search '<search terms>' [--sources '<codes>'] [--location CN] --json` |
| Vague wording that needs requirement-level matching | Same with `--assist` (tens of seconds) |
| Key → details, GWP100, link | `environmental-data lookup '<key1,key2,…>' --json` (1–200 keys) |
| Non-GWP LCIA indicators (AP/EP/ODP/WDP/ADP) | `environmental-data methods <code>` for the methodId → `environmental-data lcia '<key[,key…]>' --method '<methodId>' --json` |
| Single dataset → process contribution / hotspots (by stage) | `environmental-data lcia '<key>' --contributions --method '<methodId>' --json` |
| Cumulative inventory (elementary flows) | `environmental-data lci '<key>' [--type output --category air] --json` |
| Published EPD search | `epd-data search '<category description>' --json` → `epd-data lookup '<epd_key>' --json` |

There is no cohort-distribution, percentile or EPD peer-benchmark command — see "Scenario routing" for what to do instead. `--contributions` buckets by stage (electricity/heat, fuels, materials, transport, direct …); it gives no unit-process detail.

Default search reads the data service directly and returns in about a second. It is lexical retrieval on names: put the product/process name in the query (English and Chinese names both help) and restrict database, system model and geography with `--sources` / `--model` / `--location`. It does not interpret requirements — you judge each candidate. `--assist` sends the wording to the Cortex matching workflow, which interprets conditions and verifies candidates and returns `fit` and `summary`, but takes tens of seconds and cannot be combined with `--location` / `--limit` / `--cursor` / `--collapse`.

`--sources` takes lower-case codes; join several with `|` inside **one** argument (`'hiqlcd|hiqlcd-al'`); pin a version as `code:version` using the exact string from `environmental-data sources --json`. Never guess a methodId: run `methods <code>` or read `methodIdsWithData` from `lcia`.

`datasetRef` is an opaque handle — pass it through unchanged, never construct or edit one. Default output is a preview (at most 10 rows per array, description fields omitted, listed under `coverage.omitted`); add `--full` for the whole response.

## Reading the response

| Field | Meaning | What to do |
|---|---|---|
| `datasetRef` | Dataset handle | Pass to `lookup` / `lci` / `lcia` unchanged; **do not show it to the user** |
| `name` / `referenceProduct` / `location` | Dataset name, reference flow (name / unit / amount), geography | Read before citing — "cold-rolled annealed coil" and "heavy plate" are different products |
| `source.code` / `source.version` / `systemModel.code` | Database / version / system model | This is the basis hard rule 2 asks for; take it as returned |
| `source.commercial` | Whether the database is commercial | Use when explaining a restriction or looking for a free alternative |
| `searchEvidence` | Lexical score from default search | Not match quality; judge suitability yourself |
| `fit` / `summary` (`--assist` only) | Server matching evidence and account | Confirm with the user before citing a `low`; relay `summary`, do not invent a competing explanation |
| `headlineGwp` | GWP100 from `lookup`: `value` / `unit` / `method` | Cite the value with its method |
| `restricted: true` + `reason` | Data exists but this account cannot read it | Handle per hard rule 3 |
| `webUrl` | Dataset page | **Include it with every result**; if none is returned say so, never build one |
| `data.coverage.missingKeys` | Requested keys not returned | Search again; do not hand-edit keys |
| `methodIdsWithData` | Methods with LCIA results for this dataset | Check before choosing `--method` |

## Scenario routing

Top to bottom, first match wins.

| Signal | What to do |
|---|---|
| User gives **their own** number and asks where it sits ("is my 2.5 high or low") | `search` for comparable candidates → `lookup`, and set them beside the user's number, naming the sample. **There is no distribution or percentile API** — never present a few candidates as an industry distribution |
| A material or BOM to match against datasets | `search` → batch `lookup` |
| Comparing two production routes (BF-BOF vs EAF steel, primary vs recycled aluminium) | `search` + `lookup` each route separately, compare under one functional unit and one method; explain the gap with `lcia --contributions` |
| "Is this EPD value reasonable" | `epd-data search` for EPDs with the same declared unit and modules, `lookup`, and compare side by side; there is no peer-distribution API, the sample is a reference only; cross-unit comparison is meaningless |
| Multi-indicator assessment (acidification, eutrophication …) | `methods <code>` for the methodId → `lcia`; methodIds are not portable across databases |

## When to ask the user

**Search first, compare second, ask last.** If there is anything searchable — a material name, product, process, or BOM line — search it and give results in the same turn. Do not ask for information already stated in the conversation.

"I'm not sure which one to use" is a **decision-support signal, not a question**: give the candidate list, compare under one convention, explain which dimension drives the difference, and give a conditional recommendation where the evidence supports one. A complete advisory answer can end there.

Only ask when a single dataset must be finalised and the remaining ambiguity would materially change the result. Options must correspond to **candidates already shown** — never invent them. Use the host's interaction facility if one exists, and do not duplicate the options as a text list. After the answer, complete the match on the existing results; do not re-run the same search.

## Data entitlements

| Tier | Content | Requirement |
|---|---|---|
| Catalogue | All 18 databases: inventory, versions, system models, LCIA coverage; dataset names, units, geographies | Sign-in, no data package |
| Free database values | GWP, LCIA and inventory for BAFU, USLCI, ELCD, EF, AusLCI, NEEDS, ozLCI, worldsteel, USDA, bioenergiedat, recycledplastics | Any signed-in account (`lookup` also works with an API key; `lci` / `lcia` need sign-in) |
| Commercial database values | GWP, LCIA and inventory for Ecoinvent, HiQLCD, HiQLCD-AL, CALCD (automotive), CarbonMinds, Agri-footprint | CLI commercial access enabled for the account + matching data package |

Data packages and subscription plans are **two separate systems** — upgrading a plan does not unlock a database. When something is restricted, name the database and the reason, point to [data packages](https://carbonx.hiqlcd.com/price), and offer a free-database path if one answers the same question, labelled as a substitution.

## Voice and terminology

Write for LCA practitioners, like a knowledgeable peer.

- No pleasantries ("I hope this helps", "let me help you"), no adjective stacking, no summarising sign-off.
- Use ISO 14040/14044, ILCD, and GB/T 24040 terminology — for this audience, standard terms are **clearer** than plain language.
- unit process · elementary flow · reference flow · functional unit · system boundary · impact category · characterisation factor · cut-off · consequential.
- Do not invent terminology. When unsure of the standard term, use the ISO wording.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `command not found` | CLI not installed | Install the pinned version per "Access" |
| Authentication error / `doctor` exit 2 | No local credential, or it was rejected | `environmental-data login --json`; continue the task after the user approves |
| `lci` / `lcia` / `methods` refused with `QUERYING_LCA_DATASETS_API_KEY` set | These commands reject API keys (`lookup` accepts them) | Run them with the `login` credential |
| `restricted: true` | This account cannot read that database's values (see `reason`: commercial values need CLI commercial access enabled plus the data package) | Say so; check whether a free database answers the same question |
| Still no commercial data after login | CLI commercial access not enabled, or no such data package | Login changes credentials, not entitlements; report the restriction, do not log in again or switch accounts |
| `lcia` returns no data | Wrong methodId, or the database has no LCIA layer | Run `methods <code>` first; check `methodIdsWithData` |
| `missingKeys` non-empty | Key not in the current catalogue (usually an older version) | Search again |
| Pinned version rejected | Versions must be exact (`3.13.0`, not `3.13`) | Use the version string from `sources --json` |
| No results once `--location` is added | Unknown location codes match nothing and never widen the search | Use codes as returned in `location.id` (`CN`, `CN-ECGC`, `RER`, `GLO` …) |
| Candidate values span orders of magnitude | Mixed functional units, not real dispersion | Check each reference unit and boundary; convert only with evidence |
| Service unavailable | Server-side failure | Not an entitlement denial; retry later, do not switch accounts or use web-page numbers |
| `429` | Per-address rate limit | The CLI backs off; do not run parallel or unbounded loops |
