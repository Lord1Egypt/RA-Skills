## Description:

麦赛尔夫 is a US stock investment research agent for public-data search, fundamental analysis, and concise sourced report writing without investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzed2](https://clawhub.ai/user/yuzed2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to deploy an OpenClaw agent that gathers public market data, performs fundamental research workflows, and writes dense Markdown equity research reports for professional investors. The skill emphasizes traceable sources, current financial periods, self-calculated valuation multiples, and no unsourced investment judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment research outputs may be mistaken for investment advice or may contain stale or incomplete market data.

Mitigation: Use reports as research reference only, require inline sources for every data point, include latest financial periods and current price dates, and avoid unsourced recommendations.

Risk: Workspace memory and skill files can persist user preferences, logs, and process changes.

Mitigation: Install in a dedicated workspace and review changes to MEMORY.md and SKILLS.md before allowing them to persist.

Risk: Login-gated data or brokerage credentials could expose sensitive information if provided to the agent.

Mitigation: Use public sources only and do not provide brokerage credentials or login-gated datasets.

Risk: The optional PDF parsing workflow installs and uses pdfminer.six.

Mitigation: Pin or vet pdfminer.six before use, preferably in an isolated virtual environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuzed2/skills/investment-research-agent)
- [Research Methodology](references/methodology.md)
- [Standard Report Structure](references/report-structure.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and setup guidance with inline source links, file path conventions, shell commands, and occasional Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written as .md files with full-English paths, immediate inline citations for data points, current price data, latest financial periods, and risk disclosure.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
