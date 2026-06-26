## Description: <br>
A disciplined, reproducible workflow for AI agents to log decisions, create rollback snapshots, and generate briefings for any change or feature implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tstokes06](https://clawhub.ai/user/tstokes06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to structure implementation work around decision logs, rollback snapshots, verification, and post-change briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore commands can overwrite workspace files. <br>
Mitigation: Before installing or using restore commands, confirm exactly which files will be overwritten, prefer a version-control diff or backup first, and avoid running restores in workspaces with uncommitted changes unless replacement is intended. <br>


## Reference(s): <br>
- [Operational Framework on ClawHub](https://clawhub.ai/tstokes06/operational-framework) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural guidance for decision logs, rollback snapshots, TODO tracking, and implementation briefings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
