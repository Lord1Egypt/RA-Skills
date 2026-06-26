## Description: <br>
Browser automation CLI for AI agents, written in Go. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libi](https://clawhub.ai/user/libi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to control Chrome or Chromium through the kbr CLI for website navigation, form interaction, screenshots, data extraction, web app testing, authentication workflows, and browser task automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad browser-control authority across websites. <br>
Mitigation: Use isolated browser profiles, dedicated low-privilege accounts, and require explicit confirmation before submitting forms, changing account data, uploading files, posting content, or making purchases. <br>
Risk: Saved credentials, exported auth files, browser profiles, and network logs can contain sensitive session data. <br>
Mitigation: Treat exported state, profiles, and logs as secrets; avoid saving real passwords through command-line arguments; and disable or avoid network logging during sensitive sessions. <br>
Risk: Page content can influence agent decisions during browser automation. <br>
Mitigation: Enable content boundaries where appropriate and review browser actions before relying on page-derived output. <br>


## Reference(s): <br>
- [ko-browser ClawHub release](https://clawhub.ai/libi/ko-browser) <br>
- [Publisher profile](https://clawhub.ai/user/libi) <br>
- [ko-browser repository referenced by SKILL.md](https://github.com/libi/ko-browser) <br>
- [Chrome download](https://www.google.com/chrome/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser snapshots, screenshots, PDFs, network logs, storage state files, and downloaded files through kbr commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
