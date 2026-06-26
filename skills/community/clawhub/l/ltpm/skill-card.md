## Description: <br>
Manages multi-session, multi-stage projects by maintaining and syncing MISSION.md, PROGRESS.md, and NEXT_STEPS.md for seamless long-term progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bono5137](https://clawhub.ai/user/bono5137) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and project teams use this skill to preserve long-running project context across sessions, resume work from structured status files, and keep immediate next actions visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passive heartbeat or file-watcher behavior can save project state without enough user control. <br>
Mitigation: Require an explicit project directory and user approval before enabling auto-sync or file watching. <br>
Risk: Progress, memory, backup, or log files may capture sensitive project details. <br>
Mitigation: Keep logs and secrets out of scope, disable broad natural-language triggers where possible, and regularly inspect PROGRESS.md, MEMORY.md, and backup files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bono5137/ltpm) <br>
- [Publisher profile](https://clawhub.ai/user/bono5137) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with example shell commands and JSON/YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-tracking document templates and progress-management procedures; optional watcher and backup behavior should be explicitly scoped by the user.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
