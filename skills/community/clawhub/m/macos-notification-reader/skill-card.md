## Description:

Reads recent macOS notifications from the local notification database and exports date-organized markdown logs and work-notification summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users on macOS use this skill to review missed notifications, archive local notification history, and generate filtered summaries for work-related apps such as Teams, Outlook, and WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad macOS Full Disk Access for Python to read the protected notification database.

Mitigation: Grant access only when the notification-reading workflow is needed, prefer manual one-time runs, and remove the permission when finished.

Risk: Exported notification logs and summaries can contain sensitive plaintext from personal or work apps.

Mitigation: Review the output directory, restrict local file permissions, and delete generated files that are no longer needed.

Risk: Cron scheduling can continuously archive new notifications without further user attention.

Mitigation: Use scheduled jobs only for intentional recurring collection and disable or remove the cron entry when the workflow is no longer required.

Risk: The permission guide includes an advanced sudo-based setup method.

Mitigation: Use the System Settings Full Disk Access method and avoid the sudo setup method unless it has been independently reviewed for the target macOS version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/macos-notification-reader)
- [Publisher profile](https://clawhub.ai/user/gift-is-coding)
- [Permission setup guide](references/permission-setup.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports are local files organized by date; notification contents may include sensitive plaintext.]

## Skill Version(s):

1.1.0 (source: release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
