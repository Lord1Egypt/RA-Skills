## Description:

A finance research agent skill that gathers A-share market data, calculates multi-factor scores, runs several quantitative stock-selection strategies, and produces structured CSI 300 research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External finance researchers and agent developers use this skill to automate A-share and CSI 300 research workflows, including data collection, factor scoring, strategy comparison, allocation suggestions, and report generation. Outputs are research aids and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports bundled plaintext third-party data-service credentials.

Mitigation: Remove bundled credentials, rotate any exposed JQData or Tushare secrets, and configure fresh credentials outside the skill before installation.

Risk: Generated rankings and allocation suggestions can be mistaken for financial advice.

Mitigation: Use outputs only as research support and require human review before making investment decisions.

Risk: Scheduled runs and live market-data calls can execute repeatedly and depend on external services with changing availability.

Mitigation: Enable scheduling deliberately, monitor generated reports, and validate source data quality before relying on results.

Risk: Dependencies are specified with minimum versions rather than pinned versions.

Mitigation: Pin and review dependencies in the deployment environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/hs300-research-v6)
- [Tushare Pro](https://tushare.pro)
- [Data source notes](artifact/DATA_SOURCES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and Python configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Markdown, Excel, CSV, and scheduled report artifacts when the analysis scripts are run.]

## Skill Version(s):

6.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
