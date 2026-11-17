## Description:

Generates patent-backed research project proposal reports by defining a technology scope, running PatSnap patent searches, analyzing seven proposal modules, and assembling a complete report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, R&D teams, and proposal writers use this skill to prepare data-driven project initiation reports grounded in PatSnap patent analysis. It supports technology scoping, patent search planning, competition analysis, IP positioning, FTO risk discussion, and proposal metric design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential technical proposals or company strategy may be exposed through patent searches if the workflow is run on sensitive inputs.

Mitigation: Confirm the intended search scope and data to be submitted before invoking PatSnap MCP tools.

Risk: Patent legal status and FTO conclusions can become stale or may be mistaken for formal legal advice.

Mitigation: Include the search date, treat FTO output as preliminary, and have a qualified patent attorney review legal conclusions before relying on them.

Risk: If PatSnap MCP access is not configured, the skill cannot retrieve live patent evidence for its report.

Mitigation: Verify PatSnap MCP authorization and tool availability before asking the agent to generate a data-backed proposal report.

## Reference(s):

- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [markdown, guidance, text]

**Output Format:** [Markdown report with structured patent-analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured PatSnap MCP access for live patent retrieval; without it, the skill can only provide an analysis framework.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
