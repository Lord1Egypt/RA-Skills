## Description:

Parallel Task Executor coordinates multiple user instructions as separate tasks with priority scheduling, dependency handling, progress tracking, and execution reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erichy777](https://clawhub.ai/user/erichy777)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to break multiple independent instructions into scheduled tasks, run them in parallel or serial modes, and collect status and result reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate destructive file, shell, network, API, and database actions without clearly documented safety gates.

Mitigation: Set strict limits and require explicit confirmation before deletion, uploads, shell or script execution, API calls, database operations, cleanup, and archival tasks.

Risk: The documented scheduler examples may not be safe production code for concurrency and result handling.

Mitigation: Review and harden concurrency limits, timeout behavior, retry handling, and result aggregation before production use.

## Reference(s):

- [Execution Report Format](references/reports.md)
- [Task Priority Specification](references/priorities.md)
- [Scheduler Algorithm Notes](references/scheduler.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured task, progress, and execution-report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-style task records, progress counters, retry status, and failure summaries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
