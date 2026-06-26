## Description: <br>
Inner Life Core gives an OpenClaw agent persistent emotional state, a Brain Loop protocol, and structured memory files for behavior that adapts across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DKistenev](https://clawhub.ai/user/DKistenev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users install this skill when they want an OpenClaw agent to maintain local emotional state, relationship context, habits, task queues, and a repeatable operating protocol across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain user context and influence later agent behavior. <br>
Mitigation: Install only when persistent memory is desired, review generated memory files, and exclude them from version control or backups unless retention is intentional. <br>
Risk: Stored emotional state and task context can steer future autonomous actions with incomplete permission scoping. <br>
Mitigation: Require explicit approval before the agent uses powerful tools, performs unsolicited outreach, publishes content, accesses accounts, or spends money. <br>
Risk: The Brain Loop protocol can route behavior based on local state rather than only the current user request. <br>
Mitigation: Review BRAIN.md before deployment and keep user instructions and approval policies higher priority than generated state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DKistenev/inner-life-core) <br>
- [Publisher profile](https://clawhub.ai/user/DKistenev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command snippets, and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Initializes and updates local memory, task, and protocol files using shell scripts and JSON templates.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
