## Description:

Async Python patterns via asyncio and aiohttp for I/O-bound concurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Python developers use this skill to build and debug I/O-bound asynchronous applications with asyncio and aiohttp, including concurrent tasks, rate limits, timeouts, error handling, and async tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The database example interpolates user_id directly into SQL strings; adapting this pattern with untrusted values could allow SQL injection.

Mitigation: Use parameterized queries with bound values for all user-supplied data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-parseltongue-python-async)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue)

## Skill Output:

**Output Type(s):** [Code, Guidance, Markdown]

**Output Format:** [Markdown with inline Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progressively organized reference modules]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
