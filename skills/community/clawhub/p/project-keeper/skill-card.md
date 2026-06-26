## Description: <br>
Project Keeper helps an agent create and maintain structured workspace notes for user projects, including status, goals, architecture, locations, and plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hamzaheikal2011](https://clawhub.ai/user/hamzaheikal2011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to preserve concise project context across conversations by creating project-specific Markdown notes in the workspace. It is useful when a user repeatedly discusses ongoing projects and wants future sessions to recover goals, architecture, locations, and plans quickly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create lasting workspace project notes from ordinary project discussion, which may capture sensitive project details. <br>
Mitigation: Review and approve what is stored, and avoid saving tokens, secrets, private paths, confidential architecture, or other sensitive data unless deliberately approved. <br>
Risk: Persistent project notes may become stale or incorrect and later steer agent work in the wrong direction. <br>
Mitigation: Review project notes before relying on them, update obsolete details, and delete records that should no longer be retained. <br>


## Reference(s): <br>
- [Project Keeper on ClawHub](https://clawhub.ai/hamzaheikal2011/project-keeper) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown project notes and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent project files in the workspace when a project is discussed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
