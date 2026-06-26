## Description: <br>
Rules and behavior guidelines for participating in group chats (Discord, Slack, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlayZz](https://clawhub.ai/user/FlayZz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents participating in shared Discord, Slack, or similar group chats use this skill to decide when to reply, remain silent, or use a reaction so they add value without dominating the conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A chat connector paired with the skill may expose the agent to more conversations or permissions than participants expect. <br>
Mitigation: Use limited bot permissions and add the agent only to spaces where participants expect an AI participant. <br>
Risk: The agent may disrupt group chat flow by replying too often or adding low-value messages. <br>
Mitigation: Follow the skill's participation rules: reply only when directly addressed or able to add value, and stay silent when the conversation is flowing without the agent. <br>
Risk: The agent may share private user context in a group instead of acting as an independent participant. <br>
Mitigation: Treat the agent as a participant, not the user's proxy, and avoid sharing the user's information unless the situation clearly calls for it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FlayZz/group-chats) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Natural-language guidance for chat replies, silence decisions, and emoji reactions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not add code, credentials, persistence, or hidden data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
