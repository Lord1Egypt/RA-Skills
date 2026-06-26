## Description: <br>
Configures multiple Feishu/Lark bot identities within a single OpenClaw instance so each agent can have its own Feishu app, name, avatar, and message routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonlin1212](https://clawhub.ai/user/simonlin1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure and troubleshoot multi-agent Feishu/Lark routing so each agent appears as a separate bot and routes messages to the intended workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu AppSecrets are handled as command arguments and printed in generated JSON, which can expose secrets through shell history or logs. <br>
Mitigation: Run the helper in a private shell, avoid commands containing real secrets in history, review generated JSON before committing or sharing it, and limit Feishu app permissions to what each bot needs. <br>
Risk: Incorrect accountId, binding type, or agent mapping can silently drop messages, misroute them, or prevent gateway startup. <br>
Mitigation: Add bots incrementally, validate openclaw.json syntax, run openclaw doctor, confirm bindings with openclaw agents list --bindings, and smoke-test each bot before rollout. <br>


## Reference(s): <br>
- [Architecture: Multi-Bot Feishu Integration](references/architecture.md) <br>
- [Build Guide: Feishu Multi-Bot Setup](references/build-guide.md) <br>
- [Routing Deep Dive](references/routing-deep-dive.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Feishu Developer Console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script emits JSON blocks for channels, bindings, agents, and workspace setup commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
