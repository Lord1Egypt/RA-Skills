## Description:

Supports restaurant and retail site-selection decisions with map-derived spatial signals, Reilly and Hotelling location models, TQI traffic scoring, ROI scenarios, category recommendations, and decision-ready Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monsterdt](https://clawhub.ai/user/monsterdt)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant operators, real estate analysts, and developers use this skill to assess candidate storefronts, quantify traffic and competition, model ROI and payback scenarios, recommend food-service categories, and produce decision-ready reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map-service queries can reveal the target location and related category or competitor search terms.

Mitigation: Request explicit user consent before map MCP calls, use trusted map data, and fall back to local or manually supplied estimates when consent or trust is absent.

Risk: Generated reports may contain unsafe links or be misused if rendered in systems that allow raw HTML or unsafe link schemes.

Mitigation: Review generated reports before sharing and render them only in systems that sanitize links and disallow unsafe schemes.

Risk: Spatial proxies, model assumptions, and scenario forecasts can be mistaken for guaranteed business outcomes.

Mitigation: Validate assumptions with on-site counts or trusted third-party data, preserve uncertainty language, and treat the report as decision support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/monsterdt/skills/location-site-selection)
- [Benchmarks and Site-Selection Models](artifact/references/benchmarks.md)
- [Map MCP Data Mapping Guide](artifact/references/map_mcp_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, ASCII visualizations, JSON examples, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON inputs and optional opt-in map MCP spatial proxy data; outputs are decision support and not revenue guarantees.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
