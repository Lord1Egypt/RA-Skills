## Description: <br>
Reads recent macOS notifications from the local notification database and exports them to date-organized Markdown files for review, logging, and work summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and macOS users use this skill to review missed notifications, troubleshoot app notification delivery, archive recent local notifications, and generate short work notification summaries from apps such as Teams, Outlook, and WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full Disk Access for Python grants broad local file access beyond the notification database. <br>
Mitigation: Grant access only to the Python interpreter needed for this skill, run manually before scheduling, and revoke Full Disk Access when the skill is no longer used. <br>
Risk: Exported notification logs and work summaries may contain sensitive personal or work messages. <br>
Mitigation: Limit runs to the apps and time windows needed, review generated files, and delete logs that should not persist. <br>
Risk: Cron or recurring automation can collect more notification data than intended. <br>
Mitigation: Prefer manual runs until behavior is understood, then use narrow schedules and filters for ongoing collection. <br>


## Reference(s): <br>
- [Permission Setup Guide](references/permission-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gift-is-coding/macos-notification-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and terminal output with shell commands and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports notification logs and work summaries to date-organized local files; time windows and output paths can be adjusted through script arguments or wrapper configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
