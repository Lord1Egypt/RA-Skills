## Description:

Checks recent agent-reported failures for websites, URL routes, MCP servers, and skills, lists known access paths, and lets agents report service failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryannsj](https://clawhub.ai/user/ryannsj)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill after an external service fails to compare recent reports, identify other known access paths, and optionally report the failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status checks or failure reports may disclose private URL paths or route identifiers to a third-party service.

Mitigation: Use a normalized hostname, service ID, or catalogued access-path ID; remove sensitive route details and ask before reporting failures involving private paths.

## Reference(s):

- [NotWorking skill release on ClawHub](https://clawhub.ai/ryannsj/skills/notworking)
- [NotWorking service](https://notworking.io)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-language status summary and optional access-path suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes recent failure reports; listed paths are not independently tested or endorsed.]

## Skill Version(s):

0.1.12 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
