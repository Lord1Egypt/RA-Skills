## Description:

Use Zoom through a connected OOMOL account to read, create, and update Zoom data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Zoom users, meetings, and meeting summaries, and to create or update meetings through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags a suspicious, partially scanned release: it includes a live remote oo CLI installer that raises an install security concern and appears mismatched with the Zoom skill’s purpose.

Mitigation: Before installing, ask the publisher why the oo CLI installer is needed, verify the installation method, and clarify what the remote script does.

## Reference(s):

- [Zoom Meetings API documentation](https://developers.zoom.us/docs/api/meetings/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Zoom data; write actions require user confirmation.]

## Skill Version(s):

1.0.8 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
