## Description:

Parallel Dispatch helps agents identify independent, batched, or dependency-bound tasks and dispatch them with bounded parallelism, result aggregation, timeout handling, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan parallel execution for clearly separable work, batches of similar tasks, and staged workflows with dependencies. It is useful when an agent needs concise scheduling guidance, bounded concurrency, result aggregation, and failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel dispatch can cause multiple independent tasks to run at once, including destructive or account-changing tasks if they are batched together.

Mitigation: Use this skill only for clearly separable work, and avoid batching destructive or account-changing actions unless parallel execution is explicitly intended.

Risk: Incorrect dependency analysis can run dependent tasks in the wrong order.

Mitigation: Identify task dependencies before dispatch and use dependency-aware scheduling for workflows where later steps depend on earlier results.

Risk: Unbounded or poorly tuned concurrency can increase resource use or make failures harder to inspect.

Mitigation: Keep maximum parallelism and per-task timeouts bounded, and aggregate success and error results for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/skills/parallel-dispatch)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, PowerShell, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounded parallelism, timeout settings, dependency analysis, result aggregation, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
