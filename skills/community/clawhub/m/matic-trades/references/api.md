# Matic Trades API — skill reference

Aligned with the backend models (`ToolExecutionRequest`, `DataRequest`, `AgentChartRequest`).

**Base:** `MATIC_TRADES_API_BASE` (default `https://api.matictrades.com/api/v1`, no trailing slash).  
**Auth:** `Authorization: Bearer <MATIC_API_KEY>`.

---

## POST `/toolbox/execute` — `AI_PICK`

Tool **selection** is driven by the **`prompt`** (server-side model picks 1–3 tools from the catalog).  
**`context` is optional** and **not required** for normal use; omit it unless you are using documented API extras (e.g. `custom_handlers` on the request body per Matic docs).

**Canonical minimal body:**

```json
{
  "mode": "AI_PICK",
  "prompt": "Your full natural language request including tickers and intent"
}
```

**Optional** fields on the real API (only if you implement them explicitly): `tools`, `context`, `custom_handlers` — see OpenAPI / dashboard docs. This skill’s script sends **only** `mode` + `prompt` for toolbox.

**Response (shape):** `request_id`, `tool_runs[]`, `total_execution_time_ms` (and cost fields where exposed).

---

## POST `/data/execute` — `SMART_SEARCH`

**`prompt`** is the primary input; the service resolves Twelve Data endpoint + params.

```json
{
  "mode": "SMART_SEARCH",
  "prompt": "RSI for Apple daily",
  "symbol": "optional hint",
  "interval": "optional e.g. 1day"
}
```

**Response:** `data`, `endpoint`, `symbol`, `ai_reasoning`, `execution_time_ms`, etc.

**DIRECT** mode (explicit `endpoint` + params) exists but is **not** what this skill’s `data` subcommand uses.

---

## POST `/agent/chart/autonomous`

```json
{
  "prompt": "Analyze NVDA multi-timeframe",
  "options": {
    "images": "url",
    "max_actions": 6,
    "model": "gpt-4o"
  }
}
```

**Response:** `status`, `actions`, `analysis`, optional `snapshots` (`pre_url`, `post_url`, or base64 fields).

---

## Discovery (Bearer auth)

- `GET /toolbox/tools` — tool catalog  
- `GET /data/endpoints` — allowed Twelve Data endpoints for the account tier  
