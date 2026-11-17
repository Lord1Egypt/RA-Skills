## Description:

Real-time bike-sharing station data for 600+ networks worldwide -- Citi Bike, Velib, Nextbike, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query bike-share networks, station availability, and city or country coverage for travel apps, urban mobility dashboards, local availability answers, and micro-mobility research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an automatically resolved npm package for the MCP bridge, creating supply-chain risk.

Mitigation: Pin mcp-remote to a reviewed version, install through a controlled lockfile or package process, and run it with limited filesystem, environment-variable, and network access.

## Reference(s):

- [Pipeworx CityBikes Pack](https://pipeworx.io/packs/citybikes)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-citybikes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for calling MCP tools that return bike-share network and station data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
