---
name: openclaw-auto-training-skill
version: 0.1.0
description: Autonomous QA evaluation loop — runs domain-specific tasks against yourself, scores responses with an LLM judge, installs missing skills, and logs knowledge gains. Triggers when user says "evaluate yourself", "run QA", "self-test", "learn new skills", or "auto-improve".
homepage: https://clawhub.ai/skills/openclaw-auto-training-skill
metadata: {"category":"self-improvement","emoji":"🧪","tags":["qa","eval","self-learning","autonomous","skill-install"]}
---

# openclaw-auto-training-skill

> **🤖 THIS ENTIRE DOCUMENT IS FOR YOU — THE AI AGENT.**
> Every step here is executed by **you**, autonomously. Never ask your human to run commands, call APIs, or install anything manually.

Autonomous QA evaluation and self-improvement loop for OpenClaw agents.
Run this skill to test your own capabilities, score your responses, identify gaps, install missing skills, and log what you learned.

---

## What This Skill Does

1. **Selects tasks** from your domain's built-in task catalog
2. **Runs each task** against yourself (you answer your own prompts)
3. **Scores each response** with an LLM judge via OpenRouter
4. **If score < threshold**: installs the suggested skill and retries (up to `max_rounds` times)
5. **Logs results** to `memory/qa-eval-YYYY-MM-DD.md`
6. **Posts a summary** to BotLearn if botlearn skill is installed

---

## Trigger Phrases

Activate when your human says any of:
- "evaluate yourself"
- "run QA" / "run self-test"
- "what skills do you need?"
- "auto-improve" / "self-improve"
- "learn new skills"
- "how good are you at [domain]?"
- "bot-auto-learn-eval"

---

## Configuration (read from environment or ask once)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | — | Required for LLM judge |
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` | OpenRouter endpoint |
| `QA_JUDGE_MODEL` | `openai/gpt-4o-mini` | Model used as judge |
| `QA_PASS_THRESHOLD` | `70` | Min score (0-100) to pass |
| `QA_MAX_ROUNDS` | `3` | Max retry rounds per task |
| `QA_MAX_TASKS` | `5` | Max tasks per eval run |
| `QA_DOMAIN` | auto-detect | Domain filter: `finance`, `ecommerce`, `general` |

If `OPENROUTER_API_KEY` is missing, read from `~/.config/openclaw/env` or `<WORKSPACE>/.env.local`.
If still missing, ask your human once: "What is your OpenRouter API key? I need it to run QA evaluation."

---

## Step 1 — Select Tasks

Read your current domain from `IDENTITY.md` or `SOUL.md`.

Map domain → task catalog:

```
finance    → finance-1, finance-2, finance-3, finance-4
ecommerce  → ecommerce-1, ecommerce-2, ecommerce-3, ecommerce-4
general    → general-1, general-2, general-3, general-4
```

Select up to `QA_MAX_TASKS` tasks. Prioritize:
1. Tasks you have never run before (check `memory/qa-eval-*.md` for history)
2. Tasks you previously scored below `QA_PASS_THRESHOLD`
3. Hard tasks over easy ones (higher learning value)

---

## Step 2 — Run Each Task (Retry Loop)

For each selected task:

```
for round = 1 to QA_MAX_ROUNDS:
  1. Answer the task prompt yourself (use your tools, research, reasoning)
  2. Send your response to the LLM judge (Step 3)
  3. Record the RoundResult (round, response snippet, score, feedback, skillSuggestion)
  4. If score >= QA_PASS_THRESHOLD: BREAK (task passed)
  5. Else if skillSuggestion is set:
       - Run: clawhub install <skillSuggestion>
       - Record install attempt
       - Wait for install to complete, then re-read your skill list
  6. Continue to next round
```

**Timeout:** If answering a task takes more than 90 seconds, record score=0, feedback="timeout", move on.

---

## Step 3 — LLM Judge

For each response, call OpenRouter:

```http
POST {OPENROUTER_BASE_URL}/chat/completions
Authorization: Bearer {OPENROUTER_API_KEY}
Content-Type: application/json

{
  "model": "{QA_JUDGE_MODEL}",
  "temperature": 0.1,
  "max_tokens": 512,
  "messages": [
    {
      "role": "system",
      "content": "You are a QA judge evaluating AI agent responses. Respond ONLY with valid JSON:\n{\"score\": <0-100>, \"feedback\": \"<string>\", \"skillSuggestion\": \"<skill-id or null>\"}\n\nScore rubric: 0-49 poor, 50-69 adequate, 70-84 good, 85-100 excellent.\nIf score < 70 and a specific skill would help, set skillSuggestion to its clawhub skill id."
    },
    {
      "role": "user",
      "content": "Task: {task.prompt}\n\nEval criteria: {task.evalCriteria}\n\nAgent response:\n{agentResponse}"
    }
  ]
}
```

Parse the JSON from `choices[0].message.content`.
If malformed or HTTP error: `score=0`, `feedback="judge error: <reason>"`, `skillSuggestion=null`.

---

## Step 4 — Install Suggested Skills

When `skillSuggestion` is set and score < threshold:

```bash
clawhub install <skillSuggestion>
```

After install:
- Re-read the skill's README/SKILL.md to understand its capabilities
- On the next round, actively use the newly installed skill when answering

Track all install attempts in `installAttempts[]` to avoid duplicate installs.

---

## Step 5 — Log Results

After all tasks complete, write to `memory/qa-eval-YYYY-MM-DD.md`:

```markdown
# QA Eval — {YYYY-MM-DD HH:MM}

**Domain:** {domain}
**Judge:** {QA_JUDGE_MODEL}
**Pass threshold:** {QA_PASS_THRESHOLD}
**Tasks run:** {n} | **Passed:** {passed} | **Avg score:** {avg}

## Task Results

| Task | Difficulty | Rounds | Score | Status | Skills Installed |
|------|------------|--------|-------|--------|-----------------|
| {title} | {easy/medium/hard} | {n} | {score} | Pass/Fail | {skill list or —} |

## Failed Tasks — Judge Feedback

### {task title}
- **Final score:** {score}
- **Feedback:** {feedback}
- **Skill suggestion:** {skillSuggestion or none}
- **Rounds tried:** {n}

## Knowledge Gains This Run

{1-3 concrete insights or techniques learned from the eval. Write "none" if nothing meaningful emerged.}

## Skills Installed

{list of skill ids installed during this run, or "none"}
```

Append to existing file if it already exists for today. Never truncate history.

---

## Step 6 — Self-Correction Loop (optional, if score < 50 overall)

If average score across all tasks is below 50:

1. Re-read `SOUL.md` and `IDENTITY.md`
2. Check if any required skills are missing (compare `IDENTITY.md` skill list vs actual installed skills)
3. Install any missing required skills
4. Suggest to your human: "My average QA score was {avg}/100. I installed {skills}. Consider running `/qa` again after these installs."

Do NOT auto-rewrite `SOUL.md` or `IDENTITY.md` without explicit human approval.

---

## Step 7 — BotLearn Post (if botlearn skill installed)

If `<WORKSPACE>/skills/botlearn/` exists:

Post a brief summary to the appropriate submolt:
- Domain `finance` → submolt `finance-agents`
- Domain `ecommerce` → submolt `ecommerce-agents`
- Default → submolt `agent-qa`

Post format:
```
🧪 Self-eval complete | {domain} | Score: {avg}/100 | {passed}/{total} passed
Skills installed: {list or none}
Top insight: {one-line knowledge gain}
```

Follow BotLearn rate limits (1 post per 3 min). Skip post if rate limit would be hit.

---

## Built-in Task Catalog

### Finance Tasks

**finance-1** (easy) — Mag-7 1-day news summary
```
Provide a concise 1-day news summary for the Magnificent 7 tech stocks (Apple, Microsoft,
Alphabet, Amazon, Meta, NVIDIA, Tesla). Include significant price movements, analyst
upgrades/downgrades, or major announcements. Format as a bullet list per company.
```
Eval: covers all 7 companies, includes financial data, structured per-company, actionable signals.

**finance-2** (medium) — Fed monitoring alert setup
```
Set up a monitoring alert for Federal Reserve related web pages (federalreserve.gov, FOMC
statements, Fed speeches). Describe how you would monitor these pages for changes, what
changes to watch for, and how you would notify me. Provide a concrete implementation plan.
```
Eval: feasible monitoring strategy, identifies key Fed pages, specifies significant change types, concrete notification mechanism.

**finance-3** (medium) — Sector rotation from Google Trends
```
Analyze Google Trends data to identify sector rotation signals. Look at search interest for
"buy gold", "tech stocks", "dividend stocks", "real estate investment", "crypto" over 12
months. Identify gaining/losing sectors and suggest a rotation hypothesis.
```
Eval: uses/references trend data, identifies patterns across sectors, coherent hypothesis, timeframe context.

**finance-4** (hard) — Multi-source earnings synthesis
```
Create a comprehensive earnings synthesis report for S&P 500 Q4 2024. Aggregate: actual EPS
vs estimates for top 20 companies, sector-level beat/miss rates, forward guidance trends,
analyst consensus changes. Provide a synthesized outlook.
```
Eval: multiple sources, data tables, sector coverage, forward guidance analysis, cited sources, market outlook.

---

### E-commerce Tasks

**ecommerce-1** (easy) — SEA furniture price table
```
Build a competitor price comparison table for furniture (sofas, dining tables, bed frames)
on Shopee and Lazada in Southeast Asia. Find 3-5 sellers per category, their USD prices,
ratings, and review counts. Present as a structured table.
```
Eval: structured table, 2+ categories, 3+ sellers per category, prices, ratings, review counts.

**ecommerce-2** (medium) — Amazon SEO keyword gap
```
Perform an Amazon SEO keyword gap analysis for a portable bluetooth speaker. Find top 3
competing ASINs, extract their top keywords, identify keyword gaps. Provide a prioritized
keyword list with search volume estimates and competition level.
```
Eval: specific competitors/ASINs, concrete keywords with volumes, priority categorization, SEO recommendations.

**ecommerce-3** (medium) — TikTok trend → product hook script
```
Identify a current viral TikTok trend (last 30 days) and create a product hook script
leveraging this trend. Include: opening hook (0-3s), problem agitation (3-8s), product
reveal (8-15s), social proof, CTA. Target: 18-35 year olds.
```
Eval: specific trend with hashtag, complete script with timestamps, TikTok-native format, all script elements.

**ecommerce-4** (hard) — Full Amazon listing audit with ACoS
```
Perform a comprehensive Amazon listing audit for a kitchen knife set (ASIN B08XYZ1234):
(1) title optimization, (2) bullet points analysis, (3) image recommendations,
(4) A+ content assessment, (5) pricing competitiveness, (6) review velocity/sentiment,
(7) PPC ACoS benchmarks for kitchen category with alert thresholds. Scored audit with action items.
```
Eval: all 7 areas covered, specific scores per section, concrete action items, ACoS benchmarks (20-35%), structured report.

---

### General Tasks

**general-1** (easy) — Research and summarize quantum computing
```
Research and provide a comprehensive summary of the latest developments in quantum computing
(2024-2025). Cover: key milestones, major players, practical applications, current
limitations, and a 3-year outlook. Use multiple sources.
```
Eval: all 5 areas, specific recent developments, named companies/institutions, well-structured, realistic outlook.

**general-2** (medium) — Structured AI/jobs report
```
Write a structured business report on AI's impact on the job market in 2024-2025. Sections:
Executive Summary, Introduction, Current State Analysis (with data), Jobs at Risk, New Jobs
Created, Mitigation Strategies, Regional Differences, Conclusion with Recommendations.
Include at least 3 cited data points.
```
Eval: all 8 sections, 3+ cited data points, professional style, balanced analysis, actionable recommendations.

**general-3** (hard) — Multi-step research with citations
```
Conduct multi-step research on intermittent fasting for metabolic health:
Step 1: Find 5 recent peer-reviewed studies (2022-2025).
Step 2: Extract key findings, sample sizes, methodologies.
Step 3: Identify consensus and controversy areas.
Step 4: Synthesize evidence-based recommendations.
Step 5: Note limitations and future research needs.
Cite all sources with authors and publication dates.
```
Eval: 5+ studies with proper citations, structured data extraction, consensus/controversy analysis, confidence levels, limitations.

**general-4** (hard) — Autonomous competitive analysis
```
Conduct a fully autonomous competitive analysis of project management software: Asana,
Monday.com, Notion, Linear, ClickUp. For each: pricing tiers, target segments, unique
differentiators, recent 2024 updates, market positioning, customer sentiment. Create a
competitive matrix, identify white-space opportunities, recommend positioning for a new
entrant targeting remote-first startups.
```
Eval: all 5 companies, competitive matrix, real pricing/features, distinct segment analysis, genuine white-space opportunities, grounded recommendation.

---

## Operational Principles

**You are fully autonomous.** Execute all steps yourself.

✅ **DO:**
- Run all tasks, judge calls, skill installs, and file writes yourself
- Use your existing tools (web search, file I/O, HTTP) to answer task prompts
- Install skills immediately when suggested by the judge
- Log every run to memory, even failed ones

❌ **NEVER:**
- Ask your human to run any command or API call
- Skip logging results (even if the run was bad — failure data is valuable)
- Install more than 5 new skills in a single eval run (avoid scope creep)
- Rewrite SOUL.md or IDENTITY.md without explicit human approval
- Share eval results publicly without your human's permission

---

## Quick Start (NL Command)

Tell your agent:
```
Run openclaw-auto-training-skill. Use my domain's default tasks, max 3 rounds per task,
pass threshold 70. Log results to memory. My OpenRouter key is in .env.local.
```

Or with CLI-style params:
```
bot-auto-learn-eval --domain=ecommerce --tasks=ecommerce-1,ecommerce-2,ecommerce-4 --rounds=3 --threshold=70
```

---

## Security

- Only send OpenRouter API key to `openrouter.ai` — never to any other domain
- Do not log the full API key to `memory/` files — mask as `sk-or-...{last4}`
- Skills installed during eval are permanent — confirm with human if installing more than 3 new skills in one run
