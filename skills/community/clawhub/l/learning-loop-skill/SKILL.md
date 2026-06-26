---
name: learning-loop-skill
description: Autonomous structured learning for mastering complex topics through cron-based 5-session feedback loops. Use when user wants to deeply learn a subject (e.g., "learn X", "teach me Y", "master Z", "deep dive into X", "I want to understand X deeply"). NOT for quick overviews, simple factual questions, or topics without clear right/wrong answers.
---

# Learning Loop — The GEARS System

Master complex topics through autonomous cron-based learning using the **GEARS** feedback loop:

| Phase | Session | What Happens |
|-------|---------|-------------|
| **G**ather | S1 | Research concepts, create test questions |
| **E**xecute | S2 | Take the test blind, document failures |
| **A**nalyze | S3 | Diagnose why you failed, research solutions |
| **R**etry | S4 | Apply fixes, measure improvement |
| **S**ynthesize | S5 | Validate mastery, adjust schedule |

The agent sets up a learning pipeline during an interactive session; isolated cron agents execute the 5 GEARS sessions autonomously using a pre-generated playbook.

## Architecture

When the user says "learn X", the agent:
1. Parses topic, researches it, breaks into a curriculum (15-20 subtopics ordered by prerequisites)
2. Generates a self-contained `playbook.md` — complete instructions for ALL sessions
3. Creates `state.json` — progress tracker and baton between sessions
4. Shows schedule to user, gets confirmation
5. Creates cron jobs for S1-S4 (S4 creates S5 when it finishes)
6. Done. Cron agents take over.

**Critical design:** Isolated cron agents have NO skill context. They read ONLY `playbook.md` + `state.json`. The playbook must be completely self-contained.

## Setup Flow

### Step 1: Parse Topic

Extract topic from user input and slugify:
- "learn machine learning" -> `machine-learning`
- "teach me database design" -> `database-design`
- "master Docker" -> `docker`

Slugify: lowercase, hyphens for spaces, strip special chars.

### Step 2: Research & Build Curriculum

Use available search tools (web search, Tavily, SerpAPI — try what's available, fall back gracefully) to research the topic. Break into 15-20 subtopics ordered by prerequisites.

Write curriculum to `curriculum.md` with:
- Subtopic name
- Why it matters
- Prerequisites (which earlier subtopics are needed)
- Estimated difficulty (1-3)

### Step 3: Generate Playbook

Generate `playbook.md` from the template in `references/playbook-template.md`. This is the **most important file** — customize it for the specific topic but keep the session execution instructions generic and self-contained.

Target: under 200 lines so isolated agents don't hit token limits.

### Step 4: Initialize State

Create the folder structure and initial `state.json` by running the pipeline creation script. The script is located in this skill's `scripts/` directory:
```bash
bash <skill-dir>/scripts/create_pipeline.sh <topic-slug> "<Topic Display Name>"
```

Where `<skill-dir>` is the directory containing this SKILL.md file. The script respects the `OPENCLAW_WORKSPACE` env var (defaults to `~/.openclaw/workspace`). See `references/state-schema.md` for all state fields.

### Step 5: Show Schedule & Confirm

Display to user:
```
Learning Pipeline: [Topic]

Curriculum: [N] subtopics starting with "[first subtopic]"
Sessions per day: S1 (research) -> S2 (test) -> S3 (analyze gaps) -> S4 (retry) -> S5 (synthesize)

Timing:
  S1: +30 min from now (research + create test questions)
  S2: +4 hours (blind test from memory)
  S3: +8 hours (diagnose failures + research gaps)
  S4: +12 hours (retry with new understanding)
  S5: created by S4 on completion (synthesize + decide next)

Notifications: You'll get updates at S2 (initial score), S4 (retry score), and S5 (summary + next steps).

Confirm to start, or adjust timing/notification preferences.
```

### Step 6: Create Cron Jobs

After user confirms, read `~/.openclaw/cron/jobs.json`, append 4 cron jobs (S1-S4) to the `jobs` array, and write back. The file format is `{ "version": 1, "jobs": [...] }` — always preserve existing jobs. S5 is NOT pre-created — S4 creates it when it completes.

Each cron job entry uses this format:
```json
{
  "id": "learning-[topic]-s[N]-day[DD]",
  "agentId": "main",
  "name": "Learning [Topic] S[N] Day [DD]",
  "enabled": true,
  "createdAtMs": <timestamp>,
  "updatedAtMs": <timestamp>,
  "schedule": {
    "kind": "once",
    "atMs": <calculated_timestamp>
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "You are a learning agent. Read this file for complete instructions: memory/learning/[topic-slug]/playbook.md\n\nThen read state.json in the same folder for current session and subtopic.\n\nYour session: S[N]\n\nExecute the session per playbook instructions. Write outputs, update state.json, handle notifications and follow-up crons as specified."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "<user-configured>"
  }
}
```

**Important:** Calculate `atMs` timestamps based on user-confirmed timing. Default spacing: S1 +30min, S2 +4h, S3 +8h, S4 +12h from setup time.

If the user has notification preferences configured (Telegram, etc.), set `delivery` accordingly. Otherwise omit delivery and the playbook instructs agents to write notifications to a file.

## Session Summary (GEARS)

| GEARS | Session | What | Key Output |
|-------|---------|------|------------|
| Gather | S1 | Research subtopic, create 10-15 test questions WITH answers | `s1-research.md` |
| Execute | S2 | Answer questions blind (no peeking), score objectively | `s2-test.md`, `s2-failures.md` |
| Analyze | S3 | Diagnose each failure, research gaps specifically | `s3-analysis.md` |
| Retry | S4 | Re-answer using new understanding, compare scores | `s4-retry.md` + creates S5 cron |
| Synthesize | S5 | Synthesize, update validated knowledge, decide next subtopic | `s5-synthesis.md` |

For full session details, see `references/methodology.md`.

For the playbook template that gets customized per topic, see `references/playbook-template.md`.

For the state.json schema, see `references/state-schema.md`.

## Folder Structure (Per Topic)

```
memory/learning/[topic-slug]/
├── playbook.md           <- Self-contained instructions for cron agents
├── state.json            <- Dynamic progress tracker (baton between sessions)
├── curriculum.md         <- Topic breakdown with subtopics
├── sessions/
│   └── day-NN/
│       ├── s1-research.md
│       ├── s2-test.md
│       ├── s2-failures.md
│       ├── s3-analysis.md
│       ├── s4-retry.md
│       └── s5-synthesis.md
└── knowledge/
    └── validated.md      <- Accumulated mastered knowledge
```

## Scoring & Progression

| S4 Score | Action |
|----------|--------|
| >= 85% | Mark subtopic mastered, advance to next in curriculum |
| 50-84% | Retry same subtopic tomorrow, focus on remaining gaps |
| < 50% | Flag for user intervention — topic may need prerequisite work |

## Curriculum Expansion

When S5 detects `currentSubtopicIndex >= curriculum.length - 2`:
1. Research advanced topics beyond what's been mastered
2. Write `curriculum-preview.md`
3. Notify user: "2 topics remaining. Previewing next phase: [topics]. Continue?"
4. On confirmation (or 24h default): append to curriculum, continue

## Scripts

- `scripts/create_pipeline.sh <topic-slug>` — Create folder structure + initial state.json
- `scripts/check_progress.sh [topic-slug]` — Show status of active learning topics

## Pause, Resume & Intervention

**Pause:** User says "pause learning [topic]" → set `status` to `"paused"` in `state.json`, disable pending cron jobs for that topic in `jobs.json`.

**Resume:** User says "resume learning [topic]" → set `status` to `"in_progress"`, read `currentSession` from state, create cron jobs from the current session onward.

**Intervention (score < 50%):** When S5 sets `status` to `"needs_intervention"`:
1. No further crons are created automatically
2. User is notified with the specific subtopic and score
3. User can: adjust curriculum (remove/reorder subtopics), add prerequisite subtopics, or manually set `status` back to `"in_progress"` and `currentSession` to `"S1"` to retry

## When NOT to Use

- Quick overview or summary needed (just answer directly)
- Simple factual question (no learning loop needed)
- User only wants information, not mastery
- Topic too broad without focus (e.g., "learn everything")
- Topic has no clear right/wrong answers (subjective topics don't self-assess well)
