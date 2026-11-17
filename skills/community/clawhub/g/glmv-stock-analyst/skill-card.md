## Description:

GLM-V-Stock-Analyst helps agents analyze Hong Kong, mainland China, and U.S. stocks by collecting market data, charts, news, fundamentals, and capital-flow signals, then producing structured stock-analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zai-org](https://clawhub.ai/user/zai-org)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and market-analysis users use this skill to prepare evidence-based stock summaries and detailed reports for Chinese investors covering Hong Kong, A-share, and U.S.-listed equities. It is intended for informational analysis workflows that combine fetched market data, chart inspection, web search, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs unpinned dependencies.

Mitigation: Run the skill in an isolated environment and review or pin dependencies before installing.

Risk: Stock targets and related queries may be sent to multiple external market-data and search providers.

Mitigation: Avoid sensitive portfolio or watchlist symbols when provider privacy matters.

Risk: Some market data may come from unauthenticated HTTP endpoints.

Mitigation: Verify important prices, events, and financial conclusions against trusted HTTPS sources before relying on reports.

Risk: Generated local HTML can expose file paths.

Mitigation: Review generated HTML before sharing and avoid publishing local workspace paths.

## Reference(s):

- [Report template](artifact/references/report_template.md)
- [Hong Kong stock analysis knowledge](artifact/references/hk_stock_knowledge.md)
- [Sensitive company analysis rules](artifact/references/sensitive_companies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise chat summaries, Markdown reports, JSON data summaries, PNG chart files, HTML/PDF exports, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a multimodal host model to inspect generated chart images; an optional Tushare token can improve A-share data reliability.]

## Skill Version(s):

1.0.4 (source: evidence.release.version and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
