## Description:

Helps an OpenClaw agent owner install, verify, configure, monitor, and manage InnerWarden protections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maiconburn](https://clawhub.ai/user/maiconburn)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install and verify InnerWarden, check active protections and command verdicts, and manage monitoring or enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan flagged install instructions that pipe a changing internet script directly into a shell as a serious supply-chain risk.

Mitigation: Before installing, review the installer independently and verify its authenticity through a trusted source; do not install until the unverified download-and-run method is addressed.

Risk: The scan was partial because three referenced local paths were missing and could not be resolved.

Mitigation: Resolve and review the missing paths before relying on the scan as a complete assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/maiconburn/skills/innerwarden-security)
- [InnerWarden documentation](https://github.com/InnerWarden/innerwarden-skill)
- [InnerWarden Pro server guide](https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/pro-on-a-server.md)
- [InnerWarden Pro management guide](https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/managing-pro.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
