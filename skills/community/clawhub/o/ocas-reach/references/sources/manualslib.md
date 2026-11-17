# manualslib — Product Manuals Search & Read

## What this has

ManualsLib.com hosts 3M+ product manuals across 140K+ brands — user manuals, service manuals, installation guides, operating instructions. Coverage spans consumer electronics, appliances, tools, medical equipment, industrial machinery, automotive, and more. Manuals are stored as page images (PNG/JPG) extracted from original PDFs. The site is a Vue.js SPA — all content is client-rendered and the site blocks datacenter IPs.

ManualZZ (manualzz.com) is a mirror with the same content, better image quality, and Cloudflare protection. Both sites require indirect access via Wayback Machine and OCR.

## Auth

| | |
|---|---|
| Required | none |
| Env var | — |
| Account URL | — |
| Plan tier | free |

No API key or account needed. All access is via public endpoints and Wayback Machine.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | No published cap; throttle to <5/sec for Wayback CDX |

## Endpoints

```bash
python3 scripts/reach.py query manualslib <action> '<params_json>'
```

| Action | Purpose | Params |
|---|---|---|
| `autocomplete` | Search suggestions from OpenSearch | `{"query": "canon camera"}` |
| `search` | Find manuals via web_search + Wayback CDX | `{"query": "canon f-730sx", "limit": 5}` |
| `read_page` | Download a specific page and OCR it | `{"manual_id": "1428710", "page": 5, "brand": "canon", "slug": "f730sx"}` |
| `read_random` | Read a random page from a random manual | `{"seed": "optional"}` |

## Worked examples

```bash
# Search for manuals matching a query
python3 scripts/reach.py query manualslib search '{"query": "gilson peristaltic pump"}'

# Read page 3 of a specific manual
python3 scripts/reach.py query manualslib read_page '{"manual_id": "1916287", "page": 3}'

# Read a random page from a random manual
python3 scripts/reach.py query manualslib read_random '{}'
```

## Response shape

```json
{
  "source": "manualslib",
  "action": "read_page",
  "manual": {
    "id": "1428710",
    "title": "Canon F-730SX User Manual",
    "brand": "Canon",
    "category": "Calculator",
    "pages_total": 29,
    "url": "https://www.manualslib.com/manual/1428710/Canon-F-730sx.html"
  },
  "page": 5,
  "image_url": "https://static-data2.manualslib.com/pdf7/143/14288/1428710-canon/images/f730sx_5_bg.png",
  "ocr_text": "... extracted text ...",
  "ocr_quality": "low|medium|high",
  "wayback_snapshot": "20210419070129"
}
```

## Pipeline Details

### Discovery (OpenSearch Autocomplete)

```
GET https://www.manualslib.com/openSearch/action/autocomplete?term={query}&open=1
→ JSON array of {label, value, dalue} suggestions
```

### Page Image URL Pattern

```
https://static-data2.manualslib.com/storage/pdf{G}/{g1}/{g2}/{ID}/images/{name}_{page}_bg.{ext}
```

Where:
- `G` = storage generation (7, 10, 51, etc.)
- `g1`, `g2` = grouping digits derived from ID
- `ID` = manual ID from URL
- `name` = slug from manual URL
- `ext` = png or jpg (jpg has better OCR quality)

### Wayback Machine Enumeration

```
GET https://web.archive.org/cdx/search/cdx?url=static-data2.manualslib.com/storage/pdf{G}/{g1}/{g2}/{ID}/*&output=text&fl=original
→ list of available page image URLs
```

### OCR Pipeline

1. Download image via `curl` with browser User-Agent
2. Convert to RGB, upscale 2.5x with LANCZOS, sharpen 1.8x
3. Run `tesseract` with `--psm 6` (uniform block of text)
4. Return extracted text

### ManualZZ Alternative

```
GET https://web.archive.org/web/{YEAR}/https://manualzz.com/doc/{ID}/{slug}
→ extract https://s1.manualzz.com/store/data/{ID}_{N}-{hash}.png URLs
→ download and OCR (better quality, higher resolution)
```

## Pitfalls

- **Direct access blocked:** ManualsLib returns 403 for all datacenter IPs. Both `curl` and `browser_navigate` fail. Use Wayback Machine + direct image URLs.
- **Browser navigation fails:** `browser_navigate` returns `net::ERR_HTTP2_PROTOCOL_ERROR`. Do not attempt.
- **OCR quality varies:** ManualsLib images are 950px wide palette PNGs — OCR is poor. ManualZZ images are full-color and OCR much better. Prefer ManualZZ when available.
- **CDX timeouts:** Broad queries (`*/*`) time out. Keep queries specific to known ID ranges.
- **Image availability:** Not all pages are archived. Check multiple Wayback snapshots.
- **URL pattern varies:** Different manuals use different storage generations (pdf7, pdf10, pdf51). The custom module probes multiple patterns.
- **Cloudflare on ManualZZ:** Direct access blocked. Must use Wayback Machine.
- **No PDF download:** PDF downloads require login + captcha. Only page images are accessible.
- **Slug encoding:** Manual names replace spaces with hyphens, lowercase, special chars stripped.