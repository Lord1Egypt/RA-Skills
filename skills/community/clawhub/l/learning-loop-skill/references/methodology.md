# Learning Loop Methodology — GEARS

## The GEARS Feedback Loop

**G**ather → **E**xecute → **A**nalyze → **R**etry → **S**ynthesize

Battle-tested over 23+ days with consistent 60% -> 87%+ improvement per cycle, 100% gap recovery rate, and 9+ major topics mastered.

### Why GEARS?

Tight feedback loops = faster learning. Each phase has a distinct purpose. The cycle mirrors how humans study for exams: gather knowledge, test yourself, analyze gaps, retry, synthesize mastery.

### Session Details

#### S1 — Gather: Research & Create Tests

**Purpose:** Research the subtopic and create verifiable test questions.

**Process:**
1. Read `state.json` to get current subtopic
2. Search for information using available tools (try web search, Tavily, SerpAPI — use whatever is available, fall back gracefully)
3. Create 10-15 test questions WITH correct answers
4. Write to `sessions/day-NN/s1-research.md`
5. Update `state.json`: `currentSession` -> `"S2"`

**Question Design Rules (Critical for Quality):**
- Questions MUST have verifiable correct answers — not opinions
- Use specific, testable formats:
  - "What is [specific concept]?" -> [specific correct answer]
  - "Given [scenario], what happens?" -> [specific outcome]
  - "What are the 3 types of [X]?" -> [enumerated list]
  - "True or false: [statement]" -> [T/F with explanation]
- Include edge cases and exceptions (these reveal real understanding)
- Mix difficulty: 5 foundational, 5 intermediate, 3-5 advanced
- NO vague "explain X" questions without specific expected answers

**s1-research.md Format:**
```markdown
# S1 Research: [Subtopic] — Day [N]

## Questions

1. [Question text]
2. [Question text]
...

---
## ANSWERS (S2 agent: STOP READING HERE)
---

1. [Correct answer with brief explanation]
2. [Correct answer with brief explanation]
...

## Sources
- [Source 1]
- [Source 2]
```

#### S2 — Execute: Blind Test

**Purpose:** Answer all questions from general knowledge without looking at answers.

**Process:**
1. Read `state.json` — verify `currentSession == "S2"`
2. Read `s1-research.md` — STOP at the `ANSWERS` separator line
3. Answer each question from memory/general knowledge
4. After answering ALL questions, read the answers section
5. Score each answer: correct (1), partial (0.5), wrong (0)
6. Calculate aggregate percentage
7. Write answers to `s2-test.md`
8. Write each wrong/partial answer to `s2-failures.md` with:
   - What you said
   - What the correct answer is
   - Why you were wrong (category: missing knowledge, wrong model, confusion, edge case)
9. Update `state.json`: add/update history entry with `s2Score` = score, set `currentSession` -> `"S3"`
10. Notify user: "Day X S2 initial score: Y%"

**Scoring Rules:**
- Exact match or semantically equivalent = 1 point
- Partially correct (got the concept but missed details) = 0.5 points
- Wrong or blank = 0 points
- Score = (total points / number of questions) * 100

#### S3 — Analyze: Diagnose Gaps

**Purpose:** Research each failure specifically and prepare fixes.

**Process:**
1. Read `state.json` — verify `currentSession == "S3"`
2. Read `s2-failures.md`
3. For each failure:
   - Categorize: missing knowledge, wrong mental model, confusion between similar concepts, edge case missed
   - Search specifically for the gap (use available search tools)
   - Write corrected understanding with sources
4. Write analysis to `s3-analysis.md`
5. Update `state.json`: `currentSession` -> `"S4"`

**s3-analysis.md Format:**
```markdown
# S3 Gap Analysis: [Subtopic] — Day [N]

## Gap 1: [Description]
- **Category:** [missing/wrong-model/confusion/edge-case]
- **What I got wrong:** [specific error]
- **Correct understanding:** [researched answer with sources]
- **Why I was wrong:** [root cause]

## Gap 2: ...

## Frameworks Prepared for S4
- [Framework 1]: [brief description]
- [Framework 2]: [brief description]
```

#### S4 — Retry: Re-test & Improve

**Purpose:** Re-answer original questions using new understanding from S3.

**Process:**
1. Read `state.json` — verify `currentSession == "S4"`
2. Read `s3-analysis.md` (the researched fixes)
3. Read original questions from `s1-research.md` (questions section only)
4. Re-answer ALL questions using new understanding
5. Score against correct answers (same rubric as S2)
6. Calculate improvement: S4 score - S2 score
7. Write to `s4-retry.md`
8. Update `state.json`: update history entry with `s4Score` = score and `improvement` = s4Score - s2Score, set `currentSession` -> `"S5"`
9. Notify user: "Day X S4 retry: Y% (+Z% improvement)"
10. **Create S5 cron job** — one-shot, runs in 30 minutes

#### S5 — Synthesize: Consolidate & Decide

**Purpose:** Consolidate learning, update knowledge base, decide next steps.

**Process:**
1. Read ALL day's session files (s1 through s4)
2. Write synthesis to `s5-synthesis.md`:
   - What was learned
   - What improved (S2 -> S4 delta)
   - What's still weak
   - Connections to previously mastered subtopics
3. Update `knowledge/validated.md` — append mastered content
4. Decision logic:
   - Score >= 85%: Mark subtopic mastered, advance `currentSubtopicIndex`
   - Score 50-84%: Keep same subtopic, note focus areas for tomorrow
   - Score < 50%: Set `status` to `"needs_intervention"`, notify user
5. If `currentSubtopicIndex >= curriculum.length - 2`: trigger curriculum expansion
6. If curriculum complete: notify user to continue (deeper/broader/apply/done)
7. If continuing: create tomorrow's S1-S4 cron jobs
8. Notify user with day summary

## Gap Categories

| Category | Symptom | Fix Strategy |
|----------|---------|-------------|
| Missing knowledge | Complete blank | Research from scratch |
| Wrong mental model | Confidently wrong | Unlearn, then re-learn |
| Confusion | Mixed up similar concepts | Create clear differentiators |
| Edge case | Know rule, missed exception | Study exceptions specifically |

## Historical Performance

Across 23+ days of actual use:
- Average initial score (S2): ~60%
- Average retry score (S4): ~87%
- Average improvement per cycle: +27%
- Gap recovery rate: 100%
- Consecutive successful sessions: 26/26
