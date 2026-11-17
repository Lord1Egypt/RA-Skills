## Description:

Query Belgian railway (NMBS/SNCB) schedules via the irail CLI for train departures, connections between stations, train compositions, and service disruptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dedene](https://clawhub.ai/user/dedene)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to retrieve Belgian rail schedules, route connections, station liveboards, train composition details, vehicle information, and current service disruptions through the irail CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party dedene irail CLI and its package sources.

Mitigation: Check the upstream project and installed version before use, and install only from package sources you trust.

Risk: Rail queries are sent to the public iRail service.

Mitigation: Limit queries to Belgian rail information you are comfortable sending to the public service.

## Reference(s):

- [ClawHub Irail Skill](https://clawhub.ai/dedene/skills/irail)
- [dedene irail-cli](https://github.com/dedene/irail-cli)
- [iRail API](https://api.irail.be/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the public iRail API through the irail CLI; JSON output is recommended for agent parsing.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata version: 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
