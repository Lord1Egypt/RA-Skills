---
name: live-evo
description: Self-evolving memory system that learns from verifiable tasks. Use when completing tasks where you can verify the outcome (coding, predictions, analysis). Automatically retrieves relevant past experiences and generates task-specific guidelines.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash(python *), Read, Write, Edit
---

# Live-Evo: Online Self-Evolving Memory

You are using the Live-Evo memory system that learns from past mistakes through experience accumulation and adaptive evaluation.

**IMPORTANT — Script location**: All scripts are in the `scripts/` subdirectory next to this SKILL.md file. When running scripts, use the absolute path to the `scripts/` directory relative to where this file is located. For example, if this SKILL.md is at `/path/to/live-evo/SKILL.md`, the scripts are at `/path/to/live-evo/scripts/`.

Experience data is stored persistently at `~/.live-evo/experience_db.jsonl` (independent of skill installation location).

## Core Workflow

### 1. Retrieve & Compile (Before Acting)

Run the experience retrieval script to find relevant past experiences:

```bash
python <scripts-dir>/retrieve.py --query "YOUR_TASK_DESCRIPTION"
```

If experiences are found, they will be compiled into a task-specific guideline. **Use this guideline to inform your approach.**

### 2. Decide: Verify or Direct Apply

**You must judge whether contrastive verification (two attempts) is worthwhile** based on:

| Factor | Do Contrastive Eval | Skip, Direct Apply |
|---|---|---|
| Cost of re-running | Low (e.g. run a test) | High (e.g. long build, API costs, heavy computation) |
| Verifiability | Clear ground truth exists (tests, known answer) | No easy way to verify programmatically |
| Task complexity | Simple enough to attempt twice | Too complex/large to reasonably duplicate |
| Guideline relevance | Retrieved guideline is highly relevant | Guideline is loosely related or no guideline found |

**If contrastive eval IS worthwhile** → Go to Step 2A
**If contrastive eval is NOT worthwhile** → Go to Step 2B

#### Step 2A: Contrastive Evaluation (Two Attempts)

Make **two independent attempts**:

**Attempt A (Without Memory):**
- Solve the task using only your base knowledge
- Record your answer/approach

**Attempt B (With Guideline):**
- Apply the retrieved guideline
- Solve the task with this informed approach
- Record your answer/approach

Then verify and update weights:

```bash
python <scripts-dir>/update.py \
  --task "TASK_DESCRIPTION" \
  --result-a "RESULT_WITHOUT_MEMORY" \
  --result-b "RESULT_WITH_GUIDELINE" \
  --correct "CORRECT_ANSWER" \
  --experience-ids "id1,id2,..."
```

#### Step 2B: Direct Apply with Feedback-Based Learning

When contrastive evaluation is not feasible:

1. **Apply the guideline directly** (if one was retrieved) and complete the task
2. **Observe feedback** from any of these sources:
   - User feedback (corrections, complaints, approval)
   - Environment signals (test results, error messages, build output)
   - Outcome observation (did the result work as expected?)
3. **Store experience directly** if feedback reveals a lesson:

```bash
python <scripts-dir>/add_experience.py \
  --question "THE_TASK_QUESTION" \
  --failure-reason "What went wrong (from feedback)" \
  --improvement "Key lesson learned" \
  --category "coding|analysis|prediction|debugging|other"
```

No contrastive comparison needed — just learn from what happened.

### 3. Add New Experience (On Any Failure)

Whenever a task fails or feedback reveals a learnable lesson — regardless of which path you took — store the experience:

```bash
python <scripts-dir>/add_experience.py \
  --question "THE_TASK_QUESTION" \
  --failure-reason "What went wrong" \
  --improvement "Key lesson learned" \
  --category "coding|analysis|prediction|debugging|other"
```

### 4. Update Weights (When Possible)

If you used a retrieved guideline and can determine whether it helped:

```bash
python <scripts-dir>/update.py \
  --task "TASK_DESCRIPTION" \
  --result-a "WHAT_WOULD_HAVE_HAPPENED" \
  --result-b "WHAT_ACTUALLY_HAPPENED" \
  --correct "CORRECT_OUTCOME" \
  --experience-ids "id1,id2,..."
```

If you cannot determine whether the guideline helped, **skip weight updates** — no update is better than a wrong update.

## When to Use Live-Evo

Use this system for:
- **Coding tasks**: Bug fixes, implementations where tests can verify
- **Analysis tasks**: Where ground truth can be checked
- **Predictions**: Forecasting with eventual verification
- **Problem solving**: Tasks with objectively correct answers
- **Any task with user feedback**: Even without formal verification, user corrections are valuable signals

## Experience Format

Each experience contains:
- `question`: The original task/question
- `failure_reason`: What went wrong in the original attempt
- `improvement`: Key lesson or approach that would have helped
- `missed_information`: Information sources or considerations that were missed
- `weight`: Quality score (0.1-2.0) updated based on usefulness
- `category`: Domain category for filtering

## Key Principles

1. **Cost-Aware Verification**: Only do contrastive evaluation when the cost is justified — don't waste tokens/time on expensive double-runs
2. **Feedback is Gold**: User corrections, test failures, and error messages are direct learning signals — always store these
3. **Selective Acquisition**: Only store experiences that contain a genuine, actionable lesson
4. **Weight-based Retrieval**: Good experiences rise, bad ones fade
5. **Task-Specific Guidelines**: Don't apply raw experiences — synthesize them into actionable guidance
6. **When in Doubt, Store**: It's better to store a potentially useful experience than to miss a lesson; low-quality experiences will naturally decay via weight updates

## Manual Commands

**View all experiences:**
```bash
python <scripts-dir>/list_experiences.py
```

**Search experiences:**
```bash
python <scripts-dir>/retrieve.py --query "your search query" --top-k 5
```

**Get statistics:**
```bash
python <scripts-dir>/stats.py
```
