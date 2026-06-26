## Description: <br>
Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows for sustained collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admirobot](https://clawhub.ai/user/admirobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent-team maintainers use this skill to define multi-agent roles, route tasks through reviewable lifecycles, coordinate handoffs, and maintain shared artifacts for recurring team workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared directories or spawned-agent permissions could expose secrets or unrelated private workspaces if scoped too broadly. <br>
Mitigation: Confirm shared directories and spawned-agent permissions are limited to the project before installation or operation. <br>
Risk: Cron-style automation could perform access-sensitive or credential-related work without clear human oversight. <br>
Mitigation: Define exact schedules, triggers, and human approval points before automating recurring agent operations. <br>


## Reference(s): <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/admirobot/moa-team-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Guidance, Shell commands] <br>
**Output Format:** [Markdown with templates, tables, ordered workflows, and inline shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no install-time code execution is described in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
