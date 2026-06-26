## Description: <br>
创建新的 OpenClaw Agent，并指导配置工作区、基础记忆文件、模型认证文件和 OpenClaw 全局配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill when they need to create a new OpenClaw agent, add a bot, or configure a new model test environment. It provides checklist-style guidance for required files, directory layout, openclaw.json updates, optional Feishu binding, and post-creation validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make persistent global OpenClaw configuration changes. <br>
Mitigation: Review every openclaw.json change before applying it and install the skill only when persistent OpenClaw agent creation is intended. <br>
Risk: The skill handles auth.json and optional Feishu appSecret values, which may expose credentials if copied into chat, logs, or version-controlled files. <br>
Mitigation: Use a fresh per-agent auth.json unless credential sharing is intentional, and do not paste or store Feishu appSecret in chat, logs, or version-controlled files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AxelHu/openclaw-agent-creator) <br>
- [Publisher profile](https://clawhub.ai/user/AxelHu) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/templates/AGENTS.md](artifact/templates/AGENTS.md) <br>
- [artifact/templates/IDENTITY.md](artifact/templates/IDENTITY.md) <br>
- [artifact/templates/MEMORY.md](artifact/templates/MEMORY.md) <br>
- [artifact/templates/SOUL.md](artifact/templates/SOUL.md) <br>
- [artifact/templates/USER.md](artifact/templates/USER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, tables, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable Markdown templates for OpenClaw agent identity, behavior, memory, and user context files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
