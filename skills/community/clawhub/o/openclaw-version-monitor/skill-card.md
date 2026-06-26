## Description: <br>
Monitors OpenClaw GitHub releases, retrieves the latest release notes, translates them into Chinese, and prepares update notifications for Telegram and Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[00010110](https://clawhub.ai/user/00010110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to check OpenClaw release updates, compare the monitored version with the latest release, translate release notes into Chinese, and format notifications for Telegram and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications could be sent to an unintended Telegram chat or Feishu destination if channel identifiers are reused without verification. <br>
Mitigation: Confirm that Telegram chat ID 8290054457 and the Feishu destination belong to the installer before enabling notifications. <br>
Risk: Scheduled checks can automatically send release notifications through external services. <br>
Mitigation: Use limited-purpose Telegram bot or Feishu app credentials and enable schedules only for intended notification channels. <br>


## Reference(s): <br>
- [Push Templates](references/push-templates.md) <br>
- [OpenClaw Latest Release API](https://api.github.com/repos/openclaw/openclaw/releases/latest) <br>
- [OpenClaw Releases](https://github.com/openclaw/openclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and notification templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese release-note summaries and channel-specific notification text; Telegram messages should stay within the documented 4096-character limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
