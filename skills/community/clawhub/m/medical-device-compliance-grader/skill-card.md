## Description:

Scores medical device compliance across eight dimensions and produces a self-contained HTML scorecard with a radar chart, detailed table, and improvement advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Regulatory affairs and quality teams use it for pre-submission self-assessment, remediation checks, and comparison across products. Scores are self-assessments and do not replace qualified regulatory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selected report path may overwrite an existing file.

Mitigation: Choose a trusted output path and check whether a file already exists before generating the report.

Risk: Unescaped product, market, or date input can affect generated HTML when processing third-party data or sharing reports.

Mitigation: HTML-escape those fields before processing third-party input or sharing the report.

Risk: Compliance scores are self-assessments, and bundled security assurances may be outdated.

Mitigation: Have a qualified regulatory professional review scores and recommendations; assess security using current evidence rather than relying on bundled assurances.

## Reference(s):

- [Compliance scoring dimensions and criteria](references/合规评分维度与标准.md)
- [Publisher homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Analysis, HTML report, JSON, Guidance]

**Output Format:** [Self-contained HTML scorecard with radar chart and detailed table; optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight compliance dimensions scored 0–5 or marked N/A; HTML uses inline SVG and has no external dependencies.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
