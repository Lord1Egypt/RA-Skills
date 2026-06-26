## Description: <br>
Enables an AI agent to initialize, maintain, and reuse local memory files so it can carry user context, active tasks, and preferences across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwertyu7894](https://clawhub.ai/user/qwertyu7894) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frequent agent users use this skill to preserve lightweight local context between sessions, including identity notes, preferences, active work, handoff state, and lessons learned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can store and resurface user or session information beyond the current conversation. <br>
Mitigation: Install only when cross-session memory is intentional, avoid storing secrets or sensitive personal or business data, and periodically review the memory files. <br>
Risk: Stored memory can become stale, inaccurate, or unwanted and still influence later agent behavior. <br>
Mitigation: Keep MEMORY.md as a short index, edit or clean outdated notes, and delete MEMORY.md, memory/, and .learnings/ when memory should be cleared. <br>


## Reference(s): <br>
- [Memory Bridge on ClawHub](https://clawhub.ai/qwertyu7894/memory-bridge) <br>
- [Memory Guide](MEMORY-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with local file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local memory files such as MEMORY.md, USER.md, memory/, and .learnings/ when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
