## Description:

Guides Windows 10/11 disk-space cleanup through drive inspection, cache cleanup, selective CloudDrive2 uploads, file-by-file checks, and user-approved local deletion and cloud organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zp-home](https://clawhub.ai/user/zp-home)

### License/Terms of Use:

MIT

## Use Case:

Windows users and support agents use this skill to identify reclaimable disk space, back up selected files to a mounted cloud drive, verify uploads, and decide whether to remove local copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad access to local drives and cloud destinations can expose or overwrite unintended files.

Mitigation: Require a visible dry-run table, confirm excluded folders and the destination root, and check for overwrites before any write.

Risk: A mounted cloud file may still be queued or cached rather than fully uploaded; deleting the local copy could cause data loss.

Mitigation: Delete only after the upload queue and cache are empty, file sizes match individually, and the user explicitly confirms deletion.

Risk: CloudDrive API access has broad effects, and a token or nonlocal endpoint may expose the cloud account.

Mitigation: Keep CD2_URL on the local CloudDrive endpoint and supply CD2_TOKEN only in a trusted session.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zp-home/skills/pc-space-cleanup)
- [CloudDrive2](https://www.clouddrive2.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands, file manifests, and verification tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Upload and deletion require explicit user review; verification compares cloud and local file sizes.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
