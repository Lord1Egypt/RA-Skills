## Description: <br>
Multi Agent Group Chat automatically reposts sub-agent results from sessions_send workflows into the originating Telegram or Feishu group chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this plugin to make a multi-agent OpenClaw setup visible in group chat, so sub-agent responses are automatically shared with the Telegram or Feishu group where the task originated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can automatically post sub-agent outputs into Telegram or Feishu group chats without clear allowlists, confirmations, or content controls. <br>
Mitigation: Install only for trusted groups where automatic reposting is intended; avoid workflows with secrets, private customer data, internal reasoning, or sensitive operational details unless chat/account allowlists, explicit approval, and redaction controls are added. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/harven-droid/multi-agent-group-chat) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/harven-droid) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Chat messages and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatically sends final sub-agent replies to the detected source group when an internal sessions_send task completes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
