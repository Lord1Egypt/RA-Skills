# Monitor Configuration Reference

This is the full schema for `openstatus.yaml`, used by `openstatus monitors apply`.

## File Structure

```yaml
monitors:
  - name: "My API Monitor"
    kind: "http"
    # ... monitor fields
  - name: "Database TCP Check"
    kind: "tcp"
    # ... monitor fields
```

## Monitor Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Display name for the monitor |
| `description` | string | no | Description of what this monitors |
| `kind` | `"http"` or `"tcp"` | yes | Monitor type |
| `active` | bool | no | Whether the monitor runs on schedule (default: true) |
| `public` | bool | no | Whether results are publicly visible |
| `frequency` | string | yes | Check interval: `"30s"`, `"1m"`, `"5m"`, `"10m"`, `"30m"`, `"1h"` |
| `regions` | string[] | yes | Where to run checks from (see Regions below) |
| `retry` | int | no | Number of retries on failure |
| `timeout` | int (ms) | no | Request timeout in milliseconds |
| `degradedAfter` | int (ms) | no | Latency threshold before marking as degraded |
| `request` | object | yes | The request configuration (see below) |
| `assertions` | object[] | no | Conditions that must be met for the check to pass |
| `openTelemetry` | object | no | OpenTelemetry export config |

## Request (HTTP)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | Full URL to request |
| `method` | string | no | `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` (default: GET) |
| `headers` | map | no | HTTP headers as key-value pairs |
| `body` | string | no | Request body (for POST/PUT/PATCH) |
| `followRedirects` | bool | no | Whether to follow HTTP redirects (default: true) |

## Request (TCP)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `host` | string | yes | Hostname to connect to |
| `port` | int | yes | Port number |

## Assertions

Assertions define pass/fail conditions for each check.

| Field | Type | Description |
|-------|------|-------------|
| `kind` | string | What to assert on: `"statusCode"`, `"textBody"`, `"header"` |
| `compare` | string | Comparison operator (see below) |
| `target` | any | The value to compare against (int for statusCode, string for others) |
| `key` | string | Header name (only for `"header"` kind) |

**Comparison operators:**

| Operator | Description |
|----------|-------------|
| `eq` | Equal to |
| `not_eq` | Not equal to |
| `contains` | Contains substring |
| `not_contains` | Does not contain |
| `gt` | Greater than |
| `gte` | Greater than or equal |
| `lt` | Less than |
| `lte` | Less than or equal |
| `empty` | Is empty |
| `not_empty` | Is not empty |

## Regions

### Fly.io
`ams`, `arn`, `atl`, `bom`, `bog`, `bos`, `cdg`, `den`, `dfw`, `ewr`, `eze`, `fra`, `gdl`, `gig`, `gru`, `hkg`, `iad`, `jnb`, `lax`, `lhr`, `mad`, `mia`, `nrt`, `ord`, `otp`, `phx`, `qro`, `scl`, `sea`, `sin`, `sjc`, `syd`, `waw`, `yul`, `yyz`

### Koyeb
`koyeb_fra`, `koyeb_par`, `koyeb_sfo`, `koyeb_sin`, `koyeb_tyo`, `koyeb_was`

### Railway
`railway_us-west2`, `railway_us-east4-eqdc4a`, `railway_europe-west4-drams3a`, `railway_asia-southeast1-eqsg3a`

## OpenTelemetry

| Field | Type | Description |
|-------|------|-------------|
| `endpoint` | string | OTLP endpoint URL |
| `headers` | map | Auth headers for the endpoint |

## Complete Example

```yaml
monitors:
  - name: "Production API"
    description: "Main API health check"
    kind: "http"
    active: true
    public: true
    frequency: "1m"
    timeout: 10000
    degradedAfter: 3000
    retry: 2
    regions:
      - iad
      - fra
      - sin
      - syd
    request:
      url: "https://api.example.com/health"
      method: "GET"
      headers:
        Authorization: "Bearer ${API_TOKEN}"
    assertions:
      - kind: "statusCode"
        compare: "eq"
        target: 200
      - kind: "textBody"
        compare: "contains"
        target: "ok"

  - name: "Database TCP"
    description: "Verify database is reachable"
    kind: "tcp"
    active: true
    frequency: "5m"
    timeout: 5000
    regions:
      - iad
      - fra
    request:
      host: "db.example.com"
      port: 5432

  - name: "Webhook POST"
    description: "Verify webhook endpoint accepts payloads"
    kind: "http"
    frequency: "10m"
    regions:
      - iad
    request:
      url: "https://api.example.com/webhooks"
      method: "POST"
      headers:
        Content-Type: "application/json"
      body: '{"test": true}'
    assertions:
      - kind: "statusCode"
        compare: "lt"
        target: 300
      - kind: "header"
        compare: "not_empty"
        key: "x-request-id"
```
