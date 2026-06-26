# Required Secrets

Use this checklist before running autopilot mode.

## Baseline

| Env var | Purpose | Required | Minimum scope |
| --- | --- | --- | --- |
| `GITHUB_TOKEN` | Repo/code access for analysis; optional GitHub issue/PR creation | Strongly recommended for code-aware analysis; required only for GitHub issue/PR creation | Prefer GitHub CLI auth when already available. Token fallback: fine-grained read-only `Contents: Read`, `Metadata: Read`; use all repos only for cross-repo analysis. Issue creation: add `Issues: Read/Write`. PR creation: add `Pull requests: Read/Write` and `Contents: Read/Write` |
| `ANALYTICSCLI_ACCESS_TOKEN` | AnalyticsCLI command auth when no local login exists | Recommended | Read-only analytics access across the account |
| `ASC_KEY_ID` / `ASC_ISSUER_ID` / `ASC_PRIVATE_KEY_PATH` | Optional App Store Connect Analytics reports via `asc` CLI | Optional, ask before setup | Ongoing Reports key should use `Sales and Reports` for downloads. `Finance` or `Admin` also works for report downloads. Use a separate temporary Setup key with `Admin` only to create the initial App Analytics report request, then revoke it |
| `REVENUECAT_API_KEY` | Optional RevenueCat monetization/subscription refresh | Optional, ask before setup | Secret API key stored server-side only. Prefer v2 read permissions for charts/metrics and required project configuration; add customer/subscriber read only when needed |
| `PADDLE_API_KEY` | Optional Paddle Billing metrics refresh | Optional, ask before setup | Live Paddle API key with `metrics.read` permission from `https://vendors.paddle.com/authentication-v2`; sandbox metrics are not production evidence |
| `GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN` or `GOOGLE_APPLICATION_CREDENTIALS` | Optional Google Search Console SEO refresh | Optional, ask before setup | Search Console read-only access. Leave `GSC_SITE_URL` empty to scan all verified properties visible to the account; set it only to intentionally restrict to one property. CSV-only SEO mode does not require a live token |
| `BING_WEBMASTER_API_KEY` / `BING_WEBMASTER_SITE_URL` | Optional Bing Webmaster sitemap, feed, and URL-submission quota status | Optional, ask before setup | Bing Webmaster API key from Settings → API Access for a user that has verified-site access. Use it for Bing sitemap/indexing diagnostics; it does not replace GSC query-performance data |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | Optional paid keyword research enrichment | Optional, ask before setup | Store only when the user explicitly wants DataForSEO; commands must use `--confirm-paid` and a small `--max-paid-requests` cap |
| `SENTRY_AUTH_TOKEN` | Sentry command/API refresh | Recommended | Read-only `org:read`, `project:read`, and `event:read` scopes |
| `SENTRY_ORG` / `SENTRY_ENVIRONMENT` | Sentry account targeting | Recommended when Sentry is enabled | Non-secret org/environment. Defer project scope to app/repo/release context; use `sources.sentry.accounts[].projects[]` only for known fixed mappings. `SENTRY_ENVIRONMENT` usually `production`; set `SENTRY_BASE_URL` only for self-hosted Sentry |

## Extra Connectors

For `sources.extra[]`, set `secretEnv` only when the connector actually needs it.

Examples:

- `GLITCHTIP_API_TOKEN`
- `ASC_KEY_ID`
- `ASC_ISSUER_ID`
- `ASC_PRIVATE_KEY_PATH`
- `ASC_BOOTSTRAP_KEY_ID`
- `ASC_BOOTSTRAP_ISSUER_ID`
- `ASC_BOOTSTRAP_PRIVATE_KEY_PATH`
- `PLAY_CONSOLE_SERVICE_ACCOUNT_JSON`

## Red Lines

- Never commit secrets to git
- Never store secrets in `data/openclaw-growth-engineer/config.json`
- Never put secrets into proposal files, issues, or PR bodies
- Do not ship privileged feedback keys directly in mobile app binaries unless they are intentionally public and app-scoped
