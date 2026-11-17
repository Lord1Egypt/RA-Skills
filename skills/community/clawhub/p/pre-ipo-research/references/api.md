# Public API and portable client

Runtime: Node.js 18+, no npm dependencies, browser session or required secret.
Default base: https://preipo.polyos.ai; --base takes precedence over optional
PREIPO_API_BASE_URL. All network operations are public GETs without credentials.
--timeout-ms defaults to 15000 (range 1–60000), covering headers and body reads.
API redirects are rejected; reports allow only one same-origin .html →
extensionless canonical redirect. Response bodies are capped at 5 MiB.

## Routing

Jarsy retains /api/assets, /api/summary, /api/discovery and
/api/assets/{token}/detail for legacy JSON compatibility.
Other platforms use /api/platforms/{platform}/assets,
/api/platforms/{platform}/summary and
/api/platforms/{platform}/assets/{assetId}/detail.

The CLI defaults to jarsy. Natural-language company research without a specified
platform explicitly uses --platform all.

| Command | Scope | Result |
| --- | --- | --- |
| platforms | no platform flag | Client registry: version, baseUrl, platforms |
| summary | one platform or all | Statistics and freshness |
| search keywords | one platform or all | Paginated matches |
| list | one platform | Platform-specific filtered screen |
| detail assetId | one platform | Captured profile / full prediction topics |
| discover | jarsy only | Five Top-5 opportunity groups |
| report assetId | one platform | Published text, metadata and source links |

summary/detail/report accept --platform, --base, --timeout-ms and --json.
search/list additionally accept pagination and platform filters/sorts.
discover accepts --category and repeated --tag, not pagination.
Use --help for enums; unsupported combinations fail before any request.
Exact category/industry names come from that platform's summary, not a shared
taxonomy. See the platform references linked from SKILL.md.

## Pagination and raw output

--page maps to page; --page-size maps to pageSize. Default page size is 12.
Jarsy/all accepts sizes 6–48 and pages 1–10000; other platforms accept sizes
1–100 and pages 1–1000000. APIs may clamp page numbers: stop once the returned
page covers total, rather than repeating the last page.

Lists return items, total, page and pageSize. New platforms also return platform
and an unfiltered platform summary; it is not the filtered list's statistics.
Missing fields remain unavailable; zeroes remain zero.

Single-platform summary/search/list/detail/discover --json returns the parsed
API object unchanged, without an added wrapper or referral text.

## All-platform output

Only summary/search accept --platform all. All-platform search accepts keywords,
pagination and connection/output options, not industry/status/sort or other
platform-specific filters. Each platform retains its own default status and
sorting. No combined rank, company probability or valuation is calculated.

The JSON envelope is:
- scope: "all"
- command: "summary" or "search"
- partial: whether any platform failed
- results: five entries in registry order, each containing platform and status;
  success entries contain unchanged API data, error entries contain error text.

One failure does not cancel successful platforms. Any failure gives exit code 1,
with partial JSON on stdout. Top-level diagnostics go to stderr. Empty valid
lists succeed with exit code 0. There is no client quote cache or model fallback.

See reports.md for report's separate JSON contract and source hierarchy.
