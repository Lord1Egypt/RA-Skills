# Practice Workflows

Use this file for active recall, `/mock`, `/oral`, `/fix`, `/summary`, and practice repair loops. For strategy selection rules, see `references/learning-strategies.md`. For keeping the session focused, feedback-driven, and iterative, use `references/focus-feedback-iteration.md`.

## Active Recall

Generate questions before summaries when possible.

Formats:

- Flashcards: front/back, cloze, formula, definition, comparison. See `SKILL.md` Flashcard Export and `scripts/export_flashcards.py`.
- Short-answer checks.
- Fill-in process steps.
- Proof skeleton completion.
- Code output prediction.
- Lab operation checklist recall.

After each active-recall round, update the relevant SRS row (see `references/spaced-repetition.md`) so mastered topics are scheduled for future review and struggling topics surface sooner.

Every active-recall round must name the current focus topic, collect a visible answer signal, and end with the next iteration action: repair, repeat, interleave, escalate, de-prioritize, or schedule.

Use three levels per concept:

1. Memory: definition/formula/fact.
2. Understanding: explain why, condition, or comparison.
3. Exam application: solve, prove, calculate, debug, or analyze.

When the student already knows the basics, mix related topics instead of drilling one pattern repeatedly. Use interleaving from `references/learning-strategies.md` to force method recognition.

## Mock Exam

Specify:

- Total points and time.
- Question type distribution.
- Allowed materials assumptions.
- Difficulty distribution.
- Answer key and rubric.
- Time allocation advice.

After the user answers, grade with `question-types.md` rules.

### Pacing and Time Management

A mock is also a rehearsal of time allocation — many students lose points not from ignorance but from spending too long on hard items and rushing the rest. Make pacing explicit:

- Assign a per-question or per-section time budget up front, summing to the total time (roughly proportional to marks).
- Ask the user to log actual time per question (or note where they ran over) when feasible.
- In the post-mock review, flag pacing problems alongside content errors:

```markdown
## 节奏复盘
| 题 | 分值 | 预算 | 实际 | 判断 |
|---|---|---|---|---|
| 大题3 | 15 | 18min | 32min | 超时，应在 20min 时战略性跳过 |
```

- Teach a triage rule: attempt the highest mark-per-minute items first; set a hard cap per question; mark-and-return rather than stall.
- For machine-graded/OJ exams, pacing = which problems to attempt in what order, not partial credit.

## Error Repair

When grading or reviewing mistakes:

1. Identify the exact mistaken knowledge point.
2. Classify the error: concept, condition, formula, computation, proof gap, code edge case, experiment operation, expression.
3. Give a micro-lesson.
4. Ask for one self-explanation of the corrected step when the error involves proof, derivation, code trace, or lab operation.
5. Generate three repairs: basic, variant, mixed/comprehensive.
6. Add one recognition prompt when the mistake was choosing the wrong method.
7. Update suggested next review task.
8. Update the SRS row for this topic (see `references/spaced-repetition.md`); in agent shells prefer `scripts/srs.py update`.

End error repair with the `本轮闭环` footer from `references/focus-feedback-iteration.md`: focus = exact weak point, feedback = evidence from the answer, next round = one targeted action.

## Oral Exam Rehearsal

Use for `/oral`, viva voce, defense, and interview practice. Ask one question at a time, wait for the user's answer, grade it, then decide whether to deepen or repair.

Setup:

- Confirm subject, expected duration, and any known rubric.
- Build a 6-12 question ladder per topic.
- Default to written chat unless the environment is confirmed to support audio.

Depth ladder:

1. Definition, about 30 seconds.
2. Condition/scope, about 45 seconds.
3. Example and counterexample, about 45 seconds.
4. Application, about 90 seconds.
5. Edge case, about 60 seconds.
6. Comparison, about 60 seconds.
7. Defense against a common misconception, about 60 seconds.

Stop climbing as soon as the user gets stuck. Repair the gap before continuing.

Grade each answer on accuracy, conciseness, structure, confidence, and course vocabulary.

Teach reusable short patterns:

- Definition -> key conditions -> example -> common pitfall.
- If condition holds -> conclusion; counterexample shows limitation.
- Concept A vs. Concept B differs mainly on the named dimension.

### Voice and Immersion (Agent Shell)

When the host environment supports audio or TTS tools:

- Generate the examiner's question as audio (TTS) so the student hears the question rather than reading it, simulating real oral-exam pressure.
- If speech-to-text is available, accept the student's spoken answer and transcribe it for grading.
- Always provide a text fallback alongside audio so the student can review what was asked and answered.

In plain chat or RAG notebook, skip audio and use text only.

## Summary

For `/summary`, produce:

- Topics practiced.
- Accuracy changes.
- Updated weak points.
- SRS updates if available.
- One concrete next step.
- Focus-feedback-iteration state: current priority focus, strongest feedback signal, and next iteration target.

Keep it short enough to paste into a study log.
