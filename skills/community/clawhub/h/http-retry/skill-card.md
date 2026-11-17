## Description:

Automatically retries HTTP requests with exponential backoff, timeout control, and connection pooling to handle network errors and rate limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add retry behavior, exponential backoff, timeout handling, and connection reuse patterns to HTTP request workflows that may encounter transient network failures or rate limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic retries can repeat state-changing HTTP operations if applied without idempotency checks.

Mitigation: Restrict retries to safe or explicitly idempotent operations before using the pattern in production.

Risk: Unbounded or poorly cleaned-up retry and timeout behavior can increase latency or leave timers active.

Mitigation: Cap backoff delays, clean up timers in a finally block, and define final-attempt failure behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/http-retry)
- [ClawHub publisher profile](https://clawhub.ai/user/2233admin)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retry, backoff, timeout, and connection reuse guidance for HTTP request handling.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
