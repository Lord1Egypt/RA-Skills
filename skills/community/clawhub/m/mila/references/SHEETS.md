# Sheets Reference

Sheets are workbooks containing one or more tabs. Each tab has its own grid of cells. Cell references use A1 notation (e.g. `A1`, `B3`, `AA10`).

## Concepts

- A **sheet** (workbook) is the top-level container. It has a title, belongs to a user/server, and contains one or more tabs.
- A **tab** is an individual spreadsheet within the workbook. Each tab has a name (e.g. "Sheet 1", "Revenue"), a grid size, and its own cell data.
- **Cells** use A1 notation as keys and cell objects as values.
- **Formulas** start with `=` (e.g. `=SUM(A1:A10)`, `=B2*1.1`). Cross-tab references use `=TabName!A1`.

## Cell object

| Field | Type | Description |
|---|---|---|
| `value` | string or number | The cell's content. Prefix with `=` for formulas. |
| `format` | object | Optional formatting (see below) |

**Format options:**

| Field | Type | Example |
|---|---|---|
| `bold` | boolean | `true` |
| `italic` | boolean | `true` |
| `underline` | boolean | `true` |
| `color` | string | `"#ff0000"` |
| `bgColor` | string | `"#f0f0f0"` |
| `borderColor` | string | `"#000000"` |
| `fontSize` | number | `14` |
| `fontFamily` | string | `"Arial"` |
| `align` | string | `"left"`, `"center"`, `"right"` |
| `textWrap` | string | `"overflow"`, `"wrap"`, `"clip"` |
| `numberFormat` | string | `"general"`, `"number"`, `"currency"`, `"percentage"`, `"date"`, `"time"` |
| `decimals` | number | `2` |
| `currencySymbol` | string | `"$"` |
| `currencyCode` | string | `"USD"` |
| `dateFormat` | string | `"MM/DD/YYYY"` |
| `decimalSeparator` | string | `"."` |
| `thousandSeparator` | string | `","` |

---

## List Sheets

**REST API:**

```
GET /v1/sheets
```

Returns workbooks with tab metadata (names, positions, grid sizes) but not cell data.

**Query parameters:**

| Param | Default | Description |
|---|---|---|
| `limit` | 50 | Results per page (1-100) |
| `offset` | 0 | Pagination offset |
| `sort` | `updated_at` | Sort field: `created_at`, `updated_at`, `last_edited_at`, `title` |
| `order` | `desc` | Sort order: `asc` or `desc` |
| `server_id` | *(all)* | Filter: omit for all, `personal` for personal files, or a server ID |

```bash
curl https://api.mila.gg/v1/sheets \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `list_sheets`

Parameters: `limit`, `offset`, `sort`, `order`, `server_id` (all optional).

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "xK9mQ2vB7n",
      "title": "Sales Report",
      "tabs": [
        { "id": "abc123", "name": "Sheet 1", "position": 0, "rows": 100, "columns": 26, "color": null },
        { "id": "def456", "name": "Summary", "position": 1, "rows": 100, "columns": 26, "color": "#4f46e5" }
      ],
      "server_id": null,
      "created_at": "2026-02-26T...",
      "updated_at": "2026-02-26T..."
    }
  ],
  "pagination": { "total": 1, "limit": 50, "offset": 0 }
}
```

---

## Get Sheet

**REST API:**

```
GET /v1/sheets/:id
```

Returns the workbook with all tabs including cell data in A1 notation.

```bash
curl https://api.mila.gg/v1/sheets/xK9mQ2vB7n \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `get_sheet`

Parameters: `id` (required, string).

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "xK9mQ2vB7n",
    "title": "Sales Report",
    "tabs": [
      {
        "id": "abc123",
        "name": "Sheet 1",
        "position": 0,
        "rows": 100,
        "columns": 26,
        "color": null,
        "cells": {
          "A1": { "value": "Product" },
          "B1": { "value": "Revenue" },
          "A2": { "value": "Widget" },
          "B2": { "value": 15000 }
        }
      }
    ],
    "server_id": null,
    "created_at": "2026-02-26T...",
    "updated_at": "2026-02-26T..."
  }
}
```

---

## Create Sheet

**REST API:**

```
POST /v1/sheets
```

Creates a new workbook with one initial tab. Optionally provide cells for the first tab.

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | Yes | Workbook title |
| `cells` | object | No | Cell data for the initial tab (A1 notation keys, cell objects as values) |
| `tab_name` | string | No | Name of the initial tab (default: `"Sheet 1"`) |
| `rows` | number | No | Number of rows (default: 100) |
| `columns` | number | No | Number of columns (default: 26) |
| `server_id` | string or null | No | Server to create in (null = personal files) |

```bash
curl -X POST https://api.mila.gg/v1/sheets \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q3 Budget",
    "server_id": "xK9mP2wQ",
    "tab_name": "Budget",
    "cells": {
      "A1": { "value": "Category", "format": { "bold": true, "bgColor": "#e2e8f0" } },
      "B1": { "value": "Amount", "format": { "bold": true, "bgColor": "#e2e8f0", "align": "right" } },
      "A2": { "value": "Engineering" },
      "B2": { "value": 50000, "format": { "numberFormat": "currency", "currencySymbol": "$", "decimals": 2 } },
      "A3": { "value": "Marketing" },
      "B3": { "value": 25000, "format": { "numberFormat": "currency", "currencySymbol": "$", "decimals": 2 } },
      "A4": { "value": "Total", "format": { "bold": true } },
      "B4": { "value": "=SUM(B2:B3)", "format": { "bold": true, "numberFormat": "currency", "currencySymbol": "$", "decimals": 2 } }
    }
  }'
```

**MCP tool:** `create_sheet`

Parameters: `title` (required), `cells` (optional), `tab_name` (optional), `rows` (optional), `columns` (optional), `server_id` (optional).

---

## Update Sheet

**REST API:**

```
PUT /v1/sheets/:id
```

Updates workbook-level properties only (title). To update cell data, use the tab endpoints below.

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | Yes | New workbook title |

```bash
curl -X PUT https://api.mila.gg/v1/sheets/xK9mQ2vB7n \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Workbook Title"}'
```

**MCP tool:** `update_sheet`

Parameters: `id` (required), `title` (required).

---

## Delete Sheet

**REST API:**

```
DELETE /v1/sheets/:id
```

Deletes the workbook and all of its tabs. This is permanent.

```bash
curl -X DELETE https://api.mila.gg/v1/sheets/xK9mQ2vB7n \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `delete_sheet`

Parameters: `id` (required).

---

## Get Tab

**REST API:**

```
GET /v1/sheets/:id/tabs/:tabId
```

Returns a single tab with its cell data in A1 notation.

```bash
curl https://api.mila.gg/v1/sheets/xK9mQ2vB7n/tabs/abc123 \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `get_sheet_tab`

Parameters: `sheet_id` (required), `tab_id` (required).

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "name": "Sheet 1",
    "position": 0,
    "rows": 100,
    "columns": 26,
    "color": null,
    "cells": {
      "A1": { "value": "Product" },
      "B1": { "value": "Revenue" },
      "A2": { "value": "Widget" },
      "B2": { "value": 15000 }
    }
  }
}
```

---

## Create Tab

**REST API:**

```
POST /v1/sheets/:id/tabs
```

Add a new tab to an existing workbook.

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Tab name (default: auto-generated, e.g. `"Sheet 2"`) |
| `cells` | object | No | Initial cell data (A1 notation) |
| `rows` | number | No | Number of rows (default: 100) |
| `columns` | number | No | Number of columns (default: 26) |

```bash
curl -X POST https://api.mila.gg/v1/sheets/xK9mQ2vB7n/tabs \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summary",
    "cells": {
      "A1": { "value": "Total Revenue" },
      "B1": { "value": "=Sheet 1!B5" }
    }
  }'
```

**MCP tool:** `create_sheet_tab`

Parameters: `sheet_id` (required), `name` (optional), `cells` (optional), `rows` (optional), `columns` (optional).

---

## Update Tab

**REST API:**

```
PUT /v1/sheets/:id/tabs/:tabId
```

Update a tab's name, color, grid size, or cells. When `cells` is provided, the new cells are **merged** with existing data -- existing cells not mentioned in the request are left unchanged.

**Body** (all fields optional):

| Field | Type | Description |
|---|---|---|
| `name` | string | Tab name |
| `color` | string or null | Tab color as hex (e.g. `"#4f46e5"`), or `null` to clear |
| `cells` | object | Cells to merge (A1 notation). Set a cell's value to `null` to clear it. |
| `rows` | number | Number of rows |
| `columns` | number | Number of columns |

**Updating specific cells without affecting others:**

```bash
curl -X PUT https://api.mila.gg/v1/sheets/xK9mQ2vB7n/tabs/abc123 \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "cells": {
      "B2": { "value": 18000 },
      "B3": { "value": 30000 },
      "C1": { "value": "Notes", "format": { "bold": true } },
      "C2": { "value": "Increased from Q2" }
    }
  }'
```

**Clearing a cell** -- set its value to `null`:

```json
{
  "cells": {
    "B2": null
  }
}
```

**MCP tool:** `update_sheet_tab`

Parameters: `sheet_id` (required), `tab_id` (required), `name` (optional), `color` (optional), `cells` (optional), `rows` (optional), `columns` (optional).

---

## Delete Tab

**REST API:**

```
DELETE /v1/sheets/:id/tabs/:tabId
```

Delete a tab from the workbook. You cannot delete the last tab -- every workbook must have at least one tab.

```bash
curl -X DELETE https://api.mila.gg/v1/sheets/xK9mQ2vB7n/tabs/def456 \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `delete_sheet_tab`

Parameters: `sheet_id` (required), `tab_id` (required).

---

## Append Rows

**REST API:**

```
POST /v1/sheets/:id/tabs/:tabId/rows
```

Append one or more rows of data to the end of a tab. Rows are placed after the last occupied row.

**Single row -- array form** (fills columns A, B, C, ...):

```json
{
  "values": ["Widget", 100, "$9.99"]
}
```

**Single row -- object form** (specify columns by letter):

```json
{
  "values": { "A": "Widget", "C": 100, "E": "$9.99" }
}
```

**Multiple rows -- array form:**

```json
{
  "rows": [
    ["Widget", 100, "$9.99"],
    ["Gadget", 50, "$19.99"],
    ["Doohickey", 200, "$4.99"]
  ]
}
```

**Multiple rows -- object form:**

```json
{
  "rows": [
    { "A": "Widget", "B": 100, "C": "$9.99" },
    { "A": "Gadget", "B": 50, "C": "$19.99" }
  ]
}
```

**Body fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `values` | array or object | One of `values` or `rows` | A single row. Array fills columns sequentially; object uses column letters as keys. |
| `rows` | array | One of `values` or `rows` | Multiple rows. Each element is an array or object as described above. |

```bash
curl -X POST https://api.mila.gg/v1/sheets/xK9mQ2vB7n/tabs/abc123/rows \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [
      { "A": "2026-02-26", "B": "Deploy v2.1", "C": "success" },
      { "A": "2026-02-26", "B": "Run migrations", "C": "success" },
      { "A": "2026-02-26", "B": "Clear cache", "C": "pending" }
    ]
  }'
```

**MCP tool:** `append_rows`

Parameters: `sheet_id` (required), `tab_id` (required), `rows` (optional, array), `values` (optional, single row).

**Response:**

```json
{
  "success": true,
  "data": {
    "start_row": 5,
    "rows_added": 3,
    "cells": {
      "A5": { "value": "2026-02-26" },
      "B5": { "value": "Deploy v2.1" },
      "C5": { "value": "success" },
      "A6": { "value": "2026-02-26" },
      "B6": { "value": "Run migrations" },
      "C6": { "value": "success" },
      "A7": { "value": "2026-02-26" },
      "B7": { "value": "Clear cache" },
      "C7": { "value": "pending" }
    }
  }
}
```

The `start_row` is 1-based (matching A1 notation). The `cells` object shows exactly which cells were written.

This is useful for:
- Logging data entries over time
- Appending records without knowing the current row count
- Building spreadsheets incrementally from automated workflows
