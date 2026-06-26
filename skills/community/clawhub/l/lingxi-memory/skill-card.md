## Description: <br>
Automates extraction of useful memories from OpenClaw session files and writes the results to user-configured Feishu knowledge resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxiaolong1988](https://clawhub.ai/user/liuxiaolong1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to periodically scan completed local chat sessions, extract task, project, and knowledge memories, and store those outputs in their own Feishu tables and documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly read private OpenClaw chat logs and send conversation content to an AI agent for extraction. <br>
Mitigation: Install only when automated memory extraction is intended, avoid running it on chats containing secrets or regulated data, and review the configured session directory before enabling scheduled execution. <br>
Risk: Extracted content is written to Feishu resources and notifications are sent through the configured Feishu account. <br>
Mitigation: Use only Feishu tables, documents, and notification targets you control; complete OAuth intentionally and verify every Feishu environment variable before running the scripts. <br>
Risk: The release is designed for cron-style background execution, which can process new sessions without a manual prompt each time. <br>
Mitigation: Review the cron entries and disable or slow the schedule when handling sensitive work; protect workspace/.env and audit processed-session state files. <br>


## Reference(s): <br>
- [Lingxi-MindVault ClawHub Skill Page](https://clawhub.ai/liuxiaolong1988/lingxi-memory) <br>
- [liuxiaolong1988 ClawHub Publisher Profile](https://clawhub.ai/user/liuxiaolong1988) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment variable configuration, extracted memory text, Feishu writes, and notification messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, bash, python3, Feishu OAuth, and user-provided Feishu resource identifiers.] <br>

## Skill Version(s): <br>
1.1.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
