# Effective research with NotebookLM

Procedural knowledge for getting grounded, citation-backed answers at scale.
NotebookLM answers **only from the sources in a notebook** — it does not use open
web knowledge — so answers are hallucination-resistant and every claim can be
traced to a cited passage.

## Citation formats

Pick `source_format` on `/ask` by what the answer is for:

- `json` — machine-readable: each citation carries the source name + citation
  number + the exact cited passage. Use when the answer feeds another program,
  or when building a cache/vault.
- `expanded` — human-readable footnotes with the cited excerpts inline.
- `inline` / `footnotes` — lighter markers without full excerpts.
- `none` — answer text only.

Always prefer a format that keeps the **cited excerpts** when the answer will be
stored — those excerpts are what make a cached answer self-contained.

## The daily-quota reality (this is the main constraint)

Free Google accounts cap NotebookLM at ~**50 chat queries/day**. Two levers:

1. **Multi-account rotation** — the engine supports several Google accounts with
   auto-reauth; `/re-auth` switches accounts when a quota is hit.
2. **Ingest once, retrieve forever** — treat NotebookLM as a one-shot _ingestion_
   layer, not a live query backend for repeated questions (below).

## Batch → cache → offline retrieval (the scale pattern)

For literature reviews / SOTA surveys / any repeated querying, decouple
**ingestion** (NotebookLM, periodic, quota-bound) from **retrieval** (local,
unlimited, instant):

```
[Once per notebook, periodic]
  Generate an exhaustive question set
    → POST /batch-to-vault { questions, vault_dir, source_format: "json" }
      → one markdown file + JSON sidecar per answer (citations preserved)

[At will, unlimited, offline]
  Search the vault (e.g. with RTFM: FTS5 + semantic) → answer from cache
```

This removes both bottlenecks (quota, latency) for questions asked more than
once. The `nblm-answer-v1` sidecars are designed to be indexed by
[RTFM](https://github.com/roomi-fields/rtfm). Only re-run `/batch-to-vault` when
the sources change.

## Fresh vs. follow-up questions

- **Fresh question** (no `session_id`): fastest path, answered over NotebookLM's
  internal API. Use for independent questions.
- **Follow-up**: pass a stable `session_id` to keep conversational context across
  turns in the same notebook.

## Studio content

From a notebook's sources, generate: `audio` (podcast-style overview), `report`,
`video`, `infographic`, `presentation`, `data_table` (via `/content/generate`);
`flashcards` / `quiz` (via `/content/study-aid`); and an interactive `mind_map`
(via `/content/mind-map`). Audio/video/infographic can then be downloaded via
`/content/download`; text types are returned in the response.

## Source discovery

`/content/research` runs NotebookLM's web/Drive research (fast or deep) to find
candidate sources for a topic, and can import them into the notebook
(`import: true`).
