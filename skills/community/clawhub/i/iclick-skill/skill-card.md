## Description:

iClick Automation helps agents monitor and control connected iOS 15+ devices through the iClick no-jailbreak automation service, including device status checks, screenshots, touch actions, text input, media handling, and app operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[undefined-token](https://clawhub.ai/user/undefined-token)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to inspect connected iOS devices and run RPA-style actions such as screenshots, taps, swipes, text entry, app launching, and media file operations. It is intended for environments where the user trusts the local iClick service and has permission to control the connected devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad control over connected iOS devices, including screenshots, touch input, app operations, and media file deletion or clearing.

Mitigation: Install only in trusted environments, restrict who can invoke the skill, and require explicit user confirmation before screenshots, device-control actions, or media deletion.

Risk: The backend command dispatcher can invoke a wide range of iClick methods beyond the documented examples.

Mitigation: Prefer an allowlist of approved methods and review each requested action before execution.

Risk: Device metadata and screenshots may expose sensitive information such as IP addresses, device names, and screen contents.

Mitigation: Avoid sharing captured data unless necessary, move screenshots only to approved workspaces, and delete temporary screenshot files after use.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/undefined-token/skills/iclick-skill)
- [Publisher Profile](https://clawhub.ai/user/undefined-token)
- [iClick Website](https://iosclick.com)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with Node shell commands, JSON command responses, and temporary image file paths for screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and access to a trusted local iClick service connected to authorized iOS devices.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
