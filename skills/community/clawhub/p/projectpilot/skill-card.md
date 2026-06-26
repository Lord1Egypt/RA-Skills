## Description: <br>
Lightweight project management for agents. Create projects, track tasks, set priorities and deadlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Projectpilot to maintain local project task lists, track task status, assign owners, set deadlines, identify overdue work, and generate status summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project names, task text, assignees, deadlines, and status data are stored on disk. <br>
Mitigation: Avoid storing sensitive roadmap or personnel details unless workspace storage is acceptable; set PROJECTPILOT_DATA to a dedicated directory for clearer separation, cleanup, and backups. <br>


## Reference(s): <br>
- [Projectpilot on ClawHub](https://clawhub.ai/raychanpmp/projectpilot) <br>
- [PM Templates & Frameworks](references/pm-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores project and task records as local JSON files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
