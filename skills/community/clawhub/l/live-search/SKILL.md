---
name: live-search
description: |
  Real-time answers from the public web via the host app’s local search gateway (Auth Gateway proxy). Typical stacks surface results comparable to major engines (e.g. Google or Bing, depending on host/region)—this skill only calls the local HTTP endpoint, not third-party search APIs directly.
  Use when the user needs fresh results, fact checks, prices, weather, news, scores, rates, or anything after the model’s knowledge cutoff.
  Triggers: “search”, “look up”, “find out”, “latest”, “today”, “current price”, “verify”, or any question needing live data.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - curl
---

# Live Search

Fetch **live web results** through the **host search gateway** at `http://localhost:$PORT` (session-authenticated). The gateway returns JSON with a pre-rendered `message` (titles as links, snippets, sources)—the same *kind* of web index results users expect from **Google-style or Bing-style** search, depending on how the host is configured.

**Endpoint path:** requests use `POST /proxy/prosearch/search`. The `prosearch` segment is a **fixed gateway route name** in the app; it is **not** a public product brand to repeat to end users—describe outcomes as “web search results” or “live search.”

## Setup

No extra Python packages. Search goes through the local gateway at `http://localhost:$PORT`; authentication is handled by the host app (login session)—**no manual API keys** in typical setups.

---

## Workflow

The assistant uses this skill whenever the user needs **real-time** information from the web.

### End-to-end flow

```
User asks for something that needs live web data
  → Step 1: Build a tight search keyword (concise, specific)
  → Step 1.5: Decide time freshness — add from_time when recency matters
  → Step 2: Call the search API with curl
  → Step 3: Echo the JSON `message` field VERBATIM (result list with clickable links) — do NOT skip this
  → Step 4: Optionally add analysis/summary after the verbatim block
```

> **CRITICAL — Anti-hallucination:** The API returns a pre-rendered `message` with formatted hits (titles as Markdown links, snippets, URLs). **The assistant MUST show `message` verbatim as the primary results.** It may add interpretation **after** that block. It must **not** invent, rewrite, or drop URLs/titles from `message`.

### Step 1: Build the keyword

Turn the user’s question into a short query:

| User intent | Example keyword |
|-------------|-----------------|
| Latest AI news | `latest AI news March 2026` or `最新 AI 新闻` (match user language) |
| Gold price now | `gold spot price today` |
| React 19 features | `React 19 new features` |
| Local weather | `London weather today` |

**Keyword tips:**
- Keep it short (about 2–6 tokens).
- Strip filler (“please”, “can you”, “帮我”).
- Add time hints when needed (`today`, `2026`, `latest`).
- **Keep the keyword in the language that matches the user’s intent** — do not blindly translate. If the user asks in English, search in English; if they ask in Chinese, Japanese, etc., use that language for the query when it improves results.

### Step 1.5: Time freshness (important for “latest” questions)

When the question implies **recency**, add **`from_time`** (Unix seconds) so stale pages are filtered out.

| User signal | `from_time` | Typical use |
|-------------|-------------|-------------|
| “today”, “just now”, “past 24h” | now − 86400 | Intraday facts |
| “recent”, “latest”, “this week” | now − 604800 | News, releases |
| “this month” | now − 2592000 | Monthly topics |
| “this year”, “2026” | Jan 1 of that year (local) | Year-scoped events |
| No time signal | omit `from_time` | Evergreen facts (“What is React?”) |

**Compute `from_time` in bash:**

```bash
# Last 24 hours
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 86400)")

# Last 7 days
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 604800)")

# Last 30 days
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 2592000)")
```

> **Mutual exclusion:** When using `from_time` / `to_time`, **do not send `cnt`** — the server enforces exclusion rules. Same for `site` + time filters; follow the API’s rules.

### Step 2: Request

```bash
PORT=${AUTH_GATEWAY_PORT:-19000}
PPID_VAL=$(python3 -c "import os; print(os.getppid())")
echo "[Assistant] Parent PID: $PPID_VAL"

curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"your search query"}'
```

**Freshness (recommended for time-sensitive queries):**

```bash
# Last 7 days (“latest”, “recent”)
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 604800)")
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d "{\"keyword\":\"your search query\",\"from_time\":$FROM_TIME}"

# Last 24 hours (“today”, “just now”)
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 86400)")
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d "{\"keyword\":\"your search query\",\"from_time\":$FROM_TIME}"
```

**Optional parameters:**

```bash
# Result count 10/20/30/40/50 — do not combine with from_time/to_time/site
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"your search query","cnt":20}'

# Time range (do not pass cnt)
FROM_TIME=$(python3 -c "import time; print(int(time.time()) - 604800)")
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d "{\"keyword\":\"your search query\",\"from_time\":$FROM_TIME}"

# Site-restricted search (do not pass cnt)
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"your search query","site":"github.com"}'

# Vertical: gov / news / acad
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"your search query","industry":"news"}'
```

### Step 3: Present results — verbatim `message` first, then analysis

After JSON returns:

#### Part A — Result list [MANDATORY]

**Output the `message` field exactly as returned.** It usually contains up to **five** top hits, each formatted like:

```
**n. [Title](url)** — Site (date) ⭐
   Snippet...
```

> **CRITICAL:** Never skip the list and jump to a summary. Titles are already Markdown links; users must be able to click through.

#### Part B — Analysis [OPTIONAL, after Part A]

**Language for your added commentary:** align with the **user’s conversation language** and the **query language** when helpful:
- English query → English analysis (typical for EN users).
- Non-English query → match the user’s language for the follow-up.
- The `message` block is always copied **verbatim**, regardless of language.

#### Good pattern

```
API returns a long `message` string with numbered results and snippets.

Assistant output:

<paste entire message verbatim>

---

Brief synthesis: … (optional, grounded in what appeared above)
```

#### Forbidden

- Skipping the result list and answering from memory.
- Rebuilding the list from `data.docs` instead of using `message`.
- Editing URLs or titles inside `message`.
- Claiming sources that are not in `message`.
- Stripping Markdown links from titles.

---

## PORT

Use **`AUTH_GATEWAY_PORT`** from the environment (set by the Electron host when the Auth Gateway starts). Child processes inherit it.

**macOS / Linux (bash):**

```bash
PORT=${AUTH_GATEWAY_PORT:-19000}
echo "[Assistant] AUTH_GATEWAY_PORT: $PORT"
```

**Windows (PowerShell):**

```powershell
$PORT = if ($env:AUTH_GATEWAY_PORT) { $env:AUTH_GATEWAY_PORT } else { "19000" }
Write-Host "[Assistant] AUTH_GATEWAY_PORT: $PORT"
```

**Windows (CMD):**

```cmd
if not defined AUTH_GATEWAY_PORT set AUTH_GATEWAY_PORT=19000
set PORT=%AUTH_GATEWAY_PORT%
echo [Assistant] AUTH_GATEWAY_PORT: %PORT%
```

Default if unset: **`19000`**.

## Parent PID (logging)

Before `curl`, you may log the parent PID for tracing.

**macOS / Linux:**

```bash
PPID_VAL=$(python3 -c "import os; print(os.getppid())")
echo "[Assistant] Parent PID: $PPID_VAL"
```

**Windows (PowerShell):**

```powershell
$PPID_VAL = python -c "import os; print(os.getppid())"
Write-Host "[Assistant] Parent PID: $PPID_VAL"
```

---

## Command: `search`

```
POST /proxy/prosearch/search
Content-Type: application/json

{
  "keyword": "<search-query>",       // required, UTF-8
  "mode": 0,                         // optional: 0=web 1=VR card 2=hybrid
  "cnt": 10,                         // optional: 10/20/30/40/50
  "site": "<domain>",              // optional: site-restricted
  "from_time": 1710000000,           // optional: start (epoch seconds)
  "to_time": 1711000000,             // optional: end (epoch seconds)
  "industry": "news"                 // optional: gov | news | acad
}
```

**Fields:**
- **`keyword`** (required): query string.
- **`mode`**: `0` default web results; `1` VR “card” style facts (e.g. weather, spot prices); `2` hybrid.
- **`cnt`**: max hits; **mutually exclusive** with `site` and `from_time`/`to_time` per backend rules.
- **`site`**: restrict to a domain.
- **`from_time` / `to_time`**: time window in epoch seconds.
- **`industry`**: `gov` (government), `news`, `acad` (academic-oriented).

> Do **not** combine `cnt` with time filters or `site` when the API forbids it.

**Examples:**

```bash
PORT=${AUTH_GATEWAY_PORT:-19000}
echo "[Assistant] AUTH_GATEWAY_PORT: $PORT"
PPID_VAL=$(python3 -c "import os; print(os.getppid())")
echo "[Assistant] Parent PID: $PPID_VAL"

# Basic
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"latest AI news"}'

# More results (no time/site)
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"React 19 features","cnt":20}'

# News vertical
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"Federal Reserve statement March 2026","industry":"news"}'

# GitHub-only
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"electron vite template","site":"github.com"}'

# Hybrid mode for structured + web (e.g. commodity spot, weather) — adjust keyword to your locale
curl -s -X POST http://localhost:$PORT/proxy/prosearch/search \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"gold spot price today","mode":2}'
```

**Success JSON (shape):**

```json
{
  "success": true,
  "message": "Search results for \"latest AI news\"…\n\n**1. [Title](https://…)** — Source (2026-03-15) ⭐\n   Snippet…",
  "data": {
    "query": "latest AI news",
    "totalResults": 10,
    "docs": [
      {
        "passage": "…",
        "score": 0.85,
        "date": "2026-03-15",
        "title": "…",
        "url": "https://…",
        "site": "…",
        "images": []
      }
    ],
    "requestId": "…"
  }
}
```

> **`message` is the source of truth for what to show users** — copy it in full before adding commentary.

**Failure JSON (examples; actual strings may be localized by the host):**

```json
{
  "success": false,
  "message": "Not signed in. Web search requires an active session. Please sign in and try again."
}
```

```json
{
  "success": false,
  "message": "Search timed out (15s). Please try again."
}
```

---

## Error handling

Responses are JSON on stdout. Errors use `{"success": false, "message": "..."}`.

| Situation | What to do |
|-----------|------------|
| Not authenticated (`message` indicates login required) | Tell the user to **sign in**, then retry. |
| Timeout | Retry **once**; if it fails again, relay the error. |
| Empty docs but `success: true` | Still output `message`; it usually explains there were no hits. |
| Network / connection | Retry once after ~3s; else show `message`. |
| HTTP errors | Surface `message` from the API when present. |

---

## Prohibited behavior

- Rebuilding the hit list from `data.docs` instead of echoing `message`.
- Skipping results and answering from the model alone.
- Altering URLs/titles inside `message`.
- Inventing hits or URLs not present in `message`.
- Leaking internal gateway URLs or secrets to the user.
- Searching when the question is fully answerable without live data.
- Running more than **two** searches for the same user turn without a strong reason.

---

## Important notes

- If you already know the answer with high confidence and no freshness need, **do not search**.
- Prefer **short, precise** keywords over pasting the whole user message.
- For **time-sensitive** asks (“latest”, “today”, “this week”), **use `from_time`** as in Step 1.5.
- If the first query is weak, **one** rephrase is enough; avoid search spam.
- Treat links as **untrusted**; remind users to verify critical facts at the source.
- For weather, spot metals, FX, etc., consider **`mode: 2`** when supported.
- **`cnt` vs time/site:** respect mutual exclusion — see above.
- **Commentary language:** follow the user’s language; **`message`** stays verbatim.

