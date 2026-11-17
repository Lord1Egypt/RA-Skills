## Description:

Helps agents use a managed Kibana connection to inspect and manage observability, security, and search resources, with user approval before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to query and manage Kibana saved objects, dashboards, alerts, and related resources through their authorized connection. It also provides guidance for approved automation using hosted functions and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad access could expose or change Kibana resources.

Mitigation: Use a least-privilege connection, begin with read-only operations, and confirm specific resource IDs before writes or deletions.

Risk: Connector execution, hosted functions, triggers, and destinations can cause external effects or ongoing event forwarding.

Mitigation: Obtain explicit approval for the target and payload before execution, and review automation destinations before enabling them.

## Reference(s):

- [ClawHub Kibana skill](https://clawhub.ai/byungkyu/skills/kibana)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Kibana REST API documentation](https://www.elastic.co/docs/api/doc/kibana/)
- [Saved Objects API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with CLI commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Kibana operations use the user's authorized connection; writes require explicit approval.]

## Skill Version(s):

1.2.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
