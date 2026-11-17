## Description:

Manage and control a local Hytale dedicated server with commands to start, stop, update, and check the server status using the official downloader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newcastlegeek](https://clawhub.ai/user/newcastlegeek)

### License/Terms of Use:


## Use Case:

External server operators and developers use this skill to manage a local Hytale dedicated server lifecycle, including setup guidance and start, stop, update, status, and console commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update command runs a user-provided Hytale downloader binary with normal user privileges and no integrity check performed by the skill.

Mitigation: Download the downloader only from the official Hytale URL, verify its source or checksum when available, and review it before running update.

Risk: The downloader can use hytale-downloader-credentials.json from ~/hytale_server, which may expose account credentials if handled loosely.

Mitigation: Store the credentials file with restrictive permissions such as 600 and keep it out of backups, logs, and source control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newcastlegeek/skills/hytale)
- [Hytale Downloader](https://downloader.hytale.com/hytale-downloader.zip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
