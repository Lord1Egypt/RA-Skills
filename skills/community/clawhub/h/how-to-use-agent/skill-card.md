## Description: <br>
Use when improving an agent's own memory, skills, prompts, runtime rules, tool policies, AGENTS.md/agent.md files, or when adapting ideas from other agent projects into the current agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrichao2020](https://clawhub.ai/user/huangrichao2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent maintainers use this skill to plan, review, and document controlled changes to an agent's own memory, prompts, skills, runtime rules, and related instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed self-modifications could change prompts, permission policies, memory stores, skills, or runtime behavior. <br>
Mitigation: Require explicit user approval after listing exact files or surfaces, reason, risk, and rollback plan; review exact changes before applying them. <br>
Risk: Agent self-improvement work can expand into unrelated adjacent systems during a migration. <br>
Mitigation: Use progressive rollout, freeze adjacent systems during migration, and land one small verified step at a time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangrichao2020/how-to-use-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with structured checklists and optional command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before modifying agent-owned data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
