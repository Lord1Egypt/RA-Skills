# Set up datasets and evaluations (steps 3–4)

All endpoints: base `https://api.noveum.ai/api`, header `Authorization: Bearer $NOVEUM_API_KEY`.
Prefer the MCP tools if connected (`getting-connected.md`) — they mirror these routes exactly.
Poll cadences and terminal statuses: `api-reference.md`.

## 3a. Create a dataset

```
POST /v1/datasets
{ "name": "<human name>", "dataset_type": "conversational",   // or "agent" | "g-eval" | "custom"
  "environment": "production", "project_id": "<project>" }
```
Note the returned `slug` — everything below is slug-addressed.

## 3b. Create an ETL job (traces → dataset items)

```
POST /v1/etl-jobs
{ "name": "...", "projectId": "<project>", "datasetSlug": "<slug>",
  "environment": "production", "isConfigurationDone": false }
```

The ETL job needs Python `mapperCode` that transforms traces into dataset items. Generate
it with the AI mapper:

```
POST /v1/etl-jobs/:id/novaeval/transformation-code-gen   { "traceIds": ["<5-10 representative trace ids>"] }
→ poll GET /v1/etl-jobs/:id/novaeval/:jobRunId  (2s, cap ~5min)
```

**Gotcha (will silently no-op if skipped):** the generated `outputCode` is NOT auto-applied.
Persist it explicitly:

```
POST /v1/etl-jobs/:id/versions   { "code": "<outputCode>", "source": "ai_generated" }
```

Optional sanity checks before the full run:
- `POST /v1/etl-jobs/run-mapper { "mapperCode": ..., "traceId": ... }` — smoke-test one trace
- `POST /v1/etl-jobs/:id/trace-filter-preview { "filterConfig": ..., "skipProcessed": true }` — count what will be processed

## 3c. Run the ETL

```
POST /v1/etl-jobs/:id/trigger
{ "filterConfig": { ... }  // or "traceIds": [...]; one of the two is required
, "skipProcessed": true }
→ poll GET /v1/etl-jobs/:id/runs   (3s while active)
```

Acceptance: run status `completed` and `datasetItemsCreated > 0`. Inspect a few items —
**per item**, full content: `GET /v1/datasets/:slug/items/:itemId`. Never QA content from
the list view: it truncates some long columns **silently, mid-string, with no marker**
(live-verified: `content`, `metadata`, `agent_response`, `system_prompt`,
`conversation_context` get cut; a truncated `metadata` is silently invalid JSON) — while
other fields (`input_text`, `output_text`, `expected_output`) come back full, so the list
view is not size-bounded either. For more than a handful of items, stream to disk:
`python scripts/fetch_to_file.py "/v1/datasets/<slug>/items?fullContent=true" --out /tmp/items.json`
(see `context-safety.md`). List envelope: `{success, items[], total, scorerIds[]}` with
items as flattened columns, not nested under `content`.

## 3d. Alternative: insert items directly (no ETL)

For hand-built or imported datasets (live-verified):

```
POST /v1/datasets/:slug/items
{ "items": [ { "item_type": "conversational",
    "content": { "input_text": "...", "output_text": "...", "expected_output": "...",
                 "system_prompt": "...", "agent_response": "...", "session_id": "...", "turn_id": 1 } } ] }
→ 201 { "success": true, "created": N }     // NO item ids returned — get them from
                                            // GET /v1/datasets/:slug/items/ids (ids only, cheap)
```

Items land in the `next_release` version but read back immediately (no publish needed for
evals). **Trap:** several rule-based scorers (e.g. `is_json`, `valid_links`) read their
`prediction` from `agent_response`/`content` — if you only set `output_text`, they return
**-1 ("cannot evaluate")**, which flows into avg/min/max while `errorCount` stays 0. Set
`agent_response` for direct-inserted items you intend to score.

## 4a. Pick scorers

Get recommendations, then map them to configs yourself (recommendations are advisory —
nothing auto-applies them):

```
POST /v1/eval-jobs/recommend-scorers   { "datasetSlug": "<slug>" }
→ poll GET /v1/eval-jobs/recommend-scorers/:jobId   (3s, cap ~5min)
→ results.scorers_recommended[]: { scorer_name, reasoning, confidence, priority }
```

Cross-reference names against the catalog to get `scorerId`/`scorerType` (live-verified:
name `is_json` → id `is_json_scorer`, type `format_validation`). The **premium
discriminator** is `config.evaluationType` on each catalog entry: `"rule-based"` = free,
`"llm-based"` = 1 credit/item — use it to compute the estimate and the min-5-premium rule.
The catalog is **large (~130 scorers, ~170 KB) — never fetch it inline**; stream it to
disk once and extract just the map:

```
python scripts/fetch_to_file.py "/v1/scorers" --out /tmp/scorers.json
python3 -c "import json;d=json.load(open('/tmp/scorers.json'));print('\n'.join(f\"{s['name']}\t{s['id']}\t{s['type']}\t{s.get('config',{}).get('evaluationType')}\" for s in (d if isinstance(d,list) else d.get('scorers',d.get('data',[])))))" | head -140
```

Present the recommended set + reasoning to the user before spending credits.

## 4b. Create and trigger the eval job

```
POST /v1/eval-jobs
{ "name": "...", "datasetId": "<id>", "datasetSlug": "<slug>",
  "datasetType": "conversational",             // must match how items were shaped
  "projectId": "<project>",
  "scorerConfigs": [ { "scorerId": "...", "scorerType": "...", "scorerName": "...",
                       "threshold": 0.7 } ],
  "isEnabled": true }

POST /v1/eval-jobs/:id/trigger
{ "skipEvaluated": true }        // add datasetItemIds or filterConfig to scope; neither = full dataset
→ the trigger response IS the run object — its `id` is the runId to poll
→ poll GET /v1/eval-jobs/:id/runs/:runId   (3s while active; status running → completed)
```

**Credits (state this before triggering):** LLM-judge ("premium") scorers cost
1 credit × items × premium-scorer-count; rule-based scorers are free. If any premium
scorers are used, at least 5 are required (`MIN_PREMIUM_SCORERS_REQUIRED` otherwise).
A 429 `CREDIT_QUOTA_EXCEEDED` means the org is out of credits — stop and tell the user.

## 4c. Read results

```
GET /v1/eval-jobs/:id/results?runId=<runId>
```
**Default to disk** — the body embeds per-item `results[]` with multi-paragraph judge
`reasoning` for every scorer; items × scorers beyond ~25 results is already too big
(and any premium eval has ≥5 scorers by the min-premium rule):
`python scripts/fetch_to_file.py "/v1/eval-jobs/<id>/results?runId=<runId>" --out /tmp/results.json`,
then summarize from the file (aggregates first; sample a few failing items' reasoning).
Inline is acceptable only for tiny smoke runs (a handful of items, rule-based scorers).

Body is a **bare array**, one entry per scorer:
`{ scorerId, scorerName, totalEvaluations, avgScore, minScore, maxScore, p75/p90/p95/p99Score,
passedCount, errorCount, results[] }` — per-item results are
`{ resultId, itemId, score, passed, executionTimeMs, reasoning, metadata }`
(live-verified; `sourceTraceId` is NOT returned for direct-inserted items; `metadata` is a
JSON-encoded string). **Score `-1` means could-not-evaluate**, and it flows into
avg/min/max while `errorCount` stays 0 — exclude -1 scores before summarizing. Report:
worst scorers, failure rate, 2-3 example failures with reasoning. Then proceed to
`diagnose-novapilot.md`.
