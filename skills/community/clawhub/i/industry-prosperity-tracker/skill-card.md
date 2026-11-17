## Description:

Tracks industry prosperity by combining A-share leader financial data with macro indicators such as PMI, PPI, exports, and imports to calculate a 0-100 composite cycle score for built-in or custom sectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunsongyeah](https://clawhub.ai/user/sunsongyeah)

### License/Terms of Use:

MIT-0

## Use Case:

External users, finance analysts, and agents use this skill to gather public macro and A-share financial indicators, calculate an industry prosperity score, and produce a concise HTML dashboard with key positive and negative signals. It is intended for data aggregation and indicator calculation, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may expose users to unsafe rendering if report fields contain untrusted content.

Mitigation: Review or escape report fields before opening generated HTML, especially when sector names, stock names, or indicator text come from user input.

Risk: File-writing paths are not safely scoped according to the security summary.

Mitigation: Run the skill in a workspace sandbox and review output paths before execution.

Risk: Loosely phrased finance requests may trigger unsupported sector or stock selection.

Mitigation: Confirm sector IDs and representative A-share stock choices with the user before fetching data for custom industries.

Risk: AKShare and upstream public data interfaces may change or return delayed or missing data.

Mitigation: Pin and periodically validate AKShare, treat missing indicators as incomplete evidence, and keep the report disclaimer visible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunsongyeah/skills/industry-prosperity-tracker)
- [Data Sources](references/data_sources.md)
- [Industry Registry](references/industry_registry.md)
- [Scoring Methodology](references/scoring_methodology.md)
- [Semiconductor Indicators](references/semiconductor_indicators.md)
- [Semiconductor Industry Association](https://www.semiconductors.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated JSON or HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fetched indicator JSON, scored indicator JSON, and a one-page HTML dashboard when the bundled scripts are run.]

## Skill Version(s):

2.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
