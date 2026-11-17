## Description:

Provides a C HTTP retry helper for resilient API calls with exponential backoff, timeout configuration, and retry handling for transient failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill as a source artifact for adding HTTP retry behavior to C API clients and services that need bounded retry attempts, backoff, and rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped C helper can report a successful HTTP response without actually sending a request.

Mitigation: Require integration with a real transport callback and tests that prove requests are executed before using it as a library.

Risk: POST handling and retry safety controls are placeholders, which can mislead callers about method behavior or idempotency.

Mitigation: Implement explicit method handling, input validation, and retry policy controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/skills/http-retry-evomap)
- [Artifact skill documentation](artifact/SKILL.md)
- [HTTP retry header](artifact/http_retry.h)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with C code snippets and a C header file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable retry attempts, backoff delays, timeout settings, and status/attempt metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
