## Description: <br>
Run daily standups and generate task summaries for operations teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdmiralKittysDad](https://clawhub.ai/user/AdmiralKittysDad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations team members use this skill to run structured daily standups, record local updates, summarize weekly standup history, and report task status, overdue items, and open blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Standup notes and task summaries may contain sensitive operations, customer, credential, incident, or personnel details retained in local files. <br>
Mitigation: Avoid entering confidential details unless local retention is acceptable, and periodically delete old files under ~/.ops-commander when ongoing history is not needed. <br>
Risk: The skill reads local task and standup files, so stale or incomplete local data can produce misleading summaries. <br>
Mitigation: Review generated summaries against the underlying local files before using them for operational decisions or escalations. <br>


## Reference(s): <br>
- [Ops Reports on ClawHub](https://clawhub.ai/AdmiralKittysDad/ops-reports) <br>
- [SkillNexus](https://skillnexus.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, guidance] <br>
**Output Format:** [Markdown or plain-text responses with local JSON standup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local operations files under ~/.ops-commander when the user invokes standup history or task-summary workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
