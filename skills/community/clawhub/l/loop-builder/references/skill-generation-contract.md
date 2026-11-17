# Specialized Skill Generation Contract

Use this contract when the selected artifact is a reusable Skill. A repeated
task is not sufficient by itself; the workflow must be stable enough to
generalize across projects.

## Skillization Decision

Choose one conclusion:

- `Recommend Skillization`
- `Observe One More Run`
- `Do Not Skillize Yet`

Recommend Skillization only when:

- the same professional workflow appears across multiple tasks or projects;
- required inputs and missing-input behavior are stable;
- phase boundaries and acceptance checks are clear;
- the feedback signal is observable;
- risks, forbidden actions, and human gates are known;
- business-specific data can remain outside the Skill.

Observe another run when the workflow seems reusable but the evidence,
exceptions, or evaluator is not stable.

Do not Skillize when the task is one-off, depends on undocumented personal
judgment, or would mainly store private context.

## Mandatory Sequence

1. Model the real professional workflow.
2. Produce a Skill protocol draft.
3. Produce a temporary Prompt that can run the current task.
4. Wait for protocol approval.
5. Generate or modify Skill files only after explicit file-level approval.
6. Validate the package with the target repository's validator.
7. Request separate approval for installation, commit, push, or publication.

## Workflow Analysis

```md
## Scenario workflow analysis
- Professional role:
- Problem boundary:
- Expert's first analysis:
- Required inputs:
- Optional inputs:
- Runtime inputs:
- Phases:
  1. <phase>: entry / work / output / acceptance
- Generator responsibility:
- Evaluator responsibility:
- Human responsibility:
- Feedback signal:
- Uncertainty handling:
- Forbidden actions:
- Continue / stop / rollback / escalate rules:
```

If this analysis cannot describe a stable workflow, fall back to a Prompt,
checklist, Human-in-the-Loop flow, or specialized Agent.

## Skill Protocol Draft

```md
## Skill protocol draft

### Role
- Acts as:
- Does not act as:

### Trigger contract
- Trigger when:
- Do not trigger when:

### Input contract
- Required:
- Optional:
- Runtime-only:
- Missing required input behavior:

### Workflow phases
1. Inspect:
2. Analyze:
3. Plan:
4. Execute or generate:
5. Verify:
6. Hand off:

### Phase controls
- Allowed mutations:
- Forbidden mutations:
- Progress reporting:

### Acceptance
- Tool-based checks:
- Human checks:
- Feedback signal:
- Remaining-gap reporting:

### Circuit breakers
- Iteration limit and rationale:
- No-improvement rule:
- Scope rule:
- Permission and cost rule:

### Package
- SKILL.md:
- skill.json:
- references:
- templates:
- examples:
- scripts:

### Approval required
- Protocol:
- File generation:
- Installation:
- Publication:
```

## Temporary Prompt

Give the user a Prompt that can run the current task without pretending the
Skill already exists:

```md
You are acting as <professional role>.

Goal:
<goal>

Inputs:
<inputs>

Workflow:
1. Inspect the available evidence.
2. Stop if a required input is missing.
3. Plan one bounded work package.
4. Execute only allowed actions.
5. Verify with <signal>.
6. Stop on <rules>.
7. Present <human decision> before any risky action.

Output:
<artifacts and evidence>
```

## Package Acceptance

- The `description` contains real triggers and boundaries.
- The main instructions are concise and imperative.
- References are loaded only when needed.
- Examples include a minimal input and expected output notes.
- The package contains no credentials, local absolute paths, or private data.
- Public runtime content uses the repository's default public language.
- Repository validation passes.
- The generated package is not installed or published without separate
  authorization.
