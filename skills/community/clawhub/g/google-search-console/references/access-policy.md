# Google Search Console access policy

An access policy limits which endpoints Google Search Console connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-search-console#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Search Console: its 7 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-search-console --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "v1/urlInspection/index:inspect"},
    {"method": "POST", "path": "v1/urlTestingTools/mobileFriendlyTest:run"},
    {"method": "POST", "path": "webmasters/v3/sites/{id}/searchAnalytics/query"},
    {"method": "GET", "path": "webmasters/v3/sites/{id}/sitemaps"},
    {"method": "GET", "path": "webmasters/v3/sites/{id}/sitemaps/{id}"},
    {"method": "GET", "path": "webmasters/v3/sites"},
    {"method": "GET", "path": "webmasters/v3/sites/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Search Console endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v1/urlInspection/index:inspect | read | index | Index inspection. |
| POST | v1/urlTestingTools/mobileFriendlyTest:run | read | mobileFriendlyTest | Runs Mobile-Friendly Test for a given URL. |
| POST | webmasters/v3/sites/{id}/searchAnalytics/query | read | searchanalytics | Query your data with filters and parameters that you define. |
| GET | webmasters/v3/sites/{id}/sitemaps | read | sitemaps | Lists the [sitemaps-entries](/webmaster-tools/v3/sitemaps) submitted for this site, or included in the sitemap index file (if `sitemapIndex` is specified in the |
| GET | webmasters/v3/sites/{id}/sitemaps/{id} | read | sitemaps | Retrieves information about a specific sitemap. |
| PUT | webmasters/v3/sites/{id}/sitemaps/{id} | write | sitemaps | Submits a sitemap for a site. |
| DELETE | webmasters/v3/sites/{id}/sitemaps/{id} | write | sitemaps | Deletes a sitemap from the Sitemaps report. |
| GET | webmasters/v3/sites | read | sites | Lists the user's Search Console sites. |
| GET | webmasters/v3/sites/{id} | read | sites | Retrieves information about specific site. |
| PUT | webmasters/v3/sites/{id} | write | sites | Adds a site to the set of the user's sites in Search Console. |
| DELETE | webmasters/v3/sites/{id} | write | sites | Removes a site from the set of the user's Search Console sites. |
