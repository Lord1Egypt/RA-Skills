## Description: <br>
Lark Mention helps agents send Feishu/Lark group messages with real @ mentions for selected members, multiple members, or all-member notifications through a local bridge service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toto2016](https://clawhub.ai/user/toto2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to format and send Feishu/Lark group notifications that include real @ mentions, avoiding plain-text tags that Lark will not render. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real Feishu/Lark group notifications, including broad @all or multi-person mentions. <br>
Mitigation: Confirm the chat ID, recipients, and message text before each send, especially for @all or multi-person mentions. <br>
Risk: The local bridge service can perform message-sending actions on behalf of the agent. <br>
Mitigation: Use only a trusted local bridge service with appropriate access controls. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/toto2016/lark-mention) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, JavaScript calls, curl commands, and bridge API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send real group notifications through a trusted local Feishu/Lark bridge service.] <br>

## Skill Version(s): <br>
26.3.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
