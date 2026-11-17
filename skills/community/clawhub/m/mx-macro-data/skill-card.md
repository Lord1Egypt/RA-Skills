## Description:

Queries Eastmoney macroeconomic data from natural-language prompts and saves returned tables as CSV files with a text description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and agents use this skill to retrieve specific macroeconomic indicators, market data, and commodity series from Eastmoney and produce CSV outputs for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Eastmoney services during normal operation.

Mitigation: Run it only where those outbound requests are expected and allowed.

Risk: The EM_API_KEY credential could be exposed or misused if broadly scoped.

Mitigation: Set EM_API_KEY only for users and sessions that need the service, and avoid storing it in code, prompts, logs, or generated files.

Risk: Generated CSV files contain external data and may be opened in spreadsheet tools.

Mitigation: Treat generated CSV files as untrusted external data and inspect or sanitize them before opening them in Excel or similar applications.

Risk: The skill writes result files under the configured output directory.

Mitigation: Run it in an isolated workspace and set MX_MACRO_DATA_OUTPUT_DIR explicitly when file placement matters.

Risk: Large or ambiguous macroeconomic requests may return partial data or require follow-up queries.

Mitigation: Review the generated description and status messages, verify expected regions, indicators, and frequencies, and report or retry missing data when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/mx-macro-data)
- [Eastmoney Miaoxiang Claw service](https://ai.eastmoney.com/mxClaw)
- [Eastmoney API service endpoint](https://ai-saas.eastmoney.com)

## Skill Output:

**Output Type(s):** [CSV files, Text, Status metadata]

**Output Format:** [CSV files grouped by frequency, a UTF-8 text description file, and returned path/count metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and writes outputs under MX_MACRO_DATA_OUTPUT_DIR or the skill default output directory.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
