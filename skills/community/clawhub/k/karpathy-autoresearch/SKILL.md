---
name: autoresearch
description: "Autonomously optimize any OpenClaw skill by running it repeatedly, scoring outputs against binary evals, mutating the prompt, and keeping improvements. Based on Karpathy's autoresearch methodology. Use when: optimize this skill, improve this skill, run autoresearch on, make this skill better, self-improve skill, benchmark skill, eval my skill, run evals on."
---

# autoresearch

Autonomously optimize any OpenClaw skill by running it repeatedly, scoring outputs against binary evals, mutating the prompt, and keeping improvements. Based on Karpathy's autoresearch methodology.

## Triggers

Use when: optimize this skill, improve this skill, run autoresearch on, make this skill better, self-improve skill, benchmark skill, eval my skill, run evals on.

## Description

Autonomous prompt/strategy optimization using Karpathy's autoresearch pattern. Mutate → evaluate → keep improvements. Works on anything with a measurable score: trading strategies, content scripts, thumbnails, ad copy, email subjects.

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. BASELINE │────▶│  2. MUTATE   │────▶│  3. EVALUATE │────▶│  4. DECIDE   │
│  Score the   │     │  Change one  │     │  Run scoring │     │  Better?     │
│  current     │     │  thing       │     │  function    │     │  Keep : Revert│
│  version     │     │              │     │              │     │              │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬───────┘
                                                                    │
                                                              Loop back to 2
```

## Instructions

### Step 1: Identify the Mutable File

The **mutable file** is the thing you're optimizing. It can be:
- A SKILL.md prompt/instructions
- A trading strategy config (thresholds, parameters)
- A content template (YouTube script format, ad copy structure)
- Any text file where changes produce measurable differences

Create or identify this file. Example:
```
my-skill/
├── SKILL.md          ← this is your mutable file
├── eval/
│   ├── test_cases.json
│   └── score.py
```

### Step 2: Create an Evaluation Function

Your eval function must:
1. **Take the current mutable file as input**
2. **Run it against test cases**
3. **Return a numeric score** (higher = better)

The eval can be anything:
- **LLM-as-judge**: Send output to an LLM, ask it to score 1-100
- **Backtest**: Run a strategy against historical data, measure Sharpe/returns
- **A/B metrics**: CTR, engagement, conversion rate
- **Binary pass/fail**: Count how many test cases pass out of N

Template eval function (customize for your domain):
```python
# eval/score.py
import json
import sys

def evaluate(mutable_file_path: str, test_cases_path: str) -> float:
    """
    Score the current version of the mutable file.
    Returns a float — higher is better.
    """
    with open(mutable_file_path) as f:
        current_version = f.read()
    
    with open(test_cases_path) as f:
        test_cases = json.load(f)
    
    scores = []
    for case in test_cases:
        # YOUR SCORING LOGIC HERE
        # Example: run the prompt, compare output to expected
        score = run_and_score(current_version, case)
        scores.append(score)
    
    return sum(scores) / len(scores)

if __name__ == "__main__":
    score = evaluate(sys.argv[1], sys.argv[2])
    print(f"SCORE: {score}")
```

### Step 3: Run the Autoresearch Loop

The loop follows this exact pattern:

```
1. Git init (if not already) — every experiment is a commit
2. Run eval on current version → get BASELINE score
3. For each experiment (1..N):
   a. Read the current mutable file
   b. Generate a MUTATION (change one thing — a threshold, a phrase, a rule)
   c. Write the mutated version
   d. Run eval → get NEW score
   e. If NEW > BASELINE:
      - Git commit with message: "exp-{N}: {description} | score: {baseline} → {new}"
      - Update BASELINE = NEW
      - Log: "✅ KEPT — improvement"
   f. If NEW <= BASELINE:
      - Git checkout the mutable file (revert)
      - Log: "❌ REVERTED — no improvement"
4. Print final summary: experiments run, improvements found, final score
```

#### Agent Instructions for Running the Loop

When the user says "run autoresearch on X", follow this procedure:

1. **Locate the mutable file** — ask the user or infer from context
2. **Locate or create the eval function** — the user must have a way to score
3. **Initialize git tracking** in the project directory
4. **Run baseline eval** — record the starting score
5. **Begin experiment loop:**
   - Read the mutable file
   - Think about what single change might improve the score
   - Make the change (be specific — change ONE thing per experiment)
   - Run eval
   - Keep or revert based on score
   - Log the result
6. **Continue for N experiments** (default: 20, or until user stops)
7. **Report results:**
   - Starting score → Final score
   - Number of experiments run
   - Number of improvements kept
   - Summary of what changes worked

#### Mutation Strategy

Good mutations change ONE thing at a time:
- **Numeric parameters**: Adjust thresholds, weights, window sizes
- **Prompt wording**: Rephrase instructions, add/remove constraints
- **Structure**: Reorder sections, add examples, remove redundancy
- **Rules**: Add a new rule, tighten an existing one, relax a constraint

Bad mutations change everything at once — you can't learn what worked.

### Step 4: Git Tracking

Every experiment MUST be tracked in git:
```bash
# Before starting
git init
git add -A
git commit -m "baseline: score {X}"

# After each successful mutation
git add -A
git commit -m "exp-{N}: {what changed} | {old_score} → {new_score}"

# After each failed mutation
git checkout -- {mutable_file}
```

This gives you:
- Full history of every experiment
- Ability to diff any two versions
- Easy rollback if something breaks
- A log of what mutations worked vs didn't

## Proven Results

### Case Study 1: Gold Trading Strategy
- **Task**: Optimize XAUUSD trading parameters
- **Mutable file**: Strategy config (EMA periods, momentum threshold, position sizing)
- **Eval function**: Backtest on historical data → Sharpe ratio
- **Baseline**: Sharpe 5.80
- **Experiments**: 86 in 25 minutes
- **Final**: Sharpe 12.23 (+111%)
- **Key discoveries**: Momentum threshold 0.003→0, EMA 8/24→5/11, position sizing optimization
- See: `references/gold-results.md`

### Case Study 2: YouTube Shorts Scripts
- **Task**: Optimize script-writing prompt for higher quality scores
- **Mutable file**: SKILL.md prompt instructions
- **Eval function**: LLM judge scoring 1-100
- **Baseline**: 94.3/100
- **Experiments**: 11
- **Final**: 96.7/100 (+2.5%)
- **Key discoveries**: Atomic sentences, strict 40-50 word range, stronger negative examples
- See: `references/youtube-results.md`

## Example Usage

**User**: "Run autoresearch on my email subject line skill"

**Agent workflow**:
1. Read the skill's SKILL.md (mutable file)
2. Create eval: generate 20 test emails → score subject lines with LLM judge (1-100 on open-rate prediction)
3. Baseline: 72.4/100
4. Experiment 1: Add "use numbers in subject lines" → 74.1 ✅ KEPT
5. Experiment 2: Add "max 6 words" → 71.8 ❌ REVERTED
6. Experiment 3: Add "start with a verb" → 75.3 ✅ KEPT
7. ... continue for 20 experiments
8. Final: 79.2/100 (+9.4%)

**User**: "Optimize my trading strategy config"

**Agent workflow**:
1. Read strategy.json (mutable file)
2. Eval: run backtest script → Sharpe ratio
3. Baseline: Sharpe 2.1
4. Experiment 1: Lower stop-loss from 2% to 1.5% → Sharpe 2.3 ✅
5. Experiment 2: Increase EMA fast period 12→15 → Sharpe 1.9 ❌
6. ... continue
7. Final: Sharpe 3.8 (+81%)
