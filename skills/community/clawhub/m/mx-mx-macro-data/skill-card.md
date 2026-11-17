## Description:

Mx Macro Data lets an agent query Eastmoney macroeconomic data with natural language and save the returned data as CSV files with a text description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akiry09](https://clawhub.ai/user/akiry09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research agents use this skill to retrieve global macroeconomic indicators, monetary and fiscal data, trade data, employment data, industry data, and specific commodity prices from Eastmoney. It is most useful when an upstream planner can turn broad user intent into specific indicators, regions, commodities, and follow-up completeness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text is sent to Eastmoney's service with the user's EM_API_KEY.

Mitigation: Use the skill only when sharing the query with Eastmoney is acceptable, and keep EM_API_KEY out of code, prompts, logs, and output files.

Risk: Generated CSV files contain data from a remote source and may be opened in spreadsheet tools.

Mitigation: Review or sanitize CSV files before opening them with spreadsheet security protections disabled.

Risk: Broad region or multi-indicator requests may return incomplete coverage.

Mitigation: Have the upstream planner compare expected region and indicator pairs against each frequency-specific CSV and issue follow-up queries until complete or a retry limit is reached.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/akiry09/skills/mx-mx-macro-data)
- [Eastmoney Miaoxiang Service](https://ai.eastmoney.com/mxClaw)
- [Eastmoney Macro Data API Host](https://ai-saas.eastmoney.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, CSV files, TXT files]

**Output Format:** [Markdown guidance with shell and Python examples; runtime output is CSV files, a TXT description file, and a Python result dictionary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY. Query text is sent to Eastmoney; output files are grouped by detected frequency such as yearly, quarterly, monthly, weekly, daily, or unknown.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
