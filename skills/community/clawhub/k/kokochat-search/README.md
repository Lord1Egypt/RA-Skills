# kokochat-search

OpenClaw-side wrapper for KokoChat's hosted search API. Shared across mini-apps:
Deeply uses it for research / outline / per-section lookups, and any future
mini-app (e.g. Koko's general assistant turn) can route the same way without
shipping a Brave / Tavily / Serper key on the user's machine.

The wrapper lives in `bin/search.mjs` and calls:

```text
POST https://deeply.plus/deeply/search
```

with:

```json
{ "query": "AI investor outlook 2026", "count": 5 }
```

The Brave API key is configured only on the `deeply.plus` server. User
OpenClaw installs this wrapper via `scripts/install-openclaw-support.mjs`
into whichever agent workspaces opt in (currently `deeply`; others can join
by editing the installer's SKILLS list).

Optional env for development / private deployments:

- `KOKO_SEARCH_API_BASE` (preferred) — override API base, e.g.
  `http://127.0.0.1:8788`.
- `KOKO_DEEPLY_SEARCH_BASE` — legacy alias kept for backwards compat.
- `KOKO_SEARCH_TOKEN` (preferred) or `KOKO_DEEPLY_SEARCH_TOKEN` — Bearer
  token if the hosted endpoint requires one.
