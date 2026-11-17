## Description:

宏观经济分析工具集 - 基于AKShare的GDP/CPI/PMI/利率/汇率数据

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to gather AKShare-based GDP, CPI, PMI, money supply, earnings, market, and exchange-rate inputs and produce China-focused macro daily or weekly analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on local companion scripts and an AKShare environment that are not bundled in the artifact.

Mitigation: Confirm the referenced scripts and AKShare installation are present and trusted before running analysis commands.

Risk: Macro and market analysis can be inaccurate if source data is incomplete, stale, or interpreted without review.

Mitigation: Review generated reports against current source data before relying on conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/macro-analyst)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local companion scripts and an AKShare environment when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
