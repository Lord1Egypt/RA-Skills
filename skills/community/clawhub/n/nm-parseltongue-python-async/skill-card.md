## Description:

Async Python patterns via asyncio and aiohttp for I/O-bound concurrency

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Python developers use this skill to apply asyncio and aiohttp patterns for concurrent I/O, including task coordination, rate limiting, error handling, timeouts, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The database example interpolates values into SQL strings, which can be unsafe if values are untrusted.

Mitigation: Use parameterized queries through the database driver's API, especially for user-controlled values.

Risk: Concurrent web requests can exceed a remote service's limits or access rules.

Mitigation: Respect service terms and access policies, and bound request concurrency with semaphores and timeouts.

## Reference(s):

- [Claude Night Market Parseltongue plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-parseltongue-python-async)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with Python examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progressive modules cover async patterns, concurrency control, error handling, practical examples, and testing.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
