## Description: <br>
PostgreSQL-based job queue with priority scheduling, batch claiming, and progress tracking for building job queues without external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design PostgreSQL-backed background job queues with priority scheduling, batch claiming, retries, progress tracking, and stale job recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running install instructions from an unpinned external source could fetch code that differs from the reviewed ClawHub artifact. <br>
Mitigation: Prefer the reviewed ClawHub artifact, or inspect and pin the external source before installing. <br>
Risk: Applying the provided SQL directly to a production database could create behavior or schema choices that do not match local workload and recovery requirements. <br>
Mitigation: Review and test the SQL in a development environment before applying it to a real database. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/postgres-job-queue) <br>
- [Publisher Profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL, Go, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reference implementation patterns and review guidance; it does not execute database changes by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
