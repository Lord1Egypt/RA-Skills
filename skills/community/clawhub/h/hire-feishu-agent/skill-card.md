## Description: <br>
Guides users through adding a Feishu channel agent to OpenClaw by collecting app credentials and preparing the required openclaw.json account, agent, and binding configuration snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XRovis](https://clawhub.ai/user/XRovis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a new Feishu bot-backed OpenClaw agent. It helps collect the required agent ID, display name, Feishu App ID, and App Secret, then presents copy-ready JSON changes for accounts, agents, and bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret values can be exposed if pasted into shared chats, logs, or committed configuration files. <br>
Mitigation: Use a dedicated minimal-permission Feishu app and avoid sharing or committing real secrets. <br>
Risk: Incorrect edits to openclaw.json can disrupt existing Feishu accounts, agents, or routing bindings. <br>
Mitigation: Back up openclaw.json, append only the new account, agent, and binding entries, and review the final merged config before restarting the gateway. <br>
Risk: Persistent routing changes can continue sending Feishu messages to the new agent after testing. <br>
Mitigation: Record the added account, agent, and binding identifiers so they can be removed cleanly later. <br>


## Reference(s): <br>
- [OpenClaw Feishu agent configuration schema](artifact/schema.md) <br>
- [Hire Feishu Agent on ClawHub](https://clawhub.ai/XRovis/hire-feishu-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces copy-ready configuration snippets for openclaw.json and a restart command reminder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
