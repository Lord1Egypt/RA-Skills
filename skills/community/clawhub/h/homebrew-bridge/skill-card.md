## Description:

Expose Mac Homebrew tools like brew, gh, and other /opt/homebrew/bin CLIs on a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN and OpenClaw config auto-discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Linux OpenClaw gateways to call trusted same-LAN Mac Homebrew tools through explicit SSH wrapper paths, with optional Wake-on-LAN support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent SSH wrappers may target an unsafe host or directory if the OpenClaw config, same-LAN Mac, or target path is not trusted.

Mitigation: Use an explicit normal user@host value, verify the same-LAN Mac, and keep the wrapper target directory private and owned by the installing user.

Risk: Installer file-writing behavior needs review before use in root-owned or shared writable directories.

Mitigation: Avoid running the installer as root or against shared writable directories until host validation and symlink-safe file creation are added.

## Reference(s):

- [Skill Readiness](references/skill-readiness.md)
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/skills/homebrew-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installer and verification commands for explicit same-LAN SSH wrapper paths; installed wrappers are persistent executable files.]

## Skill Version(s):

0.6.1 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
