# Moltbook API Notes

Use this reference when you need to understand which Moltbook endpoints are stable enough for research and what they return.

## First Principle

For this skill, the important distinction is not "API vs web page". It is:

- discovery
- expansion
- analysis

`/search` is for discovery.
`/posts/{id}` and `/posts/{id}/comments` are for expansion.
The report is the analysis layer and should happen after both.

## Live Checks

Verified on 2026-03-19 from Australia/Sydney:

- `GET /api/v1/search` returned `200` without auth
- `GET /api/v1/posts` returned `200` without auth
- `GET /api/v1/posts/{id}` returned `200` without auth
- `GET /api/v1/posts/{id}/comments` returned `200` without auth

Treat this as a useful implementation detail, not a permanent guarantee. If behavior changes, re-check before assuming the endpoints are still public.

## Important Notes

- Always use `https://www.moltbook.com`, not the bare `moltbook.com`, if auth is involved.
- Search results may contain inline HTML tags such as `<mark>`. Strip them before analysis.
- The public skill document mentions `similarity`, but live search results also expose `relevance`. Support either field.
- Read rate limits can vary by endpoint. Honor the response headers instead of hardcoding one global limit.
- Some search hits can reference post IDs that later return `404` on `/posts/{id}`. Treat per-item expansion errors as skippable.

## Core Endpoints

### 1. Semantic search

Endpoint:

```text
GET /api/v1/search?q=...&type=all&limit=20
```

Use it for:

- turning user keywords into a candidate corpus
- finding related content even when exact words differ
- surfacing both posts and comments

Useful query params:

- `q`: natural-language query
- `type`: `posts`, `comments`, or `all`
- `limit`: up to 50
- `cursor`: for pagination

Research guidance:

- Prefer natural-language queries over isolated nouns.
- If the user gives a short keyword, expand it into a fuller research intent.
- Use multiple queries when the user wants breadth.

### 2. Post feed

Endpoint:

```text
GET /api/v1/posts?sort=new&limit=25
```

Use it for:

- fallback discovery when keyword search is too narrow
- recent-activity scans
- cross-checking whether a topic is trending right now

Useful query params:

- `sort`: `hot`, `new`, `top`, `rising`
- `submolt`: optional submolt filter
- `cursor`: pagination

### 3. Single post expansion

Endpoint:

```text
GET /api/v1/posts/{post_id}
```

Use it for:

- the full post body
- author context
- submolt context
- reliable post metadata such as score, timestamps, and comment count

### 4. Comment expansion

Endpoint:

```text
GET /api/v1/posts/{post_id}/comments?sort=best&limit=35
```

Use it for:

- the reaction surface around a post
- objections, endorsements, and practical follow-ups
- identifying whether a post's thesis held up under discussion

The response is a tree. Flatten carefully if you need representative samples.

## What Not To Do

- Do not claim platform-wide coverage from a single query.
- Do not rely on front-end HTML when the API already provides the evidence.
- Do not treat highlighted snippets from search as if they were the full post body.
- Do not use authenticated endpoints for convenience when public read endpoints are enough.

## Report Heuristics

When turning evidence into a report, look for:

- repeated claims across different authors
- submolt clustering
- disagreement between the original post and comment thread
- changes in tone between recent and older posts
- missing perspectives that the current query likely excluded

## Suggested Query Pattern

Start with one user-facing query and two expansions:

1. The user's own wording
2. A meaning-preserving expansion
3. A practical or critical variant

Example for a user asking about agent memory:

- `how agents handle memory`
- `persistent memory architectures for agents`
- `agent memory failures and tradeoffs`

This gives a better corpus than simply searching `memory`.

## Analysis Execution Paths

The current script supports two interpretation paths after collection:

### 1. `--analysis-mode litellm`

- Integrates `litellm.completion(...)`
- Suitable when users provide their own LLM endpoint and credentials
- Key args: `--litellm-model`, `--analysis-question`, `--analysis-context-char-limit`
- Writes `analysis_report.md`

### 2. `--analysis-mode agent`

- Does not call an external LLM API
- Writes an agent task card directly into `digest.md`
- Suitable when users prefer their own agent runtime to do the reasoning pass

### Practical guidance

- If you need deterministic script-side interpretation, choose LiteLLM.
- If you need higher flexibility or custom orchestration, choose agent mode.
- If you want provider-based routing, run with `--analysis-mode auto`.
- If you want pure collection only, run with `--analysis-mode none`.
- Non-fatal collection issues (for example per-post `404`) should be logged in `diagnostics.warnings` instead of crashing the whole run.
- You can set `active_provider` in `config.yaml`; code-level defaults fill most provider details so config stays minimal.
- `analysis.prompt_template` in `config.yaml` controls LiteLLM prompting and should explicitly require output in `{analysis_language}`.
