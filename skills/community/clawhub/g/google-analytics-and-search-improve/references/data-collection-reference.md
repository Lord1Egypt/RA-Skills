# Data Collection Reference

Complete reference for data collection: authentication setup, script usage, API details, CSV export instructions, and custom query guidance.

---

## 1. Authentication Setup (Shared by GSC & GA4)

GSC and GA4 share the same Google Service Account. Create it once to use for both.

### Step 1: Create a Google Cloud Project and Enable APIs

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project selector (top-left) → "New Project" → name it (e.g., "my-site-analytics") → "Create"
3. Confirm you've switched to the new project, then open the [API Library](https://console.cloud.google.com/apis/library)
4. Search for **"Google Search Console API"** → click into it → click "Enable"
5. Search for **"Google Analytics Data API"** → click into it → click "Enable"
6. Search for **"PageSpeed Insights API"** → click into it → click "Enable" (used for site performance auditing; without it you'll get 429 quota errors)

### Step 2: Create a Service Account and Download JSON Key

1. Open the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click "+ Create Service Account" at the top
3. Enter a name (e.g., "analytics-reader") → click "Create and Continue"
4. Skip role selection (no project-level role needed) → "Continue" → "Done"
5. Find the newly created Service Account in the list, click its email address to enter the details page
6. Click the "Keys" tab → "Add Key" → "Create new key" → select **JSON** → "Create"
7. Your browser will automatically download a `.json` file — this is the key file
8. Note the Service Account email address (format: `analytics-reader@my-site-analytics.iam.gserviceaccount.com`)

### Step 3: Place JSON Key in configs/

```bash
cp /path/to/downloaded/my-site-analytics-xxxx.json "$DATA_DIR/configs/"
```

All scripts (`gsc_query.py`, `ga4_query.py`, `ga4_funnel.py`) auto-discover the `*.json` key file from `$DATA_DIR/configs/` via the shared `utils.py` module — no need to configure the path in `.env` or set `GOOGLE_APPLICATION_CREDENTIALS`. If multiple JSON files exist, the first one (alphabetically) is used.

### Step 4: Authorize in Search Console (for GSC)

1. Open [Google Search Console](https://search.google.com/search-console/)
2. Select your site property
3. Click "Settings" at the bottom of the left menu → "Users and permissions"
4. Click "Add user" → paste the Service Account email → set permission to "Restricted" (read-only) → "Add"

### Step 5: Confirm GSC Property Type

GSC has two property types, and the `GSC_SITE_URL` value must match the actual type:

| GSC Property Type | GSC_SITE_URL Format | Example |
|-------------------|---------------------|---------|
| **Domain property** | `sc-domain:domain` | `sc-domain:example.com` |
| **URL-prefix property** | Full URL | `https://example.com` |

> How to check: In the [Search Console](https://search.google.com/search-console/) property selector (top-left), if it shows a bare domain name it's a Domain property (use `sc-domain:` prefix); if it shows a full URL it's a URL-prefix property. Using the wrong format will cause the API to return a 403 permission error.

### Step 6: Authorize Service Account in GA4

1. Open [Google Analytics](https://analytics.google.com/)
2. Click the gear icon (Admin) in the bottom-left
3. Under "Property", click "Property Access Management"
4. Click "+" (top-right) → "Add users"
5. Paste the Service Account email → set role to "Viewer" → "Add"

### Step 7: Get GA4 Property ID

1. In the Google Analytics Admin page, click "Property Settings" (or "Property Details") under "Property"
2. The "Property ID" is displayed in the top-right — a numeric string (e.g., `123456789`, no "UA-" prefix)

### Step 8: Write to .env

```bash
cat > "$DATA_DIR/.env" <<EOF
SITE_URL=provided by user
GSC_SITE_URL=provided by user (note sc-domain: or https:// format)
GA4_PROPERTY_ID=provided by user
BING_WEBMASTER_API_KEY=provided by user (optional, for Bing search data)
SOURCE_CODE_PATH=provided by user
PSI_API_KEY=
EOF
```

---

## 2. Bing Webmaster Authentication (Separate from Google)

### Setup

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters/) and sign in
2. Add your site if not already added, and complete site verification
3. Click the **gear icon** (Settings) in the top-right → **"API Access"**
4. Accept the Terms & Conditions → click **"Generate API Key"** → copy the key

> Only one API key per user account. If compromised, delete and regenerate.

Write to `.env`:
```
BING_WEBMASTER_API_KEY=your_api_key_here
```

The site URL is read from `SITE_URL` (shared with GSC). No separate Bing URL variable needed.

---

## 3. Install Dependencies

Create a Python 3.12 virtual environment via `uv` and install dependencies:

```bash
uv venv "$DATA_DIR/venv" --python 3.12
uv pip install -p "$DATA_DIR/venv" -r scripts/pyproject.toml
```

> **Note**: All Python script executions MUST activate the venv first. After activation, use `python` directly:
> ```bash
> source "$DATA_DIR/venv/bin/activate"
> python scripts/xxx.py ...
> ```

---

## 4. Data Collection Modes

### Mode A: API Auto-Collection

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

# GSC data
python scripts/gsc_query.py --dimensions query --limit 500 -o "$DATA_DIR/data/gsc_queries.json"
python scripts/gsc_query.py --dimensions page --limit 500 -o "$DATA_DIR/data/gsc_pages.json"
python scripts/gsc_query.py --dimensions device,country -o "$DATA_DIR/data/gsc_devices.json"
python scripts/gsc_query.py --dimensions date -o "$DATA_DIR/data/gsc_trends.json"
python scripts/gsc_query.py --mode sitemaps -o "$DATA_DIR/data/gsc_sitemaps.json"

# GA4 data
python scripts/ga4_query.py --preset traffic_overview -o "$DATA_DIR/data/ga4_traffic.json"
python scripts/ga4_query.py --preset top_pages --limit 100 -o "$DATA_DIR/data/ga4_pages.json"
python scripts/ga4_query.py --preset user_acquisition -o "$DATA_DIR/data/ga4_acquisition.json"
python scripts/ga4_query.py --preset device_breakdown -o "$DATA_DIR/data/ga4_devices.json"
python scripts/ga4_query.py --preset landing_pages --limit 50 -o "$DATA_DIR/data/ga4_landing.json"
python scripts/ga4_query.py --preset user_behavior --limit 100 -o "$DATA_DIR/data/ga4_behavior.json"
python scripts/ga4_query.py --preset conversion_events -o "$DATA_DIR/data/ga4_conversions.json"

# Optional: funnel exploration (if user has custom events)
# python scripts/ga4_funnel.py --steps "event1,event2,event3" -o "$DATA_DIR/data/ga4_funnel.json"

# Optional: Bing Webmaster data (if BING_WEBMASTER_API_KEY is configured)
# python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"
# python scripts/bing_query.py --mode page_stats -o "$DATA_DIR/data/bing_pages.json"
# python scripts/bing_query.py --mode rank_traffic -o "$DATA_DIR/data/bing_traffic.json"
# python scripts/bing_query.py --mode links -o "$DATA_DIR/data/bing_links.json"
# python scripts/bing_query.py --mode crawl_stats -o "$DATA_DIR/data/bing_crawl.json"
```

### Mode B: Manual CSV Export

Send the following export instructions to the user, asking them to place files in `$DATA_DIR/data/`:

> **Export GSC data**:
> 1. Open [Google Search Console](https://search.google.com/search-console/) → Select your site
> 2. Click "Search results" (Performance) in the left menu
> 3. Set date range to last 3 months, click "Export" → "Download CSV"
> 4. Save the downloaded CSV as `$DATA_DIR/data/gsc_export.csv`
>
> **Export GA4 data (export the following reports)**:
> 1. Open [Google Analytics](https://analytics.google.com/) → Select your property
> 2. Export "Pages and screens" report:
>    - Left menu: "Reports" → "Engagement" → "Pages and screens"
>    - Click the share icon (top-right) → "Download file" → CSV
>    - Save as `$DATA_DIR/data/ga4_pages.csv`
> 3. Export "Traffic acquisition" report:
>    - Left menu: "Reports" → "Acquisition" → "Traffic acquisition"
>    - Export CSV → Save as `$DATA_DIR/data/ga4_acquisition.csv`
> 4. Export "Landing pages" report:
>    - Left menu: "Reports" → "Engagement" → "Landing pages"
>    - Export CSV → Save as `$DATA_DIR/data/ga4_landing.csv`
>
> Let me know when the export is complete, and I'll read the files to start analysis.

Also ask the user for:
- **Target website URL** (required, write to `SITE_URL` in `$DATA_DIR/.env`)
- **Source code path** (optional, write to `SOURCE_CODE_PATH`)

### Mode C: Browser Audit Only

Only ask the user for:
- **Target website URL** (required)
- **Source code path** (optional)

Write to `$DATA_DIR/.env` and skip directly to Phase 4 (site audit) and Phase 5 (source code review), skipping Phase 2-3.

### PageSpeed Insights Data Collection

```bash
PSI_BASE="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$SITE_URL&category=PERFORMANCE&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES"
PSI_KEY_PARAM="${PSI_API_KEY:+&key=$PSI_API_KEY}"
curl -s "${PSI_BASE}&strategy=mobile${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_mobile.json"
curl -s "${PSI_BASE}&strategy=desktop${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_desktop.json"
```

> **PSI failure fallback**: If a 429 (quota exceeded) or other error is returned, check whether "PageSpeed Insights API" has been enabled in the Google Cloud project (see Step 1). When PSI data is missing, continue with subsequent phases and note the missing performance data in the report.

---

## 5. GSC Script Reference (gsc_query.py)

> All example commands below assume the venv has been activated: `source "$DATA_DIR/venv/bin/activate"`

Scripts auto-read `GSC_SITE_URL` from `$DATA_DIR/.env` and auto-discover the Service Account JSON key from `$DATA_DIR/configs/`.

### Search Analytics Queries

```bash
# Last 28 days grouped by query and page (default)
python scripts/gsc_query.py

# Specify dimensions and date range
python scripts/gsc_query.py --dimensions query --limit 500 \
    --start-date 2025-01-01 --end-date 2025-03-01

# Group by device and country
python scripts/gsc_query.py --dimensions device,country --limit 100

# View trends by date
python scripts/gsc_query.py --dimensions date

# Output to file
python scripts/gsc_query.py --dimensions query -o gsc_data.json
```

The `--site-url` CLI flag overrides `GSC_SITE_URL` from `.env`.

### Available Dimensions

| Dimension | Description |
|-----------|-------------|
| `query` | Search query term |
| `page` | Page URL |
| `country` | Country code |
| `device` | Device type (DESKTOP/MOBILE/TABLET) |
| `date` | Date |
| `searchAppearance` | Search result appearance type |

### Returned Metrics

Each row contains:
- `clicks` — Click count
- `impressions` — Impression count
- `ctr` — Click-through rate (clicks / impressions)
- `position` — Average ranking position

### Sitemap & URL Inspection

```bash
# Sitemap query
python scripts/gsc_query.py --mode sitemaps

# URL inspection (indexing status, crawl info, mobile usability)
python scripts/gsc_query.py --mode inspect --inspect-url "https://example.com/some-page"
```

### Custom GSC Queries for Targeted Analysis

Beyond the standard data collection, GSC can serve as a powerful auxiliary analysis tool for deeper investigation. When the standard aggregated data is insufficient, write targeted queries to drill down into specific page sections, track daily trends for particular queries, or cross-filter dimensions.

**When to use custom GSC queries**:
- Standard data reveals an area that needs deeper investigation (e.g., a page group with anomalous metrics)
- The user asks about a specific subset of pages or queries
- You need to filter, segment, or cross-reference dimensions that the standard data collection didn't cover

**How to build custom queries**: Use `gsc_query.py` for standard dimension/date queries. For advanced filtering (e.g., `dimensionFilterGroups`), write a custom script following the GSC Search Analytics API patterns. Key capabilities:
- **Dimension filtering**: Filter by page path patterns, query keywords, country, device
- **Cross-dimension filtering**: Filter on a dimension not in the `dimensions` list
- **Fresh data access**: Use `dataState: 'all'` to include preliminary data from last 1-2 days
- **Pagination**: Retrieve up to 25,000 rows per request; paginate with `startRow`
- **Multi-condition filters**: Combine multiple filters within a group using AND logic

**Common analysis scenarios**:
1. **Section-specific analysis**: Filter by page path to isolate a site section
2. **Query trend tracking**: Group by `query` + `date` with a page filter
3. **Long-tail keyword discovery**: Query with high `rowLimit`
4. **Country-specific page performance**: Filter by country and group by page
5. **Regex-based pattern matching**: Use `includingRegex` operator

Save custom query output to `$DATA_DIR/data/gsc_*.json`.

### Common GSC Analysis Scenarios

- **Find High-Impression Low-Click Keywords**: Query `search_analytics` grouped by query; find rows with high `impressions` but low `ctr`.
- **Find Pages with Declining Rankings**: Group by `date,page`; compare `position` changes across different time periods.
- **Find Unindexed Pages**: Use `inspect` mode to check the indexing status of key pages one by one.

---

## 6. GA4 Script Reference (ga4_query.py)

> All example commands below assume the venv has been activated: `source "$DATA_DIR/venv/bin/activate"`

Scripts auto-read `GA4_PROPERTY_ID` from `$DATA_DIR/.env` and auto-discover the Service Account JSON key from `$DATA_DIR/configs/`.

### Preset Query Templates

```bash
python scripts/ga4_query.py --preset traffic_overview       # Daily traffic trends
python scripts/ga4_query.py --preset top_pages --limit 50   # Top pages
python scripts/ga4_query.py --preset user_acquisition       # User acquisition sources
python scripts/ga4_query.py --preset device_breakdown        # Device distribution
python scripts/ga4_query.py --preset geo_distribution        # Geographic distribution
python scripts/ga4_query.py --preset landing_pages           # Landing pages
python scripts/ga4_query.py --preset user_behavior           # User behavior
python scripts/ga4_query.py --preset conversion_events       # Conversion events
python scripts/ga4_query.py --preset demographics_age        # Age distribution (requires Google Signals)
python scripts/ga4_query.py --preset demographics_gender     # Gender distribution (requires Google Signals)
python scripts/ga4_query.py --preset demographics_geo        # Country + city distribution
python scripts/ga4_query.py --preset demographics_language   # Language distribution
python scripts/ga4_query.py --preset demographics_interests  # Interest categories (requires Google Signals)
python scripts/ga4_query.py --preset new_vs_returning        # New vs returning users
```

The `--property-id` CLI flag overrides `GA4_PROPERTY_ID` from `.env`.

### Custom Queries

```bash
python scripts/ga4_query.py \
    --dimensions pagePath,deviceCategory \
    --metrics sessions,bounceRate,averageSessionDuration \
    --start-date 2025-01-01 --end-date 2025-03-01 \
    --order-by="-sessions" --limit 200
```

### Date Formats

Both absolute and relative dates are supported:
- Absolute: `2025-01-01`
- Relative: `today`, `yesterday`, `NdaysAgo` (e.g., `28daysAgo`)

### Common Dimensions

| Dimension | Description |
|-----------|-------------|
| `date` | Date |
| `pagePath` | Page path |
| `pageTitle` | Page title |
| `landingPage` | Landing page |
| `sessionDefaultChannelGroup` | Channel grouping |
| `sessionSource` / `sessionMedium` | Source / Medium |
| `deviceCategory` | Device category |
| `operatingSystem` / `browser` | Operating system / Browser |
| `country` / `city` | Country / City |
| `eventName` | Event name |

### Common Metrics

| Metric | Description |
|--------|-------------|
| `sessions` | Session count |
| `totalUsers` / `newUsers` | Total users / New users |
| `screenPageViews` | Page views |
| `bounceRate` | Bounce rate |
| `averageSessionDuration` | Average session duration (seconds) |
| `engagementRate` / `engagedSessions` | Engagement rate / Engaged sessions |
| `eventCount` | Event count |
| `conversions` | Conversion count |

### Preset Template Reference

| Template | Purpose |
|----------|---------|
| `traffic_overview` | Daily traffic trends; detect traffic anomalies |
| `top_pages` | Find most popular and underperforming pages |
| `user_acquisition` | Analyze user source channel effectiveness |
| `device_breakdown` | Device and browser distribution; detect compatibility issues |
| `geo_distribution` | Geographic distribution; optimize internationalization |
| `landing_pages` | Landing page performance; optimize entry experience |
| `user_behavior` | User behavior paths and engagement depth |
| `conversion_events` | Conversion event tracking and funnel analysis |
| `demographics_age` | User age distribution with engagement and conversion metrics |
| `demographics_gender` | User gender distribution with engagement and conversion metrics |
| `demographics_geo` | User geographic distribution (country + city) |
| `demographics_language` | User language distribution |
| `demographics_interests` | User interest categories (requires Google Signals) |
| `new_vs_returning` | New vs returning user comparison with engagement depth |

---

## 7. GA4 Funnel Exploration (ga4_funnel.py)

> All example commands below assume the venv has been activated: `source "$DATA_DIR/venv/bin/activate"`

### API Coverage

GA4's "Explore" section offers several exploration types. Their API availability:

| Exploration Type | API Support | Method | API Version | Script |
|---|---|---|---|---|
| **Free-form** | ✅ Fully supported | `runReport` | v1beta (stable) | `ga4_query.py` |
| **Funnel exploration** | ✅ Supported | `runFunnelReport` | v1alpha (early preview) | `ga4_funnel.py` |
| **Path exploration** | ❌ No API | — | — | — |
| **Segment overlap** | ❌ No API | — | — | — |
| **User explorer** | ❌ No API | — | — | — |
| **Cohort exploration** | ❌ No API | — | — | — |
| **User lifetime** | ❌ No API | — | — | — |

> **Note**: `runFunnelReport` is in **v1alpha** (early preview). Google may introduce breaking changes before it reaches beta. The API is fully functional but you should monitor the [Google Analytics API announcements](https://groups.google.com/forum/#!forum/google-analytics-api-notify) for updates.

Authentication: Uses the **same Service Account** as `ga4_query.py`. No additional setup needed.

### Quick Start

```bash
# Simple 3-step funnel
python scripts/ga4_funnel.py \
    --steps "page_view,signup,purchase" \
    -o "$DATA_DIR/data/ga4_funnel.json"

# With custom display names
python scripts/ga4_funnel.py \
    --steps "page_view,signup,purchase" \
    --step-names "View Page,Sign Up,Purchase" \
    -o "$DATA_DIR/data/ga4_funnel.json"
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--property-id ID` | GA4 property ID (or set `GA4_PROPERTY_ID` env) |
| `--steps "e1,e2,e3"` | Comma-separated event names for funnel steps |
| `--step-names "n1,n2,n3"` | Comma-separated display names (must match `--steps` count) |
| `--config FILE` | Path to JSON config file for advanced funnel definitions |
| `--start-date DATE` | Start date (default: `28daysAgo`) |
| `--end-date DATE` | End date (default: `yesterday`) |
| `--open` | Open funnel — users can enter at any step (default: closed) |
| `--breakdown DIM` | Dimension to break down by (e.g. `deviceCategory`) |
| `--trended` | Show trended funnel (daily trend per step) |
| `-o FILE` | Output file path (default: stdout) |

### OR Logic in Steps

Use `|` within a step to match multiple events:

```bash
# Step 1 matches either first_open OR first_visit
python scripts/ga4_funnel.py \
    --steps "first_open|first_visit,page_view,purchase" \
    --step-names "First Touch,View Page,Purchase"
```

### Open vs Closed Funnels

| Type | Behavior | Flag |
|------|----------|------|
| **Closed** (default) | Users must enter at step 1. Only users who complete step 1 are tracked. | (none) |
| **Open** | Users can enter the funnel at any step. Each step is evaluated independently. | `--open` |

### Breakdown Dimension

```bash
# See funnel performance by device type
python scripts/ga4_funnel.py \
    --steps "page_view,add_to_cart,purchase" \
    --breakdown deviceCategory

# By traffic source
python scripts/ga4_funnel.py \
    --steps "page_view,signup" \
    --breakdown sessionDefaultChannelGroup
```

### Trended Funnel

```bash
python scripts/ga4_funnel.py \
    --steps "page_view,purchase" \
    --trended --start-date 30daysAgo
```

### Advanced: JSON Config File

For complex funnels with field filters, timing constraints, or mixed conditions:

```json
{
  "steps": [
    {
      "name": "Organic First Visit",
      "events": ["first_open", "first_visit"],
      "field_filter": {
        "field_name": "firstUserMedium",
        "value": "organic",
        "match_type": "CONTAINS"
      }
    },
    {
      "name": "View Product",
      "events": ["view_item"]
    },
    {
      "name": "Add to Cart",
      "events": ["add_to_cart"],
      "within_duration": "1800s"
    },
    {
      "name": "Purchase",
      "events": ["purchase", "in_app_purchase"],
      "directly_followed_by": true
    }
  ],
  "open": false,
  "breakdown": "deviceCategory",
  "trended": false
}
```

```bash
python scripts/ga4_funnel.py --config funnel_config.json -o funnel_report.json
```

**Config step fields**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Step display name (required) |
| `events` | string[] | Event names — matched with OR logic |
| `field_filter` | object | Dimension field filter: `{field_name, value, match_type}` |
| `field_filter.match_type` | string | `EXACT`, `BEGINS_WITH`, `ENDS_WITH`, `CONTAINS`, `FULL_REGEXP`, `PARTIAL_REGEXP` |
| `directly_followed_by` | bool | If `true`, this step must immediately follow the previous one |
| `within_duration` | string | Max time from prior step, e.g. `"300s"` (5 minutes) |

**Config top-level fields** (optional, CLI flags override):

| Field | Type | Description |
|-------|------|-------------|
| `open` | bool | Open funnel |
| `breakdown` | string | Breakdown dimension |
| `trended` | bool | Trended funnel |

### Output Format

```json
{
  "funnel_table": {
    "dimensions": ["funnelStepId", "funnelStepName", ...],
    "metrics": ["activeUsers", "funnelStepCompletionRate", "funnelStepAbandonments", "funnelStepAbandonmentRate"],
    "rows": [
      {
        "funnelStepId": "0",
        "funnelStepName": "View Page",
        "activeUsers": 5000,
        "funnelStepCompletionRate": 0.35,
        "funnelStepAbandonments": 3250,
        "funnelStepAbandonmentRate": 0.65
      }
    ]
  },
  "funnel_visualization": {
    "dimensions": ["funnelStepId", "funnelStepName"],
    "metrics": ["activeUsers"],
    "rows": [...]
  },
  "query": {
    "property_id": "123456789",
    "date_range": {"start": "28daysAgo", "end": "yesterday"},
    "is_open_funnel": false,
    "breakdown": "deviceCategory",
    "trended": false,
    "step_count": 3,
    "steps": ["View Page", "Sign Up", "Purchase"]
  }
}
```

**Key metrics in `funnel_table`**:

| Metric | Description |
|--------|-------------|
| `activeUsers` | Number of users who reached this step |
| `funnelStepCompletionRate` | % of users from this step who advanced to the next step |
| `funnelStepAbandonments` | Number of users who dropped off at this step |
| `funnelStepAbandonmentRate` | % of users who dropped off at this step |

When `--breakdown` is used, rows include the breakdown dimension value. The special value `RESERVED_TOTAL` indicates the total row across all dimension values.

### Sampling

Funnel reports may use data sampling. If the response includes a `"sampling"` key, the data is sampled:

```json
{
  "sampling": [
    {
      "samples_read_count": 500000,
      "sampling_space_size": 5000000
    }
  ]
}
```

This means 500,000 out of 5,000,000 events were sampled (10% sample rate). Results are extrapolated from this sample.

### Path Exploration — No API

Google has **not** released any API for path exploration. Alternatives:
1. **GA4 web UI**: Use the path exploration directly in the GA4 Explore section
2. **BigQuery export**: If your GA4 property is linked to BigQuery, query raw event-level data to reconstruct user paths with SQL
3. **Approximate with ga4_query.py**: Query `pagePath` + `eventName` dimensions to get page-level event distributions (not true sequential paths)

### Common Dimensions for Breakdown

| Dimension | Description |
|-----------|-------------|
| `deviceCategory` | Device type (desktop, mobile, tablet) |
| `country` / `city` | Geographic location |
| `sessionDefaultChannelGroup` | Traffic channel (Organic, Direct, Social, etc.) |
| `sessionSource` / `sessionMedium` | Traffic source and medium |
| `operatingSystem` / `browser` | OS and browser |
| `newVsReturning` | New vs returning users |

---

## 8. Bing Webmaster Script Reference (bing_query.py)

> All example commands below assume the venv has been activated: `source "$DATA_DIR/venv/bin/activate"`

| Item | Details |
|------|---------|
| **Base URL** | `https://ssl.bing.com/webmaster/api.svc/json/` |
| **Authentication** | API Key (passed as `apikey` query parameter) or OAuth 2.0 Bearer token |
| **Response format** | JSON |
| **Data retention** | **6 months** (shorter than GSC's ~16 months — set up regular data collection) |
| **Rate limits** | ~40-50 calls/day per API key for stats endpoints |

Scripts auto-read `BING_WEBMASTER_API_KEY` and `SITE_URL` from `$DATA_DIR/.env`.

### Search Traffic Queries

```bash
# Top queries with traffic stats (default)
python scripts/bing_query.py

# Top pages by traffic
python scripts/bing_query.py --mode page_stats

# Overall rank & traffic stats (daily impressions/clicks)
python scripts/bing_query.py --mode rank_traffic

# Stats for a specific query
python scripts/bing_query.py --mode query_detail --query "online 3d model converter"

# Stats for a specific page
python scripts/bing_query.py --mode page_detail --page "https://example.com/tools/converter"

# Stats for a specific query + page combination
python scripts/bing_query.py --mode query_page_detail --query "3d converter" --page "https://example.com/tools/converter"

# Keyword research (with country and date range)
python scripts/bing_query.py --mode keyword --query "image compressor" --country us \
    --start-date 2026-01-01 --end-date 2026-03-01

# Related keywords
python scripts/bing_query.py --mode related_keywords --query "image compressor" --country us \
    --start-date 2026-01-01 --end-date 2026-03-01

# Inbound link analysis
python scripts/bing_query.py --mode links

# Crawl stats
python scripts/bing_query.py --mode crawl_stats

# Output to file
python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"
```

The `--site-url` CLI flag overrides `SITE_URL` from `.env`.

### Available Modes

| Mode | API Method | Description |
|------|-----------|-------------|
| `query_stats` | `GetQueryStats` | Top queries with impressions, clicks, position |
| `page_stats` | `GetPageStats` | Top pages with traffic stats |
| `rank_traffic` | `GetRankAndTrafficStats` | Daily impressions & clicks overview |
| `query_detail` | `GetQueryTrafficStats` | Detailed stats for a specific query |
| `page_detail` | `GetPageQueryStats` | All queries driving traffic to a specific page |
| `query_page_detail` | `GetQueryPageDetailStats` | Stats for a specific query + page combination |
| `keyword` | `GetKeyword` | Keyword impression data for a country & date range |
| `related_keywords` | `GetRelatedKeywords` | Related keyword suggestions with impressions |
| `links` | `GetLinkCounts` | Pages with inbound links and link counts |
| `crawl_stats` | `GetCrawlStats` | Crawl frequency, errors, and patterns |

### Returned Metrics

Each traffic stats row contains:
- `Impressions` — Impression count on Bing search
- `Clicks` — Click count from Bing search
- `AvgClickPosition` — Average ranking position (where available)
- `Date` — Date of the data point (for time-series endpoints)

Keyword endpoints return:
- `Impressions` — Search volume / impression count for the keyword
- `BroadImpressions` — Broad match impression count
- `Query` — The keyword text

### Comparison with GSC API

| Feature | GSC API | Bing Webmaster API |
|---------|---------|-------------------|
| Auth method | Service Account (OAuth2) | API Key or OAuth 2.0 |
| Dimension filtering | `dimensionFilterGroups` with operators | Per-endpoint (query/page/query+page) |
| Custom date range | `startDate` / `endDate` on all queries | Available on keyword endpoints; traffic stats return all available data |
| Data retention | ~16 months | **6 months** |
| Keyword research | Not available | ✅ `GetKeyword`, `GetRelatedKeywords` |
| Backlink analysis | Not available | ✅ `GetLinkCounts`, `GetUrlLinks` |
| Crawl stats | Limited (via URL Inspection) | ✅ `GetCrawlStats`, `GetCrawlIssues` |
| URL submission | Not via same API | ✅ `SubmitUrl`, `SubmitUrlBatch` |
| Rate limit | ~25,000 rows/request | ~40-50 calls/day |

### Common Bing Analysis Scenarios

- **Find Top Performing Queries on Bing**: Use `query_stats` mode. Sort by impressions or clicks.
- **Analyze a Specific Page's Search Performance**: Use `page_detail` mode with `--page`.
- **Keyword Research & Discovery**: Use `keyword` and `related_keywords` modes — a capability GSC doesn't offer.
- **Monitor Crawl Health**: Use `crawl_stats` mode. Cross-reference with crawl issues.
- **Compare Google vs Bing Performance**: Run the same analysis period on both GSC and Bing data to identify keywords/pages where rankings differ.
