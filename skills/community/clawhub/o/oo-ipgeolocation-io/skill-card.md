## Description:

IPGeolocation.io (ipgeolocation.io). Use this skill for ANY IPGeolocation.io request — searching and reading data. Whenever a task involves IPGeolocation.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can retrieve IP geolocation, time zone, sunrise, sunset, and moon-phase information through their connected IPGeolocation.io account. The skill guides the agent to inspect an action's schema and submit a matching request through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions include remote installer commands whose full effects are unverified.

Mitigation: Review and verify the CLI installation separately, and require approval before installing software or changing other agent skills.

Risk: IP addresses and location inputs used for lookups pass through OOMOL to IPGeolocation.io.

Mitigation: Submit only the IP or location data needed for the requested lookup.

## Reference(s):

- [IPGeolocation.io documentation](https://ipgeolocation.io/documentation.html)
- [IPGeolocation.io](https://ipgeolocation.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-ipgeolocation-io)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested action and the data supplied by the user.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
