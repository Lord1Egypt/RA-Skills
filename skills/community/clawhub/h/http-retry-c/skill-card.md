## Description:

Provides an HTTP retry helper for C agents with exponential backoff, jitter, timeout configuration, and simple convenience wrappers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when adding retry guidance or C helper code for HTTP clients that need resilience around transient failures and rate limiting. Reviewers should treat the bundled implementation cautiously because the authoritative security evidence says it can report success without making a real HTTP request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped helper can report a successful HTTP response even when no request occurred.

Mitigation: Require a real transport callback, response validation, and tests before using it for authentication, payments, audit logging, data submission, policy checks, or other workflows where a real server response matters.

Risk: POST handling is represented as a placeholder that delegates to GET behavior.

Mitigation: Implement and review method-specific request handling before using generated POST retry code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/skills/http-retry-c)
- [Publisher profile](https://clawhub.ai/user/gatsby047-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with C code snippets and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retry settings such as max attempts, base delay, maximum delay, timeout, and callback guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
