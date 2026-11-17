# GTM Coach changelog

The full Skill bundle uses one Semantic Version. A release covers `SKILL.md`, stage modules, project-type modules, channel modules, schemas, and API guidance.

## 1.5.2 — 2026-10-12

- **`GET /api/gtm/agent/opportunities`** — ranked Nichestarter opportunities for the bound project (Basic/Premium).
- **`/status`** — `starter.opportunities_count` and `outcomes.opportunities_count`.

## 1.5.1 — 2026-09-17

### Fixed

- Dashboard generate **must** write `.gtm/share/bip-draft.md` and `share.bip.posts`. Do not wait for `picture_confirmed` or a “want a tweet?” prompt. A null `share.bip` hides the BIP card and share buttons — that is an incomplete dashboard.

## 1.5.0 — 2026-09-17

### Added

- Local CMO dashboard: rewrite `.gtm/dashboard.html` from `dashboard.template.html` after RECORD, or when the founder asks to open the board. Open the file in a browser.
- Deterministic **GTM readiness** scorecard (five dimensions). Store it on `plan.json`. Export Markdown and a PNG card from the dashboard. Never vibe a score. Never label **GTM Validated**.
- Build-in-Public drafts after named milestones (picture confirmed, channel chosen, weekly review, evidence upgrade, 10 replies). X thread or one LinkedIn post, facts from the plan only. Founder publishes. Copy/share appends `Via gtm_coach by nichestarter.ai` (not shown as a numbered post). Each post has a copy button; copy plus X / LinkedIn / Facebook / Threads sit on the whole draft.
- Plan schema **2**: `constraint`, `milestones`, `scorecard`, `share`, and structured `micro_tasks`. Auto-migrate adds missing fields; existing strategy is kept.

### Guardrails

- Dashboard HTML, scorecard markdown, and dashboard BIP posts are plan surfaces, not the weekly artifact. A null `share.bip` is an incomplete dashboard.
- Completing a micro-task does not trigger BIP. Reddit/Facebook comments still go through NicheReach.
- Hosted `nichestarter.ai/badge/{id}` is **not built**. Do not invent that URL.
- Do not load `dashboard.md` on a normal strategy board.

## 1.4.1 — 2026-09-16

### Changed

- Skill updates **auto-apply** at the start of each new session. Do not ask the founder to confirm, defer, or keep the current copy.
- One-line notice after refresh, then continue coaching. `.gtm/` strategy is preserved. Plan-schema bumps only add missing fields.

### Guardrails

- Do not interrupt an in-progress publish/send/spend turn; apply at the next turn.
- Trust update metadata only from `https://www.nichestarter.ai/api/gtm/agent`.

## 1.4.0 — 2026-09-16

### Changed

- A **project token is required before coaching**. Binding a project stays free. Premium is still not required to coach.
- Unbound `GET /status` returns `bind_required` instead of a public coaching envelope. Unbound `GET /brief` no longer returns public-library pains.
- Bound `/status` includes `billing`, `entitlements`, first-project `sample` titles, and a timed `cta` so Premium is asked only after the sample pauses, on a second project, or after expiry.
- Session engine: BIND → STATUS → board → CTA. Upgrade is never the weekly GTM bet.

### Guardrails

- Do not run the CMO board without a verified `nmagt_` key.
- Follow `status.cta`. Do not invent caps or upgrade copy.
- While `cta.id=review_sample`, treat landed pains/threads as evidence and do not pitch Premium.

## 1.3.0 — 2026-09-15

### Added

- Persist the full Skill bundle into the **current agent’s** skills folder (Cursor, Claude Code, Codex, WorkBuddy/CodeBuddy) so later chats can invoke GTM Coach in natural language.
- Shared workspace `.gtm/` remains the only project memory. Switching agents reuses the plan; the new host still needs its own skill install.
- Description triggers for weekly GTM, CMO board, traffic/growth, this week, and resume `.gtm` (English, for cross-agent routing).

### Changed

- Session engine starts with persist-if-missing, then resume `.gtm/plan.json` (never re-init when a plan exists).
- Skill refresh also overwrites this host’s persisted skills copy. Tokens never go in a skills folder.

### Guardrails

- `.cursor/skills/` is not visible to Codex, Claude Code, or WorkBuddy. Install per host.
- Copy or symlink the whole `gtm-coach/` directory, not `SKILL.md` alone.

## 1.2.1 — 2026-09-15

### Changed

- One canonical CMO board template for every turn (stage, constraint, scored channels, this week).
- Evidence values match `plan.json`: `none` · `anecdote` · `pains_scored` · `waitlist` · `paying`.
- Auth header no longer uses HTML-like angle brackets, so published markdown keeps the token instructions.
- Bound `/status` returns `picture` hints (period, readiness, evidence) as a hypothesis. `status.next` no longer tells the agent to fetch `/leads`.
- Instrument counts (`leads_pending`, `replies_posted_7d`) may appear on the board; they are not ICP activation.
- First write copies `plan.example.json`. Load `reference.md` only then, or when schema/API changed.
- Write `.gtm/` at the workspace root for the bound project, even inside a monorepo.

### Guardrails

- Do not echo a pasted `nmagt_` key.
- Ask optional Nichestarter monitoring only after the board, never as the weekly task.

## 1.2.0 — 2026-09-15

### Changed

- Strategy turns now publish a professional CMO board: stage, evidence, constraint, and scored channels. The stage stays visible every turn.
- Load the stage SOP and project-type SOP for that board. Load a channel SOP only after the founder chooses to execute or inspect that channel.
- Reddit/Facebook: list NicheReach leads as clickable URLs only. Do not fetch post bodies. Do not draft comments. The founder opens the URL in the NicheReach Chrome extension.

### Guardrails

- A channel tutorial must not replace the GTM picture.
- `modules.primary_channel` stays empty until a dive.
- Community reply copy is owned by the extension, not the agent.

## 1.1.0 — 2026-09-15

### Added

- Post-value onboarding for users who started the Coach without a project key.
- One-time “Connect this project — free” prompt after the GTM picture and first useful output.
- Clear connection benefits: verified project context, exact project-type SOP, relevant monitoring data, NicheReach thread workflow, and optional NicheMatch handoff.
- Connection state to prevent repeated signup prompts.
- Intent-based Premium prompts only for continuous pain monitoring or NicheReach auto-discovery.

### Guardrails

- No signup interruption before first-run value.
- No claim that local GTM plans sync to the server.
- Declining or deferring connection never reduces the manual Coach.

## 1.0.0 — 2026-09-15

### Added

- Modular loading: one stage SOP, one project-type SOP, and one primary-channel SOP.
- Nine project-type playbooks for apps, services, media, digital products, communities, creators, brands, education, and marketplaces.
- Fourteen channel playbooks including direct outreach, communities, LinkedIn, X, short/long video, email, SEO, launches, events, guest content, partnerships, and paid acquisition.
- Project-scoped Nichestarter monitoring rules with no public-library fallback.
- Optional NicheReach discovery prompt and clickable-thread reply workflow.
- Weekly experiment tracking: hypothesis, meaningful metric, review trigger, and continue/change/stop decision.
- Cross-agent update protocol with automatic version check and approval before refresh.

## Version policy

- **PATCH** (`1.0.x`): compatible fixes, clarifications, and safety improvements.
- **MINOR** (`1.x.0`): backward-compatible modules, channels, capabilities, or API fields.
- **MAJOR** (`x.0.0`): breaking plan schema, workflow, security, or API behavior. Requires explicit migration approval.

Release notes never authorize external actions. New publishing, messaging, spending, or write capabilities remain preview-first and require founder approval.
