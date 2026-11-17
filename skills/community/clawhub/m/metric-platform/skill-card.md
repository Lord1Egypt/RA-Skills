## Description:

MetricHub multi-tenant metrics platform orchestration for metric catalog browsing, query construction and execution, visualization recommendations, and dashboard composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

MetricHub users, analysts, and developers use this skill to navigate metric workspaces, construct MetricHub/Gateway metric queries, choose visualizations, and assemble dashboards while following the documented query rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard, workspace, or Gateway configuration changes could affect shared MetricHub resources.

Mitigation: Confirm the workspace, user role, target dashboard, and Gateway/API-key setting before allowing write actions.

Risk: Metric query output can be wrong when the requested metric, dimensions, filters, or time context are underspecified.

Mitigation: Follow the skill's refusal rule and return empty JSON when query context is insufficient; review generated query JSON before execution.

Risk: API keys or Gateway credentials could be exposed if handled outside the trusted settings workflow.

Mitigation: Keep API keys inside MetricHub's workspace Gateway settings flow and avoid placing secrets in prompts, generated queries, or logs.

## Reference(s):

- [MetricHub skill page](https://clawhub.ai/bettermen/skills/metric-platform)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON query examples, route suggestions, API request shapes, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce empty JSON when query context is insufficient; may propose MetricHub route navigation and dashboard changes that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
