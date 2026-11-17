## Description:

Guides agents in using KIRI Engine to reconstruct 3D models or Gaussian-splatting assets from user-approved photos or video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taosiuman](https://clawhub.ai/user/taosiuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to choose a KIRI Engine scan mode, submit approved image sets or video, monitor reconstruction, and download 3D assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The KIRI API key is stored in a local plaintext configuration file.

Mitigation: Keep the file private, never share or commit the key, and rotate it if exposed.

Risk: Selected photos or video are sent to KIRI Engine for third-party processing.

Mitigation: Upload only user-approved media and avoid sensitive content without authorization.

Risk: Extracting a downloaded archive may overwrite files with the same names in the destination.

Mitigation: Review the archive contents and choose an empty or dedicated output directory.

## Reference(s):

- [KIRI Engine API documentation](https://docs.kiriengine.app/)
- [KIRI Engine API reference linked by the skill](https://gentlebandit.feishu.cn/wiki/PsHawWV0gi2jePkmRoycwMwXnIc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with PowerShell commands and task-status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a task identifier and download instructions; completed assets may be downloaded and extracted to a chosen directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
