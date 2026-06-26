---
name: job-search
description: Search, evaluate, and manage job opportunities for a candidate across the Russian market with hh.ru, Habr Career, Telegram vacancy channels/chats, and LinkedIn as a secondary source. Use when building a candidate profile, filtering vacancies by salary/stack/seniority/remote format, scoring job relevance, tailoring resumes or cover letters, tracking applications, or running controlled job-hunt workflows with explicit safety rules for outreach and auto-apply.
---

# Job Search

Use this skill to run a structured job-hunt workflow without turning the agent into an uncontrolled spam bot.

## Core workflow

1. Build or update the candidate profile.
2. Define target roles, salary floor, geography, work format, and exclusions.
3. Before collecting vacancies from any browser-based source (especially hh.ru), force a page refresh/reload so newly published postings appear.
4. For hh.ru in Browser Relay / logged-in browser flows, do not trust the currently rendered list until after an explicit refresh of the active search results tab.
5. Before checking whether an hh resume can be raised in search, refresh the page that shows the resume cards; stale hh UI can falsely show a cooldown when the raise is already available.
6. When the user asks to raise resumes on hh without narrowing it down, raise all relevant active resumes that are currently available after refresh, not just one.
7. Collect vacancies from the supported sources.
8. Normalize each vacancy into a common structure.
9. Score each vacancy: strong match / possible match / skip.
10. Save the shortlist and application state in durable workspace files.
11. Tailor resume / cover letter only for shortlisted roles.
12. Apply or message recruiters only under the allowed mode.

## Supported sources

Primary:
- hh.ru
- Habr Career
- Telegram vacancy channels and chats

Secondary:
- LinkedIn

Read `references/source-strategy.md` when choosing source priority and source-specific handling.

## Operating modes

### 1. Research-only
Use when the user wants market scanning, salary mapping, or a shortlist.
- Search and score vacancies.
- Do not apply.
- Do not send messages.

### 2. Assisted apply
Use when the user wants help preparing applications but still approves submission.
- Search and score vacancies.
- Tailor resume / cover letter.
- Prepare answers and a pipeline row.
- Do not submit without clear approval.

### 3. Controlled auto-apply
Use only when the user explicitly allows automatic submission.
- Apply only to strong-match vacancies.
- Respect per-source limits.
- Log every submission.
- Never send recruiter DMs unless separately allowed.

### 4. Outreach-enabled
Use only when the user explicitly allows recruiter outreach.
- Follow the same rules as controlled auto-apply.
- Use short, factual messages.
- Log every outbound message.

## Hard safety rules

- Never contact recruiters or hiring managers unless the user explicitly allows outreach.
- Never auto-apply unless the user explicitly enables auto-apply.
- Never invent experience, stack, salary history, notice period, education, or citizenship details.
- Never overwrite a candidate master profile silently; append or propose diffs.
- Prefer fewer high-fit applications over mass low-fit submissions.
- Log every external action in the project workspace.
- Never mark an hh application as sent just because the "Откликнуться" button was clicked.
- On hh, treat an application as successful only after explicit UI confirmation that the response/application was sent or the vacancy appears in the sent responses state.
- If success cannot be verified, record the state as `apply-unconfirmed` or `apply-failed`, not `applied`.
- Before deciding that hh resume raising is unavailable or still on cooldown, refresh the resume page first; stale hh UI is not a reliable signal.
- Never answer screening questions or other free-text prompts without first showing them to the user and getting approval.
- After a verified hh apply, immediately refresh the resumes page and raise all relevant active resumes that are available, unless the user explicitly disables that post-apply raise step.
- When a bundled hh apply script/workflow already encodes required post-apply behavior, prefer that script/workflow over ad-hoc manual browser clicking for real applications.

Read `references/safety-rules.md` before enabling outreach or auto-apply.

## Workspace layout

Prefer a durable project folder such as:

```text
projects/job-search/
  PROFILE.md
  TARGET_ROLES.md
  SEARCH_RULES.md
  SOURCES.md
  PIPELINE.md
  OUTREACH_RULES.md
  BLACKLIST.md
  applications/
  exports/
  logs/
```

If the project does not exist yet, create it before doing serious work.

## Vacancy normalization

Normalize each vacancy into these fields when possible:
- source
- source_url
- company
- title
- stack
- seniority
- salary_min
- salary_max
- salary_currency
- gross_or_net
- location
- remote_mode
- employment_type
- visa_or_relocation
- english_level
- contact_name
- contact_url
- summary
- fit_score
- fit_label
- fit_reasons
- red_flags
- status

## Source-specific notes

### hh.ru
- Treat as the primary source for Russian-market roles.
- Normalize salary carefully; gross/net may differ by posting.
- Capture employer type, location, and work format.

### Habr Career
- Prefer for engineering/product/design roles with better tech signal.
- Preserve stack and level details from the description.

### Telegram
- Expect noisy, duplicated, and weakly structured posts.
- Deduplicate aggressively.
- Parse salary, stack, and contact info from free text.
- Treat direct recruiter handles as contact data, not permission to message.

### LinkedIn
- Use as a secondary source.
- Focus on roles that are materially better than local-market baseline or clearly international/remote.

## Tailoring outputs

For a strong-match vacancy, prepare:
- 1 tailored resume variant
- 1 short cover letter or intro note
- 3-6 bullet reasons why the role fits
- optional answers to standard screening questions

Keep tailoring factual and specific to the vacancy.

## Scripts

Prefer the bundled Python tools over ad-hoc manual parsing.
Install the Python dependencies first when you need the scoring/deduplication libraries:

```bash
python -m pip install -r skills/job-search/scripts/requirements.txt
```

Available tools:
- `scripts/requirements.txt` — Python deps for the scoring/normalization toolkit (`pydantic`, `rapidfuzz`)
- `references/onboarding.md` — resume-first onboarding and HH Browser Relay setup guidance for first-run users
- `scripts/init_job_search_project.py` — create a durable project folder from templates
- `scripts/profile_to_json.py` — convert project markdown files into a compact scoring profile JSON
- `scripts/job_match_score.py` — score vacancy JSON against a profile JSON
- `scripts/score_vacancy_from_project.py` — score one vacancy directly against a project folder
- `scripts/score_vacancies_jsonl.py` — score a JSONL batch against a project folder
- `scripts/normalize_salary.py` — normalize salary text into structured fields
- `scripts/parse_telegram_job.py` — extract a Telegram vacancy post into structured JSON
- `scripts/batch_parse_telegram_jobs.py` — process a directory of Telegram posts into JSONL
- `scripts/normalize_vacancy.py` — normalize a raw vacancy text/JSON payload into the common vacancy schema
- `scripts/batch_normalize_vacancies.py` — normalize a directory of raw vacancy payloads into JSONL
- `scripts/dedupe_vacancies.py` — cluster likely duplicate vacancies from JSONL input
- `scripts/canonicalize_deduped.py` — convert dedupe output into canonical-only JSONL
- `scripts/pipeline_add.py` — append a structured vacancy into `PIPELINE.md`
- `scripts/export_shortlist.py` — export strong or high-score vacancies into CSV

## Assets

Use `assets/templates/` when creating a new durable job-search project. These templates seed:
- `README-START.md`
- `PROFILE.md`
- `TARGET_ROLES.md`
- `SEARCH_RULES.md`
- `SOURCES.md`
- `PIPELINE.md`
- `OUTREACH_RULES.md`
- `BLACKLIST.md`

## References

Read only what you need:
- `references/onboarding.md` — first-run flow for resume/CV intake and when/how to instruct Browser Relay setup for HH automation
- `references/source-strategy.md` — source priorities and source-specific handling
- `references/safety-rules.md` — boundaries for outreach and auto-apply
- `references/project-layout.md` — recommended durable workspace structure
- `references/data-flow.md` — practical end-to-end batch flow for this skill
- `references/file-formats.md` — expected JSON/JSONL/project markdown formats
