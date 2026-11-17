# Recall benchmark methodology

Use this workflow to compare retrieval before and after a memory migration. It
does not claim that migration improves recall.

A target-only query run is a **post-migration health check**, not a paired
benchmark. Label it that way unless the same frozen evaluation set was run
against the source before migration under a recorded, comparable identity.

## Evaluation set

Store the evaluation set outside every indexed workspace. Use JSONL with one
object per query:

```json
{"id":"q01","agent":"main","query":"synthetic query","expected_paths":["memory/example.md"],"k":5}
```

- Use stable, non-secret query IDs.
- Keep raw personal queries private.
- Do not put expected answers, reports, or query files inside indexed memory.
- Include exact, paraphrased, ambiguous, and source-specific probes.
- Freeze the set before collecting the source baseline.

## Environment identity

Record for both runs:

- OpenClaw and memory plugin versions;
- agent and source configuration;
- embedding provider, model, dimensions, and tokenizer;
- search mode, result limit, and score threshold;
- corpus file/chunk counts and dirty state.

Stop comparison if any identity field changes unexpectedly.

## Collection

For each query, run the installed OpenClaw memory search command with JSON
output against the source baseline and again after target indexing is complete.
Record only paths, ranks, scores, latency, and pass/fail evidence in a
shareable report. Keep snippets in a private report when they contain memory
text.

## Metrics

- `Hit@K`: expected evidence appears in the first K results.
- `MRR`: reciprocal rank of the first expected result.
- `nDCG@K`: optional when multiple results have graded relevance.
- latency: median and p95 over the frozen query set.

Report per-query outcomes and aggregate metrics. Never hide failed queries or
change relevance labels after seeing target results.

## Acceptance

Define acceptance before cutover. Recommended minimum:

- all critical source-specific probes pass;
- aggregate Hit@K does not regress beyond the approved tolerance;
- no agent or scope is absent;
- target index is complete and not dirty;
- any score/rank regression is reviewed against corpus duplication and
  candidate truncation.

Passing this benchmark is evidence for one run and one evaluation set, not a
general recall-improvement claim.

If the source baseline is missing, publish target Hit@K, MRR, and latency only
as health observations. Do not calculate a delta, claim non-regression, or
reconstruct the source query set from memory after cutover.
