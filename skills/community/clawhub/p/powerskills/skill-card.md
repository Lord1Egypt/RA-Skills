## Description:

Windows automation toolkit for AI agents that provides Outlook email/calendar, Edge browser automation, desktop screenshots/window management, and shell commands via PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aloth](https://clawhub.ai/user/aloth)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use PowerSkills to let agents inspect and operate Windows Outlook, Edge, desktop, and system environments through documented PowerShell actions. It is suited for local Windows automation workflows where the operator intentionally grants the agent access to email, browser, desktop input, and shell capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over Outlook, browser sessions, desktop input, application launching, and shell commands on a Windows account.

Mitigation: Install only the specific sub-skill needed and require explicit approval before sending email, submitting forms, typing keystrokes, launching applications, or running shell commands.

Risk: Edge remote debugging can expose or modify active browser state.

Mitigation: Use a separate disposable Edge profile for CDP automation and enable remote debugging only for the intended session.

Risk: PowerShell execution-policy changes or missing script files can create deployment and trust gaps.

Mitigation: Avoid persistent execution-policy changes, prefer narrowly scoped execution, and verify PowerShell scripts from a trusted release before running them.

## Reference(s):

- [PowerSkills ClawHub listing](https://clawhub.ai/aloth/skills/powerskills)
- [Microsoft PowerShell documentation](https://docs.microsoft.com/en-us/powershell/)
- [Microsoft SendKeys documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON envelopes with optional PNG screenshot files and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; outputs may include email, calendar, browser, desktop, process, environment, and command-execution data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
