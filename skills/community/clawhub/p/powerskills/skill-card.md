## Description: <br>
Windows automation toolkit for AI agents. Provides Outlook email/calendar, Edge browser (CDP), desktop screenshots/window management, and shell commands via PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aloth](https://clawhub.ai/user/aloth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use PowerSkills to let an agent operate Windows workflows through PowerShell, including Outlook mail and calendar tasks, Edge browser automation, desktop screenshots and window management, and system commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over Windows desktop, Outlook, Edge browser sessions, and PowerShell. <br>
Mitigation: Install only in a trusted local context and require confirmation before email sending, browser form submission or JavaScript execution, screenshots, keystrokes, environment-variable reads, or shell commands. <br>
Risk: Changing PowerShell execution policy can allow local scripts to run more freely. <br>
Mitigation: Verify the underlying scripts before changing execution policy and prefer the narrowest execution-policy change suitable for the deployment. <br>


## Reference(s): <br>
- [PowerSkills on ClawHub](https://clawhub.ai/aloth/powerskills) <br>
- [Root Skill Documentation](artifact/SKILL.md) <br>
- [Browser Skill Documentation](artifact/skills/browser/SKILL.md) <br>
- [Desktop Skill Documentation](artifact/skills/desktop/SKILL.md) <br>
- [Outlook Skill Documentation](artifact/skills/outlook/SKILL.md) <br>
- [System Skill Documentation](artifact/skills/system/SKILL.md) <br>
- [Microsoft SendKeys Documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys) <br>
- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Skill actions return structured JSON envelopes with status, exit_code, data, and timestamp fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
