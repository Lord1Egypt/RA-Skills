---
name: kb-keyword-graph
description: >-
  Keyword-graph reader for a knowledge base. Trigger when the user wants to
  understand a KB — "what's in it / what does it cover / knowledge structure /
  topic distribution / main themes / how do these materials relate", or explicitly
  says keyword graph / knowledge graph / word cloud / 关键词图谱 / 知识结构 /
  主题分布. It pulls the KB's three-level keyword tree and interprets it four ways:
  ① structure (knowledge outline) ② graph (progressive interactive ring chart)
  ③ topics (topic distribution) ④ relate (how two keywords relate in the tree).
  Covers even when the user doesn't say "graph" (e.g. "what's in this library").
  Current backend: 2brain (locate a library by base_id). Read-only — it never
  ingests, builds, edits, or Q&A-chats a KB, and does not route to Feishu/Lark
  Wiki or cloud docs.
user-invocable: true
license: MIT
metadata:
  requires:
    bins: ["python3"]
  env:
    - TWOBRAIN_GRAPH_KEY
    - TWOBRAIN_BASE_ID
    - TWOBRAIN_API_BASE
---

# KB Keyword Graph

> 中文版见 [references/SKILL.zh.md](references/SKILL.zh.md) (Chinese version).

Wrap a knowledge base's "keyword graph" capability into a stably-triggerable,
**read-only** workflow. All four tasks share one **three-level keyword tree**
(`keywords_tree`) pulled from the backend; the four subcommands are just
different readings of the same data. Engine: `scripts/kw_graph.py` (python3
standard library only, no third-party deps). Current backend: **2brain**
(`keyword_api`).

## First use (install-and-go)

```bash
# Option A: private config file (recommended — token stays out of env & artifacts)
mkdir -p ~/.config/2brain-keyword-map
cat > ~/.config/2brain-keyword-map/config.json <<'JSON'
{ "token": "2B-your-graph-API-key", "base_id": 700 }
JSON
chmod 700 ~/.config/2brain-keyword-map && chmod 600 ~/.config/2brain-keyword-map/config.json

# Option B: environment variables (temporary / CI)
export TWOBRAIN_GRAPH_KEY="2B-..."      # 2brain "keyword graph" API key (Bearer)
export TWOBRAIN_BASE_ID=700             # integer base_id of the target library (--base-id overrides)
# Course/test env: export TWOBRAIN_API_BASE="https://test.2brain.ai/api"

# Self-check
python3 scripts/kw_graph.py fetch --base-id 700
```

The graph API key is generated on the 2brain platform and differs from the
upload/chat keys. The host must be able to reach `TWOBRAIN_API_BASE` (default
`https://test.2brain.ai/api`).

## Privacy & Data Flow (read-only · no personal data · no autonomy)

This is a **read-only** KB-interpretation skill with a very narrow capability and
data-flow surface:

**① Capabilities**: needs only `python3` (stdlib, no third-party deps). Reads/writes
only the cache dir `~/.local/state/2brain-keyword-map/` (stores the pulled keyword
tree); the skill directory itself is read-only. **No shell, no cron, no autonomous
or scheduled behavior** — it runs once, only when you ask.

**② Data sent externally (minimal)**: it sends only **one integer base_id** to the
fixed 2brain endpoint `<TWOBRAIN_API_BASE>/kbase/keywords/keyword_api` and receives
that library's keyword tree. **No personal data, document content, resume, or
conversation is sent** — base_id is just a library number. Beyond this single
2brain endpoint it contacts no third party (no scraper, no external LLM).

**③ Credential discipline**: the graph API key is read only from **where you
configure it** — env var `TWOBRAIN_GRAPH_KEY` or the private file
`~/.config/2brain-keyword-map/config.json` (0600 recommended). It **does not read
host credentials outside the skill directory** (never touches the OpenClaw auth
store). The key is sent only as an `Authorization: Bearer` header to the fixed
endpoint and is **never** written into HTML/JSON artifacts, logs, URLs, or the
conversation (the engine guarantees zero-token artifacts — grep-verifiable).

**④ Boundaries**: no ingest, no KB creation, no edits/deletes, no Q&A; never acts
on your behalf; the keywords/counts/percentages it reports come **only from the
API's real response** — if empty it says "insufficient material", never fabricates.

## Backends (pluggable)

"Getting the three-level keyword tree" is abstracted into a backend, selected by
`--backend` / env `KWGRAPH_BACKEND` / config `backend` (default `twobrain`). The
renderer and all four tasks operate on the normalized tree, so they behave
identically across backends.

| Backend | How it gets the tree | Config |
|---|---|---|
| `twobrain` (default) | 2brain native `keyword_api` — a ready-made tree | token + base_id (see First use) |
| `local` | **computes** the tree from a folder of `.txt/.md` docs (stdlib keyword extraction + co-occurrence hierarchy) — for AI Digest or any self-hosted corpus | `--corpus <dir>` or config `corpus_dir` |
| `elasticsearch` | ES `significant_text` aggregation over an index | `--es-url` + `--index` or config `es_url`/`index` |

Examples:
```bash
python3 scripts/kw_graph.py graph  --backend local --corpus ~/ai-digest/kb --html /tmp/g.html
python3 scripts/kw_graph.py topics --backend elasticsearch --es-url http://localhost:9200 --index market_news_rag
```

`local` / `elasticsearch` compute the tree themselves, so it reflects that corpus's
own keyword co-occurrence — not identical to 2brain's engine, but the same four
readings apply. Trees are cached by config fingerprint under
`~/.local/state/2brain-keyword-map/graphs/`.

## Task routing (decide intent → read the matching execution doc → run the subcommand)

| User intent signal | Task | Subcommand | Execution doc |
|---|---|---|---|
| "what's in this library / knowledge structure / what areas / how is it structured" | Structure | `structure` | [references/workflows.md](references/workflows.md#structure) |
| "keyword graph / knowledge graph / word cloud / draw me a graph" | Graph | `graph --html <path>` | [references/workflows.md](references/workflows.md#graph) |
| "what topics / topic distribution / which area has the most / what's the focus" | Topics | `topics` | [references/workflows.md](references/workflows.md#topics) |
| "how do X and Y relate / how are these two connected" | Relate | `relate --a X --b Y` | [references/workflows.md](references/workflows.md#relate) |
| login / 401 / connection failure / empty graph | Troubleshoot | — | [references/workflows.md](references/workflows.md#troubleshooting) |

When intent is vague (e.g. just "take a look at this library"): default to
`structure`, lay out the level-1 topics, then ask which area to go deeper on.
**Restate the task and target library to the user before executing.**

## Common constraints (all four tasks must follow)

**Locating the KB — never hard-code base_id**:
1. User gave an integer base_id → use it (`--base-id`).
2. User gave only a library name → the current backend works by base_id; if you
   don't know the id, ask the user for it (don't guess a number and probe).
3. User gave nothing → use the default base_id from config, and note in the output
   which library was used.

**Credential discipline (hard rule)**:
- The token is sent only as an `Authorization: Bearer` header to the fixed 2brain endpoint;
- **never** print the token to the conversation, write it into HTML/JSON artifacts, logs, or URL query;
- the engine guarantees artifacts contain no token; don't repeat the key when relaying results.

**Output discipline**:
- Every number (node counts, count, percentage, weight) **must come from
  `kw_graph.py` stdout** — never from memory or imagination.
- The graph shows **sibling-share percentages only** (a node's count share among its
  direct siblings), not raw count; each sibling group sums to 100%. This is **not**
  a whole-KB absolute share.
- Empty or near-empty graph/structure → say "this library has too little material to
  graph", don't improvise content.
- `relate` is based only on **co-occurrence at tree levels**; state explicitly it does
  not imply causation, semantic equivalence, or document-level provenance.

**Read-only boundaries (this skill does NOT)**:
- ingest, scrape, create, delete, or edit a KB;
- do 2brain Q&A (chat) — that's a separate capability;
- route to Feishu/Lark Wiki / cloud docs / local files — "knowledge base" here means
  a 2brain platform library.

**Cache & idempotency**: a fetched tree is cached to
`~/.local/state/2brain-keyword-map/graphs/<base_id>.json`. If the user asks about the
same library again shortly after, the cache serves it; use `--fresh` to re-pull the
latest (e.g. after new material was ingested).

## Input/output example (graph)

**Input** (user says to the agent):

> Show me the keyword graph of my job library (base 700)

**Run**:

```bash
python3 scripts/kw_graph.py graph --base-id 700 --html /tmp/kw-700.html
```

**Engine stdout** (relay from this; don't paste raw JSON at the user):

```json
{"ok": true, "task": "graph", "base_id": 700, "file_count": 256,
 "levels": {"l1": 10, "l2": 21, "l3": 45},
 "metric": "sibling_count_percentage", "html": "/tmp/kw-700.html"}
```

**What you tell the user (template)**:

> The keyword graph of library 700 (256 documents) is ready: 10 level-1 topics, 21
> level-2, 45 level-3. The heaviest level-1 topics are Research and Technical. The
> chart is at `/tmp/kw-700.html`; click a level-1 topic to expand level-2/3 in the
> same view. Percentages are sibling-share, not whole-KB share.

## Script inventory

| File | Responsibility |
|---|---|
| `scripts/kw_graph.py` | Engine: backend dispatch + credential resolution + cache + four subcommands (structure/topics/graph/relate) + ring-HTML renderer |
| `scripts/backends.py` | Pluggable KB backends: `local` (compute tree from a doc folder) + `elasticsearch` (significant_text); the `twobrain` path lives in kw_graph.py |

## Boundaries (restated)

- Read-only 2brain keyword graph; no writes, no Q&A, no KB creation.
- Numbers come only from engine output; never fabricate keywords or relations.
- The token never appears in any artifact or conversation.
