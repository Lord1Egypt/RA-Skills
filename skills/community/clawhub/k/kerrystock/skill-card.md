## Description:

Kerrystock guides agents through calendar-effect seasonality analysis for individual stocks, ETFs, and funds, producing historical monthly and annual statistics, buy/sell timing logic, and optional screening workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoshun-sudo](https://clawhub.ai/user/caoshun-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and agent operators use this skill to analyze stock, ETF, or fund seasonality, cross-check historical moves, derive calendar-aware trade-plan timing, and generate report artifacts. Outputs are analytical workflow support and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs local finance-analysis scripts that call external tools and create report files.

Mitigation: Run the skill only in a trusted shell, review generated commands and report files, and install it only if local execution of finance tooling is acceptable.

Risk: Temporary NeoData tokens are passed on the command line during the documented verification flow.

Mitigation: Use short-lived tokens carefully, avoid exposing shell history or logs, and refresh or revoke tokens after use where possible.

Risk: Environment overrides such as NODE_BIN, PYTHON_BIN, WESTOCK_DATA_SCRIPT, NEODATA_SCRIPT, and WB_FINANCE_QUANT_DIR can change which local tools execute.

Mitigation: Set overrides only to trusted local paths and avoid inheriting these variables from untrusted environments.

Risk: HTML reports may incorporate names, codes, or JSON inputs supplied to the scripts.

Mitigation: Do not generate or share reports from untrusted inputs without sanitizing or escaping them.

## Reference(s):

- [Kerrystock ClawHub skill page](https://clawhub.ai/caoshun-sudo/skills/kerrystock)
- [Workflow reference](references/workflow.md)
- [Lessons learned](references/lessons.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; generated CSV, JSON, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Finance outputs should include data source, date range, sample counts, and non-investment-advice risk language.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
