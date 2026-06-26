---
name: hyperthink
version: 1.0.0
description: >
  Triple-perspective deep research engine. Triggered by /hyperthink. Runs an interrogate
  flow to narrow scope, then executes a 6-stage fully automatic pipeline: (1) Opus master
  brief + 3 persona-branched prompt variants, (2) 36 parallel deep-dives (12 sections × 3
  agents: Optimist / Analyst / Critic), (3a) Analyst-only trifecta audit — fact-checks
  Optimist, confidence-tags all claims, compresses each section to a structured comparison
  doc, (3b) unified synthesis narrative weaving all 3 perspectives with embedded confidence
  tiers, (4) executive brief + docx delivered to Telegram. Fully hands-off after trigger.
  Output: synthesis.md + brief.docx. Cost: ~$55–75/run.
requires:
  skills:
    - interrogate
  env:
    - name: ANTHROPIC_API_KEY
      description: Anthropic API key — required for all batch API calls (stages 2–4)
      required: true
      sensitive: true
    - name: BATCH_JOBS_DIR
      description: Directory for batch job state files. Defaults to ./batch-jobs/ if not set.
      required: false
      sensitive: false
    - name: NOTIFY_WEBHOOK_URL
      description: Optional webhook URL for job completion notifications
      required: false
      sensitive: false
    - name: TELEGRAM_BOT_TOKEN
      description: Optional Telegram bot token for job completion notifications
      required: false
      sensitive: true
    - name: TELEGRAM_CHAT_ID
      description: Optional Telegram chat ID for job completion notifications
      required: false
      sensitive: false
    - name: NOTIFY_LOG_FILE
      description: Optional path to a log file for job completion notifications
      required: false
      sensitive: false
  dependencies:
    - name: python-docx
      install: pip install python-docx
      reason: Required by md2docx.py to generate .docx output in Stage 4
      required: false
      note: Only needed if you want .docx output. brief.md is always written regardless.
  filesystem:
    - path: /data/hyperthink/
      access: read-write
      reason: Persistent storage for all pipeline output (master brief, sections, synthesis, final brief)
    - path: ./batch-jobs/
      access: read-write
      reason: Batch job state files, results JSONL, job registry
  network:
    - host: api.anthropic.com
      reason: Anthropic Batch API — used for stages 2, 3a, 3b, and 4
    - host: configurable
      reason: Optional notification endpoints (webhook, Telegram) — only if env vars are set
  autonomy:
    confirmation: single — user confirms scope once, pipeline runs fully unattended after that
    duration: 8–18 hours typical (dominated by Anthropic batch queue times)
    checkpoints: none after scope confirmation — by design
    note: >-
      If you want approval checkpoints between stages, modify the cron poller payloads
      to pause and notify before submitting the next stage.
---

# /hyperthink

Triple-perspective deep research engine. Triggered by `/hyperthink`.

Three agents — **Optimist**, **Analyst**, **Critic** — each produce a full deep-dive on every
section. Their outputs are fact-checked, confidence-tagged, and synthesized into one authoritative
document that reflects all three lenses without letting any one distort the whole.

Agent personas live in: `agents/` (part of this skill package)

---

## ⚠️ Prerequisites

This skill requires the **interrogate** skill to be installed.
If it's not present, prompt the user:

> "The hyperthink skill requires the **interrogate** skill. Install it first."

Check by looking for an `interrogate` skill in your skills directory before proceeding.

---

## Pipeline Overview

| Stage | What | How | Output | Max tokens |
|---|---|---|---|---|
| 1 | Master Brief + Persona Variants | Opus subagent (realtime) | `master-brief.md` + `persona-prompts/*.md` | 16,000 |
| 2 | 36 Parallel Deep-Dives (12 sections × 3 agents) | Sonnet batch + Cron 2 | `sections/{optimist,analyst,critic}/NN-title.md` | 24,000 each |
| 3a | Trifecta Audit — Analyst reviews all 3 per section | Sonnet batch + Cron 3a | `audit/NN-title-trifecta.md` (12 files) | 8,000 each |
| 3b | Unified Synthesis Narrative | Sonnet batch + Cron 3b | `synthesis.md` | 80,000 |
| 4 | Executive Brief | Sonnet batch + Cron 4 | `brief.md` + `brief.docx` | 6,000 |

**Estimated cost per run:** ~$55–75 (batch discount on stages 2–4)
**Estimated time:** 8–18 hours end-to-end
**Final delivery:** `brief.docx` delivered via your configured channel when complete
**No checkpoints** — fully automatic after trigger confirmation.

---

## Model Configuration

**Stage 1:** Opus (`anthropic/claude-opus-4-7` or your Opus alias — fall back to default if blocked)
**Stages 2–4:** Sonnet (`claude-sonnet-4-6` or your Sonnet alias — fall back to default if blocked)

Check your model whitelist before running. Note in `pipeline-state.json` which model was used.

---

## Storage

All output written to a persistent directory. **Create these before running:**

```bash
mkdir -p /data/hyperthink/[slug]/sections/optimist
mkdir -p /data/hyperthink/[slug]/sections/analyst
mkdir -p /data/hyperthink/[slug]/sections/critic
mkdir -p /data/hyperthink/[slug]/audit
mkdir -p /data/hyperthink/[slug]/persona-prompts
```

Full structure after a completed run:

```
/data/hyperthink/[topic-slug]/
  pipeline-state.json              # Stage tracking + all job IDs (source of truth)
  master-brief.md                  # Stage 1 Opus output
  persona-prompts/
    optimist-prompts.md            # 12 Optimist section prompts
    analyst-prompts.md             # 12 Analyst section prompts
    critic-prompts.md              # 12 Critic section prompts
  sections/
    optimist/
      01-[title].md                # 12 deep-dives, Optimist perspective
      ...
    analyst/
      01-[title].md                # 12 deep-dives, Analyst perspective
      ...
    critic/
      01-[title].md                # 12 deep-dives, Critic perspective
      ...
  audit/
    01-[title]-trifecta.md         # 12 trifecta comparison + audit docs
    ...
  synthesis.md                     # Stage 3b unified narrative (~50–80k words)
  brief.md                         # Stage 4 executive brief (~4–5k words)
  [slug]-BRIEF.docx                # Final brief deliverable
  [slug]-FULL.docx                 # Full synthesis as docx (on request)
  stage2-job.json                  # Batch job definitions (kept for reference)
  stage3a-job.json
  stage3b-job.json
  stage4-job.json
```

Store under `/data/` if your setup persists that path across restarts (e.g. Railway volume mounts).
Adjust the base path to match your environment.

---

## Trigger Flow

When user sends `/hyperthink [optional topic]`:

1. Check interrogate skill is installed — prompt to install if missing
2. Create output directories (see above)
3. Run **interrogate flow** — ask 4–10 questions in batches of 2 to narrow scope
4. Confirm scope summary — wait for explicit "yes"
5. From here: **fully hands-off** — no more checkpoints, no approvals needed

---

## Interrogate Flow

Ask in batches of 2, adapt based on answers. Minimum 4, maximum 10 questions.

Always cover:
- What is the core subject/concept?
- Primary goal: build it / understand it / evaluate it / compare options?
- Domain/context: tech, business, product, finance, legal, other?
- Known constraints: budget, tech stack, market, regulatory?
- Output focus: new project foundation / existing product / investment thesis / other?
- Is there a specific decision this should inform?

After answers → confirm scope summary → wait for "yes" → proceed to Stage 1.

---

## Topic Slug Rules

Lowercase, hyphens only, max 40 chars.
If slug already exists in `/data/hyperthink/`, append `-v2`, `-v3`.

---

## Stage 1 — Master Brief + Persona Variants

**Model: Opus (fall back to default model if blocked)**
**Method: `sessions_spawn` with your configured Opus model**
**No checkpoint — proceed immediately to Stage 2 after completion.**

### Subagent task:

```
Write the master reasoning brief for this research topic, then generate three
persona-specific prompt variants for the parallel deep-dive stage.

Topic: [TOPIC]
Scope: [SCOPE FROM INTERROGATE]
Goal: [GOAL]
Constraints: [CONSTRAINTS]

━━━ PART A — MASTER BRIEF ━━━

Write the master reasoning brief to /data/hyperthink/[SLUG]/master-brief.md.

The brief must contain:

1. THESIS — Central claim (5–8 sentences). Specific, testable.

2. CORE ASSUMPTIONS — All assumptions (tech, market, feasibility, regulatory).
   Label each: (a) established fact, (b) reasonable assumption, (c) uncertain bet.

3. KEY FACTS — 15–20 most important facts, figures, data points.
   Include sources/indicators where possible.

4. OPEN QUESTIONS — 8–12 genuinely unknown or debated questions.
   These are what the deep-dive sections must attempt to answer.

5. SECTION PLAN — Exactly 12 sections. For each:
   - Title
   - Precise scope (what it covers, what it excludes)
   - 5–7 key questions it must answer
   - How it connects to the thesis
   - What evidence or examples it should engage with
   - Which other sections it relates to

6. REASONING ANCHORS — 8–10 shared principles ALL sections must respect.
   These ensure internal consistency across the document.

7. KNOWN RISKS & FAILURE MODES — 5–8 ways this could go wrong.

━━━ PART B — PERSONA PROMPT VARIANTS ━━━

Using the master brief and section plan above, write three persona-specific
prompt FILES. Each file contains 12 section prompts — one per section —
deeply adapted to that persona's analytical lens.

The personas are defined in:
- [SKILL_DIR]/agents/optimist.md
- [SKILL_DIR]/agents/analyst.md
- [SKILL_DIR]/agents/critic.md

Read each persona file. Internalize the bias, tone, output style, and
behavioral rules for each one. The section prompts MUST produce radically
different outputs — not the same analysis with a different adjective at the top.

For each persona, write a file at:
- /data/hyperthink/[SLUG]/persona-prompts/optimist-prompts.md
- /data/hyperthink/[SLUG]/persona-prompts/analyst-prompts.md
- /data/hyperthink/[SLUG]/persona-prompts/critic-prompts.md

Each file must contain 12 labelled section prompts (SECTION 01 through SECTION 12).

Each section prompt must:
- Open with the full persona character declaration (3–5 sentences embodying the persona)
- Provide the standard section scope + key questions from the master brief
- Restructure the OUTPUT FORMAT to match the persona's style:
  - Optimist: lead with strongest path forward, action verbs, concrete first moves,
    opportunity framing, end each subsection with "what this unlocks"
  - Analyst: lead with precise question statement, structure as claims → evidence →
    confidence level, explicit assumptions labelled, tables where applicable,
    "X with Y% confidence because Z" framing, end with most defensible conclusion
  - Critic: lead with the strongest version of the idea being attacked, then surface
    hidden assumptions, structure as objections ranked Fatal/Serious/Minor, end with
    the single objection that would kill the plan
- Add 3–5 persona-specific bonus questions on top of the master brief questions
- Require word count target (8,000–12,000 words)
- Prohibit generic observations — every claim must be specific

Do NOT water down the personas. If the outputs look similar, the prompts failed.

━━━ AFTER WRITING ALL FILES ━━━

Return ONLY: "Stage 1 complete — master brief + 3 persona prompt files saved"
Do NOT return the file contents as a message.
```

### After Stage 1 subagent returns:
1. `read` master-brief.md to verify it exists
2. `read` each persona-prompts file to verify all 3 exist
3. Write `pipeline-state.json` → `{"stage": "2-pending", "slug": "[slug]", "topic": "[topic]", "created_at": "[ISO]"}`
4. Build `stage2-job.json` (see Stage 2 below)
5. Submit: `python3 /path/to/batch-worker.py submit --job-file .../stage2-job.json`
6. Capture Job ID + Batch ID from stdout
7. Update `pipeline-state.json` → `{"stage": "2", "stage2_job_id": "...", "stage2_batch_id": "..."}`
8. Create Cron 2 (see Cron Poller Pattern)
9. Notify user: "⚙️ **Hyperthink started.** Stage 1 done. 36 deep-dives now running — ETA 3–6h."

---

## Stage 2 — 36 Parallel Deep-Dives

**36 batch requests: 12 Optimist + 12 Analyst + 12 Critic.**
**`max_tokens: 24,000` each. Model: Sonnet.**
**Include `"project": "hyperthink"` in job JSON.**

Request IDs: `opt-s01` through `opt-s12`, `ana-s01` through `ana-s12`, `crit-s01` through `crit-s12`.

### Job JSON structure:

```json
{
  "description": "Hyperthink Stage 2 — [TOPIC] — 36 deep-dives (Optimist / Analyst / Critic)",
  "model": "claude-sonnet-4-6",
  "max_tokens": 24000,
  "project": "hyperthink",
  "requests": [
    {
      "id": "opt-s01",
      "max_tokens": 24000,
      "messages": [{"role": "user", "content": "[MASTER BRIEF + OPTIMIST SECTION 01 PROMPT]"}]
    },
    ... (opt-s02 through opt-s12) ...
    {
      "id": "ana-s01",
      "max_tokens": 24000,
      "messages": [{"role": "user", "content": "[MASTER BRIEF + ANALYST SECTION 01 PROMPT]"}]
    },
    ... (ana-s02 through ana-s12) ...
    {
      "id": "crit-s01",
      "max_tokens": 24000,
      "messages": [{"role": "user", "content": "[MASTER BRIEF + CRITIC SECTION 01 PROMPT]"}]
    },
    ... (crit-s02 through crit-s12) ...
  ]
}
```

### Per-request prompt structure:

```
MASTER BRIEF (do not deviate from thesis, assumptions, or reasoning anchors):
[FULL CONTENT OF master-brief.md]

---

[FULL PERSONA SECTION PROMPT FROM persona-prompts/[persona]-prompts.md — SECTION NN]
```

### Output file naming:
- `sections/optimist/01-[title].md` through `sections/optimist/12-[title].md`
- `sections/analyst/01-[title].md` through `sections/analyst/12-[title].md`
- `sections/critic/01-[title].md` through `sections/critic/12-[title].md`

Title = slugified section title from master brief (e.g., `01-market-landscape.md`).

When Stage 2 completes: write 36 files → build stage3a-job.json → submit Stage 3a → create Cron 3a → self-delete Cron 2.

---

## Stage 3a — Trifecta Audit

**12 batch requests — one per section.**
**Analyst reviews all three perspectives for each section.**
**`max_tokens: 8,000` each. Model: Sonnet.**

### Per-section audit prompt template:

```
You are the Analyst. Your role: evidence-based, neutral, dispassionate.
Calibrated confidence. Show the math. Label assumptions. No cheerleading. No doom-casting.

You will review three perspectives on the same research section and produce a structured
trifecta comparison document.

━━━ MASTER BRIEF EXCERPT ━━━
[SECTION TITLE, SCOPE, AND KEY QUESTIONS FROM master-brief.md FOR THIS SECTION]

━━━ OPTIMIST'S ANALYSIS ━━━
[FULL CONTENT OF sections/optimist/NN-[title].md]

━━━ ANALYST'S OWN ANALYSIS ━━━
[FULL CONTENT OF sections/analyst/NN-[title].md]

━━━ CRITIC'S ANALYSIS ━━━
[FULL CONTENT OF sections/critic/NN-[title].md]

---

YOUR TASK: Produce a structured trifecta comparison document for Section [N]: [TITLE].

Structure:

## 1. SECTION THESIS
What is the central claim all three perspectives are engaging with?

## 2. OPTIMIST AUDIT
Review the Optimist's output claim by claim. For each significant claim:
- Rate confidence: 🟢 HIGH / 🟡 MEDIUM / 🔴 DISPUTED
- Brief justification (1–2 sentences)
Flag the 3–5 claims most likely to mislead if taken at face value.

## 3. ANALYST REFERENCE VIEW
Authoritative take (400–600 words). What does the evidence actually support?

## 4. CRITIC'S TOP OBJECTIONS
Top 5 objections ranked: 🔴 FATAL / 🟠 SERIOUS / 🟡 MINOR
Is each well-founded? What does the Analyst's evidence say?

## 5. NET ASSESSMENT
What a reader should take from this section (300–500 words).
What all three views agree on. Where they diverge. What remains uncertain.

## 6. SECTION KEY TAKEAWAYS (for synthesis use)
10–15 confidence-tagged bullets. Format:
- [🟢/🟡/🔴] [Claim] — [1-sentence justification]
These are the primary input to Stage 3b synthesis — make them precise and complete.

Word target: 3,000–5,000 words.
```

### Output file naming:
- `audit/01-[title]-trifecta.md` through `audit/12-[title]-trifecta.md`

When Stage 3a completes: write 12 audit files → build stage3b-job.json → submit Stage 3b → create Cron 3b → self-delete Cron 3a.

---

## Stage 3b — Unified Synthesis Narrative

**One batch request. `max_tokens: 80,000`. Model: Sonnet.**
**Input: master-brief.md + all 12 trifecta audit docs (~55k–105k tokens — within 200k limit).**
**Target output: 50,000–80,000 words.**

### Synthesis prompt template:

```
You are the editor and synthesizer for a major triple-perspective research report.
Three agents — Optimist, Analyst, Critic — each produced a full deep-dive on every section.
An Analyst-only audit has fact-checked the Optimist's claims and produced confidence-tagged
comparison documents for each section.

Confidence tags: 🟢 HIGH / 🟡 MEDIUM / 🔴 DISPUTED — use them inline throughout.

━━━ MASTER BRIEF ━━━
[FULL CONTENT OF master-brief.md]

━━━ SECTION 01 TRIFECTA AUDIT: [TITLE] ━━━
[FULL CONTENT OF audit/01-[title]-trifecta.md]

[... all 12 trifecta audit docs ...]

---

YOUR TASK — produce the unified synthesis document:

1. TITLE PAGE — title, date, methodology note (triple-perspective: Optimist / Analyst / Critic)
2. TABLE OF CONTENTS
3. EXECUTIVE SUMMARY (1,500–2,000 words) — thesis, top 10 findings (confidence-tagged), top 5 insights, top 3 risks
4. METHODOLOGY NOTE (300–400 words) — how the three-agent approach works, how to read confidence tags
5. SYNTHESIS NARRATIVE (5,000–8,000 words) — connect all 12 sections into one coherent argument
6. FULL SECTIONS (12 total) — for each: intro (200–300 words) + Optimist/Analyst/Critic summaries + net assessment + key takeaways
7. CONFIDENCE MAP — table: per section, list top insights (🟢) and most disputed claims (🔴)
8. CONCLUSION (1,000–1,500 words) — 7–10 prioritized next steps
9. OPEN QUESTIONS REGISTRY — all open threads from all audits, grouped by theme

Word target: 50,000–80,000 words.
Format: clean markdown, H1/H2/H3 throughout.
Confidence tags embedded inline — not just in takeaways.
```

When Stage 3b completes: save `synthesis.md` → build stage4-job.json → submit Stage 4 → create Cron 4 → self-delete Cron 3b.

---

## Stage 4 — Executive Brief

**One batch request. `max_tokens: 6,000`. Model: Sonnet.**
**Input: synthesis.md (~60–80k tokens — within 200k limit).**
**Target output: 4,000–5,000 words.**

### Brief prompt template:

```
SYNTHESIS DOCUMENT:
[FULL CONTENT OF synthesis.md]

---

Write an executive brief of 4,000–5,000 words. Confidence tags (🟢/🟡/🔴) must appear
wherever the underlying evidence warrants them.

Structure:

## TL;DR (150–200 words)
Core problem, what the three-lens analysis revealed, single most important takeaway.

## What the Three Lenses Revealed (300–400 words)
Where all three agreed (high-signal). Where they sharply disagreed (the contested zone).
Which perspective proved most reliable and why.

## The Recommended Approach (400–500 words)
What to do, grounded in 🟢 HIGH-confidence findings.

## Top 12 Findings (400–500 words)
12 numbered findings. Each 2–3 sentences. Confidence-tagged. No generic observations.

## Top 5 Actions (Priority Order) (600–700 words)
What, why, effort estimate, expected outcome, confidence level for the outcome.

## The Critic's Unresolved Objections (200–300 words)
3 Fatal or Serious objections the synthesis did not fully resolve.

## What the Optimist Got Right (But Couldn't Prove) (150–200 words)
2–3 🟡 MEDIUM insights worth acting on as explicit bets, not facts.

## If You Do Nothing (75–100 words)
What happens in 6 and 12 months? Make it specific.
```

### After Stage 4 completes:
1. Save `brief.md`
2. Generate `brief.docx`: `python3 /path/to/md2docx.py brief.md [slug]-BRIEF.docx`
3. Generate `[slug]-FULL.docx` from `synthesis.md` (optional — on request)
4. Update `pipeline-state.json` → `{"stage": "complete", ...}`
5. Self-delete cron
6. Deliver `brief.docx` via your configured channel

---

## Cron Poller Pattern (Mandatory for all stages)

Same idempotent, self-terminating pattern for stages 2, 3a, 3b, 4.

### Two-step cron creation:
1. Create cron with `CRON_ID=PENDING` in payload
2. Immediately `cron update` with actual cron ID injected into payload

### Poller payload — exact 9-step sequence:

```
You are a hyperthink pipeline poller. Run these steps exactly.

━━━ STEP 0 — IDEMPOTENCY GUARD (always first) ━━━
Read: /data/hyperthink/[SLUG]/pipeline-state.json
If "stage" field is NOT "[CURRENT_STAGE]" → EXIT immediately. Do nothing.

━━━ STEP 1 — CHECK LOCAL STATE ━━━
Read: /path/to/batch-jobs/[JOB_ID]/state.json
If status == "complete" AND [OUTPUT_FLAG] == true → skip to STEP 4.
If status == "complete" AND [OUTPUT_FLAG] == false → go to STEP 3.
If status == "processing" or "pending" → go to STEP 2.

━━━ STEP 2 — POLL BATCH ━━━
Run: python3 /path/to/batch-worker.py poll
Re-read state.json. If still not complete → EXIT silently.

━━━ STEP 3 — EXTRACT OUTPUT ━━━
Read results.jsonl. Extract text from each result.
Write output files to /data/hyperthink/[SLUG]/.
Mark [OUTPUT_FLAG] = true in state.json.

━━━ STEP 4 — WRITE IDEMPOTENCY FLAG ━━━
Write pipeline-state.json: {"stage": "[NEXT_STAGE]-pending", ...}
Do this BEFORE submitting the next batch.

━━━ STEP 5 — BUILD + SUBMIT NEXT STAGE ━━━
Check if [NEXT_JOB_FILE].json already exists — if so, skip building.
Submit: python3 /path/to/batch-worker.py submit --job-file .../[NEXT_JOB_FILE].json
Capture Job ID + Batch ID.

━━━ STEP 6 — UPDATE PIPELINE STATE ━━━
Write pipeline-state.json: {"stage": "[NEXT_STAGE]", "job_id": "...", ...}

━━━ STEP 7 — SELF-DELETE THIS CRON ━━━
Call: cron action=remove jobId=[CRON_ID]
Cron ID: [CRON_ID]

━━━ STEP 8 — CREATE NEXT CRON ━━━
Create poller cron for stage [NEXT_STAGE].
Immediately update it with its own ID.

━━━ STEP 9 — NOTIFY ━━━
Send completion message via your configured channel.
```

### Invariants:
- `pipeline-state.json` stage transition written **before** next batch submission — always
- `pipeline-state.json` checked as **STEP 0** — hard gate on exact stage string
- Job file never rebuilt if it already exists on disk
- Cron always self-deletes — if it fails, notify user with the cron ID to remove manually

---

## pipeline-state.json Schema

```json
{
  "stage": "2 | 3a-pending | 3a | 3b-pending | 3b | 4-pending | 4 | complete",
  "slug": "topic-slug",
  "topic": "Full topic name",
  "created_at": "ISO timestamp",
  "stage2_job_id": "...",
  "stage2_batch_id": "...",
  "stage2_complete": true,
  "stage2_sections": 36,
  "stage2_completed_at": "...",
  "stage3a_job_id": "...",
  "stage3a_batch_id": "...",
  "stage3a_complete": true,
  "stage3a_sections": 12,
  "stage3a_completed_at": "...",
  "stage3b_job_id": "...",
  "stage3b_batch_id": "...",
  "stage3b_complete": true,
  "stage3b_word_count": 65000,
  "stage3b_completed_at": "...",
  "stage4_job_id": "...",
  "stage4_batch_id": "...",
  "stage4_complete": true,
  "stage4_word_count": 4500,
  "brief_docx": "/data/hyperthink/[slug]/[slug]-BRIEF.docx",
  "completed_at": "...",
  "last_error": null
}
```

---

## Token & Cost Reference

| Stage | Requests | max_tokens out | Est. input tokens | Est. cost (batch) |
|---|---|---|---|---|
| 1 | 1 | 16,000 | ~5,000 | ~$2.50 (realtime Opus) |
| 2 | 36 | 24,000 each | ~9,000 each | ~$35–45 |
| 3a | 12 | 8,000 each | ~43,000 each | ~$8–12 |
| 3b | 1 | 80,000 | ~58k–106k | ~$8–12 |
| 4 | 1 | 6,000 | ~60k–81k | ~$2–3 |
| **Total** | | | | **~$56–75/run** |

Batch discount (50%) applies to stages 2–4. Stage 1 is realtime.

**Context window note:** Anthropic's 200k limit is INPUT only — output tokens are separate.
Stage 3b worst-case input: ~106k tokens (well within limit). All stages verified safe.

---

## Error Handling

- Any batch failure → notify user immediately with stage + error message
- Stage 2 partial failure → notify, ask whether to retry failed sections or proceed
- Stage 3a partial failure → same
- Never silently swallow errors
- All partial results saved even on failure — work is never lost
- All errors written to `pipeline-state.json` → `last_error` field

---

## Supporting Scripts

This skill requires two supporting scripts. Spec files are included in `scripts/` — have your AI
implement them for your environment before running the pipeline.

### `scripts/batch-worker-spec.md` → implement as `batch-worker.py`
Handles Anthropic Batch API submission, polling, and result fetching.
- `submit` — send a batch job, save state locally
- `poll` — check pending jobs, download results when done, notify user
- `status` — print a summary table of all jobs
- stdlib only (no third-party packages except your notification layer)
- See spec for full API call sequences, storage layout, and state.json schema

### `scripts/md2docx-spec.md` → implement as `md2docx.py`
Converts Markdown to .docx — used to generate the final executive brief.
- Requires: `pip install python-docx`
- Handles all hyperthink output elements: H1-H4, bold/italic/code, bullets, numbered lists,
  code blocks, horizontal rules, and unicode confidence tags (🟢 🟡 🔴)
- See spec for exact styling, colours, fonts, and parsing logic

**First-time setup:**
1. Read `scripts/batch-worker-spec.md` → implement `batch-worker.py` in your workspace
2. Read `scripts/md2docx-spec.md` → implement `md2docx.py` in your workspace
3. Install python-docx: `pip install python-docx`
4. Update the batch submission paths in the cron pollers to match where you saved the scripts
5. Run `/hyperthink` — the skill handles the rest
