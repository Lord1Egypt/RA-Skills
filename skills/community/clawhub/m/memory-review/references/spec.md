# Memory Review Specification

## Contents

1. Purpose and authority
2. Scan state
3. Durable-signal filter
4. Existing-document resolution
5. Decision actions
6. Conflict and rewrite policy
7. Decision-plan schema
8. Write and verification sequence
9. Reports
10. Examples and boundaries

## 1. Purpose and authority

Memory review compresses operational history into durable, searchable current knowledge. It is not an archive copier.

Use this authority order when sources disagree:

1. Explicit current owner decision or verified current system state
2. Canonical knowledge, project, people, glossary, and post-mortem files
3. `MEMORY.md` hot cache
4. Daily logs and generated review reports

Daily logs describe what was believed at the time and may be incomplete or wrong. A newer daily entry does not automatically replace a verified canonical conclusion.

### Automatic write boundary

Allowed automatic targets:

- `memory/knowledge/**/*.md`
- `memory/projects/**/*.md`
- `memory/glossary.md`
- `memory/post-mortems.md`

Protected by default:

- `AGENTS.md`, `MEMORY.md`, `TOOLS.md`
- `USER.md`, `SOUL.md`, `IDENTITY.md`, `ENVIRONMENT.md`
- credentials, configuration secrets, and external workspaces

For protected files, report a proposed change and its evidence. Edit only when the current request explicitly authorizes it.

## 2. Scan state

Use `scripts/memory_review.py scan`; do not reimplement date and hash logic in the prompt.

State v2 stores a SHA-256 per pure daily log. This fixes three weaknesses of the legacy `{date, md5}` cursor:

- a changed older daily log is detected;
- multiple new or changed logs can be reviewed in one run;
- review reports are never mistaken for source diaries.

The scanner migrates safely from the newest legacy `lastScanned` block. On first use without any state, it scans the newest five pure daily logs and baselines older files.

Commit state only after canonical writes, report generation, and verification all succeed. `commit-state` rejects a stale plan if a source changed after scanning.

## 3. Durable-signal filter

Keep a signal only when it is likely to matter beyond the current day.

Good candidates:

- an explicit decision with rationale and scope;
- a verified reusable technique or failure mode;
- a stable interface, path, schema, or environment fact;
- a project or entity state that future work must know;
- a repeated pattern supported by multiple occurrences;
- a post-mortem lesson with cause, impact, and prevention.

Usually skip or defer:

- routine cron, backup, build, and commit results;
- temporary health, quota, latency, and queue status;
- unresolved hypotheses or planned work;
- raw benchmark samples already stored in their source repository;
- duplicate retellings of a known conclusion;
- secrets or recovery material contents.

Prefer `defer` when evidence is promising but not yet stable. Prefer `skip_duplicate` when the canonical document already says the same thing.

## 4. Existing-document resolution

Perform resolution between signal extraction and any write.

### Search order

1. Follow explicit paths and cross-references in the daily log.
2. Search filenames, H1 titles, headings, aliases, and distinctive terms with `rg`.
3. Use `memory_search` for semantic matches when available.
4. Search the full allowed target set:
   - `memory/knowledge/`
   - `memory/glossary.md`
   - `memory/projects/`
   - `memory/post-mortems.md`
5. Use `memory_review.py candidates` as a deterministic lexical fallback or audit trail.

### Candidate assessment

For each plausible document, check:

- same subject or entity;
- same operational question;
- compatible scope and audience;
- whether the new signal revises, extends, or merely repeats it;
- whether another file is already more canonical;
- whether merging would make the document clearer or less coherent.

Record candidates checked and the decision reason. Filename similarity alone is not sufficient.

### Canonical selection

Choose one canonical target when possible. Prefer the document that:

- already owns the topic's current conclusion;
- has the clearest and broadest applicable scope;
- is referenced by current files;
- can absorb the new evidence without becoming a grab bag.

If two existing documents materially overlap and neither is clearly canonical, do not create another file. Use `review_merge` and identify both candidates.

## 5. Decision actions

Every signal receives exactly one action.

### `update_existing`

Use when an existing canonical document can absorb the signal. Preserve useful structure, revise stale conclusions in place, and add only evidence or guidance that improves future use.

### `create_new`

Use only when:

- no suitable document exists after a recorded search;
- the topic has a clearly independent boundary; or
- an intentional split is needed because an existing document combines distinct responsibilities.

New knowledge filenames must be topic-based and date-free.

### `skip_duplicate`

Use when the canonical document already contains the same durable meaning. Do not edit merely to record that the event happened again unless repetition itself changes confidence or policy.

### `review_merge`

Use when two or more existing documents overlap or conflict enough to require consolidation. Report the recommended canonical target and migration plan. Do not silently merge large documents during a routine cron run.

### `defer`

Use for unstable, unverified, sensitive, or owner-decision-dependent signals. State what evidence or decision would unblock it.

## 6. Conflict and rewrite policy

Do not append contradictions chronologically and leave the reader to decide.

When verified new evidence supersedes an old conclusion:

1. rewrite the current conclusion;
2. retain short historical context only when it explains a migration or pitfall;
3. update affected cross-references;
4. cite the newer evidence path in the decision plan/report.

When authority is unclear, keep the canonical document unchanged and use `defer` or `review_merge`.

## 7. Decision-plan schema

Write a JSON plan before editing. The helper validates paths and action requirements.

```json
{
  "schema_version": 2,
  "source_files": [
    "memory/daily/2026-07/2026-07-30.md"
  ],
  "decisions": [
    {
      "signal": "Codex Hosted Search is the default quality-search route",
      "action": "update_existing",
      "destination": "memory/knowledge/fw-web-search-quality-routing.md",
      "source_refs": [
        "memory/daily/2026-07/2026-07-30.md"
      ],
      "candidates_checked": [
        "memory/knowledge/fw-web-search-quality-routing.md",
        "memory/knowledge/codex-cli-usage.md"
      ],
      "searches_performed": [
        "rg: web search quality routing",
        "memory_search: Codex Hosted Search default route"
      ],
      "reason": "The first document already owns search-routing policy."
    }
  ]
}
```

Required fields for all decisions: `signal`, `action`, `source_refs`, `reason`.

Additional rules:

- `update_existing`: `destination` must exist.
- `create_new`: `destination` must not exist; `searches_performed` must be non-empty. `candidates_checked` may be empty when the search found nothing.
- `skip_duplicate`: identify the existing destination when known.
- `review_merge`: list at least two `candidates_checked` paths.
- `defer`: explain the missing evidence or authority.

## 8. Write and verification sequence

1. Generate scan and decision plans.
2. Validate the decision plan.
3. Apply only allowed automatic writes.
4. Run `git diff --check` and inspect the full relevant diff.
5. Search for stale filenames and conflicting current conclusions.
6. Re-run candidate search for every new document; confirm the boundary still holds.
7. Re-run `scan` before committing state. If a source changed, restart review.
8. Write report and execution log atomically.
9. Run the same scan again after `commit-state`; `changed_sources` must be empty.

Idempotence means unchanged source inputs cause no canonical-memory diff. It does not require suppressing a caller-requested report, but a no-change report must say that nothing was rewritten.

## 9. Reports

Write:

- `memory/daily/YYYY-MM/YYYY-MM-DD-memory-review.md`
- `data/exec-logs/memory-review/YYYY-MM-DD.md`

Use these sections:

```markdown
## Updated

| Signal | Canonical document | Reason |

## Created

| Signal | New document | Why no existing document fit |

## Skipped duplicates

| Signal | Existing document | Reason |

## Merge review

| Signal | Candidates | Recommendation |

## Deferred

| Signal | Missing evidence or decision |

## Scan state

- Source files reviewed
- Changed / unchanged counts
- State commit result
```

Do not claim `created`, `updated`, or `merged` unless the filesystem diff proves it.

## 10. Examples and boundaries

### Repeated topic on consecutive days

Day 1 records that provider-registry loading should be lazy. No existing document fits, so review creates `memory/knowledge/fw-provider-registry-lazy-loading.md`.

Day 2 adds a verified timeout case for the same registry. Resolution finds the Day 1 document. The action is `update_existing`; add the failure condition and verification, then report one update and zero creations. A near-synonym such as `fw-provider-registry-timeout.md` would be a duplicate.

### Legitimate new boundary

An existing `fw-provider-registry-lazy-loading.md` explains when runtime providers are initialized. A later signal defines credential-rotation policy, audit requirements, and rollback. Although both mention providers, they answer different operational questions and have different readers. After checking candidates, `create_new` for `fw-provider-credential-rotation.md` is appropriate.

### Existing overlap

Two documents both describe Feishu cross-app identity resolution, and a new log adds another mapping example. Use `review_merge`; do not create a third identity document. A routine review may update neither until the canonical destination is chosen.

### Unverified incident

A daily log suspects compaction causes media reply loss but the reproduction is incomplete. Use `defer`; keep the hypothesis in the issue/daily log until verified.
