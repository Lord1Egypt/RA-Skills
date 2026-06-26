## Description: <br>
Automatic conversation backup system for Obsidian with incremental snapshots, hourly breakdowns, and formatted chat-style markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Laserducktales](https://clawhub.ai/user/Laserducktales) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to archive local conversation history into an Obsidian vault, create incremental or full Markdown snapshots, and organize conversations by hour. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain secrets, private data, or proprietary conversation content. <br>
Mitigation: Use a private, non-synced, or access-controlled Obsidian vault when conversations include sensitive information. <br>
Risk: The monitoring script can read local Telegram credentials and send external token-threshold alerts. <br>
Mitigation: Inspect or disable Telegram warning behavior unless external alerts are explicitly intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files and shell-script driven configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Obsidian-formatted conversation snapshots and local tracking files; Telegram alerts are optional but require local credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
