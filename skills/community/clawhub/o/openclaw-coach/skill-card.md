## Description: <br>
Openclaw Coach helps an OpenClaw user sync local OpenClaw docs into Obsidian and receive scheduled Feishu coaching messages with daily tips and version reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabbot42](https://clawhub.ai/user/rabbot42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to automate a personal coaching routine: sync OpenClaw documentation into Obsidian, choose daily tip topics, and send scheduled Feishu messages with selected tip content and version updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes synced documentation, tip state, logs, and version files under $HOME/Obsidian/Docs/OpenClaw. <br>
Mitigation: Review the target Obsidian folder and keep backups or version control before enabling scheduled sync. <br>
Risk: Scheduled scripts send coaching messages through the configured OpenClaw/Feishu recipient. <br>
Mitigation: Verify FEISHU_USER_ID points to the intended recipient before running the messaging scripts. <br>
Risk: The documented reply-by-number tip selection flow is not implemented by the artifact. <br>
Mitigation: Do not rely on replies to control tomorrow's tip until a handler is added; inspect daily-tips.json or choose manually. <br>


## Reference(s): <br>
- [ClawHub Openclaw Coach listing](https://clawhub.ai/rabbot42/openclaw-coach) <br>
- [OpenClaw documentation source used by sync script](https://raw.githubusercontent.com/openclaw/openclaw/main/docs) <br>
- [OpenClaw latest release endpoint used by sync script](https://api.github.com/repos/openclaw/openclaw/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown text, shell command output, and local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes under $HOME/Obsidian/Docs/OpenClaw and sends messages through OpenClaw/Feishu when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
