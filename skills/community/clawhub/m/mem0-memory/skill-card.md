## Description: <br>
mem0 local memory layer for semantic memory storage, retrieval, and management with WAL-style workflow guidance, SESSION-STATE priority, and user, session, and agent memory levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chircken891](https://clawhub.ai/user/chircken891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent local semantic memory workflows, including memory add, search, update, history, deletion, and memory-augmented chat commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist and reuse conversation details, which can include personal details, secrets, business data, URLs, and file paths. <br>
Mitigation: Install only when persistent memory is intended, inspect the referenced memory implementation before use, and ensure users can review, edit, disable, and delete saved memories. <br>
Risk: Memory-augmented chat may send conversation content to the configured LLM. <br>
Mitigation: Confirm whether MiniMax or any configured LLM receives conversation content before using the skill with sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chircken891/mem0-memory) <br>
- [ZejunCao/bilibili_code Mem0 reference](https://github.com/ZejunCao/bilibili_code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes command patterns for persistent memory operations and memory-augmented chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
