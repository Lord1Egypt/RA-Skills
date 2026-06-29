# Focus Feedback Iteration

Use this file for every multi-step review task. The skill should move the
student into a review state that is focused, feedback-driven, and iterative.

## Core Loop

Every substantial response should preserve this loop:

1. **Focus**: name the highest-value topic, task, or chapter for this round.
2. **Action**: give a concrete learning artifact or practice task.
3. **Feedback**: grade, diagnose, or compare the student's result against the
   target.
4. **Iteration**: choose the next repair, drill, SRS update, or priority change.

Do not let the session stop at passive summaries. A summary is acceptable only
when it points to the next active recall, practice, grading, or repair step.

## Output Footer

For multi-step review outputs, end with a compact footer:

```markdown
## 本轮闭环
- 重点: [P0/P1 topic or current weak point]
- 反馈: [what evidence we used or still need]
- 下一轮: [one concrete action: answer Q1, upload paper, run drill, repair topic, review due item]
```

If no student answer exists yet, the feedback line should say what evidence is
missing, for example: "需要你先完成3道诊断题才能判断掌握度".

## Focus Rules

- Prefer P0 chapters from `references/staged-review-workflow.md` when material
  evidence exists.
- Prefer overconfident weak points when confidence calibration shows a gap.
- Prefer repeated mistakes over topics the student merely says are difficult.
- Prefer high-yield standard templates in cram mode.
- Prefer prerequisites when a later topic repeatedly fails because of them.

## Feedback Rules

Feedback must be based on at least one visible signal:

- Student answer, quiz result, mock result, oral response, code output, lab
  procedure, or uploaded material.
- Past-paper frequency, exam-scope weight, or teacher emphasis.
- SRS history, accuracy history, wrong-note category, or confidence calibration.

When feedback evidence is absent, say so and ask for the smallest useful signal:
one answer, one past paper, one chapter list, or one teacher-emphasis note.

## Iteration Rules

After feedback, choose exactly one next move unless the user asks for a full
plan:

Available iteration moves are: repair, repeat, interleave, escalate, de-prioritize, or schedule.

- Repair: explain the exact weak point and give a targeted drill.
- Repeat: ask a close variant to test whether the repair worked.
- Interleave: mix a related topic once basics are stable.
- Escalate: move from memory to application or mixed questions.
- De-prioritize: move a mastered or low-yield topic to quick review.
- Schedule: update SRS or set the next due review.

## Stage Integration

- Stage 1 outputs end by selecting the first P0 action.
- Stage 2 outputs end by turning graded mistakes into weak-point repair.
- Plans convert P0/P1/P2 priorities into dated loops.
- Summaries record what changed and the next iteration target.
