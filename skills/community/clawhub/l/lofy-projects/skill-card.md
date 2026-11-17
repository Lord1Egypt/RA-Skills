## Description:

Project management for the Lofy AI assistant — tracks multiple projects with milestones, priority scoring engine (urgency × job relevance × momentum × energy match), meeting prep automation, time logging, stale project alerts, and work session recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrey401](https://clawhub.ai/user/harrey401)

### License/Terms of Use:


## Use Case:

People using the Lofy AI assistant use this skill to maintain a local project and academic work record, prioritize what to work on next, prepare for meetings, and track milestones, blockers, time logs, and deadlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain local project records and update data/projects.json during project conversations.

Mitigation: Review proposed changes before saving when project comments should not be recorded automatically.

Risk: Project status, deadlines, and time logs may become stale or inaccurate if the local project file is not maintained.

Mitigation: Review or back up data/projects.json periodically and correct stale project records before relying on prioritization recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrey401/skills/lofy-projects)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured project updates and JSON data changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or update local data/projects.json records for projects, academic deadlines, meetings, milestones, blockers, next actions, and time logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
