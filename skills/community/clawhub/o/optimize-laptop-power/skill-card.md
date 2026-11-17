## Description:

Windows power-saving reference guide with verifiable commands for balanced plan, Defender tuning, and SysMain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxpj](https://clawhub.ai/user/frankxpj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Windows laptop users use this guide to diagnose battery health, discharge rate, and high-resource processes, then manually apply selected power-plan, Microsoft Defender, or SysMain changes when the diagnostic results justify them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes Microsoft Defender exclusions and scan-direction changes that can reduce real-time protection.

Mitigation: Use those commands only after measuring a real Defender bottleneck, scope exclusions narrowly, avoid system and download directories, and keep the documented restoration commands available.

Risk: The guide includes commands that change Windows power plans and SysMain service behavior.

Mitigation: Run diagnostic commands first, execute only one change at a time in an administrator PowerShell session, and record the current power-plan GUID before changing settings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/frankxpj/skills/optimize-laptop-power)
- [Publisher Profile: frankxpj](https://clawhub.ai/user/frankxpj)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual Windows power-optimization guidance; commands are presented for user review and execution outside the skill.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
