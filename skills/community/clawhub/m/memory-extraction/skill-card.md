## Description: <br>
Extracts entities, relationships, and factual observations from conversations and updates a knowledge graph to maintain user memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paibwhgs](https://clawhub.ai/user/paibwhgs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to identify memory-worthy details in conversation, then structure them as entities, relations, and observations for a knowledge graph. It is intended for assistants that maintain persistent user profiles or project context across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages automatic storage of broad personal details without clear consent, review, retention, or deletion controls. <br>
Mitigation: Enable it only with user approval workflows that let users inspect, edit, and delete saved memories. <br>
Risk: Conversation memory can capture contact details, precise location, relationship data, or other sensitive facts. <br>
Mitigation: Configure the agent to avoid storing sensitive details unless the user explicitly requests it and minimize retained facts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paibwhgs/memory-extraction) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python examples and structured entity, relation, and observation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistent memory behavior depends on the agent's configured knowledge graph or memory tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
