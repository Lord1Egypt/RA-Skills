## Description:

Run daily standups and generate task summaries for operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admiralkittysdad](https://clawhub.ai/user/admiralkittysdad)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use this skill to run structured daily standups, record completed work, plans, blockers, and escalations, and summarize local task or standup history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Standup answers, blockers, and escalations may include sensitive operational details saved locally under ~/.ops-commander.

Mitigation: Avoid entering secrets or highly sensitive incident details, and ensure the local machine and backups are appropriate for this data.

Risk: Task summaries depend on the accuracy and freshness of local task and standup files.

Mitigation: Review summaries before using them for operational decisions or handoff communication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/admiralkittysdad/skills/ops-reports)
- [Publisher profile](https://clawhub.ai/user/admiralkittysdad)
- [SkillNexus homepage](https://skillnexus.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown text with tables and local JSON standup entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save standup entries under ~/.ops-commander and summarize local task or standup files when present.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
