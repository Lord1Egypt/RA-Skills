## Description: <br>
Governs Loki's behaviour in Telegram group chats - when to speak, when to stay silent, how to react, and platform formatting rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to guide an agent's behavior in Telegram group chats, including when to respond, react, stay silent, and preserve private context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The clean security verdict is low confidence because deeper artifact confirmation was not available to the scan. <br>
Mitigation: Install only when the marketplace page and included SKILL.md match the expected group chat protocol, and review the skill before deployment. <br>
Risk: Group chat replies may expose private context if the agent treats private memory as shareable. <br>
Mitigation: Keep private memory, direct-message history, and personal context out of group replies, as the skill directs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/group-chat-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance for agent behavior and messaging rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No outbound network requirement is declared in the release metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
