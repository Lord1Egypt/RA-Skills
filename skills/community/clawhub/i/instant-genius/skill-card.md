## Description: <br>
Instant Genius configures OpenClaw with self-learning memory, proactive behavior rules, smart heartbeat routines, correction logging, and structured memory management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenpengyu1016](https://clawhub.ai/user/chenpengyu1016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize or enhance an OpenClaw workspace with persistent learning memory, correction tracking, proactive behavior guidance, and heartbeat-based maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup process can create or change persistent memory and behavior configuration for OpenClaw. <br>
Mitigation: Review the templates before installation, back up AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, and ~/self-improving, and require a diff before appending changes. <br>
Risk: Stored corrections, preferences, and patterns may retain user-specific information longer than expected. <br>
Mitigation: Periodically inspect, edit, or delete stored memories and keep only information the user intentionally wants persisted. <br>
Risk: Proactive behavior rules may cause unwanted notifications or agent actions if they are too broad for the workspace. <br>
Mitigation: Tune cooldown, quiet-hour, and confirmation rules before enabling proactive behavior in routine use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenpengyu1016/instant-genius) <br>
- [Learning Signals Reference](references/learning-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, template additions, and shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or proposes persistent OpenClaw memory and configuration files when setup is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
