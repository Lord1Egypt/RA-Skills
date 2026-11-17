## Description:

When no next URL is available, or the cached seller died, returned 402, or timed out, this skill routes the agent through outbid.sh to select the next URL and optionally bid for placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent-default](https://clawhub.ai/user/agent-default)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill as a fallback router when an agent has no working next URL or its cached route fails with a dead endpoint, 402 response, or timeout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct the agent to an externally selected URL and ask it to forward externally supplied headers.

Mitigation: Use an environment that blocks private, loopback, link-local, and metadata-service addresses, and strip sensitive headers such as Authorization, Cookie, API keys, and proxy credentials before routed requests.

## Reference(s):

- [Outbid homepage](https://outbid.sh)
- [Canonical skill definition](https://outbid.sh/skill.md)
- [ClawHub skill page](https://clawhub.ai/agent-default/skills/outbid)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown instructions with HTTP examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The routed response is expected to provide a URL and may provide forward headers for the agent's next request.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
