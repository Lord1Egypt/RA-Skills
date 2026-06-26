# Grafana Readonly Action Checklist

## MVP actions

### 1. search_dashboards
Return at least:
- uid
- title
- folder
- tags
- url

### 2. get_dashboard
Return at least:
- uid
- title
- tags
- variables
- panels
- default time settings if available

### 3. list_panels
Return at least:
- panel_id
- title
- type
- datasource
- order consistent with the dashboard when possible

### 4. get_panel_query
Return at least:
- datasource
- queries[]
- ref_id
- query text or expression
- referenced variables

### 5. list_variables
Return at least:
- name
- current value
- type
- multi-select
- include all

### 6. run_panel_query
Support:
- default time range
- explicit time range
- variable overrides
- structured result output

## P1 actions

- preview_variable_values
- get_datasources
- run_query
- find_relevant_panels
- summarize_dashboard

## Return shape recommendation

```json
{
  "ok": true,
  "data": {},
  "summary": "..."
}
```

Error shape:

```json
{
  "ok": false,
  "error": {
    "code": "PANEL_NOT_FOUND",
    "message": "panel_id=12 not found"
  }
}
```

## Important implementation details

- A panel may have multiple queries; never assume only one target.
- Datasource may inherit from dashboard-level config.
- Variable substitution must handle single, multi, All, and empty values consistently.
- Prefer summarized output over raw Grafana JSON.
- Keep this skill read-only.
