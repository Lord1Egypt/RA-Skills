# Cost Optimization

> **Minimize token waste while maximizing agent effectiveness**
> Priority: MEDIUM | Category: Efficiency

## Overview

Unoptimized agents can burn 14 billion tokens without meaningful output. This skill provides strategies for cost-conscious autonomous operations.

## The Cost Problem

```yaml
typical_waste:
  context_drift:
    cause: "Repeatedly re-deriving same information"
    waste: "~40% of tokens"

  model_misuse:
    cause: "Using Opus for status checks"
    waste: "~30% of tokens"

  looping:
    cause: "Agent repeating same failed approach"
    waste: "~20% of tokens"

  unnecessary_retries:
    cause: "Retrying without learning"
    waste: "~10% of tokens"

potential_savings: "Up to 80% with optimization"
```

## Cost Optimization Strategies

### 1. Model Selection Optimization

```yaml
cost_per_million_tokens:
  opus_4_6:
    input: 15
    output: 75
    use_for: "Complex reasoning only"

  sonnet_4_6:
    input: 3
    output: 15
    use_for: "Daily operations (95% of work)"

  kimi_k2_5:
    input: 0.60
    output: 2
    use_for: "Background tasks, status checks"

  minimax_m2_5:
    input: 0.30
    output: 1.20
    use_for: "Simple, high-volume operations"

savings_opportunity:
  switching_from_opus_to_sonnet: "80% cost reduction"
  using_budget_models_for_status: "95% cost reduction"
```

### 2. Context Management

```yaml
context_optimization:
  avoid_redundancy:
    - "Don't include full file content repeatedly"
    - "Reference files by path after first read"
    - "Use summaries instead of full content"

  compression_strategy:
    - "Write decisions to files, not in chat"
    - "Use structured memory (MEMORY.md)"
    - "Compress session history periodically"

  selective_context:
    session_start:
      - "Read recent progress-log.md"
      - "Read current tasks from Todo.md"
      - "Read relevant sections of MEMORY.md"
      - "Don't load entire history"

    during_work:
      - "Only include relevant files"
      - "Summarize instead of full content"
      - "Reference, don't repeat"
```

### 3. Loop Prevention

```yaml
preventing_wasteful_loops:
  detect_looping:
    indicators:
      - "Same approach attempted 3+ times"
      - "Same error recurring"
      - "No progress after 2 iterations"

    action:
      - "STOP immediately"
      - "Document what's been tried"
      - "Analyze why it's not working"
      - "Try fundamentally different approach"
      - "Escalate after 3 attempts"

  cost_cap:
    per_task:
      max_tokens: 100000
      max_cost: 1.00
      action: "Stop and escalate"

    per_session:
      max_tokens: 500000
      max_cost: 5.00
      action: "Pause and require review"
```

### 4. Efficient Prompting

```yaml
prompt_optimization:
  be_specific:
    bad: "Help with the authentication"
    good: "Add JWT validation middleware to /api/protected endpoint"

  provide_context:
    bad: "Fix this bug"
    good: "Bug in auth.js:45 - null reference when user not found. Add validation check."

  avoid_redundancy:
    bad: "Read the file, then analyze it, then tell me what it does"
    good: "Analyze auth.js and summarize its purpose"

  use_structure:
    bad: [Long paragraph explaining task]
    good:
      task: "Add JWT validation"
      file: "auth.js"
      endpoint: "/api/protected"
      expected: "401 response for invalid tokens"
```

### 5. Caching & Memoization

```yaml
caching_strategy:
  document_analysis:
    cache: "File summaries in workspace/.cache/"
    invalidate: "When file changes"
    savings: "Avoid re-reading documentation"

  decision_memoization:
    cache: "Architectural decisions in MEMORY.md"
    invalidate: "Never (decisions are stable)"
    savings: "Avoid re-analyzing same problems"

  pattern_learning:
    cache: "Successful patterns in LESSONS.md"
    invalidate: "Additive only"
    savings: "Avoid re-discovering solutions"
```

## Cost Monitoring

### Track Your Usage

```bash
# Real-time cost tracking
openclaw cost monitor

# Cost breakdown by model
openclaw cost breakdown --by-model

# Cost breakdown by task type
openclaw cost breakdown --by-task

# Set budget alerts
openclaw cost budget --daily 10.00
openclaw cost alert --at 8.00

# Historical analysis
openclaw cost history --days 30

# Identify expensive operations
openclaw cost analyze --top-spenders
```

### Cost Metrics

```yaml
key_metrics:
  per_task:
    target: "< $0.50"
    warning: "> $1.00"
    critical: "> $2.00"

  per_session:
    target: "< $5.00"
    warning: "> $10.00"
    critical: "> $20.00"

  daily:
    target: "< $20.00"
    warning: "> $50.00"
    critical: "> $100.00"

  efficiency:
    good: "> 10 tasks per $1"
    acceptable: "5-10 tasks per $1"
    poor: "< 5 tasks per $1"
```

## Cost Optimization Checklist

### Before Starting Work

```yaml
pre_work_checks:
  model_selection:
    - [ ] "Is Sonnet 4.6 appropriate? (default yes)"
    - [ ] "Does this truly require Opus?"
    - [ ] "Can budget model handle this?"

  context_preparation:
    - [ ] "Read only relevant files"
    - [ ] "Summaries instead of full content where possible"
    - [ ] "Check memory for existing decisions"

  scope_clarity:
    - [ ] "Task is specific and bounded"
    - [ ] "Success criteria defined"
    - [ ] "No ambiguous requirements"
```

### During Work

```yaml
during_work_monitoring:
  loop_detection:
    - [ ] "Different approaches each iteration"
    - [ ] "Learning from failures"
    - [ ] "Documenting progress"

  cost_awareness:
    - [ ] "Checking token usage periodically"
    - [ ] "Switching to cheaper models when appropriate"
    - [ ] "Avoiding redundant operations"

  efficiency:
    - [ ] "Making progress, not spinning"
    - [ ] "Writing to files, not chat"
    - [ ] "Using memory effectively"
```

### After Work

```yaml
post_work_review:
  cost_analysis:
    - [ ] "What was the final cost?"
    - [ ] "Was it cost-effective?"
    - [ ] "What could be optimized?"

  learning:
    - [ ] "Document expensive patterns to avoid"
    - [ ] "Document cost-effective approaches"
    - [ ] "Update LESSONS.md"

  planning:
    - [ ] "How to reduce cost next time?"
    - [ ] "Are there cheaper alternatives?"
```

## Cost-Saving Techniques

### 1. Batch Operations

```yaml
technique: "Group related operations"
instead_of:
  - "Process 1 file, get summary"
  - "Process 1 file, get summary"
  - "Process 1 file, get summary"

do:
  - "Process all files, get all summaries"
  - "Single context setup"
  - "Batch processing"

savings: "~60% on similar operations"
```

### 2. Reference Instead of Repeat

```yaml
technique: "Reference previously read content"
instead_of:
  - "Include full file content in every message"

do:
  - "File at path/to/file.js (read previously)"
  - "Function getAuthConfig() (defined above)"

savings: "~40% on multi-step tasks"
```

### 3. Progressive Disclosure

```yaml
technique: "Provide context incrementally"
instead_of:
  - "Include all documentation upfront"

do:
  - "Start with task description"
  - "Read docs only when needed"
  - "Add context as questions arise"

savings: "~30% on average task"
```

### 4. Use Cheaper Models for Subtasks

```yaml
technique: "Model selection per subtask"
example_task: "Update authentication and tests"

breakdown:
  subtask_1:
    task: "Read existing auth code"
    model: "Sonnet 4.6" # Good comprehension
    cost: "$0.02"

  subtask_2:
    task: "Identify what needs updating"
    model: "Sonnet 4.6"
    cost: "$0.03"

  subtask_3:
    task: "Write new auth code"
    model: "Codex GPT-5.3" # Best for code
    cost: "$0.05"

  subtask_4:
    task: "Write tests"
    model: "Codex GPT-5.3"
    cost: "$0.04"

  subtask_5:
    task: "Run tests and report results"
    model: "Kimi K2.5" # Simple task
    cost: "$0.01"

total: "$0.15"
vs_opus: "$0.75 (80% savings)"
```

## Anti-Patterns (Cost Drains)

### ❌ The "Opus for Everything" Pattern

```yaml
problem: "Using Opus for all tasks"
cost_impact: "5x more expensive"
solution: "Default to Sonnet, upgrade only when needed"
```

### ❌ The "Full Context Every Time" Pattern

```yaml
problem: "Including all files in every message"
cost_impact: "3x more tokens per message"
solution: "Reference previously read content"
```

### ❌ The "Vague Prompt" Pattern

```yaml
problem: "Ambiguous requests requiring clarification loops"
cost_impact: "2-3x more tokens through back-and-forth"
solution: "Specific, bounded task descriptions"
```

### ❌ The "Looping on Failure" Pattern

```yaml
problem: "Trying same failed approach repeatedly"
cost_impact: "Unbounded token waste"
solution: "Stop after 2 attempts, try different approach"
```

### ❌ The "Re-deriving Knowledge" Pattern

```yaml
problem: "Re-analyzing same problems each session"
cost_impact: "~40% of tokens wasted"
solution: "Use MEMORY.md and LESSONS.md"
```

## Cost Optimization Commands

```bash
# Analyze cost trends
openclaw cost analyze --trend

# Find expensive patterns
openclaw cost patterns --expensive

# Compare model performance
openclaw cost compare-models --by-task-type

# Optimize based on history
openclaw cost optimize --apply

# Set cost limits
openclaw cost limit --per-task 1.00
openclaw cost limit --per-session 10.00
```

## ROI Calculation

```yaml
evaluating_roi:
  formula: "Value delivered / Cost incurred"

  good_roi:
    ratio: "> 10"
    description: "Excellent value"
    example: "$50 worth of work for $5 cost"

  acceptable_roi:
    ratio: "5-10"
    description: "Worthwhile"
    example: "$25 worth of work for $5 cost"

  poor_roi:
    ratio: "< 5"
    description: "Needs optimization"
    example: "$10 worth of work for $5 cost"

  improving_roi:
    - "Use cheaper models where possible"
    - "Reduce task completion time"
    - "Increase task autonomy"
    - "Prevent expensive loops"
```

## Key Takeaway

**Cost-conscious doesn't mean less capable.** Smart model selection, efficient context management, and loop prevention can reduce costs by 80% while maintaining effectiveness.

---

**Related Skills**: `model-routing.md`, `execution-discipline.md`, `memory-persistence.md`
