## Description: <br>
基于传播激活的联想神经记忆系统，帮助代理跨会话保存、检索和关联事实、决策、错误、TODO 与上下文。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to persist project and conversation memory across sessions, recall relevant context before tasks, trace causal chains, and capture decisions, errors, preferences, and TODOs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and reuses conversation-derived memories across sessions, which can expose secrets, credentials, regulated data, or private client/customer information if used without review. <br>
Mitigation: Avoid using the skill around sensitive data, verify where nmem_* tools store memories before use, and review saved memories regularly. <br>
Risk: Auto-capture and persistent recall are described without clear consent, retention, deletion, or sensitive-data limits. <br>
Mitigation: Confirm whether autoCapture can be disabled, establish retention and deletion practices, and use explicit consent before storing user or organizational information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/maske-neural-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Markdown guidance with memory-tool call examples and recalled context text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses depth 0-3, priority 0-10, max_tokens 100-10000, contextDepth 0-3, and autoContext/autoCapture boolean settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
