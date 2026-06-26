---
name: loki-query
description: Query Loki logs via API for debugging and troubleshooting. Use when user needs to: (1) Query logs by traceid or keywords, (2) Filter logs by pod name, namespace, labels, or time range, (3) Debug application issues using structured log queries, (4) Analyze logs from Kubernetes pods. Accepts parameters like traceid, keywords, start_time, end_time, pod, namespace, labels, loki_url.
---

# Loki Log Query

Query logs from Grafana Loki using the bundled script.

## Two Access Modes

### 1. Direct URL Access (Recommended)

Use when Loki is accessible via network (cloud service, remote server, etc.):

```bash
# Using remote Loki URL
python scripts/query_loki.py \
  --loki-url "https://loki.example.com:3100" \
  --query "{namespace=\"default\"}" \
  --start "now-1h" \
  --limit 50
```

### 2. Kubernetes Port-Forward

Use when Loki is only accessible via kubectl:

```bash
# Terminal 1: Port-forward Loki
kubectl port-forward -n prometheus svc/loki 3100:3100

# Terminal 2: Query logs
python scripts/query_loki.py \
  --loki-url "http://localhost:3100" \
  --query "{namespace=\"default\"}"
```

Or use inline port-forward with kubectl exec:

```bash
kubectl exec -n prometheus <loki-pod> -- curl -s "http://localhost:3100/loki/api/v1/query_range?query={namespace=\"default\"}&limit=50"
```

## Query Script

Use `scripts/query_loki.py` to query logs:

```bash
python scripts/query_loki.py \
  --loki-url "http://localhost:3100" \
  --query '{namespace="default"}' \
  --start "now-1h" \
  --end "now" \
  --limit 100
```

**Default:** If `--loki-url` is not specified, uses `http://localhost:3100`.

## Common Query Patterns

### By Namespace

```
{namespace="<namespace>"}
```

### By Pod

```
{namespace="<namespace>", pod="<pod-name>"}
```

### By Labels

```
{namespace="<ns>", app="<app-label>"}
```

### Search Keywords

```
{namespace="<ns>"} |= "ERROR"
{namespace="<ns>"} |= "traceid=<trace-id>"
{namespace="<ns>"} |= "Exception"
```

### Time Range

- Last 1 hour: `now-1h`
- Last 30 minutes: `now-30m`
- Specific range: `2026-03-27T10:00:00Z` to `2026-03-27T11:00:00Z`

## Parameters

- `loki-url`: Loki API endpoint (default: http://localhost:3100)
- `query`: LogQL query string (required)
- `start`: Start time (ISO 8601 or relative like now-1h, default: now-1h)
- `end`: End time (ISO 8601 or relative like now, default: now)
- `limit`: Max results (default: 100)
- `direction`: "forward" or "backward" (default: backward)
- `--json`: Output raw JSON instead of formatted text

## Output

Returns formatted log lines. Each entry shows timestamp and log content.

## Examples

### Query error logs from last hour

```bash
python scripts/query_loki.py --query '{namespace="production"} |= "ERROR"'
```

### Query specific trace ID

```bash
python scripts/query_loki.py --query '{namespace="default"} |= "traceid=abc123"'
```

### Query pod logs with JSON output

```bash
python scripts/query_loki.py --query '{namespace="default",pod="my-app-0"}' --json
```