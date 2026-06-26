# MockLab - Smart Mock Data Generator

**Stop waiting for the gateway. Build your own.**

---

## What It Is

When the third-party test environment isn't ready, your project gets blocked.

MockLab is an AI-powered local Mock API server. Upload any API doc format (Markdown, Word, Java source), and AI understands it, generates Mock Schema, and starts the local server — **ready to test in 5 minutes**.

Backend developers can also use it as a **request proxy** to forward and debug local interfaces visually.

---

## Problems Solved

| Before | With MockLab |
|--------|-------------|
| Waiting for gateway (3 days to weeks) | Upload doc, online in 5 minutes |
| Manual Mock setup (1-2 days per API) | AI auto-parses, no manual work |
| Manual cross-API state management (error-prone) | `is_ref` + `state:` handles it automatically |
| Rebuild everything on doc updates | AI re-parses instantly |
| No way to test latency/error/timeout | Built-in delay simulation + error injection |
| Can't simulate real API behavior for frontend | Request mirroring + dynamic responses |
| Backend debugging requires code or Postman | UI-based proxy forwarding, visual debugging |
| Schema can't be shared with teammates | One-click import/export |
| Random data can't be reproduced | Seed feature for reproducible data |

---

## v1.3 New Features（2026-04-14）

- **Real Proxy** — Backend developers can forward requests to local interfaces and view real responses visually
- **Custom Headers** — Add Authorization and other custom request headers
- **Request Validation** — Prompts when required fields are missing
- **Import/Export Schema** — Share Schema files with teammates
- **Seed** — Fixed Seed generates reproducible Mock data
- **Array Element Optimization** — Avoid identical elements from fixed values
- **Enum Fix** — Now randomly selects instead of always returning first value
- **Timestamp Fix** — No longer overridden by field name inference

---

## How to Use

### First Time

```
User: "Start MockLab, upload [API doc]"
AI:   Reads doc → Generates Schema → Starts server
User: Open browser http://localhost:18080, start testing
```

### Subsequent Use

```
User: "Start MockLab"
AI:   Starts directly, loads existing Schema automatically
```

### Backend Debugging (v1.3)

```
User: Fill in request parameters in UI
User: Enter target address (e.g. http://localhost:8080)
User: Click Send → Request forwarded to local interface, real response displayed
```

---

## Features

### AI Smart Parsing
Supports Markdown, Word, Java source, plain text, URL — no manual config needed.

### Realistic Data Generation
Valid ID cards, real phone number prefixes, compliant plate numbers, amounts, rates — all generated according to field semantics.

### Nested Structure Support
reqData, vehicle, nodeList — 2-3 levels of nesting handled automatically.

### Encrypted Field Handling
reqData / ciphertext auto-parsed, body: supports nested path access.

### Cross-API State Management
`is_ref: true` saves to state, `state:` retrieves it automatically.

### State Persistence
Survives restarts, no reconfiguration needed.

### Multi-Project Support
One server hosts multiple third-party APIs, switch anytime.

### Delay Simulation
Simulates real network latency — fixed or random range.

### Error Injection
Custom error codes, messages, and trigger probabilities — test timeout, 429, 500 scenarios.

### Real Proxy (v1.3)
Backend developers: forward requests to local interfaces and view real responses visually.

### Custom Headers (v1.3)
Add Authorization, X-Request-Id and other custom headers to requests.

### Request Validation (v1.3)
Prompts when required fields are missing before sending.

### Import/Export (v1.3)
Download Schema as JSON file, share with teammates. Import to load instantly.

### Seed (v1.3)
Set a fixed Seed for reproducible Mock data — same Seed generates same data.

### Real-Time UI
Request editor + send + formatted response + delay/error/header/seed config.

---

## Field Rules

### Basic Rules

| Pattern | Rule | Generates |
|---------|------|-----------|
| Phone number | `phone` | 11-digit real prefix (13x/15x/18x/199) |
| ID card | `idcard` | 18-digit valid ID with checksum |
| Name | `name` | Chinese name |
| Plate number | `plate` | Compliant plate |
| Amount | `amount:lo-hi` | Random amount in range |
| Interest rate | `rate:lo-hi` | Random rate in range |
| Random number | `random:6` | 6-digit random number |
| Timestamp | `timestamp:ms` | Millisecond timestamp |
| Token | `token:32` | 32-char random hex string |
| Fixed value | `fixed:VALUE` | Constant (supports {index} placeholder) |
| Enum | `enum:a,b,c` | Random from list (supports {index} placeholder) |
| Auto sequence | `sequence:key` | Date + 6-digit auto-increment |
| Skip | `skip` | Not generated (e.g. sign) |
| Nested object | `nested:schemaName` | References inner_schemas |
| Object array | `array:schemaName` | Generates array |

### Dynamic Response Rules

| Rule | Description | Example |
|------|-------------|---------|
| `mirror` | Echo same-name field from request body | Request `{"order_id": "A123"}` → Response `"order_id": "A123"` |
| `body:data.order_id` | Access nested field in request body | Gets value at `body.data.order_id` |
| `path:order_id` | Access URL path parameter | Actual value from `/order/{order_id}` |
| `query:page` | Access URL query parameter | Value of `?page=2` |
| `header:Authorization` | Access request header | Gets Authorization header |
| `state:token` | Access cross-call state | Retrieves token stored by previous call |
| `when` condition | Return field only if condition is met | `{"field": "body.is_vip", "op": "eq", "value": true}` |

### when Operators

`eq` / `ne` / `gt` / `lt` / `contains` / `exists` / `not_exists`

---

## Interface-Level Config

Each interface supports top-level config:

```json
{
  "name": "Submit Order",
  "path": "/order/create",
  "method": "POST",
  "delay": "200-500",
  "error": "500@0.05:ERR_SYS:Server Error",
  "req_fields": [...],
  "resp_fields": [...]
}
```

### Delay Config

| Value | Effect |
|-------|--------|
| `"delay": "300"` | Fixed 300ms |
| `"delay": "200-500"` | Random 200~500ms |
| `"delay": "1000-3000"` | Stress test 1~3s |

### Error Injection Config

Format: `error_type[@probability[:err_code[:message]]]`

| Example | Effect |
|---------|--------|
| `"error": "500"` | 100% → HTTP 500 |
| `"error": "timeout"` | 100% → timeout (30s wait) |
| `"error": "network_error"` | 100% → HTTP 502 |
| `"error": "rate_limit"` | 100% → HTTP 429 |
| `"error": "500@0.05"` | 5% chance → HTTP 500 |
| `"error": "500@1.0:ERR001:Custom message"` | 100% → HTTP 500, custom code + message |

---

## Real Proxy (v1.3)

Backend developers can debug local interfaces visually:

1. Fill in request parameters in the UI
2. Enter target address (e.g. `http://localhost:8080/api/user`)
3. Click Send → Request forwarded to local interface
4. View the real response directly in MockLab

Supports custom headers like `Authorization: Bearer xxx`.

---

## Import/Export (v1.3)

- **Export**: Click "Export Schema" to download the current project's JSON file
- **Import**: Click "Import Schema" to upload a JSON file and load it instantly

---

## Seed (v1.3)

Set a fixed Seed (e.g. `12345`) to generate reproducible Mock data.

Same Seed → Same data → Easy to reproduce issues and run comparisons.

---

## State Management

### Saving to State

Add `is_ref: true` to a response field — it auto-saves to state after generation:

```json
{
  "name": "accessToken",
  "rule": "token:32",
  "is_ref": true
}
```

### Retrieving from State

Use `state:fieldName` in request fields — value is auto-filled from state:

```json
{
  "name": "accessToken",
  "rule": "state:accessToken"
}
```

Use case: Token, session ID, order numbers — any value that needs to persist across multiple API calls.

---

## Typical Use Cases

**A: Gateway too slow, project blocked**
> Third-party test environment isn't ready. Upload the doc, Mock Server is up in 5 minutes.

**B: Frontend-backend integration**
> Backend is still in development. Frontend uses MockLab to simulate backend and completes integration ahead of schedule.

**C: Automated test data generation**
> Test cases need various boundary data. AI generates realistic-looking data automatically.

**D: API flow regression testing**
> Run regression with Mock Server — no cost, no external calls.

**E: API documentation review**
> Test with MockLab, documentation ambiguities are exposed immediately, not after going live.

**F: Boundary testing**
> Test network latency, error responses, timeouts — without modifying the real service.

**G: Backend debugging (v1.3)**
> Backend developers: visualize request parameters, forward to local interfaces, view real responses.

**H: Team collaboration (v1.3)**
> Export Schema → Share with teammate → Import to use. No more manual copying.

---

## Requirements

- Python 3.8+
- FastAPI, Uvicorn (installed automatically)
- httpx (for Real Proxy feature, `pip install httpx`)

---

## Install

```bash
clawhub install mocklab
```

---

## FAQ

**Q: How are signature fields handled?**
A: Fields like `sign` are automatically skipped and won't appear in the request body.

**Q: How are encrypted fields (reqData, data, ciphertext) handled?**
A: AI extracts the plaintext structure into inner_schemas. When a request arrives, reqData strings are auto-parsed as JSON, and body: rules can access nested values inside them.

**Q: How does cross-API state work?**
A: Response fields marked `is_ref: true` are auto-saved to the state store. Subsequent interfaces use `state:fieldName` to auto-fill the value.

**Q: How many projects are supported?**
A: Unlimited. Switch between projects anytime via the dropdown in the UI.

**Q: How do I configure delay and error injection?**
A: Two ways: ① Configure directly in the UI (recommended) at http://localhost:18080; ② Add `delay` / `error` fields in the Schema JSON.

**Q: How does Real Proxy work?**
A: Enter a target address (e.g. `http://localhost:8080`) and click Send. The request is forwarded to that address and the real response is displayed. Supports custom headers.

**Q: How do I share Schema with teammates?**
A: Click "Export Schema" to download a JSON file. Teammate clicks "Import Schema" to load it instantly.

**Q: How do I reproduce the same Mock data?**
A: Set a fixed Seed value in the settings. Same Seed generates the same data every time.

---

## Changelog

### v1.3（2026-04-14）
- New: Real Proxy — forward requests to local interfaces, view real responses
- New: Custom Headers — add Authorization and other headers to requests
- New: Request Validation — prompts when required fields are missing
- New: Import/Export Schema — share Schema files with teammates
- New: Seed — fixed Seed generates reproducible Mock data
- Fix: Array elements now unique instead of identical
- Fix: Enum now randomly selects instead of always returning first value
- Fix: Timestamp rule no longer overridden by field name inference

### v1.2（2026-04-02）
- New: Delay simulation (interface.delay), fixed or random range
- New: Error injection (interface.error), custom codes, messages, probabilities
- New: Request mirroring (mirror / body:xxx / path:xxx / query:xxx / header:xxx)
- New: State reference (state:xxx) for cross-call state propagation
- New: Conditional fields (when) with operators: eq / ne / gt / lt / contains / exists / not_exists
- New: UI settings bar for visual delay and error configuration
- Fix: reqData / ciphertext auto-parsing, body: now supports nested path access
- Fix: `is_ref` field name compatibility

### v1.1 / v1.0（2026-04-01）
- Initial release
- AI parses any API doc format
- Built-in Mock rule engine
- Nested object & array support
- Cross-API state management
- State persistence
- Standalone UI template
- Multi-project support
