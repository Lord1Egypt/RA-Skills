## Description:

Executes an existing project masterplan phase by phase, using the plan as the implementation contract while testing, auditing, researching ambiguities, and maintaining an execution log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement an already-approved masterplan in strict roadmap order, with real testing, self-audits, researched deviations, and resumable progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill actively reads and changes project files, runs tests or application code, may create local commits, and maintains a persistent execution log.

Mitigation: Use it in a controlled workspace, review the masterplan before execution, and inspect resulting diffs, test output, commits, and execution-log entries.

Risk: The workflow may automatically search the web to resolve ambiguity or outdated implementation details.

Mitigation: For private or regulated codebases, set explicit instructions or environment controls that restrict web access or sensitive context sharing.

Risk: Parallel subagent execution can put pressure on available system memory.

Mitigation: Follow the bundled resource-safety reference: detect available memory before each batch, compute concurrency from current capacity, and fall back to sequential execution when uncertain.

Risk: The artifact states the skill has not yet been run end to end on a real project.

Mitigation: Treat initial use as a trial and validate the generated changes against the masterplan, tests, and execution standards before relying on the result.

## Reference(s):

- [Execution Standards](references/execution-standards.md)
- [Phase Execution Checklist](references/phase-execution-checklist.md)
- [Progress Log Template](references/progress-log-template.md)
- [Resource Safety](references/resource-safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses, source-code edits, shell commands, configuration changes, and execution-log Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains docs/masterplan/execution-log.md when executing a project masterplan.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
