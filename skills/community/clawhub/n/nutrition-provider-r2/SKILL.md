---
name: nutrition-provider-r2
description: crawl the Vietnam nutrition provider page-by-page with scrapling-official and upload each raw provider record to Cloudflare R2 after fetch. use for provider-specific ingestion where the canonical data comes from the provider's foods or prepared-dish JSON APIs, records from one page may upload in parallel with stable object keys, and each page must still respect a minimum 60 second crawl-plus-upload window before the next page begins.
license: MIT-0
metadata: { "openclaw": { "emoji": "🥗", "homepage": "https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-thuc-pham", "requires": { "bins": ["uv"] }, "install": [{ "id": "uv-brew", "kind": "brew", "formula": "uv", "bins": ["uv"], "label": "Install uv (brew)" }] } }
---

# Nutrition Provider R2

This skill is a provider-specific orchestration wrapper around `scrapling-official`.

Its job is to take the payload that `scrapling-official` fetched, split each canonical page into individual provider records, and upload those records to Cloudflare R2.

It does not replace `scrapling-official` as the crawler.

Use it when the target is one of the Vietnam nutritional portal lookup listings and the job is:

- crawl page-by-page
- preserve each provider record in raw form
- upload the records from each page to Cloudflare R2 immediately after that page is fetched

Do not normalize provider records into a custom nutrition schema. Preserve provider fields, response bodies, pagination clues, and raw linked payloads exactly as obtained whenever possible.

## Required skill

This skill depends on `scrapling-official` for crawling.

- If `scrapling-official` is not installed or not set up yet, stop and tell the user to install and configure that skill first.
- Let `scrapling-official` own crawl execution, endpoint discovery, rendering mode, and fetch escalation.
- Follow `scrapling-official`'s fetch escalation strategy exactly: start with `get`, then move to `fetch` if needed, then `stealthy-fetch` only when the earlier modes fail or protection requires it.
- Do not fall back to a different crawler or browser stack when `scrapling-official` is missing.

## Workflow

1. Read `{baseDir}/references/source-notes.md` for the default source URL, pagination clues, and stop conditions.
2. Confirm the R2 credentials are present:
   - `R2_ACCOUNT_ID`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
   - `R2_BUCKET`
3. Ask `scrapling-official` to inspect the provider page and determine which payload actually contains the canonical records for the current request.
4. For this provider, prefer the canonical JSON payload when `scrapling-official` discovers it, instead of the outer HTML shell.
5. Current observed provider behavior:
   - food lookup page `gia-tri-dinh-duong-thuc-pham` exposes records from `GET /api/fe/foodNatunal/getPageFoodData`
   - prepared-dish lookup page `gia-tri-dinh-duong-mon-an` exposes records from `GET /api/fe/tool/getPageFoodData`
   - default params observed on page load:
     - foods: `page=1&pageSize=15&energy=0`
     - prepared dishes: `page=1&pageSize=15`
   - observed filter params:
     - foods: `name`, `category`, `energy`
     - prepared dishes: at least `name`, `energy`, with additional filters visible in the UI such as group and region; let `scrapling-official` discover the exact live request params
6. Treat the start of each page fetch as the start time for that page's pacing window.
7. Save the raw payload that `scrapling-official` fetched for that page without normalizing item fields.
8. If `scrapling-official` can fetch the canonical JSON payload, treat `raw.data` as the list of provider records for that page.
9. Split that page payload into one record object per item in `data`.
10. Upload each record object as its own R2 object.
11. Record uploads from the same page may run in parallel, but every record object must use a stable object key so reruns do not create duplicates.
12. Prefer a provider-stable identifier for the key:
   - `_id` first
   - then `code`
   - only use another deterministic identifier if neither exists
13. Prefer letting the helper split and upload records directly from the page payload:
   - `uv run {baseDir}/scripts/upload_page_to_r2.py --extract-foods --page-index <n> --skip-existing`
14. The helper flag name `--extract-foods` is retained for compatibility, but it may also be used for prepared-dish page payloads because both current source types return `data` arrays.
15. If the agent already split records outside the helper, it may still upload one item at a time with `--food-id`.
16. Only capture the outer HTML page as a fallback debugging artifact when `scrapling-official` cannot reach the canonical payload directly. Do not upload the HTML shell as the primary dataset.
17. Wait for all record uploads from the current page to finish.
18. Measure total time for the page as:
   - page fetch start
   - plus record extraction
   - plus all record uploads
19. If the total time for the current page is less than 60 seconds, wait the remaining time before starting the next page.
20. Let `scrapling-official` handle the actual pagination requests.
21. Use the provider payload itself to decide when to stop:
   - keep paginating while the canonical payload remains non-empty
   - stop when the provider indicates no more rows
   - stop if a next request repeats data already seen
22. Never start the next page before the current page has both:
   - finished all uploads
   - satisfied the 60 second minimum page window

## Operating Rules

- Preserve provider data as-is. Do not rewrite field names, flatten structures, or infer a nutrition schema.
- Allow lightweight wrapper metadata only outside the raw payload, such as `source_url`, `fetched_at`, `page_index`, `content_type`, and `storage_key`.
- Upload one object per provider record, not one object for the whole page payload.
- Stop naturally when pagination ends. Do not invent more pages.
- `scrapling-official` is responsible for extracting or fetching the correct provider payload.
- Prefer the provider JSON API response over rendered HTML whenever `scrapling-official` can access both.
- Do not store the page shell HTML as the primary page payload when the JSON payload already contains the canonical rows and nutrition arrays.
- Record uploads from the same page may be concurrent.
- Use stable R2 object keys so duplicate runs overwrite or skip the same object instead of creating duplicates.
- Finish all record uploads for the current page before page `N+1` begins.
- Enforce a minimum 60 second crawl-plus-upload window per page to avoid overloading the provider.
- If `scrapling-official` fetches JSON from an XHR endpoint, store that JSON body unchanged.
- If HTML is captured for debugging, store it separately from the canonical payload and do not treat it as the canonical dataset.
- If a page fails, retry briefly. If it still fails, upload a failure record only when the caller explicitly wants failure capture.

## Concurrency

Use page-sequential crawling with record-level upload concurrency.

- Exactly one page in flight at a time.
- Records from the same page may upload in parallel.
- Do not start page `N+1` until page `N` has finished all uploads.
- Enforce a minimum total duration of 60 seconds for each page, measured from the start of fetch to the completion of all uploads and any required remaining wait.

## R2 Settings

Required environment variables:

- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`

Optional environment variables used by the helper when `--key` is not passed:

- `R2_PREFIX` default `raw`
- `SOURCE_NAME` default `nutrition-provider`
- `RUN_ID` default current UTC timestamp in `YYYY-MM-DDTHH-MM-SSZ`

When supporting both provider sources, do not reuse the same storage namespace for both in the same crawl run.

- prefer `SOURCE_NAME=viendinhduong-foods` for `gia-tri-dinh-duong-thuc-pham`
- prefer `SOURCE_NAME=viendinhduong-dishes` for `gia-tri-dinh-duong-mon-an`
- or pass `--source-name` explicitly per crawl job

## Recommended Output Shape

Wrap the provider payload with minimal crawl metadata only when needed for storage traceability:

```json
{
  "source_url": "https://viendinhduong.vn/api/fe/foodNatunal/getPageFoodData?page=1&pageSize=15&energy=0",
  "page_index": 1,
  "fetched_at": "2026-03-15T10:00:00Z",
  "content_type": "application/json",
  "raw": {
    "data": [],
    "current_page": 1,
    "per_page": 15,
    "total": 853
  }
}
```

The foods endpoint currently returns page-level JSON with top-level keys `data`, `current_page`, `per_page`, and `total`. Each food item currently includes `_id`, `code`, `name_vi`, `name_en`, `category`, `categoryEn`, `nutrition`, and `energy`.

The prepared-dish endpoint currently returns page-level JSON with top-level keys `current_page`, `data`, `first_page_url`, `from`, `last_page`, `last_page_url`, `links`, `next_page_url`, `path`, `per_page`, `prev_page_url`, `to`, and `total`. Each dish item currently includes `_id`, `category_id`, `code`, `description`, `dish_components`, `food_area_id`, `image`, `name_vi`, `name_en`, `nutritional_components`, `total_energy`, `category_name`, `category_name_en`, and `category_description`.

Use those richer raw objects only as the source page payloads to split into per-record uploads.

Recommended per-record upload shape:

```json
{
  "source_url": "https://viendinhduong.vn/api/fe/foodNatunal/getPageFoodData?page=1&pageSize=15&energy=0",
  "page_index": 1,
  "fetched_at": "2026-03-15T10:00:00Z",
  "content_type": "application/json",
  "raw": {
    "_id": "6877a6b660d6c84e9bd5cca4",
    "code": "10001",
    "name_vi": "Sữa bò tươi",
    "name_en": "Milk cow, fresh (Fluid)",
    "category": "Sữa và sản phẩm chế biến",
    "categoryEn": "Milk and processed products",
    "nutrition": [],
    "energy": 74
  }
}
```

## Upload Helper

Use `uv run {baseDir}/scripts/upload_page_to_r2.py`.

The helper supports two modes:

- explicit key mode with `--key`
- generated key mode from `R2_PREFIX`, `SOURCE_NAME`, `RUN_ID`, `--page-index`, and optional `--food-id`

Generated keys follow this layout:

- record payload success: `raw/<source>/<run_id>/page-0001/food-6877a6b660d6c84e9bd5cca4.json`
- debug or failure artifact: `raw/<source>/<run_id>/failures/page-0001.json`

For this skill, per-record upload is the default and expected mode.

- prefer `--extract-foods` when the input is a full canonical page JSON payload from either supported source
- pass a stable `--food-id` only when uploading a single already-split record object
- prefer `--skip-existing` when reruns are possible
- do not upload a whole canonical page as one object unless you are intentionally storing a debug or failure artifact

Examples:

```bash
uv run {baseDir}/scripts/upload_page_to_r2.py \
  --input tmp/page-0001.json \
  --page-index 1 \
  --extract-foods \
  --skip-existing
```

```bash
uv run {baseDir}/scripts/upload_page_to_r2.py \
  --input tmp/food-10001.json \
  --page-index 1 \
  --food-id 6877a6b660d6c84e9bd5cca4 \
  --skip-existing
```

```bash
cat tmp/food-10001.json | uv run {baseDir}/scripts/upload_page_to_r2.py \
  --page-index 1 \
  --food-id 10001 \
  --skip-existing \
  --content-type application/json
```

```bash
uv run {baseDir}/scripts/upload_page_to_r2.py \
  --input tmp/food-10001.json \
  --key raw/viendinhduong/2026-03-15T10-00-00Z/page-0001/food-10001.json
```

Only for debug or failure capture:

```bash
uv run {baseDir}/scripts/upload_page_to_r2.py \
  --input tmp/page-0001.json \
  --page-index 1 \
  --failed
```

## Source Notes

For this provider target, use `{baseDir}/references/source-notes.md`.
