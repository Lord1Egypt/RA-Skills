# Input Schema

The analyzer accepts multiple JSON shapes.
Preferred order:

1. shared `signals[]`
2. crash-style `issues[]`
3. feedback-style `items[]`

## Shared `signals[]`

Use this for analytics, revenue, store, and custom connectors:

```json
{
  "project": "my-mobile-app",
  "window": "last_30d",
  "signals": [
    {
      "id": "retention_d3_drop",
      "title": "Day-3 retention dropped after onboarding paywall changes",
      "area": "onboarding",
      "priority": "high",
      "metric": "d3_retention",
      "current_value": 0.18,
      "baseline_value": 0.27,
      "delta_percent": -33.3,
      "evidence": [
        "Drop started after release 1.4.2",
        "Largest loss between onboarding step 2 and paywall view"
      ],
      "suggested_actions": [
        "Move paywall after first core value event",
        "Simplify onboarding step 2 form"
      ],
      "keywords": ["onboarding", "paywall", "trial"]
    }
  ]
}
```

## Crash `issues[]`

Works for Sentry, GlitchTip, Crashlytics-style exports:

```json
{
  "issues": [
    {
      "id": "glitchtip_1431",
      "title": "TypeError in paywall purchase callback",
      "priority": "high",
      "impact": "Conversion blocker in purchase flow",
      "events": 312,
      "users": 119,
      "stack_keywords": ["paywall", "purchase", "subscription", "callback"],
      "evidence": ["Crash occurs within 3s after paywall shown"]
    }
  ]
}
```

## Feedback `items[]`

Works for support, app reviews, in-app feedback, store review exports:

```json
{
  "window": "last_30d",
  "items": [
    {
      "id": "fb_onboarding_too_long",
      "title": "Onboarding feels too long before first value",
      "area": "onboarding",
      "priority": "medium",
      "count": 14,
      "channel": "support_tickets",
      "comment": "Users ask for a faster path to first result",
      "locations": [
        { "location_id": "onboarding/profile_step", "count": 9 },
        { "location_id": "onboarding/permissions_gate", "count": 5 }
      ],
      "keywords": ["onboarding", "friction", "first value"]
    }
  ]
}
```

## Extra Connectors

For `sources.extra[]`, the connector key becomes the source label in generated output.

Examples:

- `firebase_crashlytics`
- `app_store_reviews`
- `play_console`

Do not model GlitchTip as an extra connector when it exposes the Sentry-compatible API; use `sources.sentry.accounts[]`. Do not model ASC CLI as an extra connector in setup answers; it is the ASC / App Store Connect connector.

If your connector can already emit shared `signals[]`, use that shape. It is the least ambiguous path.

## ASC Analytics Payloads

The built-in ASC exporter can attach App Store Connect Analytics context under `meta.analytics`.
Use it for production growth/stability checks, not TestFlight crash triage.

Expected fields:

```json
{
  "project": "app-store-connect:123456789",
  "window": "latest",
  "signals": [
    {
      "id": "asc_production_crashes_detected",
      "area": "crash",
      "metric": "asc_total_crashes",
      "current_value": 3
    }
  ],
  "meta": {
    "source": "asc",
    "analyticsWindow": { "start": "2026-04-04", "end": "2026-05-03" },
    "analytics": {
      "units": { "total": 100, "previousTotal": 160, "percentChange": -0.375 },
      "redownloads": { "total": 12, "previousTotal": 10, "percentChange": 0.2 },
      "conversionRate": { "total": 4.5, "previousTotal": 6.2, "percentChange": -0.274 },
      "crashRate": {
        "total": 1.1,
        "previousTotal": 0,
        "percentChange": 1,
        "nonZeroDays": [{ "date": "2026-05-03", "value": 1.1 }]
      },
      "totalCrashes": 3,
      "crashBreakdown": [{ "label": "1.0.0 (iOS)", "value": 3 }],
      "sourceBreakdown": [
        { "title": "App Store Search", "pageViewUnique": 90, "units": 12 },
        { "title": "Web Referrer", "impressions": 110, "pageViewUnique": 10 }
      ],
      "overviewMetricCatalog": [
        {
          "section": "acquisition",
          "measure": "pageViewCount",
          "total": 80,
          "previousTotal": 120,
          "percentChange": -0.333,
          "type": "COUNT"
        }
      ]
    }
  }
}
```

Rules for recommendations:

- alert daily on non-zero production total crashes
- compare ASC crash totals with Sentry production issues/events/users when Sentry is connected
- if API-key ASC batch reports are missing, tell the user to verify `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY_PATH`, and `ASC_VENDOR_NUMBER` where Sales and Trends data is needed; do not ask for browser or web-session login
- inspect `overviewMetricCatalog` and parsed batch-report metrics so recommendations use all available ASC metrics, not only units/conversion/source traffic
- treat ASC sources according to the report instance fields available for that row: impressions, product page views, downloads, purchases, or proceeds
- turn source mix into Handlungsempfehlungen only after comparing units/downloads and conversion

## Multiple Sentry-Compatible Accounts

Use `sources.sentry.accounts[]` when an app has more than one Sentry-compatible crash source, for example Sentry Cloud plus a self-hosted GlitchTip instance:

```json
{
  "sources": {
    "sentry": {
      "enabled": true,
      "mode": "command",
      "command": "node scripts/export-sentry-summary.mjs --config data/openclaw-growth-engineer/config.json",
      "accounts": [
        {
          "id": "sentry_cloud",
          "label": "Sentry Cloud",
          "baseUrl": "https://sentry.io",
          "tokenEnv": "SENTRY_AUTH_TOKEN",
          "org": "owner-org",
          "projects": ["ios-app"],
          "environment": "production"
        },
        {
          "id": "glitchtip_selfhosted",
          "label": "GlitchTip self-hosted",
          "baseUrl": "https://glitchtip.example.com",
          "tokenEnv": "GLITCHTIP_AUTH_TOKEN",
          "org": "owner-org",
          "projects": ["backend-api", "web-app"],
          "environment": "production"
        }
      ]
    }
  }
}
```

Rules:

- keep tokens in environment variables or the OpenClaw secret file, not in config
- set one `tokenEnv` per account when Sentry Cloud and GlitchTip use different credentials
- use `projects[]` for all projects in that account that can affect the same product/app
- the exporter emits one combined `sentry:multiple` summary when more than one account/project is configured

## SEO Bing Webmaster Payloads

The built-in SEO exporter can attach Bing Webmaster Tools API context under `meta.bingWebmaster`.
Use it for Bing discovery/indexing diagnostics, sitemap/feed status, and URL-submission quota, not as a replacement for Google Search Console query performance.

Expected shape:

```json
{
  "project": "seo:https://example.com/",
  "window": "2026-03-03_2026-06-01",
  "signals": [
    {
      "id": "seo_bing_webmaster_status",
      "title": "Bing Webmaster sitemap/feed status needs monitoring",
      "area": "marketing",
      "priority": "low",
      "metric": "bing_webmaster_sites",
      "evidence": [
        "https://example.com/ feed https://example.com/sitemap.xml: status=Pending, type=Sitemap, urlCount=120",
        "https://example.com/: Bing URL submission quota daily=99, monthly=2899"
      ],
      "keywords": ["seo", "bing", "bing-webmaster", "sitemap", "indexing"]
    }
  ],
  "meta": {
    "source": "seo",
    "bingWebmaster": {
      "source": "bing-webmaster-api",
      "sites": [
        {
          "siteUrl": "https://example.com/",
          "quota": { "DailyQuota": 99, "MonthlyQuota": 2899 },
          "feeds": [
            {
              "url": "https://example.com/sitemap.xml",
              "status": "Pending",
              "type": "Sitemap",
              "urlCount": 120
            }
          ]
        }
      ]
    }
  }
}
```

Rules:

- store `BING_WEBMASTER_API_KEY` in the host env/secret file, not in config or chat
- set `BING_WEBMASTER_SITE_URL` or pass `--bing-site`; the exporter cannot infer Bing properties from GSC domain properties
- treat `Pending` as a processing state unless it persists or URL Inspection shows crawl/indexing errors
- keep URL submissions and IndexNow batches limited to canonical changed URLs
