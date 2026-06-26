# LeetCode Mock Interviewer

An [OpenClaw](https://github.com/openclaw/openclaw) skill that simulates realistic LeetCode-style coding interviews. Acts as a technical interviewer — not a tutor — forcing candidates to verbalize their thought process, decompose problems step by step, and handle follow-up questions before writing code.

## What It Does

- Picks any LeetCode problem matching the candidate's topic and difficulty — not limited to a fixed list
- Enforces a structured flow: clarify → brute force → complexity → optimize → code → follow-ups
- Asks interviewer-style follow-up questions about edge cases, tradeoffs, and constraint changes
- Delivers scored feedback (Communication, Problem-solving, Code quality) on a 1-5 scale with specific observations

## Modes

| Mode | Duration | Description |
|------|----------|-------------|
| **Full mock** | 15-30 min | One problem, complete 4-phase interview flow |
| **Follow-up only** | 10-15 min | Bring your own problem; interviewer handles questioning + feedback |
| **Rapid-fire warmup** | 10 min | 3 easy/medium problems, verbal solutions only |

## Interview Flow

```
Phase 1: Setup         → Role, difficulty, topic, hint preference
Phase 2: Present       → Problem description + examples + constraints
Phase 3: Interview     → Step A: Clarify + brute force
                         Step B: Complexity + optimization
                         Step C: Code / pseudocode
                         Step D: Follow-up probes (edge cases, tradeoffs, scaling)
Phase 4: Feedback      → Structured scorecard + ideal approach + next steps
```

## Supported Roles

- **SWE** — standard software engineering interview questions
- **MLE** — includes ML-adjacent problems (sparse matrix multiplication, LRU/LFU cache, hit counter)
- **AI Engineer** — similar to MLE with system design follow-ups

## Topics

Array, String, Hash Table, Two Pointers, Sliding Window, Stack, Queue, Linked List, Tree, Graph, BFS, DFS, Binary Search, Dynamic Programming, Greedy, Backtracking, Heap, Trie, Union Find

## Example Prompts

- "Mock interview me on a medium sliding window problem"
- "Interview me for an MLE role, hard difficulty"
- "Give me a rapid-fire warmup on arrays and hashing"
- "I solved Two Sum — interview me on my solution"
- "Practice coding interview, no hints"

## File Structure

```
.
├── SKILL.md                          # Core skill instructions
└── references/
    ├── problem-bank.md               # Example problems for inspiration (any LeetCode problem is valid)
    ├── interview-rubric.md           # 1-5 scoring criteria per category
    └── session-examples.md           # Example interview flows for each mode
```

## Key Rules

1. **No early hints** — only after 2-3 exchanges with no progress
2. **Interviewer, not teacher** — never explain the solution mid-interview
3. **Specific feedback** — no generic "good job"; cite exact moments
4. **Verbalize first** — candidates must explain before coding
5. **One question at a time** — don't overwhelm with multiple follow-ups
6. **One problem per session** — go deep, don't context-switch
7. **Help recovery, not rescue** — guide candidates out of freezes without solving for them

## Feedback Format

Each session ends with a structured scorecard:

- **What went well** — specific positive observations
- **What was missing** — specific gaps with examples
- **Scores** — Communication, Problem-solving, Code quality (each 1-5)
- **Ideal approach summary** — algorithm, complexity, key insight
- **What to practice next** — actionable suggestions

## License

MIT
