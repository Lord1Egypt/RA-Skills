## Description: <br>
项目开发助理 helps agents initialize, log, resume, and summarize development projects through structured local project records and concise status summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongtengkeji](https://clawhub.ai/user/gongtengkeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create project workspaces, keep structured development logs, resume interrupted work, track issues, and generate compact project status briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local project memory may capture sensitive details in logs or session archives. <br>
Mitigation: Use explicit project paths and avoid storing secrets or credentials in logs, status files, or session archives. <br>
Risk: Some helper commands can scan broad local project locations. <br>
Mitigation: Prefer commands scoped to a known project path and avoid global briefing, monitor, and admin statistics commands unless broad local scanning is acceptable. <br>
Risk: A statistics command can silently delete saved briefing files. <br>
Mitigation: Avoid purge-test and admin statistics commands unless deletion of old briefing files is intended, and preserve backups for important project briefings. <br>


## Reference(s): <br>
- [Project Development Workflow](artifact/references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gongtengkeji/project-development-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Concise text or Markdown with inline shell commands and JSON-backed project state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local logs, session archives, briefings, and project state when invoked for project work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
