## Description: <br>
Helps OpenClaw users design and operate a persistent multi-agent team with a Manager, specialized Workers, planning interviews, persona selection, and mandatory QA gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porkapple](https://clawhub.ai/user/porkapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, developers, and workflow owners use this skill to create or maintain a delegated AI team that plans work, assigns tasks to specialized agents, and checks deliverables before returning them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads prior OpenClaw user context, memory, and session history to design teams and verify agent communication. <br>
Mitigation: Review stored OpenClaw context before use and avoid placing secrets or sensitive material in memory, session history, or interview answers. <br>
Risk: The skill can create persistent agents and update OpenClaw configuration, including agent lists and agent-to-agent permissions. <br>
Mitigation: Back up ~/.openclaw first, inspect generated SOUL.md, AGENTS.md, openclaw.json, and session keys, and keep agentToAgent.allow limited to the required agents. <br>
Risk: Shell scripts and cleanup commands affect local OpenClaw files and workspaces. <br>
Mitigation: Review scripts before execution, verify target paths, and confirm backup integrity before running setup or uninstall cleanup commands. <br>
Risk: Security evidence flags under-disclosed network and isolation risks. <br>
Mitigation: Treat the release as requiring review before deployment and run it only in an environment whose OpenClaw permissions and network behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/porkapple/openclaw-multi-agents) <br>
- [Project homepage](https://github.com/porkapple/openclaw-multi-agent) <br>
- [Architecture guide](references/architecture_guide.md) <br>
- [Planning guide](references/planning_guide.md) <br>
- [Persona library](references/persona-library.md) <br>
- [Task categories and model matching](references/task_categories_and_model_matching.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent OpenClaw agent workspaces, SOUL.md and AGENTS.md files, openclaw.json updates, and team design documents.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
