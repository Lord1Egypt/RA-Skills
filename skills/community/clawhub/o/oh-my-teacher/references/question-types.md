# Question Types and Grading

For mock exams and error repair workflows, see `references/practice-workflows.md`. For review plans and study maps, see `references/review-plans.md`. For subject-specific adaptation of question style and rigor, see `references/subject-adaptation.md`. For retrieval practice, pretesting, interleaving, and elaborative prompts, see `references/learning-strategies.md`.

## Adaptive Difficulty

Adjust difficulty dynamically based on the user's recent performance within the current session:

- **Step up**: if the user answered the last 2–3 questions on a topic correctly, increase difficulty to the next tier (basic → variant → mixed/comprehensive).
- **Step down**: if the user got the last question wrong, drop one tier and isolate the missing prerequisite before retrying.
- **Hold**: if performance is mixed (e.g., 1 correct, 1 wrong), stay at the current tier and try a different angle.

State the adjustment briefly when it happens:

> "难度上调：你连续答对了 3 道基础题，接下来试一道综合题。"
> "难度回调：这道题做错了，我们先回到基础概念再试一次。"

When generating a question set, avoid topics listed in **Completed** in the Current Course Snapshot unless the user requests a comprehensive review or mock exam.

## `/diagnose` vs `/quiz`

These two commands both ask questions but serve opposite goals; do not conflate them.

| | `/diagnose` | `/quiz` |
|---|-------------|---------|
| **Goal** | Map *where* the user is weak across the whole course | Drill and improve *one* topic in depth |
| **Coverage** | Broad: one question per top chapter (≈5 total) | Narrow: many questions on a single topic |
| **Difficulty** | **Fixed** at a baseline tier — do NOT step up/down mid-diagnostic; consistent difficulty keeps results comparable across topics | **Adaptive** — apply the step up/down/hold rules above |
| **Output** | A weak-point report ranked by performance; write results to the snapshot's **Weak points**, **Accuracy**, and calibrate **Level** | Per-question grade plus a difficulty trajectory; update **Accuracy** and **Completed** |
| **When** | Early, before `/plan` or `/map`, when the user's level is unknown | Anytime the user wants to practice a known weak area |

After `/diagnose`, recommend `/quiz` (or `/fix`) on the lowest-scoring chapter. The diagnostic calibrates the map; the quiz works the territory.

Treat `/diagnose` as pretesting when the student has not reviewed yet: keep it low-stakes, explain that misses guide attention, and avoid interpreting a miss as failure.

## Generation Defaults

Always align questions with course profile, subject adaptation, and user level.

For each question set, include:

- Topic
- Difficulty
- Estimated time
- Answer
- Explanation or rubric
- Common mistake

For adaptive `/quiz`, include a method-recognition or interleaved question once the student answers 2-3 basic questions correctly. This prevents pattern memorization and tests whether the student can choose the right approach.

### Confidence Calibration (optional)

For `/quiz`, `/diagnose`, and high-stakes `/grade`, optionally ask the student to predict confidence (1-5) before submitting, then compare it to the actual score. A high-confidence miss is a priority weak point — it would have cost points on the real exam without warning. See `references/learning-strategies.md` → Confidence Calibration. When used, add one line to the grading output:

```markdown
## Calibration
信心 [n]/5 vs 实际 [earned]/[max] — [well-calibrated | overconfident ⚠ | underconfident]
```

## Paper Exam Types

- Multiple choice: include plausible distractors based on common misconceptions.
- Fill in the blank: test definitions, conditions, formulas, syntax, process steps.
- Short answer: require concise concept explanation and example.
- Calculation: show knowns, target, formula choice, steps, units/checks.
- Proof: require theorem conditions, structure, and each inference.
- Essay/case: provide outline, key terms, evidence, and scoring rubric.

## Programming Types

- Predict output
- Trace state changes
- Find bug
- Complete code
- Implement function
- Analyze complexity
- Design tests

Keep code within the known course level. If unknown, start with basic language constructs and ask for learned scope when needed.

## Lab Types

- Principle explanation
- Operation sequence ordering
- Instrument setup diagnosis
- Data processing
- Error/uncertainty analysis
- Report critique
- Viva Q&A

## Grading Rubric

### Strict-by-Default Calibration

For an exam-prep tool, a false positive (marking a wrong answer correct) is more harmful than a false negative — it builds misplaced confidence that surfaces as lost points on the real exam. Grade strictly:

- Before assigning a score, explicitly check the answer against the failure modes for its category (e.g. for proofs: missing theorem conditions, unjustified steps, wrong quantifier order; for code: unhandled edge cases, off-by-one, wrong complexity). Briefly state which checks you ran.
- When genuinely uncertain between two scores, choose the lower one and explain the gap, rather than rounding up.
- Do not award full marks unless the answer would survive a strict grader: complete, correct, and with no omitted conditions or untested edges.
- Never invent partial credit the rubric does not support, and never soften a deduction to be encouraging — accurate feedback is the kindness here.

### Double-Pass Grading Protocol

Strict grading is only useful when it is *accurate*. A single pass of LLM grading can hallucinate deductions — marking a correct step as insufficiently justified just because the student's notation differs from the textbook. Apply a double-pass process to every graded response:

1. **Draft pass**: Produce an initial score, deduction list, and rubric report.
2. **Self-correction pass**: Ask yourself for each deduction — "Was this point lost because the student's logic was actually wrong, or because their notation/style differs from a reference answer?"
3. **Finalize**: If the deduction was style-based (different variable name, non-standard but equivalent notation, omitted intermediate step that is obvious from context), **restore the point** and add a Style Note instead:

   > Style Note: In exams, graders typically prefer writing the intermediate step explicitly — worth 1 mark for completeness.

   If the deduction was logic-based (truly missing condition, invalid inference, wrong ordering), keep it.

This prevents the grader from penalising non-standard but correct reasoning while still catching genuine errors. The user gets accurate credit for what they got right, plus targeted repair for what they actually got wrong.

### Output

Return this structure for every `/grade`, `/quiz`, or `/mock` grading response:

```markdown
## Score
[earned]/[max] - [strict one-sentence verdict]

## Checks Performed
[Which error categories were tested]

## What Is Correct
[Parts that earn credit]

## Lost Points
[Point-by-point deductions with reasons]

## Exact Mistake
[Smallest mistaken concept, condition, step, edge case, or expression]

## Correct Version
[Corrected answer or improved answer]

## Repair Drill
[One immediate variant question or task]

## SRS Update
[Topic, score 1-5, next review if SRS is available; otherwise say not updated]
```

In ima-native environments, add this section after `Checks Performed` whenever course materials or notes are available:

```markdown
## Source Alignment
| Point | Student Answer | Course Material Wording | Alignment |
|---|---|---|---|
```

Use `search source=kb` or `fetch` to compare against course materials when needed. Mark the source level as `课程资料确认`, `ima 知识库检索`, `笔记历史`, `通用课程推断`, or `需要确认`. If source retrieval is unavailable, say `Source Alignment: not checked`.

For proofs, grade definitions, conditions, structure, logical validity, and conclusion.

For code, grade algorithm idea, correctness, edge cases, complexity, syntax, and readability only if relevant to the course.

For essays, grade thesis, concept accuracy, structure, evidence/examples, and course vocabulary.

For labs, grade principle, operation, data/calculation, error analysis, and safety/attention notes.
