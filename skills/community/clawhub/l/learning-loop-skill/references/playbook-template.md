# Learning Playbook: [TOPIC]

You are an autonomous learning agent executing a GEARS session (Gather → Execute → Analyze → Retry → Synthesize). This file contains ALL instructions you need. Read this file + `state.json` (same folder) to know what to do.

## Your Task

1. Read `state.json` to find `currentSession` (S1, S2, S3, S4, or S5)
2. Find that session's section below
3. Execute it exactly
4. Write outputs to the specified files
5. Update `state.json` when done

## File Paths

All paths are relative to this playbook's directory:
- State: `state.json`
- Sessions: `sessions/day-[NN]/` (pad day number: day-01, day-12)
- Knowledge: `knowledge/validated.md`
- Curriculum: `curriculum.md`

## Topic Context

**Topic:** [TOPIC_NAME]
**Current subtopic:** Read from `state.json` field `curriculum[currentSubtopicIndex]`

---

## S1 — Gather: Research & Create Tests

**Goal:** Research the current subtopic and create 10-15 test questions with verifiable correct answers.

**Steps:**
1. Read `state.json` — get `currentSubtopicIndex` and look up the subtopic in `curriculum` array
2. Read `curriculum.md` for subtopic context and prerequisites
3. If `knowledge/validated.md` exists, read it for prior mastered content
4. Search for information on the subtopic. Try these tools in order (use whatever works):
   - Web search tool
   - Tavily search
   - SerpAPI
   - If no search tools available, use your training knowledge and note "no external search available" in output
5. Create 10-15 test questions WITH correct answers. Rules:
   - Every question must have a specific, verifiable correct answer
   - No opinion questions or vague "explain X" without expected answer
   - Mix: 5 foundational, 5 intermediate, 3-5 advanced
   - Include edge cases
6. Create the day directory: `sessions/day-[NN]/` (use `currentDay` from state.json)
7. Write to `sessions/day-[NN]/s1-research.md` in this format:

```
# S1 Research: [Subtopic] — Day [N]

## Questions

1. [Question]
2. [Question]
...

---
## ANSWERS — DO NOT READ DURING S2
---

1. [Answer with brief explanation]
2. [Answer]
...

## Sources
- [Source URLs or "training knowledge"]
```

8. Update `state.json`: set `currentSession` to `"S2"`, set `updatedAt` to current ISO timestamp

---

## S2 — Execute: Blind Test

**Goal:** Answer all questions from memory. Do NOT look at answers until you've answered everything.

**Steps:**
1. Read `state.json` — verify `currentSession` is `"S2"`
2. Read `sessions/day-[NN]/s1-research.md` — **STOP reading at the "ANSWERS" separator line**
3. Answer every question from your general knowledge
4. After answering ALL questions, read the answers section
5. Score each answer:
   - Correct or semantically equivalent = 1 point
   - Partially correct = 0.5 points
   - Wrong or blank = 0 points
6. Calculate: `score = (total_points / num_questions) * 100`
7. Write to `sessions/day-[NN]/s2-test.md`:

```
# S2 Blind Test: [Subtopic] — Day [N]

## Answers
1. [Your answer] — CORRECT/PARTIAL/WRONG
2. ...

## Score: [X]% ([points]/[total])
```

8. Write failures to `sessions/day-[NN]/s2-failures.md`:

```
# S2 Failures: [Subtopic] — Day [N]

## Failure 1: Q[N] — [brief description]
- **My answer:** [what you said]
- **Correct answer:** [what it should be]
- **Category:** [missing-knowledge | wrong-model | confusion | edge-case]
- **Why wrong:** [brief root cause]
```

9. Update `state.json`: set `currentSession` to `"S3"`, set `history` entry with `s2Score`
10. **Notify user** (write to delivery or use message tool): "Day [N] initial score: [X]%"

---

## S3 — Analyze: Diagnose & Research Gaps

**Goal:** Research each failure from S2 and prepare corrected understanding.

**Steps:**
1. Read `state.json` — verify `currentSession` is `"S3"`
2. Read `sessions/day-[NN]/s2-failures.md`
   - **If the file doesn't exist or has no failures (100% S2 score):** Write a brief `s3-analysis.md` noting "No gaps found — perfect score." Update `state.json`: set `currentSession` to `"S4"`. Skip remaining steps.
3. For EACH failure:
   - Search specifically for the gap (try available search tools)
   - Write corrected understanding with evidence
   - Categorize the gap type
4. Write to `sessions/day-[NN]/s3-analysis.md`:

```
# S3 Gap Analysis: [Subtopic] — Day [N]

## Gap 1: [Description]
- **Category:** [missing-knowledge | wrong-model | confusion | edge-case]
- **What I got wrong:** [specific error]
- **Correct understanding:** [researched answer]
- **Source:** [URL or reference]

## Frameworks for S4
- [Key insight 1]
- [Key insight 2]
```

5. Update `state.json`: set `currentSession` to `"S4"`

---

## S4 — Retry: Re-test & Create S5

**Goal:** Re-answer original questions with new understanding. Create S5 cron.

**Steps:**
1. Read `state.json` — verify `currentSession` is `"S4"`
2. Read `sessions/day-[NN]/s3-analysis.md` (your researched fixes)
3. Read questions from `sessions/day-[NN]/s1-research.md` (questions section)
4. Re-answer ALL questions using new understanding
5. Score against correct answers (same rubric as S2)
6. Write to `sessions/day-[NN]/s4-retry.md`:

```
# S4 Retry: [Subtopic] — Day [N]

## Answers
1. [Answer] — CORRECT/PARTIAL/WRONG — [what changed from S2]
...

## Score: [X]% (S2 was [Y]%, improvement: +[Z]%)
```

7. Update `state.json`: set `currentSession` to `"S5"`, update `history` entry with `s4Score` and `improvement`
8. **Notify user**: "Day [N] retry: [X]% (+[Z]% improvement)"
9. **Create S5 cron job** — read `~/.openclaw/cron/jobs.json`, append a new entry to the `jobs` array, and write the file back:

```json
{
  "version": 1,
  "jobs": [
    ...existing jobs...,
    {
      "id": "learning-[TOPIC_SLUG]-s5-day[NN]",
      "agentId": "main",
      "name": "Learning [TOPIC] S5 Day [NN]",
      "enabled": true,
      "createdAtMs": [now],
      "updatedAtMs": [now],
      "schedule": { "kind": "once", "atMs": [now + 1800000] },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "You are a learning agent. Read: memory/learning/[TOPIC_SLUG]/playbook.md then state.json. Your session: S5. Execute per playbook."
      }
    }
  ]
}
```

Add a `delivery` section to the job if `state.json` has notification config. **Important:** Always preserve existing jobs in the array — read first, append, write back.

---

## S5 — Synthesize: Consolidate & Decide Next

**Goal:** Consolidate learning, update knowledge base, schedule next day.

**Steps:**
1. Read ALL session files for today (s1-research, s2-test, s2-failures, s3-analysis, s4-retry)
2. Write to `sessions/day-[NN]/s5-synthesis.md`:

```
# S5 Synthesis: [Subtopic] — Day [N]

## What Was Learned
- [Key concept 1]
- [Key concept 2]

## Score Progression
- S2 (initial): [X]%
- S4 (retry): [Y]% (+[Z]%)

## Remaining Weaknesses
- [Any gaps still present]

## Connections to Prior Knowledge
- [How this connects to previously mastered subtopics]
```

3. Append mastered content to `knowledge/validated.md`:

```
## [Subtopic] (mastered Day [N], score: [X]%)
- [Key validated fact 1]
- [Key validated fact 2]
```

4. **Decision logic** — read S4 score from `state.json`:

   **Score >= 85%:**
   - Set subtopic as mastered in history
   - Increment `currentSubtopicIndex`
   - Set `currentSession` to `"S1"`, increment `currentDay`

   **Score 50-84%:**
   - Keep same `currentSubtopicIndex`
   - Set `focusAreas` in the current history entry — list the specific concepts still weak (these guide tomorrow's S1 research)
   - Set `mastered` to `false` in history entry
   - Set `currentSession` to `"S1"`, increment `currentDay`

   **Score < 50%:**
   - Set `status` to `"needs_intervention"`
   - Notify user: "Score below 50% on [subtopic]. May need prerequisite work."
   - Do NOT create next day's crons

5. **Curriculum expansion check:**
   If `currentSubtopicIndex >= curriculum.length - 2`:
   - Research advanced subtopics beyond current curriculum
   - Write `curriculum-preview.md`
   - Notify user: "2 subtopics remaining. Next phase preview: [topics]. Reply to confirm."

6. **If curriculum complete:**
   - Set `status` to `"curriculum_complete"`
   - Notify user with full summary + options: go deeper, go broader, apply knowledge, or finish

7. **If continuing (score >= 50% and curriculum not complete):**
   Read `~/.openclaw/cron/jobs.json`, append tomorrow's S1-S4 cron jobs to the `jobs` array, and write back. Use `dailyStartHour` from `state.json` (default 9) as the base hour, with timing offsets from `sessionTiming`. Always preserve existing jobs in the array.

8. **Notify user** with day summary: scores, mastery status, next subtopic
