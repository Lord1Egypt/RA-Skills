## Description:

Skill operativa read-only para análisis de Jira Cloud con enfoque en contexto, bloqueadores y triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, and operations teams use this skill to analyze Jira Cloud issues, summarize status, identify blockers, triage backlog items, and prepare stakeholder updates without changing Jira data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read Jira issues, comments, worklogs, projects, statuses, and transitions available through the connected Jira plugin.

Mitigation: Install only when that Jira read access is acceptable, and grant the plugin the least Jira permissions needed for the intended analysis.

Risk: Operational summaries or triage recommendations could be mistaken for confirmed facts.

Mitigation: Require outputs to separate observed Jira facts from inferences and missing data before acting on recommendations.

Risk: Users may expect the skill to update Jira even though this release is read-only.

Mitigation: Keep create, edit, comment, assignment, and transition actions disabled for this skill version.

Risk: The skill instructions and examples are written in Spanish.

Mitigation: Provide translated operating instructions or examples for teams that do not work in Spanish.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kansodata/skills/kansodata-jira-ops)
- [Examples](artifact/examples.md)
- [Scope](artifact/scope.md)
- [Usage Rules](artifact/usage-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with clearly separated facts, inferences, and missing data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Jira analysis; no create, edit, comment, assignment, or transition actions]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
