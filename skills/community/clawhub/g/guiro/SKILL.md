---
name: Guiro
description: Turn structured data into shareable visual dashboards, reports, charts, and calendars. Publishes an A2UI JSON bundle to guiro.io and returns a short-lived share link that anyone can view — no login required.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - GUIRO_API_KEY
      bins:
        - curl
      anyBins:
        - bash
        - sh
    primaryEnv: GUIRO_API_KEY
    emoji: "🔗"
    homepage: https://guiro.io
---

# Guiro – Shareable Visual Snapshots

**Guiro** (<https://guiro.io>) is an ephemeral Presentation Layer as a Service. You give it a structured JSON bundle describing a layout of visual components, and it returns a short-lived, publicly accessible share link (e.g. `https://guiro.io/s/{slug}`). The rendered page is a polished, read-only visual — a dashboard, report, chart, calendar, or status page. No login or account is needed to view it.

Use this skill whenever you produce structured results — metrics, tables, timelines, financial data, event schedules, progress tracking — and want to turn them into a shareable visual artifact the user can open in a browser, send to a colleague, or print to PDF.

## What you can build

| Type      | Best for                                                    |
|-----------|-------------------------------------------------------------|
| Dashboard | KPI metrics, data tables, timelines, progress bars, badges, icons |
| Calendar  | Read-only month views with highlighted dates and event detail |
| Chart     | Bar charts with multi-series comparisons                    |
| Donut     | Progress rings, savings goals, category breakdowns          |

## API workflow

1. **Fetch capabilities** — discover supported protocol versions and component catalogs.
2. **Build payload** — assemble an A2UI JSON bundle targeting the live contract values.
3. **Validate** — confirm the payload is well-formed before creating.
4. **Create** — publish the bundle and receive the share link.

## Endpoints

Base URL: `https://api.guiro.io`

| Action       | Method | Path                    |
|--------------|--------|-------------------------|
| Capabilities | GET    | /v1/create/capabilities |
| Validate     | POST   | /v1/validate            |
| Create       | POST   | /v1/create              |

## Authentication

All requests require an API key via the `X-API-Key` header. The key is read from the `GUIRO_API_KEY` environment variable. If the key is missing, ask the user to provide one.

## Commands

```bash
# 1 – Fetch capabilities (saves to .guiro/runtime-capabilities.json)
bash "{baseDir}/scripts/fetch-capabilities.sh"

# 2 – Write a sample payload (dashboard | calendar | chart | donut)
bash "{baseDir}/scripts/write-sample-payload.sh" ./payload.json dashboard

# 3 – Validate and create the guiro
bash "{baseDir}/scripts/create-guiro.sh" --payload ./payload.json --idempotency-key run-001
```

The sample payloads are starting points. Replace the placeholder content with real data relevant to the user's request.

## Payload structure

A valid A2UI bundle has this shape:

```json
{
  "storage_version": "1",
  "a2ui_version": "0.9",
  "catalog_id": "guiro.shadcn.detached.v1",
  "theme": {
    "primary": "#0f766e",
    "secondary": "#0f172a"
  },
  "messages": [
    {
      "version": "v0.9",
      "createSurface": {
        "surfaceId": "share-main",
        "catalogId": "guiro.shadcn.detached.v1"
      }
    },
    {
      "version": "v0.9",
      "updateComponents": {
        "surfaceId": "share-main",
        "components": [ ... ]
      }
    }
  ]
}
```

- `storage_version`, `a2ui_version`, `catalog_id` — use values from the capabilities response.
- `messages` must contain one `createSurface` message and one `updateComponents` message.
- Target exactly one surface.

## Component reference

The `components` array is a flat list of component objects. Each has an `id` (unique string) and a `component` type. Parent components reference children by id. The tree must include a component with `id: "root"`.

### Layout

| Component | Props                                           | Description              |
|-----------|-------------------------------------------------|--------------------------|
| Card      | `child` (string id)                             | Container card; use as the root wrapper |
| Column    | `children` (string id[]), `gap` (`sm`\|`md`\|`lg`) | Vertical stack           |
| Row       | `children` (string id[]), `gap` (`sm`\|`md`\|`lg`) | Horizontal stack         |
| List      | `children` (string id[])                        | Ordered list             |

### Content

| Component          | Props                                                     | Description             |
|--------------------|-----------------------------------------------------------|-------------------------|
| Text               | `text`, `variant` (`h1`\|`h2`\|`body`), `tone` (`muted`) | Heading or paragraph    |
| Badge              | `label`, `variant` (`secondary`\|`outline`\|`success`), `size` (`sm`) | Status badge or tag |
| Icon               | `name` or `icon`, `size`, `strokeWidth`, `color`, `label` | Lucide icon accent for headers, callouts, and status cues |
| ProgressIndicator  | `value` (number), `max` (number)                          | Progress bar            |
| DataTable          | `columns` (`{key, header}`[]), `data` (object[])          | Tabular data            |
| Calendar           | `title`, `description`, `month` (YYYY-MM-DD), `selected` (YYYY-MM-DD), `selectionMode` (`single`), `events` (`{date, label, detail, tone}`[]) | Read-only calendar with highlighted days and details below |
| Chart              | `title`, `description`, `chartType` (`bar`\|`donut`), `xKey`, `series` (`{key, label}`[]), `data` (object[]), `valueFormat` (`currency`), `currency` (ISO code) | Bar or donut chart |

### Component tree example

```json
[
  { "id": "root", "component": "Card", "child": "page" },
  { "id": "page", "component": "Column", "gap": "lg", "children": ["heading", "metrics"] },
  { "id": "heading", "component": "Text", "text": "Monthly Report", "variant": "h1" },
  { "id": "metrics", "component": "Row", "gap": "md", "children": ["badge1", "progress1"] },
  { "id": "badge1", "component": "Badge", "label": "Active: 42", "variant": "outline" },
  { "id": "progress1", "component": "ProgressIndicator", "value": 75, "max": 100 }
]
```

## Theme

Colors accept hex (`#0f766e`) or oklch (`oklch(0.527 0.154 150.069)`) values:

```json
{ "primary": "#0f766e", "secondary": "#0f172a" }
```

Choose theme colors that suit the content. Use contrasting primary and secondary values.

## Rules

- Always fetch capabilities first and use the returned values for `storage_version`, `a2ui_version`, and `catalog_id`.
- Always validate before create.
- The bundle must target exactly one surface.
- The `updateComponents` array must include a component with `id: "root"`.
- Treat validation errors as authoritative — fix the payload and re-validate until it passes.
- Use the sample payloads as structural templates but replace all placeholder content with real data from the user's request.
- Prefer `Icon` for section headers, callouts, and status accents when it improves scanability.

## Output

Successful create returns:

```json
{
  "slug": "abc123",
  "url": "https://guiro.io/s/abc123",
  "expires_at": "2025-07-15T12:00:00Z"
}
```

Share the `url` with the user. Guiros are ephemeral — after `expires_at`, the link shows a standardized "This Guiro has Expired" page.
