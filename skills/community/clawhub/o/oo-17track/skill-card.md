## Description:

Use the OOMOL-connected 17TRACK service to read shipment data and create or update tracking records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query shipment status and manage tracking records through their connected 17TRACK account. It covers reads as well as registration, updates, and other tracking changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious because it instructs downloading and running a remote installer whose necessity is unclear; the scan was partial and the installer contents were unavailable.

Mitigation: Do not install until the remote installer is independently verified and its necessity is explained; its behavior remains incompletely assessed.

## Reference(s):

- [17TRACK homepage](https://www.17track.net/)
- [17TRACK API documentation](https://api.17track.net/en/doc)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON data and concise text summaries]

**Output Parameters:** [Varies by action; supported batch actions handle up to 40 tracking numbers.]

**Other Properties Related to Output:** [Action-dependent shipment, quota, and tracking information.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
