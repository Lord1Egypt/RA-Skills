## Description: <br>
一个基于 hiagent 的智能助手技能，用于与 hiagent 进行对话。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honglei24](https://clawhub.ai/user/honglei24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to create or resume hiagent conversations, send queries, and retrieve conversation history through the configured hiagent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, user identifiers, conversation IDs, and retrieved chat history are shared with the configured hiagent service. <br>
Mitigation: Use only trusted hiagent endpoints, avoid sensitive content unless approved, and configure the least-privileged API key available. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the HIAGENT_API_URL, HIAGENT_API_KEY, and HIAGENT_USER_ID environment variables.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
