# Painpoint To PRD Contracts

This file is the runtime contract for discovery, persistence, and PRD generation.

Runtime note:

- `scripts/` is not part of the runtime interface.
- The supported interface is `npm run tidb -- <command>`.

## Scoring Rubric

Score each opportunity from `0-100`:

- `recurrence` (`0-25`)
- `severity_and_urgency` (`0-20`)
- `workaround_burden` (`0-20`)
- `buying_or_switching_signal` (`0-15`)
- `evidence_quality_and_freshness` (`0-20`)

Confidence is separate:

- `High`
- `Medium`
- `Low`

Use `insufficient evidence` when ranking is too weak to support confidence.

## Payloads

### `EvidenceRow`

Required fields:

- `source_url`
- `source_type`
- `author_handle`
- `community_or_site`
- `published_at`
- `snippet`
- `pain_cluster_id`
- `engagement_signals`
- `retrieval_timestamp`
- `traceability_status`

```json
{
  "source_url": "https://example.com/thread",
  "source_type": "reddit_comment",
  "author_handle": "user123",
  "community_or_site": "r/startups",
  "published_at": "2026-03-20T12:00:00Z",
  "snippet": "We still stitch three tools together.",
  "pain_cluster_id": "run_20260328_01:cluster_a",
  "engagement_signals": { "score": 18 },
  "retrieval_timestamp": "2026-03-28T13:00:00Z",
  "traceability_status": "verified"
}
```

### `WorkerEvidenceBundle`

Workers may return only this payload.

Required fields:

- `run_id`
- `worker_id`
- `query_scope`
- `evidence_rows`
- `notes`

```json
{
  "run_id": "run_20260328_01",
  "worker_id": "worker_reddit_a",
  "query_scope": { "source": "reddit", "query_family": "competitor complaints" },
  "evidence_rows": [
    {
      "source_url": "https://example.com/thread",
      "source_type": "reddit_post",
      "author_handle": "user123",
      "community_or_site": "r/legaltech",
      "published_at": "2026-03-20T12:00:00Z",
      "snippet": "The workflow is manual and hard to review.",
      "pain_cluster_id": "run_20260328_01:cluster_a",
      "engagement_signals": { "score": 41 },
      "retrieval_timestamp": "2026-03-28T13:00:00Z",
      "traceability_status": "verified"
    }
  ],
  "notes": "No strong Hacker News threads found."
}
```

### `OpportunitySnapshot`

Required fields:

- `opportunity_id`
- `run_id`
- `rank`
- `title`
- `affected_user`
- `job_to_be_done`
- `pain_statement`
- `score_total`
- `score_breakdown_json`
- `confidence`
- `confidence_reason`
- `pain_cluster_key`
- `supporting_evidence_json`
- `contradictions_json`
- `query_scope_json`

```json
{
  "opportunity_id": "opp_20260328_01",
  "run_id": "run_20260328_01",
  "rank": 1,
  "title": "Review-safe drafting workflow",
  "affected_user": "In-house IP counsel",
  "job_to_be_done": "Draft and review faster without adding risk",
  "pain_statement": "Manual stitching creates slow review loops.",
  "score_total": 83,
  "score_breakdown_json": { "recurrence": 21, "severity_and_urgency": 18 },
  "confidence": "High",
  "confidence_reason": "Repeated recent complaints with concrete workflow detail.",
  "pain_cluster_key": "run_20260328_01:cluster_a",
  "supporting_evidence_json": [{ "source_url": "https://example.com/thread" }],
  "contradictions_json": [{ "note": "Lower pain at low volume" }],
  "query_scope_json": { "sources": ["reddit"], "date_range_days": 365 }
}
```

### `PrdRecord`

Required fields:

- `prd_id`
- `run_id`
- `opportunity_id`
- `title`
- `status`
- `target_user`
- `goal`
- `structured_prd_json`
- `markdown_snapshot`
- `source_evidence_json`

```json
{
  "prd_id": "prd_20260328_01",
  "run_id": "run_20260328_01",
  "opportunity_id": "opp_20260328_01",
  "title": "Review-safe drafting assistant",
  "status": "draft",
  "target_user": "In-house IP counsel",
  "goal": "Reduce manual drafting and review loops.",
  "structured_prd_json": { "problem": "Drafting is slow and brittle." },
  "markdown_snapshot": "# Lightweight PRD: Review-safe drafting assistant",
  "source_evidence_json": [{ "source_url": "https://example.com/thread" }]
}
```

## Command Interface

All commands accept JSON via stdin or `--input-file <path>`.

Success envelope:

```json
{ "ok": true, "command": "name", "result": {} }
```

Failure envelope:

```json
{ "ok": false, "error": "message" }
```

Preferred discovery flow:

1. collect evidence
2. `save-evidence-batch`
3. cluster and rank
4. `save-opportunity-batch`

Preferred commands:

- `save-evidence-batch`
- `save-opportunity-batch`
- `get-opportunity`
- `save-prd`
- `get-prd`
- `list-runs`

Compatibility/manual recovery commands:

- `save-evidence`
- `save-opportunity`

### `save-evidence`

Input: `EvidenceRow`

### `save-evidence-batch`

Input:

```json
{
  "run_id": "run_20260328_01",
  "evidence_rows": [{ "source_url": "https://example.com/thread", "source_type": "reddit_comment" }]
}
```

Result fields:

- `run_id`
- `saved_count`

### `save-opportunity`

Input: `OpportunitySnapshot`

### `save-opportunity-batch`

Input:

```json
{
  "run_id": "run_20260328_01",
  "opportunities": [{ "opportunity_id": "opp_20260328_01", "rank": 1 }]
}
```

Result fields:

- `run_id`
- `saved_count`

### `get-opportunity`

Input:

- `{"opportunity_id":"opp_20260328_01"}`
- `{"run_id":"run_20260328_01","rank":1}`

### `save-prd`

Input: `PrdRecord`

### `get-prd`

Input:

- `{"prd_id":"prd_20260328_01"}`
- `{"opportunity_id":"opp_20260328_01"}`
- `{"run_id":"run_20260328_01"}`
- `{"latest":true}`

### `list-runs`

Input: optional empty object

## PRD Rules

- Generate a PRD only from a persisted `OpportunitySnapshot`.
- Carry forward evidence and constraints instead of inventing scope.
- Optimize for a coding agent.
- Prefer a thin vertical slice.
- Include non-goals, constraints, and acceptance criteria.

## Output Rules

- Prefer repeated, concrete complaints over clever one-offs.
- Separate category pain from vendor-specific complaints.
- Preserve contradictions when evidence conflicts.
- Down-rank hype, memes, and unsupported wishlists.
- Keep evidence traceable through `source_url` and `pain_cluster_id`.
