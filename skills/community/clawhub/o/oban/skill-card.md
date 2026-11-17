## Description:

Design and implement Oban background job workers for Elixir, including queues, retry strategies, uniqueness constraints, cron scheduling, error handling, worker code, queue configuration, and test setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add background jobs, asynchronous processing, scheduled tasks, recurring cron jobs, and Oban test coverage to Elixir applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated webhook workers may post data to arbitrary URLs.

Mitigation: Require authorized endpoint allowlists, tenant ownership checks, request signing, timeouts, bounded retries, and tests before production use.

Risk: Generated notification workers may send email or SMS to unintended recipients.

Mitigation: Validate recipient authorization, user preferences, tenant scoping, unsubscribe or consent rules, and avoid logging sensitive message contents.

Risk: Generated import or cleanup workers may read arbitrary file paths or perform broad database writes and deletes.

Mitigation: Scope file access to approved storage, validate tenant identifiers, review retention rules, bound batch sizes, and test destructive jobs with representative fixtures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gchapim/skills/oban)
- [Worker Patterns Reference](artifact/references/worker-patterns.md)
- [Testing Oban Workers Reference](artifact/references/testing-oban.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Elixir code blocks, bash commands, configuration examples, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Oban worker modules, queue configuration, migration commands, cron schedules, retry and uniqueness settings, test patterns, and monitoring guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
