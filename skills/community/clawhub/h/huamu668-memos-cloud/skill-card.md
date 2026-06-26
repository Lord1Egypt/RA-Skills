## Description: <br>
Recall memories from MemOS Cloud before responding when the user needs context about previous conversations, preferences, or decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to retrieve relevant memories from MemOS Cloud and incorporate prior conversation context into replies. It is intended for recall of user preferences, past decisions, and previous project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived queries may be sent to a cloud memory service. <br>
Mitigation: Use only with trusted MemOS Cloud accounts and avoid sending secrets, credentials, regulated data, or sensitive project details. <br>
Risk: The referenced local helper `memos-api.js` was not included for review in the artifact evidence. <br>
Mitigation: Verify the local helper implementation before installation or execution. <br>
Risk: Broad automatic memory recall can surface unrelated or sensitive context. <br>
Mitigation: Prefer explicit manual memory actions and review recalled memories before including them in responses. <br>


## Reference(s): <br>
- [MemOS Cloud](https://memos.memtensor.cn) <br>
- [MemOS API Dashboard](https://memos-dashboard.openmem.net) <br>
- [OpenClaw Plugin](https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user query text to retrieve cloud memory results for optional inclusion in the agent response.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
