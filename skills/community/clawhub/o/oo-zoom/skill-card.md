## Description:

Use an OOMOL-connected Zoom account to read user and meeting data, create meetings, and update existing meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Zoom account use this skill to retrieve Zoom user and meeting information and to create or update meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a changing remote installer and may involve automatic skill installation.

Mitigation: Review the CLI installation and its permissions separately, check OOMOL's Zoom access and automatic installation behavior, and require approval before running a remote installer.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-zoom)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Zoom Meetings API documentation](https://developers.zoom.us/docs/api/meetings/)
- [Zoom](https://www.zoom.com)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Guidance]

**Output Format:** [Text guidance, shell command examples, and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the oo CLI; writes require confirmation before execution.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
