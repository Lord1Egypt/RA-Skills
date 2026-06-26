# FlowForge YAML Format

FlowForge workflows are defined in YAML files with a simple, predictable structure.

## File Structure

```yaml
name: workflow-name
description: Brief description of what this workflow does
start: first-node-name

nodes:
  node-name-1:
    task: Task description
    next: node-name-2

  node-name-2:
    task: Another task
    # ... continuation
```

## Top-Level Fields

### `name` (required)

Unique identifier for the workflow. Used in CLI commands like `flowforge start <name>`.

Rules:
- Lowercase with hyphens (e.g., `code-review`, `my-workflow`)
- No spaces or special characters
- Must be unique across all workflows

### `description` (required)

Human-readable description of the workflow's purpose.

```yaml
description: Review pull requests for code quality and standards
```

### `start` (required)

Name of the first node to execute when workflow starts.

```yaml
start: initialize
```

Must reference a node defined in the `nodes` section.

## Node Definition

Each workflow consists of one or more nodes. A node represents a step in the workflow.

### Basic Node Structure

```yaml
nodes:
  node-name:
    task: What to do at this step
    next: next-node-name  # or branches, or terminal
```

### Node Fields

#### `task` (required)

Natural language description of what to do at this node. Can be single line or multi-line:

```yaml
task: Run tests and verify all pass
```

```yaml
task: |
  Read the pull request description and code changes.
  Identify areas that need review:
  - Logic correctness
  - Code style
  - Test coverage
```

The agent executing the workflow uses this text as instructions.

#### Flow Control Fields (exactly one required)

A node must have exactly ONE of these:

1. **`next`**: Name of next node (linear flow)
2. **`branches`**: Array of conditional paths (branching flow)
3. **`terminal`**: Set to `true` (end of workflow)

## Node Types

### 1. Linear Node

Simplest form — one task, one next node.

```yaml
nodes:
  step1:
    task: First step
    next: step2

  step2:
    task: Second step
    next: step3
```

### 2. Branching Node

Multiple possible next nodes based on conditions.

```yaml
nodes:
  check-tests:
    task: Run test suite and check results
    branches:
      - condition: all tests pass
        next: deploy
      - condition: tests fail
        next: fix-bugs
      - condition: tests timeout
        next: investigate
```

**Rules:**
- Each branch has `condition` (description) and `next` (target node)
- When executing, use `flowforge next --branch N` (1-indexed)
- Conditions are documentation — agent decides which applies

**Common branching patterns:**

Success/failure:
```yaml
branches:
  - condition: success
    next: continue
  - condition: failure
    next: retry
```

Multiple outcomes:
```yaml
branches:
  - condition: approved
    next: merge
  - condition: changes requested
    next: revise
  - condition: rejected
    next: close
```

### 3. Terminal Node

Marks end of workflow. No next node.

```yaml
nodes:
  complete:
    task: Generate final report and close workflow
    terminal: true
```

When agent reaches terminal node and runs `flowforge next`, workflow is marked complete.

## Complete Examples

### Example 1: Simple Linear Workflow

```yaml
name: simple-review
description: Basic code review workflow
start: read

nodes:
  read:
    task: Read the code changes
    next: analyze

  analyze:
    task: Check for bugs and style issues
    next: report

  report:
    task: Write review comments
    terminal: true
```

### Example 2: Workflow with Branching

```yaml
name: ci-pipeline
description: Continuous integration workflow
start: build

nodes:
  build:
    task: Compile code and create artifacts
    branches:
      - condition: build succeeds
        next: test
      - condition: build fails
        next: notify-failure

  test:
    task: Run all test suites
    branches:
      - condition: tests pass
        next: deploy
      - condition: tests fail
        next: notify-failure

  deploy:
    task: Deploy to staging environment
    next: verify

  verify:
    task: Run smoke tests on deployed version
    terminal: true

  notify-failure:
    task: Send failure notification and log details
    terminal: true
```

### Example 3: Loop Pattern

Workflows can loop back to previous nodes:

```yaml
name: iterative-improvement
description: Improve code until quality threshold met
start: write

nodes:
  write:
    task: Write or modify code
    next: review

  review:
    task: Check code quality metrics
    branches:
      - condition: quality acceptable
        next: done
      - condition: needs improvement
        next: write

  done:
    task: Commit changes
    terminal: true
```

## Best Practices

### Keep Nodes Focused

Each node should have one clear purpose:

**Good:**
```yaml
read-docs:
  task: Read API documentation
  next: write-code

write-code:
  task: Implement feature using API
  next: test-code
```

**Bad (too much in one node):**
```yaml
do-everything:
  task: Read docs, write code, run tests, and deploy
  terminal: true
```

### Use Descriptive Names

Node names should indicate what happens:

**Good:** `check-build-status`, `deploy-to-prod`, `notify-team`

**Bad:** `step1`, `thing`, `node`

### Keep Workflows Short

Aim for 3-7 nodes. If workflow grows beyond 10 nodes, consider splitting into multiple workflows.

### Write Clear Tasks

Task descriptions should be specific and actionable:

**Good:**
```yaml
task: |
  Run `npm test` and check exit code.
  If any tests fail, read failure logs.
```

**Bad:**
```yaml
task: Do testing stuff
```

### Use Branches Sparingly

Branching adds complexity. Use only when genuinely needed:

**When to branch:**
- Success vs. failure outcomes
- Multiple distinct error cases
- Different user decisions

**When not to branch:**
- Sequential steps (use linear flow)
- Minor variations (handle in task description)

### Document Conditions Clearly

Branch conditions should be unambiguous:

**Good:**
```yaml
branches:
  - condition: HTTP status 200 and response contains "success"
    next: complete
  - condition: HTTP status 4xx or 5xx
    next: retry
```

**Bad:**
```yaml
branches:
  - condition: it worked
    next: next-step
  - condition: something went wrong
    next: other-step
```

## Validation Rules

FlowForge validates workflows when you run `flowforge define`:

1. **Required fields**: `name`, `description`, `start`, `nodes`
2. **Start node exists**: `start` must reference a node in `nodes`
3. **All referenced nodes exist**: Every `next` field must point to a valid node
4. **Terminal correctness**: Terminal nodes can't have `next` or `branches`
5. **Branch structure**: Each branch must have `condition` and `next`
6. **No orphaned nodes**: All nodes should be reachable from `start`

## Advanced Patterns

### Multi-Stage Pipeline

```yaml
nodes:
  stage1:
    task: Execute stage 1
    next: stage2

  stage2:
    task: Execute stage 2
    next: stage3

  stage3:
    task: Execute stage 3
    terminal: true
```

### Retry Logic

```yaml
nodes:
  attempt:
    task: Try operation (track attempts in task)
    branches:
      - condition: success
        next: done
      - condition: retryable failure
        next: wait
      - condition: fatal error
        next: abort

  wait:
    task: Wait 5 seconds before retry
    next: attempt

  done:
    task: Operation succeeded
    terminal: true

  abort:
    task: Log error and exit
    terminal: true
```

### Approval Gate

```yaml
nodes:
  prepare:
    task: Generate change preview
    next: request-approval

  request-approval:
    task: |
      Show preview to user.
      Ask: "Approve these changes? (yes/no)"
    branches:
      - condition: approved
        next: apply
      - condition: rejected
        next: cancel

  apply:
    task: Apply changes
    terminal: true

  cancel:
    task: Discard changes
    terminal: true
```

## Troubleshooting

### "Node not found"

Typo in `next` or `branches[].next` field. Check node names match exactly.

### "This node has branches. Use --branch <N>"

You ran `flowforge next` without `--branch` on a branching node. Run with `--branch 1`, `--branch 2`, etc.

### "Workflow not found"

Workflow name in `flowforge start <name>` doesn't match `name:` field in YAML. Run `flowforge list` to see available workflows.

### Workflow doesn't validate

Read error message from `flowforge define`. Common issues:
- Missing required fields
- Invalid node references
- Terminal node with `next` field

## See Also

- [SKILL.md](../SKILL.md) — How agents execute workflows
- [setup.md](../setup.md) — Installation guide
- [examples/](examples/) — Template workflows
