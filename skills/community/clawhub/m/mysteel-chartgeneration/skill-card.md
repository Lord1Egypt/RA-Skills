## Description:

Generates ECharts chart configurations and HTML visualizations from natural-language chart requests or structured data using Mysteel's chart generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn chart descriptions or structured datasets into ECharts option JSON and interactive HTML chart files for reports and exploratory analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart data and the API token are sent to Mysteel's external API.

Mitigation: Use the skill only with chart data suitable for that external service and store the API key carefully.

Risk: Generated HTML can execute unsafe JavaScript from user-controlled or API-controlled chart content.

Mitigation: Avoid opening generated HTML from untrusted inputs or serving it from a trusted origin without review.

Risk: The generated HTML loads ECharts from a CDN.

Mitigation: Prefer a fixed renderer that bundles ECharts or uses integrity-pinned assets.

## Reference(s):

- [API Parameters](references/api-parameters.md)
- [Mysteel AI Chart API](https://mcp.mysteel.com/mcp/info/genie-tool/v1/tool/ai-chart)
- [ClawHub Skill Page](https://clawhub.ai/wyb92/skills/mysteel-chartgeneration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files]

**Output Format:** [Markdown guidance with shell commands, generated ECharts option JSON, metadata JSON, and rendered HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses synchronous API requests only and requires a user-provided API key stored in references/api_key.md.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
