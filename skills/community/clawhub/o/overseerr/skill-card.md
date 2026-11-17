## Description:

Request movies/TV and monitor request status via the Overseerr API (stable Overseerr, not the beta Seerr rewrite).

This skill is ready for commercial/non-commercial use.

## Publisher:

[j1philli](https://clawhub.ai/user/j1philli)

### License/Terms of Use:


## Use Case:

Developers and operators of self-hosted Overseerr instances use this skill to search for movie or TV titles, submit media requests, inspect request status, and monitor request updates through the Overseerr API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create media requests on the configured Overseerr server.

Mitigation: Install it only where the agent is expected to create and inspect Overseerr requests, and prefer searching first or using exact titles before submitting a request.

Risk: The Overseerr API key is sent to the configured server URL.

Mitigation: Use HTTPS for LAN or remote servers and keep OVERSEERR_API_KEY protected and narrowly scoped where possible.

Risk: Monitoring polls the Overseerr request endpoint repeatedly.

Mitigation: Use a reasonable monitor interval and limit filters so polling volume stays appropriate for the server.

## Reference(s):

- [Overseerr project homepage](https://overseerr.dev/)
- [ClawHub skill page](https://clawhub.ai/j1philli/skills/overseerr)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown instructions with shell commands; scripts print JSON or JSON Lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus OVERSEERR_URL and OVERSEERR_API_KEY; request actions call the configured Overseerr API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
