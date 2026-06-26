## Description: <br>
中式智慧记忆引擎 is a Chinese-language long-term memory skill based on the M-flow knowledge graph that adds emotion-aware memory, promise tracking, relationship context, timing awareness, and preference inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent personal memory behavior to an agent, including emotion-tagged memories, commitment reminders, relationship-aware context, and timing-sensitive recall. It is intended for agents that deliberately maintain long-lived user profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently builds emotional, relationship, promise, preference, and trust profiles. <br>
Mitigation: Install only when persistent personal profiling is intended, avoid storing secrets or highly sensitive personal details, and regularly review and clean ~/.mflow-memory-cn/. <br>
Risk: The skill requires an LLM_API_KEY credential. <br>
Mitigation: Use a narrowly scoped key and rotate or revoke it if exposure is suspected. <br>
Risk: The skill extends and installs behavior from the inherited mflow-memory setup. <br>
Mitigation: Inspect the inherited mflow-memory setup before running it in an agent environment. <br>


## Reference(s): <br>
- [M-flow homepage](https://github.com/FlowElement-ai/m_flow) <br>
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/mflow-memory-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and LLM_API_KEY; stores persistent local memory under ~/.mflow-memory-cn/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
