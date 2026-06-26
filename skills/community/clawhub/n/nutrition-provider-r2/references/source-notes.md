# Source Notes

## Provider

Use this skill only for the Vietnam nutritional portal sources:

`https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-thuc-pham`

`https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-mon-an`

This file contains provider-specific notes for those sources, not generic crawling guidance.

## Canonical data source

The canonical data is not the outer HTML shell.

When `scrapling-official` inspects this provider, it should prefer the JSON records payload over the outer page shell.

Observed canonical foods endpoint:

`https://viendinhduong.vn/api/fe/foodNatunal/getPageFoodData?page=1&pageSize=15&energy=0`

Observed foods response shape:

- top level: `data`, `current_page`, `per_page`, `total`
- food item fields include `_id`, `code`, `name_vi`, `name_en`, `category`, `categoryEn`, `nutrition`, `energy`

Observed canonical prepared-dish endpoint:

`https://viendinhduong.vn/api/fe/tool/getPageFoodData?page=1&pageSize=15`

Observed prepared-dish response shape:

- top level: `current_page`, `data`, `first_page_url`, `from`, `last_page`, `last_page_url`, `links`, `next_page_url`, `path`, `per_page`, `prev_page_url`, `to`, `total`
- dish item fields include `_id`, `category_id`, `code`, `description`, `dish_components`, `food_area_id`, `image`, `name_vi`, `name_en`, `nutritional_components`, `total_energy`, `category_name`, `category_name_en`, `category_description`

Observed search/filter params:

- foods:
  - `page`
  - `pageSize`
  - `name`
  - `category`
  - `energy`
- prepared dishes:
  - `page`
  - `pageSize`
  - observed from request: `name`, `energy`
  - additional filters are visible in the UI such as group and region; let `scrapling-official` inspect the live request params before assuming exact field names

Preserve that JSON response exactly as fetched for each page when `scrapling-official` retrieves it, then split `data` into individual record objects for upload.

- raw JSON page payload from the API
- one uploaded object per item from `data`
- raw query params used for that page
- raw linked detail payloads only if the crawl expands beyond the page endpoint
- page-level payload storage only for debugging or failures, not as the default dataset

Prefer handing the full page JSON to the upload helper in `--extract-foods` mode so splitting, key generation, and duplicate handling stay in one place. The helper flag name is legacy, but it works for both current sources because both return a `data` array.

Do not remap names, nutrients, vitamins, minerals, dish components, or ingredients into a custom schema.

Do not upload the outer HTML shell as the main dataset when `scrapling-official` can access this JSON payload.

## Pagination clues

Pagination is exposed directly in the observed API response.

- increment `page`
- keep `pageSize` stable unless the user asks otherwise
- stop when `data` becomes empty
- stop when `current_page * per_page >= total`
- stop if the next page repeats data already seen

## Pacing

Use one page at a time.

- records within the same page may upload in parallel
- wait for all record uploads from the page to finish
- ensure each page consumes at least 60 seconds total from fetch start to upload completion plus any remaining wait
- only then begin the next page

## Stop conditions

Stop when any of these happens:

- the API returns an empty `data` array
- `current_page * per_page >= total`
- the next request repeats a page already seen
- the provider returns an error page or block page

## Suggested storage layout

- `raw/viendinhduong/<run_id>/page-0001/food-6877a6b660d6c84e9bd5cca4.json`
- `raw/viendinhduong/<run_id>/page-0001/food-10001.json`
- `raw/viendinhduong/<run_id>/page-0002/food-....json`
- `raw/viendinhduong/<run_id>/failures/page-0003.json`

For prepared dishes, keep the same key layout and prefer `_id`, then `code`, as the stable object identifier.

Use distinct source namespaces when storing both datasets in R2.

- foods: prefer `SOURCE_NAME=viendinhduong-foods`
- prepared dishes: prefer `SOURCE_NAME=viendinhduong-dishes`

## Practical note

Run sequentially first. Only enable low concurrency after responses and pagination stay stable.
