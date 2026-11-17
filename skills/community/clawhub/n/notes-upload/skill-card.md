## Description:

Upload the named team-backup.zip archive to the configured team endpoint with checksum logging, timeout handling, and HTTP status validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymous9n23](https://clawhub.ai/user/anonymous9n23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform teams use this skill to send the team-backup.zip archive produced by notes-pack to their configured team endpoint and confirm the upload status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send files outside the intended archive location.

Mitigation: Before use, verify the destination, archive contents, and exact resolved source path; protect the configuration and archive location from untrusted changes; prefer a version that confines uploads to the intended archive location and rejects symlinks.

## Reference(s):

- [Notes Upload on ClawHub](https://clawhub.ai/anonymous9n23/skills/notes-upload)
- [Publisher profile: anonymous9n23](https://clawhub.ai/user/anonymous9n23)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Upload status and timestamped audit log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the archive name, byte size, SHA-256 checksum, and HTTP upload status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
