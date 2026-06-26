## Description: <br>
Integrates a three-layer memory system, a self-evolution workflow, and proactive action mode so agents can use persistent memory, learning records, and task state to guide future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory, learning logs, task state tracking, and proactive workflow checks to an agent workspace. It is intended for agents that should remember prior context, record lessons and errors, and update operating files as part of recurring work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad persistent memory writes that may capture sensitive user context or credentials. <br>
Mitigation: Require explicit approval before memory writes and exclude secrets, API keys, and sensitive personal data from memory files. <br>
Risk: The skill describes scheduled or recurring self-evolution behavior that can change agent behavior over time. <br>
Mitigation: Disable scheduled actions by default and require a human-reviewed diff before enabling or applying recurring changes. <br>
Risk: The skill directs agents to update files that can control future behavior, including AGENTS.md, TOOLS.md, HEARTBEAT.md, and session state files. <br>
Mitigation: Require reviewed diffs and approval before modifying files that affect future agent instructions or tool usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/integrated-memory-evolution-action) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chungvic) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, file path conventions, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to read and write persistent memory, learning logs, task state files, and workflow-control files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
