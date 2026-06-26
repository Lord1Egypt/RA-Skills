## Description: <br>
Lobster Fork Mode helps agents spawn subagents with concise parent-session context when the subagent needs project background, prior decisions, or user preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create fork-style subagent prompts that carry task goals, relevant files, decisions, user preferences, and project structure from a parent session. It is best suited for subagent work that depends on shared context rather than isolated mechanical tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spawned subagents may receive parent-session or MEMORY.md-derived context that is broader than the task requires. <br>
Mitigation: Share only task-relevant context, exclude secrets and unrelated memory, and ask before including MEMORY.md-derived preferences. <br>
Risk: Summarized parent context can omit constraints or introduce misleading assumptions for the subagent. <br>
Mitigation: Review the fork prompt before spawning the subagent and keep task goals, constraints, files, and decisions concise and explicit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with structured prompt templates and spawn configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes suggested context limits and truncation guidance for inherited parent-session context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
