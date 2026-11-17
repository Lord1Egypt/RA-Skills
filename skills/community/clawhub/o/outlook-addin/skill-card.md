## Description:

Outlook sidebar add-in that brings the full power of your OpenClaw agent into Microsoft Outlook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nachtsheim](https://clawhub.ai/user/nachtsheim)

### License/Terms of Use:

MIT-0

## Use Case:

Outlook and OpenClaw users use this skill to set up an Outlook sidebar that lets them chat with their agent about selected emails, use available tools and skills, and draft replies from Outlook Desktop Classic or Outlook Web.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running remote add-in code may introduce dependency or supply-chain risk.

Mitigation: Review the referenced repository and dependency lockfile before installing, and prefer a pinned commit with pinned npm commands.

Risk: Selected Outlook email content may become available to the connected agent and enabled tools or automations.

Mitigation: Use the add-in only with a trusted local OpenClaw Gateway and review enabled tools before connecting sensitive mail.

## Reference(s):

- [OpenClaw Outlook Add-in Repository](https://github.com/nachtsheim/openclaw-outlook-addin)
- [OpenClaw Outlook Add-in README](https://github.com/nachtsheim/openclaw-outlook-addin#readme)
- [ClawHub Skill Page](https://clawhub.ai/nachtsheim/skills/outlook-addin)
- [Publisher Profile](https://clawhub.ai/user/nachtsheim)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup of an Outlook Office.js add-in that connects to a trusted local OpenClaw Gateway.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
