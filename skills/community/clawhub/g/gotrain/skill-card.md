## Description:

MTA system train departures (NYC Subway, LIRR, Metro-North). Use when the user wants train times, schedules, or service alerts for MTA transit. Covers MTA Subway, LIRR, and Metro-North across the greater New York area.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for MTA station searches, train departures, service alerts, and favorite-station commands through the gotrain CLI.

### Deployment Geography for Use:

Global; transit information is specific to the MTA Subway, LIRR, and Metro-North systems in the greater New York area.

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm command globally.

Mitigation: Install only if the npm package and maintainer are trusted, avoid elevated privileges, and prefer a pinned or locally scoped install when stronger supply-chain control is required.

Risk: Transit departures and service alerts may change quickly.

Mitigation: Treat returned schedules and alerts as time-sensitive operational guidance and confirm critical trips against an official MTA source when needed.

## Reference(s):

- [gotrain ClawHub Skill Page](https://clawhub.ai/gumadeiras/skills/gotrain)
- [gumadeiras ClawHub Publisher Profile](https://clawhub.ai/user/gumadeiras)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gotrain CLI binary; command results depend on the installed npm package and current MTA data.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
