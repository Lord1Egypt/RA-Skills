## Description: <br>
Openclaw Config Expert helps OpenClaw users validate, repair, optimize, migrate, and recover configuration for agents, routing, plugins, models, and Gateway operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samlinfj](https://clawhub.ai/user/samlinfj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage OpenClaw configuration, including validation, repair, agent setup, model routing, plugin management, version migration, and emergency recovery. It is intended for administrative workflows that may change local configuration and service state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad OpenClaw configuration changes, including plugin changes, rollbacks, backup deletion, and Gateway restarts. <br>
Mitigation: Require manual confirmation before config overwrites, plugin changes, rollback, backup deletion, or Gateway restart actions. <br>
Risk: Persistent automation can be enabled through cron setup. <br>
Mitigation: Review cron_manager.py and approve each scheduled job before enabling cron setup. <br>
Risk: The security review flags under-disclosed model or agent prompt changes. <br>
Mitigation: Review scripts/knowledge_optimization.py and any prompt or agent changes before installation or deployment. <br>
Risk: The skill requires sensitive credentials for model providers. <br>
Mitigation: Keep provider API keys in approved secret storage and avoid pasting secrets into prompts, logs, or generated configuration examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samlinfj/openclaw-config-expert) <br>
- [OpenClaw architecture documentation](https://docs.openclaw.ai/concepts/architecture) <br>
- [DeepSeek platform documentation](https://platform.deepseek.com) <br>
- [Alibaba Cloud DashScope documentation](https://dashscope.aliyun.com) <br>
- [Configuration template documentation](artifact/config_templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python command examples, JSON configuration templates, and status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or invoke local OpenClaw configuration changes, backups, rollbacks, cron setup, plugin changes, and Gateway restarts when the operator approves those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
