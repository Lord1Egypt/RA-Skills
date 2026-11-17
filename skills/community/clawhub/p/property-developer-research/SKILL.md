---
name: property-developer-research
description: Research Indonesian property projects and developers using Webwright/browser evidence. Use when the user asks to investigate a property, housing cluster, developer legality, official website, Sikumbang, Sireng, or generate a buyer due-diligence report from a property/developer name.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "node", "npm", "npx"] },
        "install":
          [
            {
              "id": "playwright-npm",
              "kind": "exec",
              "command": "npm install -g playwright && npx playwright install chromium",
              "label": "Install Playwright + Chromium for browser evidence capture"
            },
            {
              "id": "python-reporting-deps",
              "kind": "exec",
              "command": "python3 -m pip install --user requests beautifulsoup4 lxml pillow reportlab weasyprint pypdf",
              "label": "Install Python scraping/reporting dependencies"
            }
          ]
      }
  }
---

# Property + Developer Research

Use this skill to investigate an Indonesian housing/property project and developer with screenshot-backed evidence. Default sources for now:

1. Official developer/project website
2. Google Maps coordinate for project/location pinpointing
3. SIKUMBANG (`https://sikumbang.tapera.go.id`)
4. SIRENG (`https://sireng.pkp.go.id`)
5. BNPB InaRISK flood raster (`https://gis.bnpb.go.id/server/rest/services/inarisk/layer_risiko_banjir/ImageServer`)

Use the Webwright workflow: create a task workspace, write `plan.md`, drive Playwright, save screenshots/logs under `final_runs/run_<id>/`, verify evidence, then summarize or generate PDF/ZIP if asked.

## Prerequisites and setup

Before starting, verify required tools are available:

```bash
python3 --version
node --version
npm --version
npx playwright --version
```

If Playwright or Chromium is missing, install it before browsing:

```bash
npm install -g playwright
npx playwright install chromium
```

For Python helpers/report generation, install missing packages as needed:

```bash
python3 -m pip install --user requests beautifulsoup4 lxml pillow reportlab weasyprint pypdf
```

Optional but useful for polished outputs: `zip`, `pandoc`, and `ffmpeg`. If unavailable, proceed with HTML/PDF generated from Python and clearly note any skipped artifact.

If the `webwright` skill is installed, follow it for browser automation and screenshot verification. If it is not installed, use direct Playwright scripts and preserve the same evidence/log folder structure described below.

## Inputs

Ask only if missing and not inferable:

- `property_name` — e.g. `Clarity House`
- `developer_name` — e.g. `Easton Urban Kapital` / `PT Easton Urban Kapital`
- optional: known location, official URL, Google Maps URL/place name, requested output (`summary`, `PDF`, `evidence ZIP`)

If user gives only one of property/developer, proceed with web search to infer candidates, but label inferred values clearly.

## Workspace convention

Use:

```text
outputs/property_research_<slug>/
├── plan.md
├── final_script.py
└── final_runs/run_<id>/
    ├── final_script.py
    ├── final_script_log.txt
    ├── screenshots/
    ├── data/
    ├── report.pdf          # default for Telegram/group-chat reports unless chat-only requested
    ├── flood_map.png       # if InaRISK checked
    └── evidence.zip        # if requested
```

`slug` should combine normalized property + developer when available.

## Critical points for `plan.md`

Always include these unless explicitly out of scope:

- [ ] CP1: Identify official project/developer website result and capture source screenshot.
- [ ] CP2: Extract official project facts: address/location, unit count, house types, facilities, price/pricelist statement if visible.
- [ ] CP3: Extract/pinpoint project coordinate from Google Maps and save the Maps URL/screenshot.
- [ ] CP4: Query InaRISK flood raster at/around the Google Maps coordinate and save raw samples/map image.
- [ ] CP5: Search SIKUMBANG by exact `Nama Perumahan`.
- [ ] CP6: If exact SIKUMBANG search fails, run parallel fallback queries and rank candidates by similarity.
- [ ] CP7: Search SIKUMBANG by `Nama Pengembang` for the developer.
- [ ] CP8: Search SIRENG for developer registration/status and capture registration rows/certificate links.
- [ ] CP9: State gaps/caveats clearly: missing project in SIKUMBANG, multiple SIRENG rows, no public price, exact coordinate NoData, etc.
- [ ] CP10: Save screenshots, raw text/API responses, and final log under `final_runs/run_<id>/`.

## Source workflow

### 1) Official website

Preferred path:

1. Search web for `"<property_name>" "<developer_name>" official` and exact property/developer terms.
2. Prefer developer-owned domains over portals/marketplaces.
3. Capture screenshots for:
   - top/title section
   - project facts/type section
   - price/pricelist/availability statement
   - official brochure/download link if available
4. If e-brochure is linked, open/download it when public. Capture relevant pages and OCR if needed.

Extraction targets:

- project name
- developer/legal entity shown
- address/location
- unit count
- house types and specs
- official prices, or exact statement if prices are not publicly published
- source URLs

Do **not** quote marketplace prices as official. If price is only on marketplace, label it as third-party listing data.

### 2) Google Maps coordinate + InaRISK flood risk

For location-based risk, prefer Google Maps place coordinates over broad listing coordinates or address geocoding.

Coordinate extraction priority:

1. User-provided Google Maps URL.
2. Official website embedded Maps/link.
3. Google Maps search result for exact project name + city/area.
4. SIKUMBANG/listing coordinate only as fallback; label it clearly.

Extraction rules:

- Parse coordinates from Maps URLs when available, especially `@<lat>,<lon>,<zoom>`, `!3d<lat>!4d<lon>`, `q=<lat>,<lon>`, or `ll=<lat>,<lon>`.
- If only a place page is available, open it with browser/Webwright, capture a screenshot, and save the canonical URL containing coordinates.
- Record `lat`, `lon`, coordinate source, Google Maps URL, place title, and confidence (`exact place`, `entrance/POI`, `address-level`, `fallback`).
- If a coordinate conflicts with official/SIKUMBANG address, preserve both and explain the mismatch.

InaRISK flood lookup:

- Endpoint: `https://gis.bnpb.go.id/server/rest/services/inarisk/layer_risiko_banjir/ImageServer`
- Query the exact Google Maps coordinate and surrounding samples/rings. Use a small local grid around the point, with summaries for ~100 m, 250 m, 500 m, and 1 km when practical.
- Treat pixel values as continuous flood-risk index `0–1`. Report classes: `Low < 0.333`, `Medium 0.333–0.666`, `High >= 0.666`.
- Exact coordinates may return `NoData`. If so, do not stop; use nearby valid samples and report exact pixel as `NoData` plus ring average/max and high-risk sample share.
- Save raw JSON responses/samples, query URLs/parameters, and a map image/legend screenshot when possible.
- Caveat every report: InaRISK is screening data, not parcel-level proof. Recommend field checks: resident flood history, drainage, elevation, river/canal proximity, and access-road flooding.

### 3) SIKUMBANG

Base endpoint often works for structured lookup:

```text
https://sikumbang.tapera.go.id/ajax/lokasi/search
```

Parameters:

```text
keyword=<query>
selectedSearch=data-lokasi
skalaPerumahan=semua
sort=terbaru
searchBy=nama-perumahan | nama-pengembang
page=1
limit=50
```

Required searches:

1. Exact property search: `searchBy=nama-perumahan`, `keyword=<property_name>`.
2. Developer search: `searchBy=nama-pengembang`, `keyword=<developer_name>` and common variants with/without `PT`.

If exact property search returns 0, run fallback fan-out in parallel:

- exact phrase
- lowercase normalized phrase
- no-space variant
- first two words
- adjacent bigrams
- meaningful tokens length >= 5
- location token if known
- developer/project aliases found from official website

Deduplicate by `idLokasi`. Rank candidates using phrase similarity + token overlap. Report:

- original query
- exact query result count
- fallback query that found top candidate
- similarity score
- `idLokasi`
- `namaPerumahan`
- developer name
- province/city/district/village if available
- commercial/subsidy unit counts
- house types and prices if present in SIKUMBANG

For detail/siteplan pages, capture screenshots when candidate is strong enough or when user asks for deeper extraction.

### 4) SIRENG

Use official site:

```text
https://sireng.pkp.go.id
```

Search exact developer name and variants:

- without `PT`
- with `PT`
- normalized company words

Capture:

- result table screenshot
- raw visible text
- API response if available
- certificate links (`/certificate/...`) when present

Extract:

- developer name
- registration number (`SRG-...`)
- association
- address
- status (`AKTIF`/other)
- certificate URL/PDF if public

If multiple rows exist, do not collapse them. List each row and explain that the buyer must confirm which legal entity/NPWP/signatory is used for the transaction.

## Report structure

Default to generating a PDF report for Telegram/group-chat property research unless the user explicitly asks for chat summary only. If time is tight, create a concise PDF from the verified findings and include references/evidence file paths; do not leave the result as chat-only.

For a PDF or final written report, use this order:

1. Executive verdict: Low / Moderate / High public-source risk
2. What was checked
3. Official website findings
4. Google Maps coordinate and InaRISK flood-risk findings
5. SIKUMBANG findings
6. SIRENG findings
7. Key gaps and buyer questions
8. Recommended documents to request before booking fee / DP
9. Evidence appendix with screenshots, source URLs, and raw evidence paths

Risk heuristics:

- Lower risk: official site exists, SIKUMBANG project match, SIRENG active developer, consistent names/locations.
- Moderate risk: official + SIRENG positive, but exact SIKUMBANG project missing or names mismatch.
- Higher risk: no official source, no SIKUMBANG match, no active SIRENG row, conflicting developer/legal names, or high InaRISK flood-risk surroundings without convincing mitigation evidence.

Always say this is public-source due diligence, not a substitute for AHU, OSS/NIB, NPWP, land certificate/BPN, PBG/SLF, PPJB/AJB review, or notary/PPAT verification.

## Evidence standards

- Every major claim needs a screenshot, URL, raw text/API response, or downloaded PDF.
- Save exact query URLs and result counts.
- When data conflicts, preserve both values and name the source for each.
- Before sending, verify generated PDFs with page count + text extraction and verify screenshots/maps are readable.
- For InaRISK findings, save both raw numeric samples and the visual map/screenshot used for interpretation.

## Telegram delivery preference

When delivering artifacts to Telegram, send:

1. concise summary message
2. PDF report if generated
3. evidence ZIP if generated

Keep the chat summary short; details belong in the PDF/evidence pack.
