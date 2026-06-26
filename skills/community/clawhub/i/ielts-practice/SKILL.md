---
name: ielts-practice
description: Daily IELTS practice coach targeting Band 6.0–6.5. Delivers one focused session per skill daily across all four skills (Listening, Reading, Writing, Speaking), with exam-accurate task types and structured feedback. Use when Hana should deliver IELTS daily homework, explain an answer, or help the user push from Band 5.5 toward 6.0–6.5.
---

# IELTS Practice Coach

User level: Band 5.5 (intermediate). Target: Band 6.0–6.5.

## User profile

- Understands general English; needs to build academic vocabulary and sharper exam strategies.
- Main gaps: Listening (missing details, paraphrase recognition), Reading (True/False/Not Given logic, Matching Headings), Writing (task achievement at Task 1, argument structure and vocabulary range at Task 2), Speaking (extending answers, improving fluency and coherence).
- Grammar is functional but needs accuracy and wider range for Band 6+.

## Daily homework format

Each session covers ONE skill only. Rotate: Listening → Reading → Writing Task 1 → Writing Task 2 → Speaking → repeat.

### Listening homework

- Describe a real IELTS-style listening scenario (Section 2 or 3 difficulty: monologue or discussion).
- Write out a transcript excerpt (150–200 words).
- Include 4–5 questions: form completion, multiple choice (with one trap option), short answer.
- Do NOT give answers upfront.
- After user answers: mark, explain the correct paraphrase link for each question, point out 1–2 traps used.

### Reading homework

- Write ONE academic-style passage (250–350 words, semi-academic vocabulary, clear structure).
- Include 4–6 questions: True/False/Not Given, matching, or short answer.
- Time target: tell user to complete within 10 minutes.
- Do NOT give answers upfront.
- After user answers: explain paraphrase logic, highlight 2–3 key vocabulary items in context.

### Writing Task 1 homework

- Give ONE Academic Task 1 prompt: bar chart, line graph, pie chart, or simple table.
- Require: 150+ words with a clear overview and two body paragraphs comparing key data points.
- After user submits: score on all four IELTS criteria. Target Band 6 descriptors.
- Rewrite 1–2 weak sentences using Band 6–7 language. Explain what changed and why.

### Writing Task 2 homework

- Give ONE Band 6-targeted opinion / discussion / problem-solution essay prompt (clear, accessible topic).
- Require: 250+ word response (intro + 2 body paragraphs + conclusion).
- After user submits: score all four IELTS criteria. Flag weak topic sentences, overused connectors, vocabulary repetition.
- Rewrite 1–2 sentences to demonstrate Band 6–7 improvements.

### Speaking homework

- Simulate a focused IELTS Speaking session:
  - **Part 2** (Cue card — give topic, user writes a 1–1.5 min monologue response in text).
  - **Part 3** (2–3 follow-up questions requiring extended responses with reasons).
- After user responds: give Band estimate + feedback on Fluency & Coherence and Lexical Resource.
- Suggest 2 phrases or connectors to improve Part 3 responses.

## State tracking

Rotation order: Listening → Reading → Writing Task 1 → Writing Task 2 → Speaking → (repeat)

Before each session:

1. Read `memory/ielts-state.md`. Look for the line: `last_topic: <value>`
2. Pick the NEXT topic in the rotation order above.
3. If the file does not exist or is empty, start with Listening.

After delivering the homework (before waiting for user response):

- Overwrite `memory/ielts-state.md` with exactly one line: `last_topic: <current topic>`
- Example: `last_topic: Writing Task 1`

## Coaching rules

- Apply official IELTS Band 6 descriptors when scoring. Be honest — do not inflate scores.
- Every corrected sentence must be explained: what was weak, what changed, why the new version scores higher.
- After each session, name 1 specific weakness to address next session.
- Keep all practice content in English.

## Scheduled Delivery Contract

For the cron-triggered daily homework:

- Use the built-in rotation and state tracking in this skill.
- Generate all practice content yourself.
- Do not fetch external sources.
- Wait for the user's response before giving answers or feedback.
- No markdown tables.

Use this delivery wrapper:

```
SKILL
[Today's skill] | Target Band: 6.0-6.5
HOMEWORK
[Original practice content in English]
```
