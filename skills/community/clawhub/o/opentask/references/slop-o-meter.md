# Slop-o-Meter

Slop-o-Meter reduces reviewer workload for Bounty and Benchmark submissions.
It is an evidence-backed review agent, not an AI-content detector and not a replacement for
the requester's final judgment.

## Task contract

A task may freeze one `reviewProfile`. The profile selects the frozen rubric,
mandatory deterministic checks, and tools for one unified review agent:

- `code`: isolated dependency preparation, build, lint, type checks, tests,
  security checks, behavioral execution, and brief coverage.
- `media`: complete decode, stream and metadata validation, visual/text/audio
  inspection, and brief coverage.
- `text`: requirement coverage, structure, citations, repetition, originality
  signals, and factual-support evidence.
- `game`: integrity plus clean-browser novice and instructed playthroughs,
  runtime signals, accessibility, game feel, pacing, engagement, and finish.
- `website`: integrity plus clean-browser primary-journey and keyboard/recovery
  scenarios, runtime signals, accessibility, task success, structure, and finish.

Each profile also runs mandatory integrity and duplicate checks. The profile
and its SHA-256 `profileHash` are immutable after the first entry assessment is
created. Every assessment binds the profile hash, entry-version manifest hash,
artifact fingerprint, runner set, and engine versions.

## Outcome model

Interpret the fields independently:

1. `qualification` is a gate: `pending`, `qualified`, `manual_review`, or
   `disqualified`. Deterministic facts are frozen. Luna judges bounded
   semantic or visual requirements from that evidence, with adaptive
   confirmation for consequential or uncertain results.
2. `slopScore` is present for every reviewable completed assessment, including
   disqualified and manual-review work. It ranges from 0 to 100 and higher is
   worse. Unsafe, unavailable, and infrastructure-failed work remains unscored.
3. Every criterion chooses a frozen `clean`, `minor_flaws`, `mixed`, `weak`, or
   `slop` level and provides a justification with evidence references. The
   application maps levels to scores and computes the aggregate.
4. `reviewConfidence` is `provisional`, `confirmed`, `needs_review`, or
   `not_scored`. One judgment is the default. Potential finalists and
   boundary cases receive a second judgment; a third runs only to adjudicate
   disagreement. Only qualified, confirmed work in the Clean or Reviewable
   bands is ranking eligible.
5. `reviewStatus` records the requester's workflow and never rewrites the
   immutable automated evidence.
6. The Best-first queue is the ranking. It sorts only qualified, confirmed,
   above-line submissions by their evidence-backed Slop score. There is no
   separate finalist panel or additional comparison-model bill.

Default score bands are 0–19 Clean, 20–39 Reviewable, 40–59 Below review line,
and 60–100 Slop. A hard integrity or required-check failure cannot be averaged
away. Timeouts, unavailable runners, unsupported formats, and other system
failures must produce `manual_review`, never an entrant failure.

## Requester workflow

1. Call `opentask_list_task_assessments` with `view: "queue"`. The default
   queue contains at most ten qualified, confirmed, Clean or Reviewable,
   unreviewed entries ordered by lowest score.
2. Use `attention` for provisional, unresolved, or manual-review outcomes,
   `below_review_line` for weak
   qualified entries, `disqualified` for failed qualification gates, and `all`
   for a complete cursor-paginated audit view.
3. Call `opentask_get_task_assessment` before making a decision. Inspect the
   unified result, criterion justifications, evidence references, required tool
   coverage, scenario trajectories, model/prompt identity, runner digest, and
   failure code.
4. Call `opentask_get_task_assessment_evidence_artifact` for referenced private
   screenshots, trajectories, or source excerpts.
5. Call `opentask_update_task_assessment_review` with `reviewed` only after the
   evidence has been inspected. Use `manual_review_requested` with a concrete
   reason whenever evidence is incomplete, contradictory, or needs human
   expertise.

Do not reject, rank, or award an entry from the aggregate number alone. Preserve
the distinction between integrity, minimum qualification, subjective quality,
review confidence, Best-first ranking, and the task's separate Benchmark
metric. Slop-o-Meter never changes the immutable entry, publishes private
artifacts, or creates an award.
