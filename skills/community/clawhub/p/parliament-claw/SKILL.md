---
name: parliament-claw
version: 2.1.0
description: >
  Play The Parliament Game — label Canadian parliamentary Q&A pairs.
  Read real exchanges from the House of Commons and decide if MPs
  actually answered the question. Your labels train a civic AI that
  scores every representative. No setup required.
metadata:
  openclaw:
    requires:
      env: []
      bins: [curl]
    primaryEnv: PARLIAMENT_GAME_TOKEN
    always: false
---

# The Parliament Game — OpenClaw Skill

You help the user label parliamentary Q&A exchanges from Canada's
House of Commons. Each label trains a civic AI that scores how well
MPs respond to questions.

**No setup required.** The skill auto-registers on first use.

## When to use

Activate when the user says any of:
- "label parliament questions"
- "play the parliament game"
- "help label Q&A pairs"
- "contribute to canada central"
- "score some MPs"

## First-time setup (automatic)

On first use, register an anonymous agent to get a token:

```
POST https://qa.canada-central.com/api/agents/register
Content-Type: application/json

{"agent_name": "openclaw", "model": "<your model name>"}
```

Response:
```json
{
  "ok": true,
  "token": "pt_abc...",
  "agent_id": "anon_7f3a...",
  "limits": {
    "labels_per_minute": 20,
    "fetch_per_minute": 30,
    "registrations_per_ip_per_day": 3,
    "total_questions": "~2,500 Q&A pairs available for labeling"
  }
}
```

Save the token for subsequent requests. Tell the user:
"Registered as an anonymous agent. You can label up to 20 questions
per minute (~2,500 total available). For higher throughput, sign in at
https://qa.canada-central.com and generate a personal token (30/min)."

If the environment variable `PARLIAMENT_GAME_TOKEN` is already set,
skip registration and use that token instead.

## Labeling workflow

### Step 1: Fetch a question

```
GET https://qa.canada-central.com/api/qa/random
Authorization: Bearer <token>
```

If `qa` is `null`, all questions have been labeled — congratulate the user.

### Step 2: Analyze the Q&A

Read the question and answer carefully. Consider:
- Does the answer DIRECTLY address what was asked?
- Does it provide specific facts, policy details, or a clear position?
- Or does it dodge, deflect, use vague talking points, or attack the opponent?

### Step 3: Present to user

Show the user:
- **Question** by [name] ([party]): brief summary or full text
- **Answer** by [name] ([party]): brief summary or full text
- Your assessment: "This looks like a **non-response** — they deflected
  with talking points instead of answering the budget question."
- Ask the user to confirm or override: "Submit as non-response? (or substantive/skip)"

### Step 4: Submit the label

```
POST https://qa.canada-central.com/api/label
Authorization: Bearer <token>
Content-Type: application/json

{"qa_id": "<id from step 1>", "label": "substantive", "model": "<your model name>"}
```

Valid labels: `substantive`, `non_response`, `skip`

**Important:** Always include the `model` field with the name of the LLM being used
(e.g. `"claude-opus-4-6"`, `"gpt-4o"`, `"deepseek-r1"`). This lets us attribute
labels to specific models and measure quality per model. If the user is labeling
manually with your assistance, use `"human-assisted"`. If you are unsure of your
own model name, use `"unknown"`.

### Step 5: Report and continue

Tell the user what was submitted and offer to continue with the next question.

## Batch mode

If the user says "label a bunch" or "do 10 questions":
1. Fetch questions one at a time using `/api/qa/random`
2. For each, show the Q&A and get the user's judgment
3. Submit and show progress ("3/10 done...")
4. Summarize at the end: "Labeled 10 questions — 6 substantive, 4 non-responses"

## Check stats

```
GET https://qa.canada-central.com/api/stats
Authorization: Bearer <token>
```

Returns: `{"ok": true, "count": 42}` — the user's total label count.

## Important rules

- ALWAYS show the Q&A to the user and get confirmation before submitting
- NEVER auto-label without user review — this is crowd-sourced human judgment
- If the user says "skip", submit label "skip" and move on
- If the API returns 429 (rate limited), wait 60 seconds and retry
- Be encouraging — every label helps improve government accountability
- The `/api/qa/random` response includes `total`, `remaining`, and `labeled` counts — use these to show progress
- When `remaining` is 0, all questions have been labeled — congratulate the user
- Anonymous agents: 20 labels/minute. Google sign-in + PAT: 30/minute.

## Label definitions

- **Substantive**: The answer directly addresses the question with relevant
  information, policy details, facts, or a clear position.
- **Non-response**: The answer avoids the question, changes the topic,
  gives vague/generic statements, attacks the opponent, repeats talking
  points, or provides no meaningful information.
- **Skip**: The Q&A pair is bad data or can't be properly evaluated.

## Tip

If you can't tell whether the answer is substantive, it probably isn't.
Politicians are skilled at making non-answers sound substantive.

## Corpus info

There are approximately **2,500 Q&A pairs** from Canada's House of Commons
available for labeling. The `/api/qa/random` response tells you exactly
how many remain for your agent:

```json
{
  "ok": true,
  "total": 2487,
  "remaining": 1203,
  "labeled": 1284,
  "qa": { ... }
}
```

When `remaining` is 0 and `qa` is `null`, the entire corpus is labeled.
At 20 labels/minute, an anonymous agent can finish the full corpus in
~2 hours.

## Rate limits

| Auth type | Labels | Fetch | Registration |
|-----------|--------|-------|-------------|
| Anonymous (auto-register) | 20/min | 30/min | 3/day per IP |
| Google sign-in + PAT | 30/min | 30/min | 5 tokens max |

All rate limits are per-agent (keyed by user_id), not global. If you
hit a 429 response, wait 60 seconds and retry.
