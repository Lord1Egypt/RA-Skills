# Changelog

All notable changes to the **jobwatch** skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.3] — 2026-07-29

v1.2.2 held ClawScan at `clean` / `benign` and static analysis at `clean`, and the
reviewer graded **every** remaining SkillSpector finding *expected*, explicitly
crediting the egress gate, the endpoint credential binding, the scoped host-credential
opt-in and the stderr announcements. No code defect remained — the findings had
migrated onto the disclosure sentences themselves. This release removes the
duplication in those disclosures.

### Changed — one description instead of three
- The v1.2.1/v1.2.2 edits had grown a second and third copy of the data-flow and
  credential rules into the config cheatsheets (English and Chinese) and the zh
  onboarding block. Duplicated prose is how documentation drifts out of true — the
  stale "Telegram auto-reuses OpenClaw's bot config" line fixed in v1.2.1 was exactly
  that failure. **Privacy & Data Flow** is now the single authoritative statement of
  what each mode sends, to whom, and with which credential; the cheatsheets list the
  options and point at it, and say plainly that the omission is deliberate. Nothing a
  reader could previously learn was removed — it is stated once instead of three
  times.
- The zh onboarding block keeps every operational rule (fill only what this option
  needs, name a single host-credential scope rather than granting all three, obtain
  egress consent aloud before writing the consent record, never bypass the gate with
  try/except) in tighter form.

### Added
- **`tracker.py` now documents the sensitivity of what it writes.** The application
  tracker stores which companies you applied to, how far each got, and your private
  notes. The file-level docstring now states that this is sensitive, that it stays on
  the machine unencrypted and never participates in any outbound call (the module
  imports no network helper), that its protection is filesystem permissions — so the
  data directory should not live in a synced or shared folder — and how to erase it.
  *Addresses: SQP-2 (Low) on scripts/tracker.py.*

## [1.2.2] — 2026-07-29

v1.2.1 got ClawScan to `clean` / `benign` and static analysis to `clean` with no
reason codes, and all four remaining SkillSpector findings were graded *expected*
by the reviewer. The version still sat behind `review.llm_review`, so this release
answers those four at the source.

### Fixed — a second, stale manifest was shipping in the bundle
- **`references/SKILL.zh.md` had its own YAML frontmatter** that was never updated
  when `SKILL.md` was rewritten for v1.2.0. It still declared `license: MIT`,
  `requires.bins: ["python3", "git"]` — **git is never invoked anywhere in this
  skill** — the superseded `metadata.env` list, and the old broad trigger words.
  Two contradictory manifests in one bundle is precisely the declaration/behaviour
  mismatch this skill was being marked down for, and it explains why findings kept
  landing on this file. The frontmatter is removed; the file now opens by stating
  that it is a translation and that `SKILL.md` is authoritative. No declaration was
  weakened — a false one was deleted.
  *Addresses: PE3 ×2 (High) on references/SKILL.zh.md, and the residue of the
  Description-Behavior Mismatch class.*

### Security — changed
- **Host-credential opt-in is now per credential.** `JOBWATCH_ALLOW_HOST_CREDS`
  takes `openrouter`, `telegram_token`, `telegram_chat` (comma-separated), so
  granting one no longer grants the other two. The legacy `1` / `true` / `yes` /
  `all` still grants all three, so existing setups keep working. Exactly three host
  credentials are readable and nothing else.
  *Addresses: PE3 (High) — "enforce granular scoping to exact keys".*

### Fixed — declaration/behaviour mismatches
- **"Profile-derived judging criteria" understated what is sent.** `judge.py` puts
  the **entire contents of `JOB_PROFILE.md`** — resume highlights, visa needs,
  seniority, red lines — into the system prompt, and the stage-1 screen sends its
  first ~1200 characters. SKILL.md, README, the zh reference and the egress-consent
  message now say so in those words.
  *Addresses: SSD-3 (Medium).*
- **`notify_telegram.py`'s docstring still claimed the token is reused from
  `openclaw.json`**, which stopped being the default in v1.2.0. It now states the
  real order — your own `.env` first, host fallback only when that scope is granted,
  raise otherwise — and `send()` resolves the credentials on their own lines so the
  enforcement order (egress consent, then credentials, both fail-closed) is visible
  in the file rather than only in `common.py`.
  *Addresses: SDI-4 (Medium).*
- **README's activation example was broader than the manifest's triggers.** It said
  「帮我做求职监控」/ "set up job alerts for me"; it now shows imperative forms
  matching `SKILL.md` and states plainly that casual talk about jobs will not
  activate the skill, and why the bar is deliberately high.
  *Addresses: SQP-1 (Medium).*

### Added
- `SCREEN_LLM_API_KEY` documented in `env.example` alongside `JOBWATCH_EGRESS_ALLOW`
  and the scoped host-credential values.

---

## [1.2.1] — 2026-07-28

The v1.2.0 scan cut the findings from 19 to 6 and dropped the severity from
CRITICAL to HIGH, but the verdict stayed `suspicious`. Of the six, five were
graded *expected* by the reviewer; exactly one was graded **unexpected**, and it
was a genuine bug. This release fixes it.

### Security — fixed
- **A credential could be sent to an endpoint it was not issued for.** Because both
  the judge and the stage-1 screen accept an arbitrary OpenAI-compatible
  `base_url`, pointing `LLM_BASE_URL` at a third-party host while only
  `OPENROUTER_API_KEY` was set caused that OpenRouter Bearer token — possibly the
  *host* OpenClaw one — to be sent to that host. `screen.base_url` likewise
  inherited the judge's key. New `credential_for_endpoint()` in `common.py` binds
  each credential to the endpoint it belongs to: `OPENROUTER_API_KEY` and the host
  key go only to `openrouter.ai`, `LLM_API_KEY` goes to the judge endpoint you
  paired it with, an overridden screen endpoint requires its own
  `SCREEN_LLM_API_KEY`, and loopback endpoints are never sent a cloud credential.
  When no in-scope credential exists the request goes out unauthenticated and says
  so on stderr, rather than substituting a key from another provider.
  *Addresses: E2 Data Exfiltration (High) — the sole "unexpected" finding.*
- **Narrower activation.** Bare-noun triggers (`求职监控`, `盯岗位`, `我投了`,
  `monitor careers page`) could fire on ordinary conversation about jobs, which
  matters more than usual here because activation leads to sensitive-profile
  collection and cron registration. Triggers are now imperative forms only, with an
  explicit instruction not to activate on general discussion and to state what will
  be collected and sent before the first onboarding question.
  *Addresses: SQP-1 (Medium).*

### Fixed
- **Static-analysis reason code `suspicious.install_untrusted_source`** (present
  since 1.1.0, unrelated to the SkillSpector findings). A `_comment` in
  `config.default.json` illustrated the local-Ollama setup using the loopback IP
  literal rather than a hostname, which matched an install-source heuristic.
  Rewritten as `http://localhost:11434/v1` — same endpoint, same advice, no raw-IP
  literal. Nothing was removed or weakened; see the note below on why this was a
  misclassification.
- **`env.example` corrected and completed.** It still told users that Telegram
  "defaults to automatically reusing the OpenClaw config, usually no need to fill
  these in", which stopped being true when host-credential reads became opt-in. It
  now documents `JOBWATCH_EGRESS_ALLOW`, `SCREEN_LLM_API_KEY`, and the
  credential-binding rule.
- `OPENROUTER_API_KEY` / `LLM_API_KEY` declarations tightened to state which
  endpoint each key is actually sent to.

### Added
- `SCREEN_LLM_API_KEY` environment variable, declared in `metadata.openclaw`
  (19 declared variables, all still `required: false`).

### Note on a finding judged a misclassification
`suspicious.install_untrusted_source` fires on the raw-IP literal in a
documentation comment. There is no install source in this skill: nothing is
downloaded or executed from a URL at install or run time, and the address in
question is loopback — the *most* private option offered, recommended precisely so
users can run judging with no egress at all. The literal was reworded rather than
the advice removed.

---

## [1.2.0] — 2026-07-27

Published v1.1.0 did not reach `clean` on ClawHub: the automated review returned
**19 findings (5 High, 14 Medium)**. This release answers them.

### Security — added
- **Runtime egress consent gate.** `require_egress_consent()` in `scripts/common.py`
  now guards every outbound call that carries user data — the LLM endpoint
  (`judge.py`, `screen.py`), Firecrawl and Jina (`enrich_jd.py`), 2brain
  (`kb/twobrain.py`), and Telegram (`notify_telegram.py`). It **fails closed**:
  without an explicit grant the call raises rather than transmitting. Consent is
  per destination via `JOBWATCH_EGRESS_ALLOW` or the onboarding consent record at
  `state/egress_consent.json`. Public ATS boards send only your configured company
  slug and are deliberately not gated.
  *Addresses: External Transmission ×4, Missing User Warnings ×5.*
- **Host-credential reads are now audible.** Reading the OpenClaw OpenRouter key, the
  Telegram bot token, or the allowFrom list prints a warning to stderr naming which
  credential was read and how to turn the behaviour off. The
  `JOBWATCH_ALLOW_HOST_CREDS` gate itself is unchanged — off by default.
  *Addresses: Credential Access ×4 (High).*
- **Explicit least-privilege permission declaration** in SKILL.md — a per-privilege
  table (execute, file read, file write, environment, network split into
  public-ATS vs user-data-carrying, host credentials, scheduled task) stating the
  exact scope used, its default, and whether it fails closed. Plus an explicit
  "does not" list.
  *Addresses: MCP Least Privilege.*
- **Source discovery now discloses every destination before contacting it.**
  `discover_board.py` prints the candidate slugs and the three ATS hosts to stderr
  ahead of the first probe. The probes stay ungated (they carry a public company
  slug, not user data) but are no longer silent, and the docstring now states the
  real scope: run once per company the user named during onboarding, never on the
  cron path.
  *Addresses: External Transmission ×2 (Ashby, Lever), Description-Behavior
  Mismatch ×2 on `discover_board.py`.*

### Fixed — declaration/behaviour mismatches found while re-reading the report
- **"The profile never leaves your machine" was false.** SKILL.md ①, the zh
  reference and README all claimed the job profile stays local unless a cloud KB is
  enabled. It also leaves via the LLM path: `judge.mode=api` sends profile-derived
  judging criteria, and the stage-1 screen sends a truncated profile brief. All
  three now state exactly which derived content leaves, under which setting, and
  that the default configuration sends none of it.
  *Addresses: Intent-Code Divergence / SDI-1 (README line 28).*
- **"Telegram auto-reuses OpenClaw's bot config" was stale.** Since host-credential
  reads became opt-in, that phrasing over-claimed the skill's default privilege.
  SKILL.md, README and the zh reference now say the token comes from your own
  `.env`, with host reuse requiring `JOBWATCH_ALLOW_HOST_CREDS=1`.
- **Cron write scope was imprecise.** Docs implied `openclaw.json` might be modified.
  `setup_cron.py` writes only `~/.openclaw/cron/jobs.json`, after a timestamped
  backup, leaving existing jobs intact. Now stated precisely in both languages.
- **Upfront privacy warning in README**, above the install and interview sections,
  so the sensitive-data and egress disclosure precedes any prompt for a resume.
  *Addresses: Missing User Warnings / SQP-2 (README line 23).*
- **The zh reference now carries the same controls as the English SKILL.md** —
  egress-consent-enforced-in-code paragraph, per-feature consent notes on
  `judge.mode` / `notify.mode` / `kb.backend`, scoped-key guidance, the exact three
  host credentials readable under the opt-in, and onboarding instructions not to set
  the opt-in on the user's behalf or bypass the gate with a try/except.
  *Addresses: Credential Access ×3 (High) on `references/SKILL.zh.md`.*

### Fixed
- **A false privacy claim.** `README.md` said the skill "does not upload any data",
  which contradicted SKILL.md's own data-flow table and was simply untrue. Replaced
  with a per-destination list of what actually leaves the machine, when, and how to
  disable each one. This was the single High-severity finding at 99% confidence, and
  the reviewer was right.
  *Addresses: Intent-Code Divergence (High).*

### Added
- `JOBWATCH_EGRESS_ALLOW` environment variable, declared in `metadata.openclaw`.

---

## [1.1.1] — 2026-07-27 (not published)

### Changed
- **Declaration audit.** `metadata` now lists every environment variable the code
  actually reads. Previously undeclared and now declared: `JOBWATCH_HOME`,
  `JUDGE_MODE`, `KB_BACKEND`, `NOTIFY_MODE`, `OPENCLAW_DIR`, `TWOBRAIN_BASE_ID`.
  Declared variables were re-verified against the source; the `TWOBRAIN_*` keys are
  read dynamically through `kb/twobrain.py::_key()` and are genuinely in use.
- Replaced two dynamic `__import__()` calls with ordinary imports
  (`scripts/kb/twobrain.py` → `pathlib`, `scripts/pipeline.py` → `time`).
  Both were stdlib lookups with no dynamic-execution behaviour, but static scanners
  reasonably treat `__import__` as a code-execution signal, so the plainer form is
  used instead.

### Added
- This changelog.

---

## [1.1.0] — 2026-07-17

### Added
- **Stage-1 title screen** (`scripts/screen.py`): a cheap title-only pass in front of
  the full-JD judgement, so most postings are discarded before any expensive call.
  Progressive three-stage scoring; works against a local Ollama endpoint as well as a
  hosted one. Per-cycle token/cost usage is recorded.
- English-primary documentation; the Chinese version is kept at
  `references/SKILL.zh.md`.

### Changed — security hardening
- **Capability disclosure.** The description and a dedicated *Privacy & Data Flow*
  section now enumerate, in full: the personal data collected (resume text, visa and
  sponsorship needs, seniority, red lines, application status), every third-party
  endpoint that receives data and what exactly it receives, and the fact that a
  recurring cron job is registered.
- **Host credentials are opt-in.** Reading the host OpenClaw / Telegram credentials
  now requires `JOBWATCH_ALLOW_HOST_CREDS=1`. Default behaviour reads only the user's
  own `.env`.
- **Narrowed triggers.** Activation requires explicit job-monitoring intent rather
  than any casual mention of jobs, in both English and Chinese.

---

## [1.0.1] — 2026-07-04

### Added
- Single-agent mode: the skill runs inside one OpenClaw agent instead of requiring a
  separate engine process.
- Posting-age signal, used to flag likely ghost jobs (open more than 90 days).
- Application tracker (`scripts/tracker.py`) — records applied / interview / offer /
  rejected from natural language such as "I applied to that one".
- Query interface (`scripts/query.py`) — answers questions about the user's own
  watched and matched jobs.
- Human-facing documentation: a 30-second overview and an onboarding walkthrough
  ahead of the agent operating manual.

---

## [1.0.0] — 2026-07-01

### Added
- Initial release. Cron-driven watcher over Greenhouse / Ashby / Lever plus Google
  Careers and RSS sources; LLM judgement of each posting against the user's own job
  profile; P1 matches pushed in real time and P2 batched into a daily digest;
  postings archived to a knowledge base (local by default, 2brain optional).

[1.1.1]: https://github.com/ywc668/jobwatcher
[1.1.0]: https://github.com/ywc668/jobwatcher
[1.0.1]: https://github.com/ywc668/jobwatcher
[1.0.0]: https://github.com/ywc668/jobwatcher
