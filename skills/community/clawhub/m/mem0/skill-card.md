## Description: <br>
Mem0 adds an intelligent memory layer for Clawdbot that searches and stores user preferences, patterns, and conversational context across interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhayjb](https://clawhub.ai/user/abhayjb) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and assistant operators use this skill to retrieve relevant memories before responding and store explicit or conversation-derived preferences after interactions. It supports personalized responses, semantic recall, memory review, and memory deletion workflows for Clawdbot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived personal context. <br>
Mitigation: Configure the intended user ID, store only appropriate non-sensitive memories, and periodically review or delete stored memories. <br>
Risk: Memory text may be processed through OpenAI using the user's API key. <br>
Mitigation: Do not store secrets or sensitive personal data, and confirm OpenAI API key use is acceptable before adding memories. <br>


## Reference(s): <br>
- [Mem0 Integration Patterns](references/integration-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with bash and JavaScript examples; helper scripts can also emit JSON when JSON_OUTPUT is set.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENAI_API_KEY for Mem0 embedding and memory extraction; memory commands are scoped by user ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
