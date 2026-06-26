---
name: matic_trades
description: Matic Trades API — AI toolbox (AI_PICK), Twelve Data (SMART_SEARCH), autonomous charting. Use for stocks, crypto, indicators, charts, news, sentiment. Triggers analyze NVDA, bitcoin RSI, unusual options, chart patterns, Matic, Twelve Data.
metadata:
  openclaw:
    emoji: 📈
---

# Matic Trades

This skill tells you how to call **Matic Trades** from OpenClaw using the bundled script. Keep instructions **short**: run the script, pass the user’s words as `--prompt`, return a clear summary (and image URLs when present).

## How OpenClaw uses this

- Skills are **markdown + optional files**; the model follows this file when the task matches the description.
- Prefer **`python3 "{baseDir}/scripts/matic.py" …`** so requests stay **consistent** with the real API (no hand-rolled JSON in chat).
- After the script prints JSON, **summarize for the user**; don’t dump raw JSON unless they ask.

Docs: [OpenClaw — Creating skills](https://docs.openclaw.ai/tools/creating-skills), [Skills loading](https://docs.openclaw.ai/tools/skills).

## Config

| Variable | Required | Purpose |
|----------|----------|---------|
| `MATIC_API_KEY` | **Yes** | Bearer token (same as dashboard API key). Alias: `MATIC_TRADES_API_KEY`. |
| `MATIC_TRADES_API_BASE` | No | Default `https://api.matictrades.com/api/v1` (no trailing slash). Override if your deployment uses another host. |

Never print or log the API key.

---

## 1) Toolbox — `AI_PICK` (default for “use Matic tools”)

**What the API does:** `POST /toolbox/execute` with `mode: AI_PICK`. The server uses the **prompt alone** to decide which tools to run (e.g. `chart_analysis`, `market_news`, `social_search`), then executes them. **`context` is not required** and is **not** what drives tool selection in normal use—put everything important **in the prompt** (tickers, timeframe, what they want).

**Minimal request body (this is correct):**

```json
{ "mode": "AI_PICK", "prompt": "User’s full request in natural language" }
```

**Run:**

```bash
python3 "{baseDir}/scripts/matic.py" toolbox --prompt "USER_TEXT_HERE"
```

**Examples (prompt-only):**

- `toolbox --prompt "Unusual options activity and any relevant news today"`
- `toolbox --prompt "Chart and sentiment for NVDA — focus on near-term levels"`
- `toolbox --prompt "Crypto whale moves and what people are saying on social"`

Do **not** require or invent a `context` object for AI_PICK unless you are implementing a **documented** advanced API feature (e.g. `custom_handlers` from Matic’s API docs). For ClawHub users, **prompt-only is the supported path.**

---

## 2) Data — `SMART_SEARCH` (Twelve Data via natural language)

**What the API does:** `POST /data/execute` with `mode: SMART_SEARCH`. The server maps the **prompt** to an allowed Twelve Data endpoint and parameters.

**Run:**

```bash
python3 "{baseDir}/scripts/matic.py" data --prompt "USER_TEXT_HERE"
```

Optional hints only if the user gave them: `--symbol AAPL`, `--interval 1day`. The API still centers on **`prompt`** for SMART_SEARCH.

---

## 3) Agent charting — autonomous charts + analysis

**What the API does:** `POST /agent/chart/autonomous` — multi-step chart agent; can return image URLs or base64 in `snapshots`.

**Run:**

```bash
python3 "{baseDir}/scripts/matic.py" chart --prompt "USER_TEXT_HERE" --images url
```

Use `--images url` when the client can open links; `b64` or `both` if the UI supports inline images.

Optional: `--max-actions N`, `--model MODEL` (see `references/api.md`).

---

## Which command when?

| User goal | Command |
|-----------|---------|
| Broad research, multiple possible tools, news/social/chart mix | **`toolbox`** (AI_PICK, **prompt only**) |
| “Get RSI / price / indicator / series for …” in plain English | **`data`** (SMART_SEARCH) |
| “Walk through charts”, “show me the chart”, visual narrative | **`chart`** |

**Chaining:** Only if it clearly helps—e.g. `data` for numbers, then `toolbox` for synthesis, or `chart` for visuals. Avoid redundant double calls.

---

## Response handling

- Parse JSON stdout; explain **tool_runs** / **analysis** / **data** in plain language.
- If **`snapshots.pre_url`**, **`snapshots.post_url`**, or URLs appear in outputs, **give the user those links**.

## Errors

- **401** — Missing/wrong `MATIC_API_KEY`.
- **429** — Rate limit; slow down or check plan.
- Quota / billing messages — Point to Matic dashboard.

## Files

- `references/api.md` — request/response shapes.
- `README.md` — install, ClawHub upload, env setup.

## Scope

Only call `matic.py` with user-supplied **prompt** text (sanitized for shell if needed). HTTP targets only `MATIC_TRADES_API_BASE` paths used by this script. No arbitrary `curl` to other hosts with user data.
