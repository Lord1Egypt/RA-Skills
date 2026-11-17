## Description:

Ask a hosted judge before risky agent actions. Returns approve, hold, or escalate with a confidence number and the rule that fired, and keeps a reviewable decision log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huckcity](https://clawhub.ai/user/huckcity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check risky proposed actions before execution, including deleting data, spending money, touching production, changing credentials, or messaging customers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action descriptions and tool-call details are sent to and retained by the hosted jev-gate service.

Mitigation: Redact secrets, credentials, customer data, and regulated information before checks.

Risk: Optional MCP or hook client files are downloaded from the hosted service before use.

Mitigation: Review downloaded client files before enabling them in an agent environment.

Risk: If the hosted gate is unreachable or rejects the request, risky actions could otherwise proceed without review.

Mitigation: Treat gate errors as blocked, consistent with the skill's documented behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huckcity/skills/jev-gate)
- [jev-gate service homepage](https://jev-gate.fly.dev)
- [jev-gate dashboard](https://jev-gate.fly.dev/dashboard)
- [jev-gate client files](https://jev-gate.fly.dev/client)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper command returns approve, hold, escalate, or error through stdout and exit codes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
