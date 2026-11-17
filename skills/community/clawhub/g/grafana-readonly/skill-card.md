## Description:

Read existing Grafana dashboards and panels without modifying them. Use when answering questions about values already visible in Grafana, locating the right dashboard/panel, extracting panel queries, listing dashboard variables, or rerunning panel-backed queries with a different time range or variable set. Best for Grafana-first analytics workflows where read-only access is preferred.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwqcode](https://clawhub.ai/user/qwqcode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analytics users use this skill to answer questions from existing Grafana dashboards, inspect dashboard structure, review panel queries, list variables, and rerun panel-backed queries without modifying Grafana resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to read Grafana dashboards, panel queries, variables, and query results that may contain sensitive operational or business data.

Mitigation: Install only where the agent is authorized to read those Grafana resources, and review answers before sharing data outside the intended audience.

Risk: Requests to create, edit, or delete dashboards fall outside the skill's read-only scope.

Mitigation: Use a separate explicitly authorized workflow for Grafana modification tasks.

## Reference(s):

- [Grafana Readonly Action Checklist](references/action-checklist.md)
- [Grafana Skill Evaluation Notes](references/evaluation-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/qwqcode/skills/grafana-readonly)
- [ClawHub Publisher Profile](https://clawhub.ai/user/qwqcode)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with structured summaries and optional JSON-shaped action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Grafana workflow guidance; no executable code is bundled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
