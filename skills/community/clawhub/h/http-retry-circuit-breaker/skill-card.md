## Description:

Implements HTTP request retries with exponential backoff and a configurable circuit breaker to reduce transient failures and limit cascading errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwe123sddfsdfs](https://clawhub.ai/user/qwe123sddfsdfs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add configurable retry, timeout, jitter, and circuit breaker behavior around HTTP calls to unreliable services. It is most appropriate for idempotent or explicitly safeguarded requests where retry behavior is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retry and timeout behavior can make state-changing API calls unsafe if repeated requests are not acceptable.

Mitigation: Use the skill only where repeated requests are safe, or add idempotency keys and explicit retry controls for POST, PUT, DELETE, payments, submissions, account changes, and deletes.

Risk: A request timeout does not prove that the remote service stopped processing the operation.

Mitigation: Treat timed-out state-changing requests as uncertain, reconcile with the remote system, and avoid automatic blind retries unless the operation is idempotent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qwe123sddfsdfs/skills/http-retry-circuit-breaker)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [PERFORMANCE.md](artifact/PERFORMANCE.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, configuration snippets, and npm test commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Node.js >=14.0.0 and has no package dependencies; retry behavior should be reviewed before use with state-changing requests.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
