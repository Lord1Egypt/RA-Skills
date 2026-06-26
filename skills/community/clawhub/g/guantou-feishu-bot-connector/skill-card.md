## Description: <br>
Connects an agent to a Feishu bot by adding Feishu bot account configuration and routing bindings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leochens](https://clawhub.ai/user/leochens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure Feishu bot accounts, bind them to agents, and route account-level or group-level messages to the intended agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw configuration and stores Feishu App Secret values. <br>
Mitigation: Review the planned account and routing changes before execution, avoid exposing real secrets on the command line, and check permissions on ~/.openclaw and its backups. <br>
Risk: The skill can restart the OpenClaw gateway after configuration changes. <br>
Mitigation: Run it during an acceptable maintenance window and plan for a short service interruption. <br>
Risk: Incorrect agent, account, or group routing values can send Feishu messages to the wrong agent. <br>
Mitigation: Verify the target agent ID, routing mode, account ID, and group chat ID before confirming changes. <br>


## Reference(s): <br>
- [Feishu OpenClaw bot setup page](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>
- [ClawHub release page](https://clawhub.ai/leochens/guantou-feishu-bot-connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw configuration, create a backup file, and print terminal status messages when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
