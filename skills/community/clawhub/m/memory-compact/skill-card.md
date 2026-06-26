## Description: <br>
Daily memory automation that backs up local OpenClaw memory files, extracts key points, appends them to MEMORY.md, and prepares notification text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GarryFan-AI](https://clawhub.ai/user/GarryFan-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to summarize recent memory notes into long-term MEMORY.md entries and retain the original daily files in a local backup directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory summaries and backups may retain sensitive or incorrect information from local OpenClaw memory files. <br>
Mitigation: Review generated MEMORY.md entries and backup files before relying on them or sharing workspace contents. <br>
Risk: Notification workflow content may expose memory details if routed outside the local workspace. <br>
Mitigation: Enable notification delivery only after confirming where notification text will be stored or sent. <br>
Risk: Automated daily execution may repeatedly process local memory files without direct review. <br>
Mitigation: Review cron configuration and run the script manually first to confirm expected file paths and output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GarryFan-AI/memory-compact) <br>
- [Publisher profile](https://clawhub.ai/user/GarryFan-AI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, notification text, logs, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local MEMORY.md entries, backup copies, logs, and notification content in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
