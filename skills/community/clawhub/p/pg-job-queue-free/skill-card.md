## Description: <br>
Pg Job Queue Free helps agents provide PostgreSQL-backed job queue guidance, including table design, SKIP LOCKED batch claiming, priority scheduling, retries, timeout recovery, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and troubleshoot lightweight asynchronous job queues on PostgreSQL without adding Redis or RabbitMQ. It is suited for small-team workflows such as email queues, report generation, data cleanup, retry handling, and queue health monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests write and command-execution capability in a PostgreSQL workflow even though it is primarily a guidance document. <br>
Mitigation: Install only when those permissions are acceptable for the host agent, and review generated commands before running them. <br>
Risk: Generated SQL or queue operations could affect database state or production workloads. <br>
Mitigation: Review SQL manually, test against a non-production database first, and keep database credentials out of skill files and prompts unless intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pg-job-queue-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL snippets and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PostgreSQL schema, query, and operational advice; generated SQL and commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
