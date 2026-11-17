## Description:

Local browser and Windows desktop control for Mavis using Playwright-based browser automation and a PowerShell plus .NET helper for desktop actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fvegiard](https://clawhub.ai/user/fvegiard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent control a local Edge browser session and perform Windows desktop operations such as mouse, keyboard, clipboard, window, screenshot, shell, and PowerShell actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute arbitrary shell and PowerShell commands through Windows desktop helpers.

Mitigation: Require explicit approval for command execution and review helper files before installation or use.

Risk: The skill can control the user's local desktop, clipboard, windows, screenshots, and mouse or keyboard input.

Mitigation: Use it only when local desktop control is intended, keep the session supervised, and confirm sensitive actions before execution.

Risk: Browser automation over a debug Edge profile can act on logged-in sessions and sensitive websites.

Mitigation: Use a dedicated non-personal browser profile and avoid sensitive logged-in accounts in the controlled session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fvegiard/skills/mavis-tools)
- [Server-resolved GitHub provenance](https://github.com/fvegiard/mavis-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell and Node.js command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged local-control commands that should be reviewed before execution.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
