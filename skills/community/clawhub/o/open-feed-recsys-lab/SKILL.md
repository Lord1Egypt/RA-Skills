---
name: open-feed-recsys-lab
description: Review open feed recommendation repositories with source-backed evidence, artifact-readiness checks, and cautious architecture summaries. Use when a user asks for a grounded read of xai-org/x-algorithm, Phoenix, Home Mixer, Thunder, Grox, candidate pipelines, ads blending, or public recommender-system claims.
---

# Open Feed Recsys Lab

Use this skill to review public feed recommendation repositories and separate what the source supports from what remains unproven.

Default target: `https://github.com/xai-org/x-algorithm`.

## Review Workflow

1. Confirm the target repository, commit, public link, or user-provided file set.
2. Build an evidence ledger with repository/ref, files inspected, supported claims, weak claims, and open questions.
3. Separate source inspection from runnable-model proof. If Phoenix artifacts are missing, say execution is not verified.
4. Map the visible architecture: Home Mixer, Phoenix retrieval/ranking, Thunder, Grox, ads blending, and candidate pipelines when present.
5. Treat public algorithm claims as hypotheses. Mark each claim `supported`, `partly_supported`, `unsupported`, or `not_public_repo`.
6. Frame shareable output around reproducibility and evidence. Do not present the public source as a reach predictor or full live-platform clone.

## Phoenix Artifact Readiness

Only treat Phoenix execution as verified after the official artifacts are present and the user has supplied a local run result. The expected extracted directory is:

```text
phoenix/artifacts/oss-phoenix-artifacts/
```

Expected files include:

- `retrieval/model_params.npz`
- `retrieval/embedding_tables.npz`
- `retrieval/config.json`
- `ranker/model_params.npz`
- `ranker/embedding_tables.npz`
- `ranker/config.json`
- `sports_corpus.npz`
- `example_sequence.json`

If the report says Phoenix is not run-ready, state that source inspection succeeded but execution is blocked by missing extracted LFS artifacts.

## Boundaries

- Use public source or user-provided local files only.
- Do not request or inspect private user data, authenticated account pages, or non-public analytics.
- Do not promise reach, ranking, virality, revenue, or live-platform equivalence.
- Do not claim that public source contains every production weight, threshold, model version, or serving rule.
- Do not execute repository code or delete local files as part of a review unless the user separately asks for that engineering work.

## Output Shape

Return a concise review with:

- `Target`: repo, ref, and source date when known.
- `Supported`: claims backed by public source.
- `Blocked`: missing artifacts, missing configs, or live-platform gaps.
- `Architecture`: short component map.
- `Risks`: overclaims, ambiguous evidence, or unsafe product positioning.
- `Next check`: the smallest concrete verification step.

The preferred public-safe framing is:

```text
I verified the open X For You algorithm locally at commit <sha>; here is the report.
```

## Companion Skills

Use `x-algo-claim-auditor` when the user asks whether a public claim, screenshot text, or viral thread is supported by the source.

Use `tinytroupe-feed-research-lab` when the user asks to compare draft posts, simulate audience reactions, or pretest a post before publishing. Keep that work labeled as synthetic audience research, not source verification or reach prediction.
