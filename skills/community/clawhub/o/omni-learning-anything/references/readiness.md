# First-use readiness and observations

Use with `onboarding.md`. The agent operates tools and records observations; the learner chooses goals/location and reviews official grants. Never ask the learner to fill these JSON files.

## Local check before expensive generation

Create the agreed writable course archive, prepare the selected-route config in private staging, then run:

```sh
OMNI doctor --config /private/staging/config.json
```

After initialization, `OMNI doctor` reads the archive's config. Python modules are checked only for formats/routes that need them; HTML/Markdown do not need DOCX/PDF packages or TeX. XeLaTeX discovery includes existing TinyTeX paths; successful compilation and font inspection remain necessary. An environment variable's presence, installed CLI or `delivery.ready` means configuration only, not live access or write permission. `doctor` makes no network requests or remote writes and does not read credential stores.

Interpret the fields separately:

- `local_ready`: archive/interpreter/selected dependencies checked locally; this alone does not certify rendering, account access or host tools.
- `host.*`: `unknown`, `unavailable` or evidence-backed host attestation. `unknown` is not success. Capability checks should use real tools, not infer from an installed skill or a subscription name.
- `ready_to_generate`: local/config checks plus required host attestations for the requested context. Without a host report this stays false; the agent can still investigate missing capabilities and prepare a plan. It is advisory and does not approve/publish a course.
- `unattended_ready`: true only for a fresh correctly scoped background report with all required capabilities. A foreground report cannot establish it.

For each unavailable item use its exact `next_action`, install only selected dependencies and retry that check. Preserve the destination and existing work. If a viewer, image workflow or scheduler is missing, report that precise limitation and offer an explicitly accepted alternative; do not silently change formats or announce success.

## Host evidence contract

Use actual tool results and keep the report private in the course archive. Record only a short evidence reference (e.g. a tool call/job/test identifier), never authentication output, token-bearing URLs, credentials or the contents of private keychains. Reports are **host attestations**, not cryptographically verified results. The helper checks scope/context/freshness; it cannot prove the observation itself happened.

```json
{
  "host": "current-client",
  "project": "/absolute/course",
  "config_hash": "ACTUAL_SHA256_FROM_DOCTOR",
  "context": "foreground",
  "checked_at": "ACTUAL_TIME_WITH_TIMEZONE",
  "capabilities": {
    "execution": {"status": "verified", "evidence": "actual-file-and-command-check"},
    "research": {"status": "verified", "evidence": "actual-source-opening"},
    "images": {"status": "unknown"},
    "inspection": {"status": "unknown"},
    "notification": {"status": "unknown"},
    "scheduler": {"status": "unknown"},
    "credentials": {"status": "unknown"}
  }
}
```

Replace example values from actual observations; never copy example `verified` statuses without testing. `images` may use agreed licensed-source-image access instead of AI generation. `inspection` must match the chosen format; inspect an actual artifact. `notification` needs evidence of the agreed user-facing delivery mechanism; a job merely existing is insufficient. Reports are accepted for 24 hours, with at most five minutes of future clock skew, and bind the canonical course path and exact config bytes. An edited config requires a new report. Evidence strings are not echoed by `doctor`.

```sh
OMNI doctor --host CURRENT_HOST --host-report /private/course/host-check.json
OMNI doctor --host REGISTERED_HOST --background --host-report /private/course/background-check.json
```

Supply the actual expected execution host with `--host`; it must match the report. Background reports must come from the **actual scheduled execution host/context**, after learner approval and real job verification. Add the real `job_id` to the background report; it must match `state.schedule.job_id`, and `state.schedule.host` must match `--host`. The course must be active, approved, non-sample and use its own archived config. A handoff or changed job requires new evidence. They need execution/research/images/inspection/notification/scheduler, plus `credentials` for cloud routes. Verify official account/location access in that context without exporting tokens. Obsidian/local files instead depend on the archive/Vault and execution context. Do not create live jobs for sample projects. If background access is unavailable, offer manual continuation and preserve all pending artifacts. Never block a foreground plan simply because scheduling cannot be certified.

Successful `publish`, content readback and actual visual inspection still establish each delivered document separately. Reuse pending page/task IDs; readiness reports never substitute for receipts or permit duplicate creation.

## Observe first-use friction privately

Use `onboarding-record` in the course archive before `init` if useful. It creates only `onboarding/events.json`; the ledger never changes plan/config/approval/delivery state and is excluded from the distributed Skill. No telemetry is sent anywhere.

```sh
OMNI onboarding-record --event started --id intake-start
OMNI onboarding-record --event user_action --id destination-choice --user-actions 1
OMNI onboarding-record --event intent_ready --id brief-ready
OMNI onboarding-record --event authorization_started --id auth-attempt-1
# Once this attempt ends: success, expiry, cancellation or failure. This event is not proof of permission.
OMNI onboarding-record --event authorization_finished --id auth-attempt-1-ended
OMNI onboarding-record --event blocked --id missing-scope-1 --stage authorization
OMNI onboarding-record --event resumed --id resumed-1
OMNI onboarding-record --event plan_ready --id first-usable-plan
OMNI onboarding-record --event first_lesson_ready --id first-usable-Day01
OMNI onboarding-status
```

Record `plan_ready` / `first_lesson_ready` only after actual agreed-route publication and inspection make the content usable, not when draft text is generated. These observations are separate from learner approval and lesson delivery records. Record actual meaningful user actions; do not count each automated poll as a learner action. Use stable non-secret IDs so restart/retry does not add duplicates. A conflicting reuse is rejected without modifying the prior observation. Start once; resume the same ledger. Pair each authorization attempt's started/finished observations before beginning another; record the exact blocked stage separately. Observation times come from the current process, not invented historical timestamps.

Allowed events: `started`, `user_action`, `authorization_started`, `authorization_finished`, `intent_ready`, `plan_ready`, `first_lesson_ready`, `blocked`, `resumed`. Allowed stages: `intent`, `requirements`, `dependencies`, `authorization`, `destination`, `render`, `inspection`, `publish`, `scheduler`.

The summary shows first-milestone wall time and authorization waiting separately, including an unfinished authorization interval. Counts cover **recorded** actions only; no completeness is inferred. A paused/resumed session may include time away from the app. Do not call wall time pure generation latency or subtract authorization time from milestones without checking interval overlap.

When the host actually exposes metered usage, `--usage /private/meter.json` can attach `{"source":"host_meter","input_tokens":100,"output_tokens":50,"cost":0.01,"currency":"USD"}` to an event. Use only observed fields; cost and currency must appear together. Never estimate currency costs from a subscription or invented pricing. Unknown usage is omitted; `total_cost` remains null because partial event observations do not prove full-course billing. The helper records fixed metadata, not free-form error text, login URLs or account identities. Private reports/ledgers may be removed at the learner's request without altering delivery receipts.
