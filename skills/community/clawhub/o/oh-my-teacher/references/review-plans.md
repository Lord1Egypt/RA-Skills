# Review Plans and Study Maps

Use this file for `/plan`, `/map`, `/cram`, `/last-page`, `/dashboard`, multi-course planning, final review sheets, and progress heat maps. For selecting retrieval, spacing, interleaving, elaboration, self-explanation, and dual coding, see `references/learning-strategies.md`. For turning the plan into a focus-feedback-iteration loop, see `references/focus-feedback-iteration.md`. For explicit daily/weekly reminders or knowledge digests, see `references/opt-in-reminders.md`.

## Study Map

Produce:

- Course profile assumptions.
- Chapter or knowledge tree.
- Priority labels: must know, high-yield, hard, quick scan, low priority.
- A "Most Worth Studying Chapters" table when materials include exam scope, past papers, or teacher emphasis. Rank P0/P1/P2 by exam-scope weight + past-paper frequency + teacher-emphasis strength; mark missing evidence as unknown.
- Exam actions: memorize, understand, derive, calculate, code, draw, operate.
- Likely question types and common traps.
- Next practice set.
- Progress heat map when the Current Course Snapshot has accuracy or SRS data.
- Current review loop: focus, feedback evidence, and next iteration target.

If materials include past papers, estimate topic weight from repeated concepts and question types. Avoid claiming certainty.

## Progress Heat Map

For `/map` and `/plan`, include a compact ASCII progress bar per chapter/topic when mastery data exists:

```text
Topic                    Mastery
Limits and continuity    [########--] 80%  (8/10 accuracy, SRS streak 3+)
Differentiation          [######----] 60%  (6/10 accuracy)
Integration              [##--------] 20%  (2/10 accuracy)
Series                   [----------]  0%  (not yet practiced)
```

Compute mastery as:

1. If Accuracy has a score for the topic: `pct = accuracy_score * 10`, capped at 100.
2. If no Accuracy data but SRS has entries: `pct = topics_at_streak_3_plus / total_topics_in_chapter * 100`.
3. If neither exists: `pct = 0`.

Place the heat map after the knowledge tree and before common traps.

## Review Plan

Use available days and daily hours. Keep plans realistic.

Include:

- Daily minimum line: tasks required for the goal.
- Optional bonus line: tasks for a higher score.
- Active recall every day.
- Strategy label for each study block: retrieval, spaced review, interleaving, self-explanation, Socratic, Feynman, dual coding, or mock.
- Error repair after practice.
- Mock exam near the end.
- Final 30-minute sheet.
- A loop line for each day: Focus -> practice/feedback signal -> iteration action.

Modes:

- Pass-only: prioritize standard questions, definitions/formulas, and common templates.
- High-score: add hard variants, proofs, mixed problems, and timed full mocks.
- Cram: remove low-yield reading, use last-page sheet, standard methods, and focused drills.
- Multi-course: rank by exam date, difficulty, credit/importance, and current weakness.

Default daily block structure:

1. Pretest or retrieval warm-up before reading.
2. Focused repair or explanation for the weakest point.
3. Practice set, preferably interleaved after basics are stable.
4. Error repair with self-explanation.
5. SRS update and next due review.

## Cram Mode

Use when time remaining is short or the user explicitly requests `/cram`.

- Start from scoring yield, not chapter order.
- Focus on standard methods, formula conditions, common traps, and high-frequency question types.
- Prefer short drill loops over long summaries.
- Produce a final-page sheet and a short "do not waste time on" list.

### Managing Exam Anxiety

Late-stage cramming is as much an emotional state as a knowledge gap; a panicking student retains little. Without being saccharine:

- **Open with a quick win.** Lead with one high-yield item the student can get right now, to break the spiral and create momentum before harder material.
- **Make the scope finite and concrete.** "3 topics, ~90 minutes" beats an open-ended "study everything" — a bounded plan reduces overwhelm.
- **Normalize triage.** Explicitly permit skipping low-yield material; "deciding not to study X" is a strategy, not failure.
- **Protect basics under pressure.** Remind the student that locking in definitions, formulas, and standard templates secures more marks than gambling on the hardest problems.
- Keep the tone calm and directive. Give the next single action, not a lecture on study habits.

## Last Page

For final review, generate a compact sheet:

- Must-know definitions/formulas.
- Standard templates.
- Common traps.
- Time allocation.
- Things to check before submitting.
- For labs: steps, data table, error analysis, viva Q&A.

In ima-native environments, build `/last-page` from `/source-map`, `/teacher-emphasis`, the Weak Point Board, SRS due items, and high-yield formulas/templates. Prefer writing it to ima-note; use it as the default input for `/ppt`.

## Dashboard

For `/dashboard`, generate a Markdown dashboard instead of relying on the local terminal dashboard:

```markdown
# 复习仪表盘

## 今日状态
- 距离考试:
- 当前目标:
- 今日必须完成:

## 掌握度热力图
[topic progress bars]

## 错误类型分布
[error-category table from wrong notes; see `references/wrong-note.md` → Error-Type Analytics. Omit if no wrong notes yet.]

## 今日待复习
| Topic | 原因 | 建议动作 |
|---|---|---|

## 最大风险
1.
2.
3.

## 下一步
```

In ima-native environments, gather data from `memory_recall`, `search source=note`, the course homepage, SRS table, weak-point board, and recent wrong notes. Update the dashboard through `ima-note` when available.
