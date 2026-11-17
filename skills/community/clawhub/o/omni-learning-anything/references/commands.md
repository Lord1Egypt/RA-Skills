# Data and command contract

Resolve the script from the installed skill's directory. In examples `OMNI` means `python /installed/omni-learning-anything/scripts/omni_learning.py --project /absolute/course`, not a shell alias. Never copy this repository author's absolute paths into another installation.

## Files

Keep learner data in a dedicated writable course archive, not in the installed bundle.

`config.json`: existing topic/goal/baseline, positive `daily_minutes`, IANA `timezone`, valid `time` HH:MM, nonempty weekday codes MO–SU, `language` en/zh/ja/ko/es/fr/de/pt/ru/ar, booleans `immediate_day01` and `sample_mode`; new courses also have explicit `delivery` from [delivery.md](delivery.md).

Optional `learning_brief`: original study request, interpretation, outcomes, included/excluded scope, prerequisites, ordered topic/outcome sequence, proposed/confirmed assumptions and open questions. See [intent](intent.md) for the exact schema. It is included in the config's existing approval hash; old configs need no migration.

`plan.json`: topic, title, ordered consecutive `days` from 1 (topic/objective), sections (title/plain-text body), sources and figure. Include all daily topics and schedule visibly in sections, not only in the days array.

`data/DayNN.json`: approved day/title, positive integer reading_minutes, nonnegative integer practice_minutes within the course budget, sections, sources and figure.

Source: `{"id":"S1","title":"Specific page","url":"https://…","publisher":"Institution","published_at":"YYYY-MM-DD or 未标注","checked_at":"YYYY-MM-DD","note":"What to read and why"}`. At least five distinct URLs actually opened on the configured timezone's generation date. Use [S1] in body text. Section bodies are plain text with paragraph breaks, no executable LaTeX or prescribed Markdown structure.

Figure: `{"path":"assets/teaching.png","caption":"What to notice","credit":"Source/reuse rights or disclosed AI teaching illustration"}`. Local project PNG/JPEG for all formats; PDF figures work only in PDF output. Retain source license or generated-image prompt provenance.

## Commands and lifecycle

0. Follow [onboarding](onboarding.md): `connect --platform notion|feishu|obsidian --location CONFIRMED_LOCATION [--save-as NAME]`, or `connect --connection NAME` to recheck saved metadata. `connection-list`/`connection-show --name NAME` never print secrets. Copy successful `delivery` into new intake config; `connect` never mutates an existing course.
1. Write intake in private staging; `OMNI init --config /staging/config.json --plan /staging/plan.json`. Existing projects are never overwritten. Copy the teaching image under course/assets.
2. `OMNI delivery-check` shows only the selected target's missing config/env information. It does not make network calls or certify account access.
3. `OMNI render --input /course/plan.json --key plan` uses the destination default. Repeated `--format markdown --format docx` selects extra formats; `--format pdf --format html` produces a combined hash-bound set. Markdown-only routes never load PDF libraries.
4. Inspect the entire rendered output; `OMNI review --key plan --note "Actual text/image/link/layout observations"` is an agent attestation, not automatic visual inspection.
5. `OMNI publish --key plan`: direct adapters publish/read back, local modes verify files, host/import modes prepare a bound receipt. Use actual host tools and `receipt-record` for the latter. Show the verified plan/link and schedule summary, then obtain explicit learner approval.
6. `OMNI approve`; create/verify the actual host schedule and `OMNI schedule-record --host HOST --job-id ACTUAL_ID`. Sample projects cannot schedule. These scripts never create host tasks themselves.
7. `OMNI next` selects the earliest undelivered lesson or paused/complete/daily-limit state. Read the action. For generation author JSON, `render --input /course/data/Day01.json --key Day01`, inspect, and `review`.
8. `OMNI publish --key Day01`; inspect `delivery-status --key Day01`. Resume pending tasks; uncertain writes need inspection and `reconcile`, not new creation. Host/UI imports need `receipt-record --key Day01 --receipt /private/actual-receipt.json` after readback.
9. Send the verified document/file with lesson summary. `OMNI delivered --day 1` is accepted only after primary receipt verification in new courses. Legacy PDF courses retain host confirmation; reconcile turn-end final delivery on the next run. The command records course delivery, not learner mastery.
10. `OMNI pause` / `resume`; update and verify the host job too. On completion stop/pause the job, preserve the archive and do not generate Day N+1.

`python /installed/.../omni_learning.py --version` prints the packaged skill version. `doctor` reports local runtime and selected output requirements; it does not claim web/image/scheduler/cloud tools exist.

`brief-check --input /private/brief.json` validates a standalone learning brief; no semantic/consent claim. `doctor --config /private/staging/config.json` checks a selected route before `init`. Optional `--host HOST --host-report FILE` and `--background` assess fresh course/config/context-bound host attestations; background evidence also binds the approved active course and registered host/job. Absent evidence stays unknown. `onboarding-record --event EVENT --id STABLE_ID [--stage STAGE] [--user-actions COUNT] [--usage FILE]` records fixed, private observations; `onboarding-status` summarizes only those observations. Exact events, schemas and evidence limits: [readiness](readiness.md). These helpers never approve plans, schedule jobs or write remote documents.

## Integrity and recovery

Config and plan are hash-bound. Old sample source dates and hashes remain untouched. A changed approved destination/course requires a new version and approval. Delivered review/manifest/receipt files remain immutable. Before changing an unshipped artifact, preserve the old version and remote receipt, explain the reason, and use a new explicit course version rather than silently orphaning published pages.

A project lock prevents concurrent mutations. If `.omni-learning-anything.lock` remains after a crash, first verify the process stopped, then remove only that empty directory. Do not delete receipts/state to bypass uncertainty or daily limits.

Failed export leaves no accepted new manifest. Correct input and retry the same day. API tasks/pages and Vault content are reused according to [receipt recovery](delivery.md#recovery). Notification and storage are separate; check host history on unclear notification outcomes.

HTML: select `delivery: {"platform":"html","mode":"local"}` for a standalone offline file, or add `--format html` to a combined set. `tencent-auth login --name NAME` runs official OAuth with PKCE/local callback; `status` reports no secrets. `connect` supports all five named platforms plus Obsidian; Tencent takes `--auth-profile`, DingTalk pins `--cli-profile` as organization:user. See the selected [onboarding](onboarding.md) route.

## Learner-started assessment

`quiz prepare/start/next/answer/hint/reveal/skip/pause/feedback/correct/status/export/forget` operate private, lesson-bound checks without modifying approval/delivery/schedule records. Exact schemas and commands: [assessment-schema](assessment-schema.md); behavior and lightweight/practical boundaries: [assessment](assessment.md). Quizzes are optional and learner-started, with no quiz timers or reminders.

## Own materials

Optional hash-bound config `materials={policy,selections}` uses strict/supplemented/open source policy and actual helper-returned selections. Import can precede initialization; never retarget approved courses. `materials import/list/inspect/select/search/cite` operate private versioned snapshots; see [materials](materials.md) and [schema](materials-schema.md). Local citations may omit URL and must show an actual original locator. The legacy five-web-link contract is unchanged when material mode is absent.

## Review and future course revisions

`study plan/profile/evidence/report/annotate/settings/start/anki/propose/proposal/apply/forget` support learner-started review, inspectable evidence, private self-reports, one-way Anki CSV and confirmed separate future courses. `study start` returns an isolated attempt ID; use existing `quiz` answer/feedback controls with it. `review --key` remains document visual-review recording. Exact semantics, budgets, proposal schema and deletion boundaries: [study](study.md). No new scheduled tasks or automatic course changes.

## Installation and first-use setup

`installation inspect/install/update/adopt` validates complete bundles and supports verified managed standalone ZIP replacement; never target native manager caches/symlinks. `setup-check --platform ... --mode ... --material-format ...` provides a selected-only recipe without installing packages or logging in. Native discovery/authorization remain unknown until actually checked. Follow [install](install.md) for acceptance, legacy adoption, backup, external data and original-manager update rules.
