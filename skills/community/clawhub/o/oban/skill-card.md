## Description: <br>
Design and implement Oban background job workers for Elixir, including queues, retry strategies, uniqueness constraints, cron scheduling, error handling, worker code, queue configuration, and test setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add background jobs, asynchronous processing, scheduled tasks, recurring cron jobs, and related tests to Elixir applications that use Oban. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated webhook worker patterns can send payloads to externally supplied destinations. <br>
Mitigation: Validate webhook destinations, sign payloads, enforce timeouts, and avoid sending sensitive payload fields. <br>
Risk: Cleanup and pruning workers can perform destructive or broad database writes. <br>
Mitigation: Scope cleanup queries carefully and test destructive or bulk-write jobs with rollback or dry-run plans before production use. <br>
Risk: Import and ETL worker examples can read from file paths supplied in job arguments. <br>
Mitigation: Prefer server-controlled import paths or upload IDs, and validate inputs before processing. <br>


## Reference(s): <br>
- [Worker Patterns Reference](references/worker-patterns.md) <br>
- [Testing Oban Workers Reference](references/testing-oban.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Elixir and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Oban worker modules, queue and plugin configuration, migration commands, cron examples, testing patterns, and monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
