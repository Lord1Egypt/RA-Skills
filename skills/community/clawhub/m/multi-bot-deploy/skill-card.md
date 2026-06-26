## Description: <br>
OpenClaw 多 Bot 多 Agent 一键搭建技能。根据用户提供的 Bot 名称、职能、模型和飞书凭证，自动完成 Agent 创建、账号配置、路由绑定和验证测试全流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bacon-123](https://clawhub.ai/user/Bacon-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create and link multiple Feishu bots by generating OpenClaw agent, channel, credential, binding, gateway restart, and verification steps from user-provided bot details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store Feishu app secrets in OpenClaw configuration. <br>
Mitigation: Use least-privilege Feishu credentials, avoid sharing production appSecret values in general chat, and confirm how stored secrets can be removed. <br>
Risk: The skill can change live OpenClaw agent, channel, route binding, and gateway configuration. <br>
Mitigation: Request a dry run, review the exact planned commands and configuration changes, and approve them before execution. <br>
Risk: Gateway restart and routing changes can affect active bot traffic. <br>
Mitigation: Run during an appropriate maintenance window and verify agent lists, bindings, and bot responses after changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bacon-123/multi-bot-deploy) <br>
- [OpenClaw Agents documentation](https://docs.openclaw.ai/cli/agents) <br>
- [OpenClaw Channels documentation](https://docs.openclaw.ai/cli/channels) <br>
- [Feishu Open Platform documentation](https://open.feishu.cn/document) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation results and next-step guidance for testing the created Feishu bot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
