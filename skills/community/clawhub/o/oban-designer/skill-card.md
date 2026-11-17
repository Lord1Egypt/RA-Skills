## Description:

Design and implement Oban background job workers for Elixir. Configure queues, retry strategies, uniqueness constraints, cron scheduling, and error handling. Generate Oban workers, queue config, and test setups. Use when adding background jobs, async processing, scheduled tasks, or recurring cron jobs to an Elixir project using Oban.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, generate, configure, and test Oban workers for Elixir applications that need asynchronous jobs, scheduled tasks, retries, uniqueness controls, and queue tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied webhook or CSV-import worker examples may expose data or overwrite records if adapted without application-specific controls.

Mitigation: Validate webhook destinations, avoid secrets in job args, use trusted upload IDs instead of raw paths, enforce tenant authorization, limit import size, and make overwrite behavior explicit.

Risk: Generated background-job guidance may be incomplete for a production application's security and reliability requirements.

Mitigation: Review the skill before installation and review generated workers, queue settings, and examples before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gchapim/skills/oban-designer)
- [Worker Patterns Reference](references/worker-patterns.md)
- [Testing Oban Workers Reference](references/testing-oban.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Elixir and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Oban worker modules, queue configuration, migration examples, cron schedules, retry and uniqueness settings, and test patterns.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
