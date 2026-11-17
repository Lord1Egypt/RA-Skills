## Description:

Analyzes bundled sales data with query, chart-generation, and trend-analysis functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xilef999](https://clawhub.ai/user/xilef999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query a bundled sales dataset, create simple sales or profit charts, and generate basic trend insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chart PNGs use fixed filenames in the system temporary directory, so a later chart can overwrite an earlier chart.

Mitigation: Copy or rename chart outputs that must be retained before generating another chart with the same metric and chart type.

Risk: The skill is designed for Chinese-language prompts and may not understand other languages reliably.

Mitigation: Use Chinese-language analysis prompts or review responses carefully when using translated prompts.

Risk: Analysis is limited to the bundled sales.csv dataset.

Mitigation: Confirm the bundled dataset is appropriate for the intended analysis before using results for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xilef999/skills/l3-sales-data-analyzer)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Chinese text responses and PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Charts are saved as PNG files in the system temporary directory with fixed filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
