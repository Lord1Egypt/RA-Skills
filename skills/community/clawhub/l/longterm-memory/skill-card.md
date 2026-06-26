## Description: <br>
永久记忆自动归档系统。每次对话自动记录，语义搜索，跨会话继承。重启不丢、永不覆盖、0学习成本。用于用户提到记忆、历史、之前说过、记得什么等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujw0214](https://clawhub.ai/user/liujw0214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preserve AI conversation context across sessions, summarize durable preferences and decisions into MEMORY.md, and search prior memory files when asked about earlier discussions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to automatically and permanently archive broad conversation history, which may include secrets, personal data, private contacts, or sensitive business information. <br>
Mitigation: Install only when persistent local conversation memory is intended, avoid using it for sensitive or regulated information, and review stored memory files regularly. <br>
Risk: The documented forget or delete behavior may not remove archived data because the security evidence notes unclear real deletion controls. <br>
Mitigation: Treat memory as append-only unless a user manually audits and purges the relevant MEMORY.md and memory log entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujw0214/longterm-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown memory files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or searches MEMORY.md and date-sharded memory logs when the host agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
