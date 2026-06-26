## Description: <br>
Guides OpenClaw users through creating multiple agents in one gateway and binding each agent to a separate Feishu bot account for isolated identities and memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kolikoliko](https://clawhub.ai/user/kolikoliko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators configuring OpenClaw Gateway use this skill to set up multiple Feishu bots, route each bot to a different agent, and verify isolated workspaces, memory, and identities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app secrets stored in OpenClaw configuration or backups could be exposed if shared or committed. <br>
Mitigation: Keep ~/.openclaw/openclaw.json and backups out of source control and shared locations, restrict local file access, and rotate any exposed Feishu app secret. <br>
Risk: Incorrect agent-to-account bindings could route messages or replies through the wrong Feishu bot identity. <br>
Mitigation: Verify each binding with openclaw agents list --bindings before using the bots in real chats. <br>
Risk: Over-permissioned Feishu apps increase impact if credentials are misused. <br>
Mitigation: Use only Feishu apps you control and grant the minimum bot permissions needed. <br>


## Reference(s): <br>
- [Configuration Fields](references/config-fields.md) <br>
- [Feishu Bot Creation Guide](references/feishu-app.md) <br>
- [Multi-Agent Architecture](references/architecture.md) <br>
- [FAQ](references/faq.md) <br>
- [Backup and Restore](references/backup.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [ClawHub Skill Page](https://clawhub.ai/kolikoliko/multi-agent-feishu) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only setup guidance; no runtime code is produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
