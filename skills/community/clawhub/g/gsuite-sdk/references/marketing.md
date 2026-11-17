# Search Console, Analytics and Tag Manager

Read-only. Not in the default login: enable the **Google Search Console API**,
**Google Analytics Admin API** + **Google Analytics Data API** and **Tag
Manager API** in the Cloud project, then log in with their scopes
(`marketing` is the three together):

```bash
gsuite auth login --force --scopes default,marketing
```

Without them, calls fail with `PermissionDeniedError`. Every method returns
plain dicts and lists, as the Google APIs send them.

## CLI

```bash
gsuite searchconsole sites -o json
gsuite searchconsole query sc-domain:example.com --start 2026-03-01 --end 2026-03-28 --dim query --limit 50 -o json
gsuite searchconsole query sc-domain:example.com --start 2026-03-01 --end 2026-03-28 --dim page --filter query:contains:shoes
gsuite searchconsole query sc-domain:example.com --start 2026-03-01 --end 2026-03-28 --dim query --dim page --all -o json
gsuite searchconsole inspect sc-domain:example.com https://example.com/pricing -o json
gsuite searchconsole sitemaps sc-domain:example.com

gsuite analytics accounts -o json                       # find property IDs
gsuite analytics report 123456 --metric sessions --dim date --start 7daysAgo -o json
gsuite analytics report 123456 --metric activeUsers --dim country --order-by activeUsers --limit 10
gsuite analytics realtime 123456 --dim country

gsuite tagmanager accounts -o json
gsuite tagmanager containers accounts/123
gsuite tagmanager tags accounts/123/containers/456/workspaces/7 -o json
gsuite tagmanager versions accounts/123/containers/456
```

`--filter` is `dimension:operator:expression` (repeatable, ANDed); operators
are `equals`, `notEquals`, `contains`, `notContains`, `includingRegex` and
`excludingRegex`. Search Console data lags 2-3 days.

## Search Console

`SearchConsole(auth)` from `gsuite_searchconsole`. Properties are URL
prefixes (`https://example.com/`) or domains (`sc-domain:example.com`).

```python
from gsuite_core import GoogleAuth
from gsuite_searchconsole import SearchConsole

auth = GoogleAuth()
sc = SearchConsole(auth)

for site in sc.list_sites():
    print(site.site_url, site.permission_level)

rows = sc.query(
    "sc-domain:example.com",
    "2026-03-01",
    "2026-03-28",
    dimensions=["query", "page"],
    filters=[{"dimension": "country", "operator": "equals", "expression": "arg"}],
    row_limit=1000,
)
for row in rows:
    print(row.keys["query"], row.keys["page"], row.clicks, row.impressions, row.ctr, row.position)

result = sc.inspect_url("sc-domain:example.com", "https://example.com/pricing")
print(result.verdict, result.coverage_state, result.last_crawl_time)  # result.raw: full result
for sitemap in sc.list_sitemaps("sc-domain:example.com"):
    print(sitemap.path, sitemap.last_downloaded, sitemap.errors, sitemap.warnings)
```

Results are dataclasses (`Site`, `SearchAnalyticsRow`, `UrlInspection`,
`Sitemap`); each keeps the API resource in `.raw`. A row's `keys` maps each
requested dimension to its value.

`query` returns at most `row_limit` rows (up to 25000); page with `start_row`,
or call `sc.query_all(site, start, end, dimensions=[...], max_rows=None)` (CLI:
`--all`) to get every row.

## Analytics (GA4)

`Analytics(auth)` from `gsuite_analytics`. Property IDs are `"123456"`,
`123456` or `"properties/123456"`.

```python
from gsuite_analytics import Analytics

ga = Analytics(auth)

for account in ga.account_summaries():
    for prop in account.properties:
        print(account.display_name, prop.display_name, prop.property_id)

report = ga.run_report(
    "123456",
    ["date"],
    ["activeUsers", "sessions"],
    date_ranges=[("28daysAgo", "today")],
    dimension_filters=[{"field": "country", "value": "Argentina"}],
    order_by="date",
    descending=False,
)
for day in report.rows:  # metrics are numbers (int or float; None if unparseable)
    print(day.dimensions["date"], day.metrics["activeUsers"], day.metrics["sessions"])

ga.run_realtime_report("123456", ["country"], ["activeUsers"])  # also a Report
```

`account_summaries` returns `AccountSummary` (with `PropertySummary` items),
`list_properties`/`get_property` return `Property`, and both reports return a
`Report` (`dimensions`, `metrics`, `rows`, `row_count`, `totals`).

Filters: `{"field": f, "value": v}` (exact), `{"field": f, "operator":
"CONTAINS", "value": v}`, `{"field": f, "values": [..]}` (in list), numeric
`{"field": m, "operator": "GREATER_THAN", "value": 10}`; add `"not": True` to
negate.

## Tag Manager

`TagManager(auth)` from `gsuite_tagmanager`. Everything is addressed by its
API path: `accounts/1`, `accounts/1/containers/2`,
`accounts/1/containers/2/workspaces/3`.

```python
from gsuite_tagmanager import TagManager

gtm = TagManager(auth)

for account in gtm.list_accounts():
    for container in gtm.list_containers(account.path):
        print(container.public_id, container.name, container.path)

workspace = "accounts/1/containers/2/workspaces/3"
for tag in gtm.list_tags(workspace):
    print(tag.name, tag.type, tag.firing_trigger_ids, tag.paused)
gtm.list_triggers(workspace)
gtm.list_variables(workspace)

for version in gtm.list_versions("accounts/1/containers/2"):
    print(version.container_version_id, version.name, version.num_tags)
live = gtm.get_live_version("accounts/1/containers/2")  # the published version
print(len(live.tags), len(live.triggers), len(live.variables))
```

Results are dataclasses (`Account`, `Container`, `Workspace`, `Tag`, `Trigger`,
`Variable`, `VersionHeader`, `ContainerVersion`), each with its API resource in
`.raw`. Tags and variables carry the API's `parameter` list as `parameters`;
trigger conditions are in `trigger.raw`.
