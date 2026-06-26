---
name: pipintama-charts
description: Create, fetch, share, or update hosted Pipintama Charts through the MCP server. Use when a user needs a line, bar, pie, or radar chart from text or structured values, and the right output is a hosted chart link or PNG instead of only prose.
---

# Pipintama Charts

Use this skill when the user would benefit from a hosted chart instead of only plain text.

Primary MCP endpoint:

- `https://api.pipintama.com/mcp`

Access model:

- this hosted MCP requires a valid Pipintama API key
- clients should provide it through `Authorization: Bearer <key>` or `x-api-key`
- usage is attributed to the authenticated client, not only the IP address

## Authentication

This skill requires a Pipintama API key.

The agent must:
- check if a valid API key is available before calling the MCP endpoint
- ask the user to provide or configure credentials if missing
- never attempt requests without authentication

Health check:

- `https://api.pipintama.com/mcp-health`

Primary tools:

- `list_chart_modes`
- `create_chart`
- `get_chart`
- `share_chart`
- `set_chart_visibility`
- `update_chart`
- `export_chart_png`

## When to use this skill

Use Charts when the user asks for:

- a line chart
- a bar chart
- a pie chart
- a radar chart
- a chart from numbers in plain text
- text to chart
- AI data visualization
- a visual comparison of quantities

Do not use Charts when:

- the user needs a process diagram
- the user wants a mindmap or architecture view
- a hosted board is more appropriate than a quantitative chart

## Core workflow

1. Understand the request and decide whether a chart is useful.
2. Choose the simplest correct chart type.
3. Build a concise chart title.
4. Preserve the user intent in `source_text` instead of rewriting the task into something unrelated.
5. Default visibility to `shared` unless the user explicitly wants `public` or `private`.
6. Do not pass `workspace_id` unless the user explicitly provides one. Let the authenticated API key determine the workspace.
7. Call the MCP tool that matches the job.
8. Return the hosted viewer URL first.
9. Add one short sentence explaining what the chart shows.

## Mode selection

- `line`: trends over time or sequence
- `bar`: category comparison or ranking
- `pie`: part-to-whole distribution with a small number of slices
- `radar`: multidimensional profile comparison

Prefer the simplest correct mode. Do not use `pie` for long lists or precise trend reading.

## Mode-specific rules

### `line`

Use when:

- the user wants a trend
- values change across time or ordered steps

Rules:

- keep the x-axis labels short
- use one or two series unless the user clearly asks for more

### `bar`

Use when:

- the user wants to compare categories
- ranking is more important than distribution

Rules:

- keep category labels readable
- avoid too many bars in a single chart

### `pie`

Use when:

- the user wants part-to-whole share
- the slice count is small

Rules:

- avoid pie charts for many categories
- use when visual share matters more than exact comparison

### `radar`

Use when:

- the user wants to compare profiles across the same dimensions
- there are a few shared axes and one or two entities

Rules:

- keep axis labels short
- use a small number of dimensions

## Visibility rules

- default to `shared`
- use `public` only when the user explicitly wants an open link
- use `private` only when the user explicitly asks for restricted access

## Tool usage

### `create_chart`

Use this for the first chart creation.

Expected inputs:

```json
{
  "title": "Weekly Active Agents",
  "chart_type": "line",
  "source_text": "Mon: 12\nTue: 18\nWed: 15\nThu: 22\nFri: 28",
  "visibility": "shared"
}
```

### `get_chart`

Use this when the user asks to inspect or retrieve an existing chart.

### `share_chart`

Use this when a chart should be opened through a tokenized share link.

### `set_chart_visibility`

Use this when the user explicitly asks to make a chart private, shared, or public.

### `update_chart`

Use this when the user wants to refine an existing chart instead of creating a new one.

Typical cases:

- change chart type
- update values
- rename title
- change visibility
- improve labels or series wording

### `export_chart_png`

Use this when the user needs an actual image file instead of only a hosted link.

Typical cases:

- Telegram
- WhatsApp
- quick previews in chat
- channels where an image is more useful than a URL alone

## Output format

Default output:

1. hosted viewer URL
2. one short explanation sentence

If the channel supports images and visual attachments are useful:

1. hosted viewer URL
2. PNG export URL
3. one short explanation sentence

Good response pattern:

```text
I created the chart:
https://pipintama.com/charts/<chart-id>?t=<share-token>

It shows weekly active agents as a line trend.
```

Image-friendly pattern:

```text
I created the chart and exported a PNG for easy sharing:
Viewer: https://pipintama.com/charts/<chart-id>?t=<share-token>
PNG: https://api.pipintama.com/mcp-chart-exports/<chart-id>.png?theme=light
```

Only use live Pipintama URL patterns.

Valid:

- `https://pipintama.com/charts/<chart-id>`
- `https://pipintama.com/charts/<chart-id>?t=<share-token>`
- `https://api.pipintama.com/mcp-chart-exports/<chart-id>.png?theme=light`

Invalid:

- `https://cdn.pipintama.com/charts/<chart-id>.png`
- `https://pipintama.com/chart/<chart-id>`

## Guardrails

- do not use `pie` for long category lists
- do not use `radar` when a bar chart would communicate more clearly
- do not fabricate Pipintama URLs
- do not dump raw chart JSON first when the hosted link is more useful
