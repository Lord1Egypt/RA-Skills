## Description:

A-share quantitative market-data helper that uses AkShare to support stock quote lookup, historical price retrieval, financial analysis, sector review, fund-flow checks, and related A-share research tasks.

This skill is for research and development only.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to answer A-share market-data questions and generate AkShare-based examples for quotes, K-line history, sectors, financial indicators, IPO data, margin data, and stock search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AkShare and upstream market-data sources may change or fail at runtime.

Mitigation: Run the skill in an isolated Python environment, pin AkShare where practical, and validate data retrieval in the target environment before relying on results.

Risk: Stock analysis output could be mistaken for investment advice.

Mitigation: Treat generated analysis as informational research only and require human financial review before making investment decisions.

Risk: The bundled fund-flow command is likely incomplete because the script calls the fund-flow function without the AkShare namespace.

Mitigation: Review and fix the fund-flow command before enabling that workflow for users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/make453/skills/new-akshare-stock-bak2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; bundled scripts may emit JSON or console analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language A-share data workflows; results depend on AkShare installation, network access, and upstream data-source availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
