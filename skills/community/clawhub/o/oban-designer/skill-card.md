## Description: <br>
Design and implement Oban background job workers for Elixir. Configure queues, retry strategies, uniqueness constraints, cron scheduling, and error handling. Generate Oban workers, queue config, and test setups. Use when adding background jobs, async processing, scheduled tasks, or recurring cron jobs to an Elixir project using Oban. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design, configure, implement, and test Oban background job workers in Elixir applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook worker examples may be adapted to call user-controlled destinations. <br>
Mitigation: Validate and allowlist webhook destinations before enqueueing or executing delivery jobs. <br>
Risk: Job arguments may include untrusted URLs, file paths, or secrets if copied directly into production code. <br>
Mitigation: Avoid raw user-controlled URLs and file paths in jobs, keep secrets out of job arguments, and resolve sensitive values from trusted server-side storage. <br>
Risk: Cleanup and import examples include database deletes and bulk writes that could affect the wrong records if scoped incorrectly. <br>
Mitigation: Narrowly scope database updates and deletes by tenant, owner, or lifecycle state, and test those queries before production use. <br>
Risk: Migrations and cron schedules can affect production job execution if enabled without validation. <br>
Mitigation: Test Oban migrations and cron schedules in a non-production environment before enabling them in production. <br>


## Reference(s): <br>
- [Oban Designer on ClawHub](https://clawhub.ai/gchapim/oban-designer) <br>
- [Worker Patterns Reference](references/worker-patterns.md) <br>
- [Testing Oban Workers Reference](references/testing-oban.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Elixir and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
