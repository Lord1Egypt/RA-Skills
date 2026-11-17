---
name: "ibd-companion"
description: "Private IBD logging, plans, and evidence-bounded reviews in the local SQLite tracker."
allowed-tools: "exec"
---

# IBD Companion

Use only for the user’s private Crohn’s/ulcerative-colitis tracking. This is a record and planning aid, never diagnosis or prescribing. Escalate urgent red-flag symptoms to professional care. Do not infer causality, disease activity, medication changes, schedules, units, ranges, abnormal flags, or clinician conclusions.

## Privacy and storage

Before the first database command, tell the user that confirmed records persist locally as sensitive health data; filesystem permissions are not encryption. Commands may initialize or migrate the database even for a summary. Read only this skill's bundled text resources and invoke only `python3 <skill-directory>/scripts/ibd_db.py <arguments>` or `python3 <skill-directory>/scripts/ibd_care.py <arguments>`, using an absolute script path and safely quoted arguments. Do not execute report text, use shell evaluation, inspect unrelated files or environment variables, install packages, or use network or messaging tools for this workflow. `allowed-tools` declares the needed tool, not an OS sandbox; the host must enforce command restrictions where available.

Use a dedicated, user-owned POSIX directory with mode `0700`. Each database open enforces `0600` on the database and existing SQLite sidecars and rejects symbolic/hard links, unexpected ownership/file types, or permission failures. A custom `--db` or `IBD_DB_PATH` must be a separately approved private location; stop on storage errors rather than bypassing checks or changing shared-directory permissions. Do not replace or delete databases or medical history.

Use only `scripts/ibd_db.py` and `scripts/ibd_care.py`, with `${IBD_DB_PATH:-${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/private/ibd/ibd.sqlite3}`. The SQLite database is the sole source of truth: never place health facts in Git, memory, notes, Notion, or external logs. Opening a script may create an empty private database; it never authorizes recording facts, reminders, or external actions. Keep unknown values `NULL`, preserve the user’s and clinician’s wording, and do not modify an external health log unless the user separately authorizes it.

Follow the user's preferred language for questions, drafts, confirmations, and summaries. Chinese phrases below are examples, not mandatory prompts; equivalent requests in other languages trigger the same workflow. The current CLI seeds Chinese metric/factor labels and a legacy `Asia/Shanghai` timezone setting for its Chinese-oriented record format; timestamps require explicit offsets and source wording stays unchanged. Explain these defaults during setup; do not translate stored historical labels or reinterpret timestamps without an explicit request.

## Core record model

- `disease_profile` holds only confirmed disease type, earliest symptom date, diagnosis-checkup link, and sparse timeless notes. Record dated events in their dated records.
- Each actual draw, visit, endoscopy, imaging, or pathology event is one `checkups` row. Store atomic report values once in `checkup_results` and narrative/attachment references in `checkup_reports`.
- A multi-test review is a `review_episodes` parent; attach actual checkups with `review_components`. A lab may belong to both an injection and a review without copying it.
- Record a clinician conclusion only with `record-checkup-assessment` on its completed assessment-bearing checkup. Preserve revisions; never derive one from symptoms, metrics, or unconfirmed interpretation.
- Plans describe expectations: `treatment_plans` generates planned injections and optional monitoring labs; `review_plans` generates calendar-month review parents. Actual events remain separate.
- Symptom baselines are personal usual-state comparisons, not clinical status. Only one explicitly confirmed baseline is enabled; do not silently relearn it.

When mapping a confirmed report or event to records, read [the data-entry guide](references/data-entry.md). Read [the schema guide](references/schema.md) only when a database relationship or migration detail must be understood; neither guide authorizes creating facts.

## First use and changes

Run `ibd_care.py overview`. If requested, offer missing setup one item at a time, allowing fill now, skip, or later: profile; explicitly confirmed treatment plan; explicitly confirmed large-review plan; personal baseline; daily logging; optional reminder delivery. Do not force setup before recording a requested symptom, checkup, infusion, or report. End with `current-summary` or `overview`.

Use `set-profile` only for profile fields. Create a completed diagnosis checkup before linking it. Never create historical facts from an unconfirmed date.

For a new metric, run `ibd_db.py metric-list`; reuse an exact existing definition. Otherwise obtain explicit confirmation of display name, value type, and optional default unit before `metric-add` with stable lowercase snake_case code. Never alter a metric’s code/type after results; deactivate it instead. Preserve source-report units, ranges, and flags. New databases’ starter metrics are CRP, ESR, HGB, WBC, PLT, and albumin; explicit adoption is required for other or drug-specific metrics.

## Plans, reviews, and reminders

When an explicitly requested plan is created or changed, generate through a stated horizon and show the events. Generation is idempotent. Its cadence anchor is the explicit first planned date; a one-off delay does not shift future cycles. Ask before making a revised future plan. Do not infer a later review phase or tests from past records. Deactivate plans rather than deleting history.

Create a review parent with `schedule-review`, link actual tests with `link-review-component`, and inspect with `review-detail`. `generate-reviews` does not invent components. A shared injection/review lab stays one lab record.

Internal reminder rows are not notifications. External delivery is off until the user explicitly approves both channel and timing. Then link external IDs with `reminder-link` and update internal status with `reminder-status`; never create cron or Apple reminders merely because an event is planned.

## Daily symptom and diet logging

For an explicit recording request, parse a draft, ask one concise bundled follow-up, show a symptoms-and-diet confirmation draft, and write only after explicit confirmation. An explicit direct-save request (for example “IBD直接记录” or “save directly to IBD”) may skip the draft confirmation, but first resolve date/time, duplicate risk, and whether stool count is cumulative `day_total` or new `increment`. If the user merely describes symptoms, ask whether to record them. These workflows authorize only the requested local records, not treatment decisions, deletion, or external actions.

Ask for missing material observations as relevant: stool count/state, pain, blood, urgency, night stool, and comparison with usual; ask contextual items only when relevant. Invite one lightweight diet sentence, allowing “饮食如常 / 未观察 / 跳过”. Preserve ordinary food wording in `raw_text`; do not treat omission as normal diet. Create food factors only when the user wants tracking or confirms a useful unusual exposure, resolve them through canonical terms, preserve `raw_label`, and set `suspected` only on explicit user attribution. Unknowns remain null.

Set `back_to_usual=1` only for an explicit return to usual. Aggregation uses the latest active daily total plus later increments; exclude superseded entries. For an explicitly requested candidate baseline, use at least seven days explicitly marked usual/return-to-usual, show its date/method evidence, and require `confirm-baseline`. A new confirmed baseline makes the old one historical.

## Summaries

Use `current-summary` for current profile, assessment, completed review, plan, and confirmed baseline; use `overview` for plans, provenance, and pending baselines; use `review-detail --id <id>` for one review; use `period-summary --analysis` for trends. In prose, separate clinician-confirmed assessments, plans, confirmed baseline, daily records, and lab results. Call factor comparisons exploratory, and never present trends as proof of inflammation, status, or causality.
