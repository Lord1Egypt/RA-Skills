# Learning Strategies

Use this file to choose study methods for `/plan`, `/quiz`, `/fix`, `/socratic`, `/feynman`, `/flashcards`, and any request about how to learn efficiently. Pair strategy choice with `references/focus-feedback-iteration.md` so each strategy produces focus, feedback, and a next iteration.

## Strategy Selection

Prefer strategies that make the student retrieve, explain, compare, or transfer knowledge. Avoid long passive summaries unless the user is seeing a topic for the first time.

| Need | Use | Output |
|---|---|---|
| Remember facts, formulas, definitions | Retrieval practice | Short-answer prompts, flashcards, cloze cards |
| Keep knowledge over days/weeks | Spaced practice | SRS schedule and due review |
| Distinguish similar methods or question types | Interleaving | Mixed set with "choose the method" prompts |
| Understand why something works | Elaborative interrogation | Why/when/what-if questions |
| Check whether the student can teach it | Feynman technique | Student explanation, naive questions, repair card |
| Build reasoning step by step | Socratic questioning | One focused question, hint ladder, student summary |
| Avoid abstract memorization | Concrete examples | Positive example, counterexample, boundary case |
| Learn structure/process/mechanism | Dual coding | Text plus diagram, table, state trace, timeline, or flow |
| Improve solution monitoring | Self-explanation | Student explains each step's purpose and condition |
| Prepare attention before reading | Pretesting | Attempt a diagnostic question before explanation |
| Transfer across variants | Analogical comparison | Compare two problems, two concepts, or two solutions |
| Catch "I thought I knew it" gaps | Confidence calibration | Predict confidence before answering, then compare to the actual score |

## Evidence-Informed Defaults

- Use retrieval practice before rereading whenever the student has seen the topic once.
- Use spaced practice after every graded or repaired topic when a due date can be tracked.
- Use interleaving after the student can solve basic single-topic questions.
- Use elaborative interrogation when the student gives memorized but shallow answers.
- Use self-explanation for proofs, derivations, algorithms, code traces, and lab procedures.
- Use concrete examples before analogies when precision matters.
- Use dual coding for processes, systems, spatial relations, state transitions, timelines, and mechanisms.
- Use pretesting before materials review when the student does not know what to focus on.
- Use confidence calibration on high-stakes or "I definitely know this" topics — exam points are lost most often where confidence outruns competence.
- After any strategy produces feedback, choose one iteration move: repair, repeat, interleave, escalate, de-prioritize, or schedule.

## Strategy Recipes

### Retrieval Practice

Ask before explaining:

1. One memory question: definition, formula, theorem condition, syntax, or lab step.
2. One understanding question: why, when, compare, or counterexample.
3. One application question: solve, prove, calculate, debug, interpret, or operate.

After grading, update SRS.

### Interleaving

Use when the student has practiced at least two related topics.

Question set shape:

1. A topic A problem.
2. A topic B problem that looks similar.
3. A "choose the method first" problem.
4. A mixed problem requiring the student to state why the selected method applies.

Always include a short "how to recognize the question type" note after grading.

### Elaborative Interrogation

Ask:

- Why does this condition matter?
- What breaks if the condition is removed?
- What is the smallest example where this works?
- What is the smallest counterexample where it fails?
- Which adjacent concept is easiest to confuse with it?

Use this in Socratic mode, oral rehearsal, proof repair, and concept comparison.

### Self-Explanation

Use for multi-step solutions. Ask the student to annotate each step:

```markdown
Step:
Reason:
Condition used:
Possible trap:
```

Grade whether each reason is logically valid, not just whether the final answer is correct.

### Concrete Examples

For a hard concept, require three examples:

- Positive example: satisfies the definition or method.
- Non-example: close-looking case that does not satisfy it.
- Boundary example: smallest, extreme, degenerate, or edge case.

For programming, boundary examples are empty input, one element, duplicates, maximum size, invalid input if relevant, and off-by-one edges.

### Dual Coding

Pair text with the smallest useful visual:

- Math: proof dependency graph, number-line picture, function sketch, condition table.
- CS: state trace, memory diagram, stack/queue/table, algorithm flow.
- Physics/engineering: free-body diagram, circuit/process flow, unit table.
- Medicine/biology/chemistry: mechanism chain, structure-function map, comparison table.
- Humanities/law/economics: timeline, argument map, case comparison table.

In plain chat, use ASCII or Markdown tables. In agent shell, use Mermaid, plots, HTML, or runnable demos when appropriate.

### Pretesting

Before reading or summarizing a chapter, ask 2-3 low-stakes questions first. The goal is not scoring; it primes attention.

Output:

```markdown
Pretest:
1. [question]
2. [question]
3. [question]

After you answer, I will use the misses to decide what to explain.
```

### Analogical Comparison

Use when two concepts feel similar or the student chooses wrong methods.

Output:

```markdown
| Dimension | Concept/Method A | Concept/Method B | Exam signal |
|---|---|---|---|
```

Then give one mixed recognition question.

### Confidence Calibration

Use to expose overconfidence — the gap between *feeling* prepared and *being* prepared, which is where exam points quietly leak.

1. Before revealing the answer or grading, ask the student to rate confidence 1-5 (or %): "答这道题前，先估一个把握度 1-5。"
2. Grade as usual.
3. Compare prediction to outcome and name the calibration zone:

```markdown
| 信心 | 实际 | 校准 |
|---|---|---|
| 5（很有把握） | 6/10 | 过度自信 ⚠ 优先复习 |
| 2（没把握） | 9/10 | 低估自己，可少花时间 |
```

- **Overconfident** (high confidence, low score): flag as a priority weak point even though it "felt" known; route to `/fix` and SRS.
- **Underconfident** (low confidence, high score): reassure and de-prioritize to save time.
- **Well-calibrated**: proceed normally.

Track recurring overconfidence in the snapshot's Weak points so the final-week plan front-loads those topics.

## Anti-Patterns

- Do not replace practice with a long summary when the user asks to prepare for an exam.
- Do not use Feynman mode for complete beginners before teaching the first explanation.
- Do not use interleaving before the student has at least a basic grasp of each component topic.
- Do not create visuals that decorate without clarifying a relationship, process, or state.
- Do not mark a topic mastered from one correct easy answer; require transfer or variant success.
- Do not end a multi-step review response without a concrete next iteration target.
