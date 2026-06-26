## Description: <br>
Auto-deliver final messages to loved ones after 30 days of inactivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dilboy](https://clawhub.ai/user/dilboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to record a text or voice final message, configure email delivery, and monitor inactivity so the message can be sent after 30 days without activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive final messages and email credentials locally. <br>
Mitigation: Use only test content until credential storage uses a real secret store or encryption without plaintext fallback. <br>
Risk: Debug and delivery flows may send final messages too easily. <br>
Mitigation: Use a test recipient until debug sending is isolated from real messages and delivery flows require clearer confirmation. <br>
Risk: Warning and status flows may reveal recipient or message details. <br>
Mitigation: Redact sensitive status output and ensure warning emails go only to the user. <br>


## Reference(s): <br>
- [Last Words ClawHub page](https://clawhub.ai/dilboy/last-words) <br>
- [Publisher profile](https://clawhub.ai/user/dilboy) <br>
- [QQ Mail](https://mail.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown chat guidance with inline shell commands and configuration prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite records, local audio files, and email delivery configuration when the agent runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and changelog, released 2024-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
