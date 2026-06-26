---
name: gui-new
description: "Create shareable HTML canvases via the gui.new API. Use when: (1) generating visual output (dashboards, charts, forms, tables, diagrams, landing pages, interactive tools), (2) user asks to share or preview HTML as a live link, (3) user wants to turn code output into something viewable by others, (4) creating Mermaid diagrams as shareable links. POST HTML, get a live URL with real-time input sync and state persistence built in."
---

# gui.new

HTML in, URL out. One API call turns HTML into a shareable link.

## Create a Canvas

```bash
curl -X POST https://gui.new/api/canvas \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Hello</h1>", "title": "My Canvas"}'
```

Response: `{"id": "abc123", "url": "https://gui.new/abc123", "edit_token": "...", "expires_at": "..."}`

Always share the `url` with the user after creating.

## Update a Canvas

```bash
curl -X PUT https://gui.new/api/canvas/CANVAS_ID \
  -H "Authorization: Bearer EDIT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Updated</h1>"}'
```

## Extend Expiry

```bash
curl -X POST https://gui.new/api/canvas/CANVAS_ID/extend \
  -H "Authorization: Bearer EDIT_TOKEN"
```

## Mermaid Diagrams

```bash
curl -X POST https://gui.new/api/flow \
  -H "Content-Type: application/json" \
  -d '{"mermaid": "graph TD\n  A[Start] --> B[End]"}'
```

## Pro API Key (optional)

For extended expiry and higher limits, pass `x-api-key` header + `"expires": "7d"` body field (1h, 24h, 7d, 30d). No API key is needed for free tier usage.

## Security Note

This skill sends HTML content to https://gui.new, a third-party hosted service. Do not send sensitive, private, or confidential data. Canvases are publicly accessible via their URL. Links expire (24h free, up to 30d Pro).

## Built-in Components (auto-injected)

Use these tags directly — no script imports needed:

- `<gui-chart type="bar" data='[{"label":"Q1","value":42}]'>`
- `<gui-table data='[{"name":"Alice","role":"Eng"}]'>`
- `<gui-card title="Metric" value="1,247" change="+12%">`
- `<gui-code language="javascript">code</gui-code>`
- `<gui-timeline data='[{"date":"Mar 1","title":"Launch"}]'>`
- `<gui-kanban columns='[{"title":"Todo","items":["Task 1"]}]'>`
- `<gui-form fields='[{"name":"email","type":"email","label":"Email"}]'>`
- `<gui-grid columns="3">content</gui-grid>`

## Real-Time Sync

All form inputs (text, range, select, checkbox) sync across viewers automatically. No setup needed.

## Design Defaults

Dark background (#09090b), light text (#fafafa), system-ui font. Self-contained HTML with inline styles/scripts. Responsive.

## Limits

Free: 2MB max, 24h expiry, 3 edits, 5 creates/hour.
Pro: 10MB max, up to 30d expiry, unlimited edits, 100 creates/hour.

## SDKs

- npm: `npm install gui-new`
- pip: `pip install gui-new`
- Full docs: https://gui.new/docs
- llms.txt: https://gui.new/docs/llms.txt
