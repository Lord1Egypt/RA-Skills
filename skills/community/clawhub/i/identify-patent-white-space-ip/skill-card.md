## Description:

Identifies candidate patent white-space signals from patent maps or matrices, tests false-space explanations, assesses the underlying problem, diagnoses route breaks and contradictions, and proposes principle-level resolution directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IP strategy teams use this skill to explore patent-map white-space hypotheses, rank sparse signals, test artifact explanations, and produce structured contradiction and resolution-direction reports while keeping downstream validation out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries, map details, and business context may be shared with PatSnap MCP services if live retrieval is authorized.

Mitigation: Authorize PatSnap MCP access only when that disclosure is acceptable, and continue from user-provided map evidence when live retrieval is not approved.

Risk: The skill may create a local self-contained HTML report containing sensitive patent-map analysis.

Mitigation: Keep generated reports in an appropriate workspace location and review their contents before sharing outside the intended audience.

Risk: White-space signals and resolution directions can be mistaken for validated technical, commercial, or legal conclusions.

Mitigation: Treat outputs as hypotheses, honor both confirmation gates, and perform separate technical feasibility, commercial, patentability, FTO, and filing-strategy review before decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/identify-patent-white-space-ip)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [Candidate patent white-space evaluation framework](references/evaluation-framework.md)
- [Patent white-space output templates](references/output-templates.md)
- [PatSnap Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown analysis with tables, confirmation prompts, and a self-contained HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires two explicit user confirmation gates; may use PatSnap MCP retrieval only with user authorization; excludes technical feasibility, commercial validation, patentability, FTO, and filing-strategy conclusions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
