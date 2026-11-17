---
name: mindgraph
description: MindGraph diagrams from a topic plus diagram type (8 Thinking Maps, mind map, or concept map), or precise node text edits via PATCH.
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["MINDGRAPH_BASE_URL", "MINDGRAPH_ACCOUNT", "MINDGRAPH_TOKEN"]}}}
---

# MindGraph

MindGraph is an AI-assisted diagram platform. Use this skill with the configured base URL, account number (phone), and API token.

## What the user usually provides

**Typical request — two inputs:**

1. **Topic / subject** — the central idea or short instruction (maps to API field **`prompt`**).
2. **Diagram type** — which chart they want (maps to **`diagram_type`**).

For `POST /api/generate_graph`, **`prompt`** is always required except special dimension-only modes. Add **`diagram_type`** when the user names one of the chart types above; if they only give a topic and not a type, you may omit **`diagram_type`** so MindGraph can **auto-detect** a suitable type from the text.

**Advanced request — fix specific node text:**

If the user wants **exact labels** on certain nodes (not a full regeneration), use **`GET /api/diagrams/{id}`** to read **`spec`** and node IDs, then **`PATCH /api/diagrams/{id}/nodes`** with structured **`updates`** (`node_id`, `new_text`). Re-fetch the PNG after edits (see §3).

### Supported `diagram_type` values (MindGraph)

**Eight Thinking Maps** (use these strings in JSON):

| `diagram_type` | Typical use |
|----------------|-------------|
| `circle_map` | Brainstorm & associate around a center |
| `bubble_map` | Describe attributes of a topic |
| `double_bubble_map` | Compare & contrast two topics |
| `tree_map` | Classify & group |
| `brace_map` | Whole & parts |
| `flow_map` | Sequence & steps |
| `multi_flow_map` | Cause & effect |
| `bridge_map` | Analogies |

**Also supported:**

| `diagram_type` | Notes |
|----------------|--------|
| `mind_map` | Hierarchical mind map. Alias **`mindmap`** is normalized to **`mind_map`**. |
| `concept_map` | Concept maps (concepts + labeled links). Extra fields like **`concept_map_topic`**, **`concept_a`**, **`concept_b`** exist for focused modes — see OpenAPI / `GenerateRequest` when the user asks for relationship-only or similar. |

Other diagram features are optional; use them only when the user’s wording clearly requires that mode:

- **`fixed_dimension`** — tree / brace / bridge maps (preserve a classification, decomposition, or analogy pattern)
- **`dimension_only_mode`** — tree / brace maps only (dimension known, topic generated)

## Authentication (every request)

Set headers on all HTTP calls:

- `Authorization: Bearer {MINDGRAPH_TOKEN}` — token starts with `mgat_`
- `X-MG-Account: {MINDGRAPH_ACCOUNT}` — same phone number as the MindGraph account (no spaces); **required** with `mgat_` (auth fails without a matching account)
- `X-MG-Client: openclaw` — **recommended** on every request for attribution (not required for auth). Missing → server treats client as `unspecified`. Matches Chrome extension `chrome-extension`; `[TokenAudit]` / `client_source` use this label
- `X-Request-Id` — optional; **recommended on long calls** (especially web-content PNG). Use a fresh UUID per request. On the web-content PNG path it appears in `[TokenAudit]` and LLM metadata (`http_request_id`); general `mgat_` TokenAudit logs client/path only

Never print or log the token or account in assistant-visible output.

**Use current env on every request.** Substitute `MINDGRAPH_BASE_URL`, `MINDGRAPH_ACCOUNT`, and `MINDGRAPH_TOKEN` from the skill environment each time you build a URL or headers. Do not reuse token or account values from earlier messages if the user said they updated credentials—use the latest configured values.

## Updating auth (works immediately on the server)

- **MindGraph API** checks the Bearer token and `X-MG-Account` on **every** request. There is no sync delay: after the user generates or regenerates a token in the app, that token is valid on the **next** HTTP call with matching headers. Regenerating revokes the previous token immediately.
- **OpenClaw / WorkBuddy host** may inject `env` only when the app starts or when the skill reloads. If the user changed `MINDGRAPH_*` in config but requests still behave like the old credentials, they should **save** the config and **restart** the client (or use the host’s reload/restart skill action if it has one). After the new env is loaded, requests use the new values immediately—no extra step on MindGraph’s side.

## Setup

1. Log into MindGraph in the browser.
2. Open **账户信息** → **API Token** → **生成 Token**.
3. Copy the token once; set `MINDGRAPH_TOKEN` and `MINDGRAPH_ACCOUNT` (phone) and `MINDGRAPH_BASE_URL` (default test deployment: `https://test.mindspringedu.com`; override for your own host) in OpenClaw skill env.
4. Tokens expire after 90 days; regenerate from the same UI.

## 1. Generate diagram spec

`POST {MINDGRAPH_BASE_URL}/api/generate_graph`

JSON body (minimal — topic + type):

```json
{
  "prompt": "Photosynthesis",
  "diagram_type": "mind_map",
  "language": "en",
  "llm": "qwen"
}
```

- **`prompt`** — user’s **topic** or instruction (required except special dimension-only modes; see `GenerateRequest` in the app).
- **`diagram_type`** — one of the **Thinking Maps**, **`mind_map`**, or **`concept_map`** (see tables above). Optional for auto-detection.
- **`language`** / **`llm`** — match user preference and host defaults when relevant.

Response JSON includes **`success`**, **`spec`** (diagram JSON), **`diagram_type`**, and optional **`error`**. Prefer checking **`success`** before saving.

## 2. Save diagram

`POST {MINDGRAPH_BASE_URL}/api/diagrams`

```json
{
  "title": "My diagram",
  "diagram_type": "mind_map",
  "spec": { }
}
```

Use the `spec` from step 1. Response includes `id` (diagram id string).

## 3. Push diagram image to the user

After create or any edit:

`GET {MINDGRAPH_BASE_URL}/api/diagrams/{id}/png`

Use the same auth headers as every other call (**Authorization** + **X-MG-Account**; `mgat_` requires both). Omitting them returns **401** (`JWT token required for this endpoint`).

Response JSON:

- **`url`** — Signed, time-limited link to a PNG under **`/api/temp_images/`**. The **path** ends with **`.png`** (e.g. `.../temp_images/diagram_<uuid>.png?sig=...&exp=...`); the **`?sig=` / `&exp=`** part is required for access, not optional decoration.
- **`filename`** — Suggested filename (always **`diagram_<hex>.png`**) for downloads or the image tool.

Pass **`url`** to the **image** tool so the user sees the current canvas. Fetching **`url`** does **not** send Bearer tokens (signature is in the query string). The **`GET /api/temp_images/...`** response includes `Content-Disposition` with a **`.png`** filename for browser downloads.

## 4. Read diagram (before edits)

`GET {MINDGRAPH_BASE_URL}/api/diagrams/{id}`

Use the returned `spec` and node IDs before patching.

## 5. Patch nodes (optional)

`PATCH {MINDGRAPH_BASE_URL}/api/diagrams/{id}/nodes`

Use this when the user has **specific edits** (wording on named nodes) rather than regenerating from a topic alone.

Either full replace:

```json
{ "spec": { } }
```

Or structured updates (preferred for targeted label changes):

```json
{ "action": "update", "updates": [{ "node_id": "branch_0", "new_text": "New label" }] }
```

Actions: `update`, `add`, `delete` (see API error messages for required fields). **`add`** appends a new child under the diagram root (server assigns the id); there is no parent-targeting field. **Always** `GET` the diagram first (§4) when **`node_id`** values are unknown. Then call step 3 again for a fresh image.

## 6. Inline recommendations

These routes live **without** the `/api` prefix (root of `MINDGRAPH_BASE_URL`):

- `POST {MINDGRAPH_BASE_URL}/thinking_mode/inline_recommendations/start`
- `POST {MINDGRAPH_BASE_URL}/thinking_mode/inline_recommendations/next_batch`
- `POST {MINDGRAPH_BASE_URL}/thinking_mode/inline_recommendations/cleanup`

**Response type:** `start` and `next_batch` return **`text/event-stream` (SSE)**, not a single JSON body. The stream emits `data: {...}` lines. Parse JSON after each `data:` prefix; handle events such as `recommendation_generated` (includes recommendation text) and `error`.

Request bodies must match the server schema (e.g. `session_id`, `diagram_type`, `stage`, `node_id`, `nodes`, `language`, `count` — see the app’s OpenAPI or `InlineRecommendationsStartRequest` / `InlineRecommendationsNextRequest`).

Workflow: `start` (SSE) → optional `next_batch` (SSE) for more items → `cleanup` (JSON) with `node_ids`. Present suggestions to the user; apply the chosen item via PATCH (step 5) and push image (step 3).

If the HTTP client cannot read SSE, inline recommendations may not be usable from that environment — prefer the browser UI for that flow.

## 7. Web page → mind map PNG (API / Chrome extension)

Mind map **only** from extracted page text (same auth headers as above).

**JSON spec only**

`POST {MINDGRAPH_BASE_URL}/api/generate_from_web_content`

```json
{
  "page_content": "plain or markdown text",
  "content_format": "text/plain",
  "page_title": "Optional title",
  "page_url": "https://...",
  "language": "zh"
}
```

`content_format` is `text/plain` or `text/markdown`. `page_content` max length **32000** characters. Returns **JSON** with the generated spec (LLM only; faster than the PNG route).

**Single-step PNG download**

`POST {MINDGRAPH_BASE_URL}/api/web_content_mindmap_png`

Same JSON body as above, plus optional `width` and `height` (viewport size for PNG capture; defaults **1200×800** if omitted). Response: **`image/png`** body (**not** JSON). Default `Content-Disposition` filename is **`mindgraph-web-content.png`**; when the server also saves the diagram, it may send **`X-MG-Diagram-Id`** and rename the file to **`mindgraph-{diagram_id}.png`**. On error, the server may return **JSON** with `detail` (HTTP 4xx/5xx). **Do not** call `response.json()` on success—read bytes.

Both web-content routes require the account’s **chrome_extension** school-tier feature (same gate family as API tokens). Trial / lite orgs that lack that feature get **403**.

**Timeouts (critical for OpenClaw / any HTTP client)**  
The PNG path runs **LLM generation** plus **Playwright screenshot** of the export page. End-to-end latency often exceeds **60 seconds**. Use a **client read timeout of at least 180 seconds (3 minutes)** on this request (the Chrome extension uses the same). Shorter timeouts produce misleading “network” failures. The JSON-only route (`generate_from_web_content`) is also LLM-bound; allow **several minutes** if your stack defaults to 30–60s.

**Chrome extension (same API)**  
The repo ships **`chrome-extension/`** (Load unpacked in `chrome://extensions`). It captures the active tab via a **short** message to the service worker, then runs **`fetch` + download in the popup** so the MV3 worker is not held across a long request. **Base URL** in settings must be the **API origin** (e.g. `https://your-host.example.com`), same as `MINDGRAPH_BASE_URL` here—not the SPA path `/mindgraph` alone.

## 8. Also useful (optional shortcuts)

Same auth headers as above. Use when the default generate → save → PNG flow is heavier than needed:

| Method | Path | When |
|--------|------|------|
| `GET` | `/api/diagrams` | List the user’s diagrams (paginated) before editing an existing one |
| `POST` | `/api/generate_png` | Prompt → PNG bytes in one call (skip explicit save) |
| `POST` | `/api/export_png` | Existing spec → PNG bytes |
| `POST` | `/api/generate_dingtalk` | Prompt → markdown-friendly image URL (DingTalk / similar bots) |

Rate limits apply (e.g. diagram PNG URL around **20/min**; many generate routes around **100/min**). On **429**, back off and retry.

## Best practices

- Always send **Authorization** + **X-MG-Account** on every `mgat_` call, using **current** `MINDGRAPH_*` env values (see **Authentication** and **Updating auth** above).
- Prefer **`X-MG-Client: openclaw`** on every call; add **`X-Request-Id`** especially on long web-content PNG calls.
- Default flow: map the user’s **topic** → **`prompt`** and their **chart choice** → **`diagram_type`** from the eight Thinking Maps plus **`mind_map`** / **`concept_map`** as needed.
- Use **long HTTP timeouts** for **`web_content_mindmap_png`** and other heavy routes (see §7).
- After **any** mutation, fetch the PNG URL (step 3) before replying.
- Prefer reading the diagram (step 4) before PATCH when IDs are unknown.
- Warn the user before token expiry when relevant (tokens last **90 days**).
- If auth fails after the user updated env in WorkBuddy/OpenClaw, suggest saving config and restarting the host app so new variables are picked up; then retry.
- On **403** for web-content or token minting, the school tier may lack `api_token` / `chrome_extension` (trial / lite).
