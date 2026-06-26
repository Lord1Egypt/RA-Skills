---
name: kibana-data-views
description: "Manage Kibana Data Views (formerly index patterns) via REST API. Use when: (1) Creating, listing, updating, or deleting data views, (2) Checking data view existence before dashboard creation, (3) Troubleshooting missing index patterns, (4) Programmatically managing Kibana index patterns. API endpoints: POST /api/data_views, GET /api/data_views, GET /api/data_views/{viewId}, PUT /api/data_views/{viewId}, DELETE /api/data_views/{viewId}."
---

# Kibana Data Views API Skill

Manage Kibana Data Views (formerly "index patterns") via the Kibana REST API.

## Base URL

```
http://<kibana-host>/api/data_views
```

For Omni-Monitor: `http://192.168.99.43/api/data_views`

## Authentication

Kibana API requires `kbn-xsrf: true` header. For authenticated requests, use Kibana's session cookie or Basic auth.

---

## API Endpoints

### 1. List All Data Views
```
GET /api/data_views
```

**Response:**
```json
{
  "data_views": [
    {
      "id": "...",
      "title": "zbx-metrics-*",
      "name": "Zabbix Metrics",
      "timeFieldName": "@timestamp"
    }
  ]
}
```

### 2. Get a Data View
```
GET /api/data_views/{viewId}
```

**Path Parameters:**
- `viewId` (string, required): Data view identifier

**Response 200:**
```json
{
  "data_view": {
    "id": "...",
    "title": "zbx-metrics-*",
    "name": "Zabbix Metrics",
    "timeFieldName": "@timestamp",
    "fields": {...}
  }
}
```

### 3. Create a Data View
```
POST /api/data_views/data_view
```

**Headers:**
- `kbn-xsrf: true` (required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "data_view": {
    "title": "zbx-metrics-*",
    "name": "Zabbix Metrics",
    "timeFieldName": "@timestamp",
    "allowNoIndex": true
  }
}
```

**Response 200:** Returns created data_view object

**Response 400:** Bad request (e.g., duplicate title)

### 4. Update a Data View
```
PUT /api/data_views/{viewId}
```

**Path Parameters:**
- `viewId` (string, required): Data view identifier

**Request Body:**
```json
{
  "data_view": {
    "title": "zbx-metrics-*",
    "name": "Zabbix Metrics Updated",
    "timeFieldName": "@timestamp"
  }
}
```

### 5. Delete a Data View
```
DELETE /api/data_views/{viewId}
```

**Headers:**
- `kbn-xsrf: true` (required)

**Response 204:** Successfully deleted

**Response 404:** Data view not found

### 6. Check if Data View Exists (by title)
```
GET /api/data_views
```

Then search results for matching title.

### 7. Validate Index Pattern
```
POST /api/data_views/validate
```

Check if indices exist without creating a data view.

---

## Common Data View Titles for Omni-Monitor

| Title | Description |
|-------|-------------|
| `zbx-metrics-*` | Zabbix CPU/Memory/Disk metrics |
| `zbx-hosts-*` | Zabbix hosts |
| `zbx-problems-*` | Zabbix problems |
| `zbx-triggers-*` | Zabbix triggers |
| `k8s-pod-logs-*` | K8s pod logs |
| `k8s-audit-logs-*` | K8s audit logs |
| `vm-system-logs-*` | VM system logs |
| `ingress-nginx-logs-*` | Ingress nginx logs |
| `*-logs-*` | All logs |

---

## Usage with Kibana Proxy

When accessing Kibana API from external tool, you may need to proxy through Kibana:

```
http://192.168.99.43/api/console/proxy?path=<encoded-path>&method=<GET|POST|PUT|DELETE>
```

Example - List data views via proxy:
```
GET http://192.168.99.43/api/console/proxy?path=%2Fapi%2Fdata_views&method=GET
```

---

## Troubleshooting Lens "indexpattern" Errors

If Lens fails with error `Cannot read properties of undefined (reading 'indexpattern')`:

1. **Check if data view exists:**
```bash
curl -s "http://192.168.99.43/api/data_views" \
  -H "kbn-xsrf: true"
```

2. **Check data view ID matches what dashboard references:**
   - Dashboard references contain `indexpattern-datasource-layer-<uuid>` references
   - The uuid must match a real data view ID

3. **Recreate missing data view:**
```bash
curl -X POST "http://192.168.99.43/api/data_views/data_view" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "data_view": {
      "title": "zbx-metrics-*",
      "name": "Zabbix Metrics",
      "timeFieldName": "@timestamp",
      "allowNoIndex": true
    }
  }'
```

4. **Check .kibana index health:**
```bash
# Query from within k8s cluster
kubectl exec -n elastic elasticsearch-0 -- curl -s -u 'elastic:Changeme123' \
  'http://localhost:9200/.kibana/_search?size=100' \
  -H 'Content-Type: application/json' \
  -d '{"query": {"prefix": {"type": "index-pattern"}}}'
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `list_data_views.py` | List all data views from Kibana |
| `create_data_view.py` | Create a new data view |
| `delete_data_view.py` | Delete a data view |
| `check_and_fix_data_views.py` | Diagnose and fix missing data views |

---

## See Also

- [kibana-lens-builder](../kibana-lens-builder/SKILL.md) - Create Lens visualizations and dashboards