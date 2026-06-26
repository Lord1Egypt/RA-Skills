## Description: <br>
Memory system v4.13: Dual-layer structure (todos for execution + knowledge for strategy) with Dream/Refinement memory mechanisms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jujitao](https://clawhub.ai/user/jujitao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain local, structured memory of user preferences, feedback, project context, and references across agent sessions. It provides guidance for memory recall, consolidation, drift checks, and separation of execution, strategy, and classified memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and recalls local memories about the user, preferences, and projects across sessions, which may include confidential, sensitive, or stale information. <br>
Mitigation: Install only when persistent local memory is desired, and periodically inspect and prune MEMORY.md, USER.md, memory/, knowledge/, and todos.md. <br>
Risk: Outdated memories can conflict with current workspace state or user intent. <br>
Mitigation: Verify referenced files, functions, paths, and project facts against current observations before relying on remembered information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jujitao/memory-never-forget) <br>
- [Memory System v2.0 - Detailed Design](references/memory-v2.md) <br>
- [Memory Writing Templates v2.0](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead the agent to create or update local memory, knowledge, and task-tracking files.] <br>

## Skill Version(s): <br>
4.1.3 (source: server release metadata; skill content describes v4.13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
