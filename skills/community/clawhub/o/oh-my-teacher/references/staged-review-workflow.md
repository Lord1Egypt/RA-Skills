# Staged Review Workflow

Use this file when the user asks for a phased exam-prep workflow, a "personal
review assistant", "stage 1", "core review materials", "most worth studying
chapters", or a complete path from materials to mock training and weak-point
repair.

## Trigger

Route natural-language requests such as:

- "请你作为我的专属复习助手"
- "先从阶段1开始"
- "输出核心复习资料"
- "最值得花时间的章节"
- "根据课件、考试范围、往年题和老师强调点帮我复习"

Use existing commands instead of inventing a separate command:

`/profile -> /materials -> /paper-analyze -> /teacher-emphasis -> /map -> /plan -> /mock -> /grade -> /fix`

If the user provides only partial materials, still output a low-confidence Stage
1 artifact and list missing inputs.

Use `references/focus-feedback-iteration.md` throughout: Stage 1 selects the
focus, Stage 2 collects feedback, and each response chooses the next iteration.

## Stage 1 Inputs

Try to cover these material dimensions:

| Input | What to extract | If missing |
|---|---|---|
| Chapter slides or lectures | Core points, cases, extensions, formulas, definitions | Ask for table of contents or one chapter first |
| Exam scope | Official topics, chapter weights, high/low-frequency labels | Mark exam weights as unknown |
| Past papers from 3-5 years | Question types, topic frequency, wording style, scoring pattern | Mark frequency as unknown |
| Teacher emphasis | Repeated warnings, easy mistakes, required derivations, case-analysis demands | Mark emphasis as unknown |

Never present inferred scope as confirmed. Label each conclusion as material
confirmed, past-paper inferred, teacher-emphasis confirmed, or low-confidence
general inference.

## Stage 1 Output Contract

After material analysis, produce these modules in order.

### 1. Must-Memorize Content And Concept Summary

Include:

- **Must-memorize items**: chapter conclusions, formulas, theorem statements,
  original definitions, key data, standard templates.
- Mark priorities with `★★★`, `★★`, or `★`.
- Reserve `★★★` for high-frequency past-paper items, official high-weight
  scope, or teacher-emphasized points.
- **Concept summary**: use nested lists or a compact concept map. For confusable
  concepts, use `definition + conditions + comparison dimension`.
- **Concept extension**: practical meaning, boundary with similar concepts, or
  where the concept appears in exam questions.

### 2. Question-Type Recognition And Solution Steps

For each real or likely question type, include:

| Question type | Recognition keywords | Distractor/trap pattern | Linked knowledge | Answer steps |
|---|---|---|---|---|

Rules:

- Recognition keywords should match wording patterns such as "以下属于",
  "简述", "计算", "证明", "结合材料分析".
- Distractor/trap patterns should name the mechanism: concept swap,
  over-generalization, missing condition, exception wording, sign/unit mistake,
  or irrelevant case detail.
- Answer steps must follow: read the question -> link knowledge -> organize the
  answer -> check.
- For subjective questions, provide a reusable template such as: theory basis ->
  material link -> structured analysis -> final summary.

### 3. Most Worth Studying Chapters

This section is mandatory when Stage 1 is requested.

Rank chapters using the three evidence dimensions below:

1. **Exam-scope weight**: official chapter percentage, point value, or scope
   emphasis.
2. **Past-paper frequency**: how often the chapter or topic appears in 3-5 years
   of papers, plus question type.
3. **Teacher-emphasis strength**: repeated classroom emphasis, review notes,
   starred slides, Q&A warnings, or required derivations/cases.

Use this table:

```markdown
| Priority | Chapter/topic | Exam-scope weight | Past-paper frequency | Teacher emphasis | Why this rank | Best next action | Confidence |
|---|---|---:|---:|---|---|---|---|
| P0 |  |  |  |  |  | Must master / drill today |  |
| P1 |  |  |  |  |  | Focused breakthrough |  |
| P2 |  |  |  |  |  | Understand and quick scan |  |
```

Priority rules:

- `P0`: high weight, repeated past-paper appearance, or strong teacher emphasis.
  These chapters must be mastered first.
- `P1`: medium weight, occasional past-paper appearance, or moderate teacher
  emphasis. These need focused practice after P0.
- `P2`: low weight, rare appearance, or only background understanding. Quick
  scan unless the student is aiming for a high score.

If exact percentages are unavailable, use `unknown`, `high`, `medium`, or `low`
instead of inventing numbers. The `Why this rank` column must state the evidence,
for example: "Chapter 3 is 30% of the scope, appeared in 2 of the last 3 papers,
and teacher emphasized case analysis."

After this table, choose the first concrete P0 action and include the `本轮闭环`
footer: focus = selected P0 chapter/topic, feedback = evidence used or missing,
next round = the first diagnostic/practice/material step.

## Stage 2: Mock Training And Weak-Point Repair

Start Stage 2 only after the student completes practice or asks for simulation.

### 1. Generate Mock Questions And Answers

- Create 3-5 mock sets only when requested or when the plan reaches mock stage.
- Match real question types, difficulty, score distribution, and topic weights.
- Provide detailed answers with scoring points and solution-review notes.

### 2. Correct Mistakes And Select Weak Points

Analyze mistakes across three dimensions:

| Weak point | Knowledge type | Question ability | Chapter | Evidence | Repair action |
|---|---|---|---|---|---|

Knowledge types include concept misunderstanding, condition missing, formula
misuse, theorem misuse, case-analysis gap, or operation/procedure error.
Question abilities include question reading, distractor recognition, derivation,
calculation, proof structure, answer organization, and time allocation.

### 3. Deepen Each Weak Point

For each weak point, provide:

- Extension material: textbook section, lecture slide, paper excerpt, or safe
  general explanation. Do not fabricate sources.
- 3-5 targeted questions, including at least one variant question.
- Error warning: preconditions, boundary cases, units/signs, exception wording,
  or required answer structure.

### 4. Training Flow

Produce a concrete loop:

基础巩固 -> 专项突破 -> 模拟冲刺

Include daily or weekly task volume, and use this feedback cycle:

做题 -> AI 批改 -> 复盘薄弱点 -> 针对性训练 -> SRS/错题本更新

Recommend a review method such as wrong-note taxonomy, concept-link recall, or
teach-back when it matches the error type.
