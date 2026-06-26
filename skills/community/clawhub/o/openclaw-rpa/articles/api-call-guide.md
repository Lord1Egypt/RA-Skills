# API Recording Guide (`api_call`)

The recorder supports **`api_call`** steps: **GET/POST** (or other methods) via **httpx**, with the response optionally saved to the Desktop. Full field list and progressive-probing tips: **[SKILL.en-US.md — `api_call`](../SKILL.en-US.md)** and **Scenario 1**.

---

## What `api_call` does

Adds a step that issues an **HTTP request** to a URL (independent of the current browser page) and optionally writes the response to a Desktop file (`save_response_to`).

---

## Key embedding strategy

In the `record-step` JSON, use **`__ENV:ENV_VAR_NAME__`** in `params` or `headers` **and** include the actual key in the step's **`"env"` field**:

```json
{
  "action": "api_call",
  ...,
  "params": {"apikey": "__ENV:ALPHAVANTAGE_API_KEY__", ...},
  "env": {"ALPHAVANTAGE_API_KEY": "your-real-key"}
}
```

The code generator detects the `env` field and **writes the key directly into the script** (e.g. `'apikey': 'your-real-key'`) — no `export` needed for replay; the script runs as-is.

If `env` is omitted, the generated code uses `os.environ.get("VAR", "")` and requires `export VAR=…` before running.

**Summary:** Use **`__ENV:NAME__`** + **`"env"` field** together → key written into script, no `export` needed.

---

## Alpha Vantage daily example (from Case §3)

Docs: [TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily). Typical `record-step`:

- `base_url` + `params` (`function`, `symbol` = IBM, `outputsize` = compact, …)
- `apikey` = `"__ENV:ALPHAVANTAGE_API_KEY__"`
- `env` with real key
- `save_response_to` = output filename

---

## Combined flow: quotes + news page + local brief

One task can:
1. Save quote JSON to Desktop via `api_call`
2. Open a news page in the browser
3. `extract_text` into the same brief filename (append rules in [SKILL.en-US.md — Scenario 1](../SKILL.en-US.md))

**Plain-language task prompt** for this flow: see [README.md — Case §3](../README.md#api-quotes-news-brief).

---

## Caveats

- **Compliance:** Follow each site's terms of service and policies. This repo does not endorse evading safeguards or scraping where it isn't allowed.
- **High-friction sites (e.g. LinkedIn):** Even with auto sign-in or session reuse, you may still hit **2FA, device checks, CAPTCHAs, and risk blocks** that require **human steps**.
