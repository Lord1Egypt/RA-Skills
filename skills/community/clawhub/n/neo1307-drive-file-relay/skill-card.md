## Description:

Copy (relay) a local file from this machine into Google Drive for desktop (GoogleDriveFS) so it can be downloaded from a phone when the phone is not on the same LAN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to copy a known local file into a Google Drive for desktop folder so it can be retrieved from a phone, with source and destination size and SHA256 verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact refers to a PowerShell relay script that is not included.

Mitigation: Review or supply `scripts/drive_relay.ps1` before use and confirm it only copies the intended file to the expected Google Drive folder.

Risk: A file could be copied to the wrong Google Drive account or destination folder.

Mitigation: Verify the detected Drive mount, destination folder, copied file size, and SHA256 before treating the transfer as complete.

## Reference(s):

- [Drive File Relay on ClawHub](https://clawhub.ai/neo1307/skills/neo1307-drive-file-relay)
- [neo1307 ClawHub publisher profile](https://clawhub.ai/user/neo1307)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline PowerShell command and verification details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source path, destination path, size in bytes and MB, and SHA256 after copy verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
