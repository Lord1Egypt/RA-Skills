---
name: kibana-saved-objects
description: "Manage Kibana Saved Objects (dashboards, lens, visualizations) via REST API. Use when: (1) Creating/updating/deleting dashboards and Lens visualizations programmatically, (2) Importing/exporting saved objects via NDJSON, (3) Bulk creating/updating objects, (4) Managing references between objects, (5) Troubleshooting corrupted saved objects. Key operations: create, update, delete, bulk_create, bulk_get, export, import_objects."
---

# Kibana Saved Objects API Skill

Manage Kibana Saved Objects including dashboards, Lens visualizations, and other Kibana entities via REST API.

## Base URL

```
http://<kibana-host>/api/saved_objects
```

For Omni-Monitor: `http://192.168.99.43/api/saved_objects`

**Required Header:** `kbn-xsrf: true`

---

## Core Endpoints

### 1. Create Saved Object
```
POST /api/saved_objects/<type>
```
**Body:**
```json
{
  "attributes": {
    "title": "My Dashboard",
    "description": "..."
  },
  "id": "optional-custom-id",
  "references": [{"id": "...", "name": "...", "type": "index-pattern"}]
}
```

### 2. Get Saved Object
```
GET /api/saved_objects/<type>/<id>
```

### 3. Update Saved Object
```
PUT /api/saved_objects/<type>/<id>
```
**Body:**
```json
{
  "attributes": {
    "title": "Updated Title"
  },
  "references": [...]
}
```

### 4. Delete Saved Object
```
DELETE /api/saved_objects/<type>/<id>
```

### 5. Bulk Get
```
POST /api/saved_objects/_bulk_get
```
**Body:**
```json
{
  "objects": [
    {"type": "dashboard", "id": "abc123"},
    {"type": "lens", "id": "def456"}
  ]
}
```

### 6. Bulk Create
```
POST /api/saved_objects/_bulk_create
```
**Body:**
```json
{
  "objects": [
    {"type": "dashboard", "id": "...", "attributes": {...}},
    {"type": "lens", "id": "...", "attributes": {...}}
  ]
}
```

### 7. Export Saved Objects
```
POST /api/saved_objects/_export
```
**Body:**
```json
{
  "objects": [
    {"type": "dashboard", "id": "abc123"},
    {"type": "lens", "id": "def456"}
  ]
}
```
**Returns:** NDJSON stream of saved objects

### 8. Import Saved Objects
```
POST /api/saved_objects/_import?overwrite=true
```
**Content-Type:** `multipart/form-data`
**Form field:** `file` = NDJSON file

### 9. Find (Search) Saved Objects
```
POST /api/saved_objects/_find
```
**Body:**
```json
{
  "type": "dashboard",
  "search": "title keyword",
  "searchFields": ["title", "description"],
  "page": 1,
  "perPage": 20
}
```

---

## Common Object Types

| Type | Description |
|------|-------------|
| `dashboard` | Kibana dashboards |
| `lens` | Lens visualizations |
| `visualization` | Classic visualizations (TSVB, etc.) |
| `index-pattern` | Data views (index patterns) |
| `search` | Saved searches |
| `map` | Map visualizations |
| `tag` | Tags for organizing |
| `canvas-workpad` | Canvas workpads |

---

## References System

References link objects together. For example, a dashboard panel (lens) references:
1. The `index-pattern` (data view) it uses
2. Any parent dashboard it belongs to

**Reference format:**
```json
{
  "id": "b58d25c5-c05c-47be-a6cb-4073ef478a8f",
  "name": "indexpattern-datasource-layer-aca264a7-bf68-47b3-af63-db1e67fe0646",
  "type": "index-pattern"
}
```

**Creating with references:**
```json
{
  "type": "lens",
  "attributes": {
    "title": "CPU Usage",
    "state": {
      "datasourceStates": {...},
      "visualization": {...}
    }
  },
  "references": [
    {"id": "b58d25c5-c05c-47be-a6cb-4073ef478a8f", "name": "indexpattern-datasource-layer-xxx", "type": "index-pattern"}
  ]
}
```

---

## Dashboard Structure

**Dashboard attributes:**
```json
{
  "title": "Dashboard Name",
  "description": "Optional description",
  "panelsJSON": "[{\"type\":\"lens\",\"gridData\":{...},\"embeddableConfig\":{...}}]",
  "optionsJSON": "{\"useMargins\":true,\"syncColors\":false,\"hidePanelTitles\":false}",
  "timeRestore": true,
  "timeTo": "now",
  "timeFrom": "now-24h",
  "refreshInterval": {
    "pause": false,
    "value": 300000
  }
}
```

---

## Lens Object Structure

Lens is Kibana's next-generation visualization. Key structure:

```json
{
  "type": "lens",
  "attributes": {
    "title": "Metric Title",
    "state": {
      "datasourceStates": {
        "formBased": {
          "layers": {
            "<layer-uuid>": {
              "columns": {
                "<accessor-uuid>": {
                  "label": "Metric Label",
                  "dataType": "number",
                  "operationType": "count|average|sum|max|min",
                  "sourceField": "field.name",
                  "isBucketed": false,
                  "scale": "ratio"
                }
              },
              "columnOrder": ["<accessor-uuid>"],
              "incompleteColumns": {}
            }
          }
        }
      },
      "visualization": {
        "layerId": "<layer-uuid>",
        "layerType": "data",
        "metricAccessor": "<accessor-uuid>"
      }
    }
  },
  "references": [
    {"id": "<index-pattern-id>", "name": "indexpattern-datasource-layer-<layer-uuid>", "type": "index-pattern"}
  ]
}
```

**lnsMetric (single metric):**
```json
{
  "layerId": "...",
  "layerType": "data",
  "metricAccessor": "<accessor-uuid>"
}
```

**lnsXY (line/bar/area chart):**
```json
{
  "layerId": "...",
  "layerType": "data",
  "layers": [{
    "layerId": "...",
    "accessors": ["<accessor-uuid>"],
    "position": "top",
    "seriesType": "bar|line|area",
    "showGridlines": false,
    "xAccessor": "<accessor-uuid>"
  }]
}
```

---

## Important Rules

1. **Never use `__records___` as sourceField** → causes "Field not found" errors
2. **Text fields must use `.keyword` suffix** for aggregations (e.g., `host.keyword`)
3. **References must use correct format** → `indexpattern-datasource-layer-<layer-uuid>`
4. **Lens layerId and accessor UUIDs must be unique** per visualization

---

## NDJSON Import/Export Format

**Export produces:**
```
{"attributes":{"title":"Dash 1"...},"id":"abc","type":"dashboard","references":[...]}
{"attributes":{"title":"Lens 1"...},"id":"def","type":"lens","references":[...]}
```

**Import:** Same format, `overwrite=true` replaces existing objects.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `list_dashboards.py` | List all dashboards |
| `export_dashboard.py` | Export a dashboard and its dependencies |
| `import_ndjson.py` | Import NDJSON file to Kibana |
| `create_lens_metric.py` | Create a simple metric Lens visualization |

---

## See Also

- [kibana-data-views](../kibana-data-views/SKILL.md) - Manage data views (index patterns)
- [kibana-lens-builder](../kibana-lens-builder/SKILL.md) - Generate Lens visualizations for monitoring

---

## Troubleshooting

### "Cannot read properties of undefined (reading 'indexpattern')"

**Cause:** Dashboard/lens references a non-existent data view.

**Fix:**
1. List data views: `GET /api/data_views`
2. Verify referenced data view ID exists
3. Recreate missing data views with [kibana-data-views](../kibana-data-views/SKILL.md)

### "Field not found" errors

**Cause:** Using text field without `.keyword` suffix.

**Fix:** Use `host.keyword` not `host`, `metric_type.keyword` not `metric_type`

### Corrupted saved objects (404 on GET but appears in list)

**Fix:**
1. Delete the corrupted object: `DELETE /api/saved_objects/<type>/<id>`
2. Recreate with proper data