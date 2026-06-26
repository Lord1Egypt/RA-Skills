## Description: <br>
Track tasks with priorities, owners, and statuses for operations teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdmiralKittysDad](https://clawhub.ai/user/AdmiralKittysDad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations managers and team members use this skill to maintain a local task board, track owners and due dates, and surface blockers, overdue work, and unassigned critical tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, owners, due dates, and notes are saved locally in ~/.ops-commander/tasks.json. <br>
Mitigation: Avoid storing secrets or sensitive data in task notes, and review local file handling expectations before installation. <br>
Risk: Delete operations and bulk status changes can alter multiple task records. <br>
Mitigation: Confirm destructive or broad changes before writing updates to the local task file. <br>


## Reference(s): <br>
- [Ops Tasks on ClawHub](https://clawhub.ai/AdmiralKittysDad/ops-tasks) <br>
- [SkillNexus](https://skillnexus.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON task file at ~/.ops-commander/tasks.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
