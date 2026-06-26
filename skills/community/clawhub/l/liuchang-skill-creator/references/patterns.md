# Agent Skill Design Patterns

Based on Google ADK's 5 patterns + Claude Code best practices.

---

## Pattern 1: Tool Wrapper

**Purpose**: Make your agent an instant expert on any library or framework.

**When to use**: When you need the agent to work with specific libraries, APIs, or frameworks correctly.

**Structure**:
```
skill/
├── SKILL.md
└── references/
    └── conventions.md  # Library-specific rules
```

**Template**:
```markdown
---
name: api-expert
description: FastAPI development best practices. Use when building, reviewing, or debugging FastAPI applications.
metadata:
  pattern: tool-wrapper
  domain: fastapi
---

You are an expert in [library/framework]. Apply these conventions.

## Core Conventions
Load 'references/conventions.md' for complete rules.

## When Reviewing Code
1. Load conventions reference
2. Check user's code against each rule
3. Suggest fixes for violations

## When Writing Code
1. Load conventions reference
2. Follow every convention exactly
3. Add type annotations
```

**Example**: `skills/fastapi-expert/` → teaches FastAPI conventions

---

## Pattern 2: Generator

**Purpose**: Produce structured documents from a reusable template.

**When to use**: When you need consistent output format (reports, docs, commits).

**Structure**:
```
skill/
├── SKILL.md
├── references/
│   └── style-guide.md    # Formatting rules
└── assets/
    └── template.md       # Output template
```

**Template**:
```markdown
---
name: report-generator
description: Generates structured technical reports. Use when user asks to write, create, or draft a report.
metadata:
  pattern: generator
  output-format: markdown
---

You are a [type] generator. Follow these steps:

Step 1: Load 'references/style-guide.md' for rules.

Step 2: Load 'assets/template.md' for output structure.

Step 3: Ask user for missing variables.

Step 4: Fill template using style guide.

Step 5: Return completed document.
```

**Example**: `skills/report-generator/`, `skills/commit-message-generator/`

---

## Pattern 3: Reviewer

**Purpose**: Score code/content against a checklist by severity.

**When to use**: Code review, security audits, quality checks.

**Structure**:
```
skill/
├── SKILL.md
└── references/
    └── review-checklist.md  # Criteria by severity
```

**Template**:
```markdown
---
name: code-reviewer
description: Reviews code for quality and bugs. Use when user submits code for review.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

You are a [language] reviewer.

Step 1: Load 'references/review-checklist.md'

Step 2: Read and understand the code.

Step 3: Apply each rule. For violations:
- Note location
- Classify severity: error/warning/info
- Explain WHY and suggest fix

Step 4: Output structured review:
- Summary
- Findings (grouped by severity)
- Score 1-10
- Top 3 recommendations
```

**Example**: `skills/python-reviewer/`, `skills/security-audit/`

---

## Pattern 4: Inversion

**Purpose**: Agent interviews you before acting. Gathers requirements first.

**When to use**: Planning, system design, any complex task needing context.

**Key**: Explicit gating - DO NOT start until all phases complete.

**Template**:
```markdown
---
name: project-planner
description: Plans projects by gathering requirements first. Use when user says "I want to build", "help me plan".
metadata:
  pattern: inversion
  interaction: multi-turn
---

You are conducting a structured interview. DO NOT start building until all phases complete.

## Phase 1 — Discovery
Ask questions one at a time. Wait for each answer.
- Q1: "What problem does this solve?"
- Q2: "Who are the users?"
- Q3: "What's the expected scale?"

## Phase 2 — Constraints (only after Phase 1 complete)
- Q4: "Deployment environment?"
- Q5: "Tech stack preferences?"
- Q6: "Non-negotiable requirements?"

## Phase 3 — Synthesis (only after all answered)
1. Load 'assets/plan-template.md'
2. Fill template with gathered info
3. Present plan
4. Ask for feedback
5. Iterate until confirmed
```

**Example**: `skills/project-planner/`, `skills/architecture-designer/`

---

## Pattern 5: Pipeline

**Purpose**: Strict multi-step workflow with hard checkpoints.

**When to use**: Complex tasks where skipping steps is dangerous.

**Key**: Diamond gates - require user approval between steps.

**Template**:
```markdown
---
name: doc-pipeline
description: Generates API docs through multi-step pipeline. Use when user asks to document code.
metadata:
  pattern: pipeline
  steps: "4"
---

You are running a pipeline. Execute each step in order. DO NOT skip steps.

## Step 1 — Parse
Analyze code, extract public API.
Present inventory. Ask: "Complete?"

## Step 2 — Generate Docstrings (GATE: requires user approval)
Load 'references/docstring-style.md'
Generate docstrings for undocumented functions.
Present for approval. DO NOT proceed until confirmed.

## Step 3 — Assemble
Load 'assets/api-template.md'
Compile into documentation.

## Step 4 — Quality Check
Load 'references/quality-checklist.md'
Verify completeness. Fix issues.
Present final document.
```

**Example**: `skills/doc-pipeline/`, `skills/deployment-pipeline/`

---

## Choosing a Pattern

```
What does your skill need to do?
│
├── Provide knowledge → Tool Wrapper
├── Generate content?
│   └── Need requirements first? → Inversion → Generator
├── Evaluate/Review → Reviewer
└── Complex multi-step → Pipeline
    └── Add review at end? → Pipeline + Reviewer
```

---

## Combining Patterns

Patterns are not mutually exclusive:

- **Pipeline + Reviewer**: Pipeline ends with self-review
- **Generator + Inversion**: Start by gathering variables
- **Tool Wrapper + Reviewer**: Wrapper for context, Reviewer for output

---

## Metadata Field

Add to frontmatter to document pattern choice:

```yaml
metadata:
  pattern: [tool-wrapper|generator|reviewer|inversion|pipeline]
  # Pattern-specific fields:
  domain: fastapi           # for tool-wrapper
  output-format: markdown    # for generator
  severity-levels: error,warning,info  # for reviewer
  interaction: multi-turn    # for inversion
  steps: "4"                # for pipeline
```
