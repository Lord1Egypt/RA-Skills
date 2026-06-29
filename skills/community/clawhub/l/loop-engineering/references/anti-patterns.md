# Anti-Patterns and Corrections

In Loop Engineering practice, the following 6 anti-patterns are the most common and most destructive. Each entry includes symptoms, consequences, causes, and correction strategies.

---

## 1. Loops Without Termination Conditions

### Symptoms

The Agent runs continuously in `/loop` or `/goal`, with the round counter in the logs steadily increasing, but no meaningful progress in task state. CPU and token consumption grow linearly until resources are exhausted or the process is forcefully terminated externally.

Log example:

```
[Round 47] Still working on task...
[Round 48] Still working on task...
[Round 49] Still working on task...
```

### Consequences

- Token budget is exhausted, preventing other tasks from executing
- Output quality degrades as rounds increase (context bloat)
- By the time the user notices, substantial wasteful consumption has already occurred

### Causes

- `maxRounds` is not set, or is set too high
- Goal conditions are vaguely defined and not objectively verifiable (e.g., "make the code better")
- Completion detection logic has a bug that always returns false

### Correction Strategy

1. All `/loop` and `/goal` must set `maxRounds`, with a default not exceeding 20
2. Completion conditions must be objectively verifiable: file exists, tests pass, metrics met, diff is empty
3. Add progress checkpoints within the loop body -- terminate early if N consecutive rounds show no meaningful change
4. Use an independent model for completion judgment, avoiding self-assessment by the executing Agent

```yaml
# Correct example
loop:
  maxRounds: 10
  completionCheck:
    type: external
    condition: "testResult.passed == true && coverage >= 80"
  earlyExit:
    noProgressRounds: 3
```

---

## 2. Overly Large Single-Agent Responsibilities

### Symptoms

A single Agent is asked to simultaneously handle requirements analysis, code writing, testing, deployment, and documentation generation. As rounds progress, the context window becomes filled with fragmented information from each phase, the Agent begins to forget early decisions, and output quality drops off a cliff.

### Consequences

- Context window frequently overflows, losing early information
- Multiple tasks execute serially, total time far exceeds parallel approaches
- Difficult to locate errors -- hard to trace which phase the problem originated in
- Single point of failure: one Agent crash zeroes out the entire task

### Causes

- Mistakenly equating "one task" with "one Agent"
- Underestimating the complexity of context management
- Not evaluating the natural boundaries and parallelizability of tasks

### Correction Strategy

1. Split by responsibility into Sub-agents: analysis Agent, coding Agent, testing Agent, review Agent
2. Each Sub-agent receives only the minimum context needed to fulfill its responsibility
3. Use `sessions_spawn` to dispatch independent sub-tasks in parallel
4. The main Agent is only responsible for orchestration and result aggregation, not participating in specific execution

```yaml
# Anti-pattern: one Agent does everything
agent:
  tasks:
    - analyze
    - implement
    - test
    - deploy

# Correct: split into Sub-agents
orchestrator:
  subAgents:
    - name: analyzer
      task: "Analyze requirements and output spec"
    - name: coder
      task: "Implement code according to spec"
      dependsOn: [analyzer]
    - name: tester
      task: "Write and run tests"
      dependsOn: [coder]
```

---

## 3. Ignoring Feedback Signals

### Symptoms

The Agent repeatedly encounters the same compilation errors, test failures, or type mismatches during execution, but applies the same fix strategy each round (or ignores them outright) without performing root cause analysis. The same error pattern can be seen repeating 3+ times in the logs.

### Consequences

- Problems accumulate continuously, eventually causing the entire task to fail
- Many rounds are wasted on ineffective fixes
- More serious architectural issues are masked

### Causes

- Feedback signals are not structurally parsed; the Agent only sees "it failed"
- Missing a check mechanism to verify "whether the previous round's fix was effective"
- Root cause analysis steps are not embedded in the loop design

### Correction Strategy

1. Structure feedback signals: error type, location, occurrence count, list of attempted fixes
2. Introduce a "fix retrospect" step: before each round's fix, first check whether the previous round's fix took effect
3. When the same error occurs 2 consecutive times, forcibly trigger root cause analysis instead of continuing to fix
4. For issues that cannot be self-resolved, set up an escalation mechanism to notify a human

```yaml
# Feedback handling flow
feedback:
  onFailure:
    - action: parseError
      extract: [type, file, line, message]
    - action: compareWithPrevious
      if: "sameErrorCount >= 2"
      then: rootCauseAnalysis
    - action: escalate
      if: "sameErrorCount >= 5"
      notify: human
```

---

## 4. State Loss

### Symptoms

The Agent re-reads files, re-analyzes context, and re-establishes understanding of the task in every round, as if the previous round never happened. Logs show a large number of repetitive "exploratory" operations, with each round's conclusions being highly similar but disconnected from one another.

### Consequences

- Progress cannot accumulate across rounds; the task hovers near the starting point indefinitely
- Repeated context loading consumes substantial tokens
- Decision quality cannot improve across rounds

### Causes

- Worktree or equivalent persistence mechanism is not used to save intermediate state
- The context window is limited, causing early state to be naturally evicted
- State format is not standardized, so subsequent rounds cannot parse the previous round's output

### Correction Strategy

1. Write critical state to Worktree at the end of each round: current progress, confirmed decisions, pending issues
2. At the start of each round, prioritize restoring state from Worktree rather than re-scanning
3. Use structured formats (JSON/YAML) to save state, ensuring machine parsability
4. Distinguish between "persistent state" (unchanged across rounds) and "round state" (temporary for this round) to avoid confusion

```yaml
# Worktree state management
worktree:
  stateFile: ".loop/state.json"
  schema:
    progress: "string"       # Description of current progress
    decisions: "array"       # Confirmed decisions
    pending: "array"         # Pending issues
    lastRoundOutput: "object" # Summary of previous round output
```

---

## 5. Over-Engineering

### Symptoms

A simple conditional logic (e.g., "skip if file exists") is wrapped into a full loop system: Automation trigger -> Worktree state save -> Sub-agent execution -> feedback loop validation -> multiple rounds. Implementing a simple check requires 5+ files and hundreds of lines of configuration.

### Consequences

- System complexity far exceeds the problem itself, maintenance costs skyrocket
- Difficult to debug -- a simple logic error requires tracing through multiple layers of abstraction
- Other team members struggle to understand and modify the system
- The overhead of the loop system (scheduling, context switching) exceeds the actual task overhead

### Causes

- Blindly applying Loop Engineering patterns without evaluating the true complexity of the task
- Over-designing for extensibility that "might be needed in the future"
- The team's understanding of Loop Engineering stops at "everything must use loops"

### Correction Strategy

1. Before deciding, first ask: does this task truly require multiple rounds? Can it be done with a single call?
2. Follow the "minimum viable loop" principle: start with the simplest implementation, introduce loops only when truly needed
3. Complexity judgment criterion: if the configuration code is more than 3x longer than the business logic, it indicates over-engineering
4. Simple if-else, scripts, and cron jobs remain valid choices -- do not replace them with loop systems

```
Decision flow:

Does the task involve multiple rounds?
  |-- No -> Use a single call / script / if-else
  |-- Yes -> Is there a clear feedback signal?
              |-- No -> May not need a loop, re-evaluate
              |-- Yes -> Minimal loop design (maxRounds <= 5)
```

---

## 6. Feedback Signal Contamination

### Symptoms

The Agent generates feedback signals and consumes them itself, forming a closed confirmation bias loop. For example: after writing code, the Agent writes its own tests, runs them itself, and judges them as passing. The tests all pass because they didn't cover edge cases, the Agent concludes the task is complete, but in reality the code has serious defects.

### Consequences

- False sense of security: all metrics are green, but actual quality is substandard
- Errors are systematically amplified -- the Agent goes further and further in the wrong direction
- External review is bypassed, problems accumulate until late stages before being exposed, making fixes extremely costly

### Causes

- The generator and the verifier are the same Agent or the same model
- Feedback signals (tests, reviews, checks) are not independently verified
- Lacking external standards or ground truth as a reference

### Correction Strategy

1. Separate generation from evaluation: the Agent executing the task and the Agent evaluating results must be different instances
2. Use a different model or at least a different temperature for evaluation
3. Introduce external feedback sources: actually run tests, lint checks, type checks -- rather than relying solely on Agent judgment
4. Also validate the evaluation Agent itself: spot-check whether its judgments match actual results

```yaml
# Feedback signal separation
pipeline:
  - stage: implement
    agent: coder-1
  - stage: test
    agent: tester-1           # Different Agent
    tool: "npm test"          # External tool verification
  - stage: review
    agent: reviewer-1         # Different Agent, different model
    model: "claude-sonnet"    # Ensure model differs from executing Agent
  - stage: finalCheck
    tool: "npm run lint && npm run typecheck"  # Pure external verification
```

---

## Correction Strategy Summary

| Anti-Pattern | Core Symptom | Root Cause | Corrective Action |
|--------|----------|------|----------|
| Loops without termination conditions | Round counter monotonically increases, no meaningful progress | Missing maxRounds / completion conditions not verifiable | Set maxRounds; use objectively verifiable completion conditions; add progress checkpoints |
| Overly large single-Agent responsibilities | Context frequently overflows, output quality degrades in later rounds | Multiple responsibilities coupled within one Agent | Split into Sub-agents by responsibility; dispatch independent tasks in parallel |
| Ignoring feedback signals | Same error repeats 3+ times, no root cause analysis | Feedback signals not structured; missing retrospect checks | Structurally parse errors; trigger root cause analysis on consecutive same errors; set escalation |
| State loss | Re-explores each round, outputs similar but disconnected | Worktree not used; state format not standardized | Structured state persistence; restore from Worktree each round; distinguish persistent/temporary state |
| Over-engineering | Configuration code is 3x+ longer than business logic | Blindly applying loop patterns; over-designing for the future | Evaluate true task complexity; start from minimal implementation; keep it simple |
| Feedback signal contamination | All metrics green but actual quality is poor | Generator and verifier are the same Agent | Separate generation from evaluation; use different models/instances; introduce external verification |

> These anti-patterns are not mutually exclusive -- it is common to see multiple anti-patterns appearing simultaneously in real projects. When troubleshooting, check from top to bottom item by item; typically, after resolving the first 2-3, the remaining issues will naturally ease.