## Description: <br>
Manage Movedone kanban projects, columns, tasks, comments, and task links via the local HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaichaosun](https://clawhub.ai/user/kaichaosun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage local Movedone kanban data through curl commands against the Movedone HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bearer token provides full access to the local Movedone HTTP API and can expose project data if shared. <br>
Mitigation: Keep MOVEDONE_AUTH_TOKEN private, use the local base URL, and avoid logging or pasting the token into shared contexts. <br>
Risk: Project, column, task, comment, and link operations can change or delete kanban data. <br>
Mitigation: Double-check project, column, and task IDs before allowing delete, move, or bulk update commands. <br>


## Reference(s): <br>
- [Movedone](https://movedone.ai) <br>
- [Movedone download](https://movedone.ai/#download) <br>
- [ClawHub release page](https://clawhub.ai/kaichaosun/movedone) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, MOVEDONE_BASE_URL, and MOVEDONE_AUTH_TOKEN.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
