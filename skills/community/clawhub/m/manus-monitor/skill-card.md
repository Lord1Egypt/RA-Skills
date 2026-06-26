## Description: <br>
Create and manage Manus AI tasks via API, save task metadata locally, monitor saved task status, and download completed output files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tallman2014](https://clawhub.ai/user/tallman2014) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users with a Manus API key use this skill to create autonomous Manus tasks, poll and save task status, download output files, and receive optional status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task details are sent to Manus, and output files may be downloaded locally. <br>
Mitigation: Use the skill only with prompts, task data, and output files approved for Manus handling. <br>
Risk: The skill can create a recurring OpenClaw monitor and save local task metadata. <br>
Mitigation: Review the saved task list and monitor job before use, stop the monitor when it is no longer needed, and clear saved tasks when appropriate. <br>
Risk: Optional Telegram notifications can expose task details and Manus links to the configured chat. <br>
Mitigation: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID only for an approved destination, or leave them unset to avoid Telegram notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tallman2014/manus-monitor) <br>
- [Manus API Reference](https://open.manus.ai/docs) <br>
- [Manus Documentation](https://manus.im/docs) <br>
- [Manus Homepage](https://manus.im) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MANUS_API_KEY; optional Telegram notifications use TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
