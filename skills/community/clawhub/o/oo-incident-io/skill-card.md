## Description:

Search and read incident.io incidents, actions, statuses, and severities through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Incident responders and operations teams use this skill to retrieve incidents and related actions, statuses, or severities from an authorized incident.io workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup instructions can run changing remote code without clearly explaining or confirming local changes; the exact behavior of the remote installers is unverified.

Mitigation: Review setup before installing, use a verified CLI release, approve local changes, and review or disable automatic skill synchronization.

Risk: Incident data may be processed through OOMOL when using its connected account.

Mitigation: Use read-only permissions where available and confirm that the workspace's incident data handling requirements allow this connection.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [incident.io](https://incident.io)
- [incident.io API documentation](https://api-docs.incident.io/)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured incident.io data returned as JSON, with text summaries where appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only incident and action data, depending on the selected action]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
