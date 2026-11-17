## Description:

Generates inventor resignation monitoring briefs by identifying potentially departed inventors, checking their recent patent activity at other organizations, assessing technical similarity, and producing structured HTML risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Corporate IP teams and patent analysts use this skill to monitor inventors who may have left a target company and review whether their later patent filings suggest technical or legal risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may embed untrusted patent or JSON content as active HTML or JavaScript.

Mitigation: Open generated reports cautiously and review or sanitize report inputs until HTML fields are escaped or an effective content security policy is added.

Risk: Company, inventor, and technology-domain queries are sent to the configured PatSnap MCP account.

Mitigation: Install and run the skill only where sharing those queries with the configured PatSnap account is acceptable.

## Reference(s):

- [Workflow](references/workflow.md)
- [Inventor Monitor Data Schema](references/data_schema.json)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/inventor-resignation-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON-shaped monitoring data, terminal summaries, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured HTML reports under session report paths when PatSnap MCP data and monitor JSON are available.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
