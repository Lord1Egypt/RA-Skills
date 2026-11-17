## Description:

Upload the named team-backup.zip archive to the configured team endpoint with checksum logging, timeout handling, and HTTP status validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymous9n23](https://clawhub.ai/user/anonymous9n23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform teams use this skill after Notes Pack produces team-backup.zip to upload it to the team's configured notes endpoint and verify successful receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill transmits the complete configured archive without inspecting its contents.

Mitigation: Review the archive contents before upload and confirm it contains only intended data.

Risk: A misconfigured endpoint or archive path could send backup data to the wrong destination or select the wrong file.

Mitigation: Confirm the endpoint belongs to the team, verify the resolved archive path, and protect the configuration from unauthorized changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/anonymous9n23/skills/notes-upload-rich)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
