---
name: oo-g2
description: "G2 (g2.com). Use this skill for ANY G2 request — reading, creating, updating, and deleting data. Whenever a task involves G2, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "G2"
  author: "OOMOL"
  version: "1.0.2"
  services: ["g2"]
  icon: "https://static.oomol.com/logo/third-party/g2.svg"
---

# G2

Operate **G2** through your OOMOL-connected account. This skill calls the `g2` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected G2. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "g2" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "g2" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_research_board_product` — Add a product to a research board. [write]
- `add_research_board_products` — Add multiple products to a research board. [write]
- `create_product_mapping` — Create a product mapping. **No scope required.** [write]
- `create_research_board` — Create a research board. [write]
- `delete_research_board` — Delete a research board. [destructive]
- `get_activate_settings` — Retrieves G2 Activate settings for a product. **Requires `g2_activate.read` scope.**
- `get_category` — Get a G2 category by UUID or slug, optionally including related categories and products.
- `get_credit_account` — Retrieve credit account details for an organization. **No scope required.** Retrieve API metering credit account details including balance and total credits. Use `?include=deductions` to include the last month of deductions in the response.
- `get_my_product_review` — Show review for a product. **⚠️ G2 is currently restricting access to this endpoint.** This endpoint retrieves the review for a specific product owned by the current user.
- `get_product` — Get a G2 product by UUID or slug. Requires products.read permission.
- `get_product_ratings` — A product's ratings. **Requires `products.ratings.read` scope.**
- `get_question` — Shows a single question. **Requires `questions.read` scope.**
- `get_report` — Get a licensed report and its product snapshots. **Requires `reports.read` scope.** The report type selects the response shape: `grid` returns `grid_reports` with Grid product scores; `momentum` returns `momentum_reports` with Momentum Grid product scores; `implementation` returns `implementation_reports` with Implementation Index scores; `relationship` returns `relationship_reports` with Relationship Index scores; `results` returns `results_reports` with Results Index scores; `usability` returns `usability_reports` with Usability Index scores. Add `include=report_products` to receive the product snapshots. Unsupported report types do not match a route (404).
- `get_research_board` — Get a research board.
- `get_screenshot` — Shows a screenshot. **Requires `screenshots.read` scope.**
- `get_unlocked_company` — Shows a single unlocked company with resolved contacts. **Requires `g2_activate.read` scope.**
- `get_vendor` — Shows a single vendor. **Requires `vendors.read` scope.**
- `list_all_category_features` — List all category product features grouped by category. **Requires `product_features.read` scope.**
- `list_all_product_features` — List all product features grouped by product. **Requires `product_features.read` scope.**
- `list_categories` — List G2 categories with name, slug and date filters.
- `list_category_features` — List features for a specific category. **Requires `product_features.read` scope.**
- `list_credit_deductions` — Retrieve aggregated credit deductions by month and year. **No scope required.** Retrieve credit account deductions aggregated by month and year. Use filter parameters to narrow results: - `filter[month]`: Filter by month (1-12) - `filter[year]`: Filter by year (e.g., 2024)
- `list_data_solutions_reviews` — Lists reviews with all Data Solutions fields. **Requires `ds_reviews.read` scope.** **⚠️ BETA API**: This endpoint is a beta endpoint and it definition might change by the official release.
- `list_data_subscriptions` — Lists data subscriptions for given partner and account. **Requires `data_subscriptions.read` scope.** Data Subscriptions require a Partner ID and appropriate scope. Contact G2 for a unique Partner ID.
- `list_locked_companies` — Lists locked companies (masked) showing intent for a product. **Requires `g2_activate.read` scope.**
- `list_market_intelligence_reviews` — List Market Intelligence reviews for one product. Requires products.reviews.read and Market Intelligence access; competitor products in meta must be queried separately.
- `list_market_signals` — Retrieve buyer intent signals for a date range. **Requires `market_signals.read` scope.** Retrieve buyer intent signals (interactions) for specific categories. Returns one result per buyer intent interaction within the specified date range. Each interaction includes the category UUID, company name, and domain. If no dates are provided, defaults to today for both start and end date. Results are paginated using cursor-based pagination (default 25, max 250 per page).
- `list_owned_products` — List all products owned by current account. **⚠️ G2 is currently restricting access to this endpoint.** This endpoint shows subscription-specific product information, of products that the current account has ownership of.
- `list_product_badges` — Lists medals (badges) awarded to given product. **Requires `product.badges.read` scope.**
- `list_product_competitors` — Lists competitors related to given product. **No scope required.**
- `list_product_discussions` — Lists discussions related to given product. **Requires `products.discussions.read` scope.**
- `list_product_downloads` — Lists Downloads related to given product. **Requires `products.downloads.read` scope.**
- `list_product_features` — List features for a specific product. **Requires `product_features.read` scope.**
- `list_product_integration_reviews` — Lists integration reviews for given product. **Requires `integration_reviews.read` scope.**
- `list_product_mappings` — List of product mappings. **No scope required.**
- `list_product_reviews` — List standard or removed G2 product reviews. Requires products.reviews.read and the corresponding product license.
- `list_product_screenshots` — Lists Screenshots related to given product. **Requires `products.screenshots.read` scope.**
- `list_product_snippets` — Lists reviews of given product. **Requires `products.snippets.read` scope.**
- `list_product_video_reviews` — Lists video reviews related to given product. **Requires `products.video_reviews.read` scope.**
- `list_product_videos` — Lists videos related to given product. **Requires `products.videos.read` scope.**
- `list_products` — Search G2 products by name, category, domain, rating or other filters. Requires products.read permission.
- `list_questions` — List of questions. **Requires `questions.read` scope.**
- `list_reports` — Discover licensed Grid, Momentum, Usability, Implementation, Results and Relationship reports. Lists released Grid, Momentum, Usability, Implementation, Relationship, and Results report snapshots accessible through claimed or owned products. Each item is a reports resource with a report_type attribute; sparse fields use fields[reports]. Requires reports.read and an active report entitlement. One-off purchases do not require a Content Access subscription. Year is the named report season year (for example Winter 2025), not the calendar-quarter label. The legacy product-ID endpoint remains unchanged.
- `list_research_board_products` — List products on a research board.
- `list_research_boards` — List research boards for current user.
- `list_screenshots` — Lists screenshots. **Requires `screenshots.read` scope.**
- `list_unlocked_companies` — Lists unlocked companies for a product. **Requires `g2_activate.read` scope.**
- `list_vendors` — List of vendors. **Requires `vendors.read` scope.**
- `query_buyer_intent` — Browse buyer intent interactions (product-agnostic). **Requires `buyer_intent.read` scope.** Query buyer intent data across one or more products in a single request. Pass product_id to specify which products, or omit to use your assigned products. Supports multi-product queries — the data is not scoped to a single subject product.
- `query_product_buyer_intent` — Browse buyer intent interactions for a product. **Requires `buyer_intent.read` scope.** Query buyer intent data using an analytical query interface. ## Query Language This endpoint uses an OLAP-style query language that supports: - **Dimensions**: Group and categorize data (e.g., company_name, company_domain, day) - **Measures**: Aggregate numerical values (e.g., total_activity, visitor_count) - **Filters**: Apply conditions to limit results ### Filter Operators Filters use the format `dimension_filters[name_suffix]` where `name` is the dimension name and `suffix` indicates the operation: - `_eq`: Equals (exact match) - `_not_eq`: Not equals - `_cont`: Contains (substring match) - `_not_cont`: Does not contain - `_gt`: Greater than - `_gteq`: Greater than or equal - `_lt`: Less than - `_lteq`: Less than or equal - `_present`: Field has a value - `_empty`: Field is empty ### Time Series vs Aggregated Data - **Aggregated**: Request dimensions without `day` for company-level summaries - **Time Series**: Include `day` dimension for daily breakdowns over time ### Sorting Results Use the `sort` parameter to order results by any dimension or measure: - **Ascending**: `sort=company_name` or `sort=total_activity` - **Descending**: `sort=-company_intent_score` (prefix with `-`) - **Default**: Results are sorted by `-company_intent_score` (highest intent first) Available sort fields include all dimensions and measures listed above. ### Signal Types The `signal_type` dimension identifies the type of buyer activity on G2 (e.g., `profile`, `pricing`, `compare`). ### Competitive Signals Results include activity on both your product and competitor products in your categories. Compare `left_product_id` to `subject_product_id` to distinguish the two: - **`left_product_id` = `subject_product_id`**: Direct signal — activity on your product. - **`left_product_id` ≠ `subject_product_id`**: Competitive signal — activity on a competitor. The `signal_type` indicates what the buyer did (e.g., viewed the competitor's `profile` or `pricing` page). Use `left_product_name` / `left_product_slug` to identify the competitor. ### Examples - Company summary: `dimensions=company_name,company_domain&measures=total_activity` - Time series: `dimensions=company_name,day&measures=company_intent_score` - Filtered: `dimension_filters[company_name_cont]=Acme&dimensions=company_name` - Sorted by activity: `dimensions=company_name&measures=total_activity&sort=-total_activity` - Competitive activity: `dimensions=company_name,signal_type,left_product_name,left_product_id&measures=total_activity`
- `query_sandbox_buyer_intent` — Browse sandbox buyer intent interactions for a product. **No scope is required to access this sandbox endpoint** **⚠️ Sandbox API**: This endpoint is a sandbox endpoint and is data limited. Only data between 6 months to 1 year ago will be available. Query buyer intent data using an analytical query interface. ## Query Language This endpoint uses an OLAP-style query language that supports: - **Dimensions**: Group and categorize data (e.g., company_name, company_domain, day) - **Measures**: Aggregate numerical values (e.g., total_activity, visitor_count) - **Filters**: Apply conditions to limit results ### Filter Operators Filters use the format `dimension_filters[name_suffix]` where `name` is the dimension name and `suffix` indicates the operation: - `_eq`: Equals (exact match) - `_not_eq`: Not equals - `_cont`: Contains (substring match) - `_not_cont`: Does not contain - `_gt`: Greater than - `_gteq`: Greater than or equal - `_lt`: Less than - `_lteq`: Less than or equal - `_present`: Field has a value - `_empty`: Field is empty ### Time Series vs Aggregated Data - **Aggregated**: Request dimensions without `day` for company-level summaries - **Time Series**: Include `day` dimension for daily breakdowns over time ### Sorting Results Use the `sort` parameter to order results by any dimension or measure: - **Ascending**: `sort=company_name` or `sort=total_activity` - **Descending**: `sort=-company_intent_score` (prefix with `-`) - **Default**: Results are sorted by `-company_intent_score` (highest intent first) Available sort fields include all dimensions and measures listed above. ### Examples - Company summary: `dimensions=company_name,company_domain&measures=total_activity` - Time series: `dimensions=company_name,day&measures=company_intent_score` - Filtered: `dimension_filters[company_name_cont]=Acme&dimensions=company_name` - Sorted by activity: `dimensions=company_name&measures=total_activity&sort=-total_activity`
- `remove_research_board_product` — Remove a product from a research board. [write]
- `remove_research_board_products` — Remove multiple products from a research board. [write]
- `search_activate_industries` — Match a free-text business description to NAICS industry names. **Requires `g2_activate.read` scope.**
- `submit_product_review` — Submit or update a review for a product. **⚠️ G2 is currently restricting access to this endpoint.** This endpoint allows the user to submit or update a review for a specific product. The review is based on predefined questions and answers.' [write]
- `unlock_companies` — Spends G2 Activate credits to unlock one or more locked companies. **Requires `g2_activate.write` scope.** Accepts 1-25 opaque `sig` tokens from the locked_companies response and spends credits to reveal each company's identity. Always returns 200 — per-sig failures land in `meta.skipped[]` rather than as HTTP errors. Idempotent: replaying an already-unlocked sig costs 0 credits and returns the existing record. [write]
- `update_activate_settings` — Updates G2 Activate settings for a product. **Requires `g2_activate.write` scope.** [write]
- `update_product_mapping` — Update a product mapping. **No scope required.** [write]
- `update_research_board` — Update a research board. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change G2 state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — G2 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/g2
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- G2 homepage: https://www.g2.com
