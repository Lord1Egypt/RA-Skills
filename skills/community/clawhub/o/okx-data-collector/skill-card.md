## Description:

Provides guidance and a helper script for collecting and analyzing OKX real-time tick data and multi-period historical K-line data for quantitative trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading engineers use this skill to plan OKX market-data collection, fetch historical K-line datasets, and prepare data for backtesting and strategy research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can write or overwrite files outside the intended output directory if run with crafted arguments.

Mitigation: Review the helper script before running it, use a dedicated output directory, avoid untrusted or generated values for --symbol and --bar, and run it as a low-privilege user until path validation is added.

## Reference(s):

- [OKX API documentation](https://www.okx.com/docs-v5/en/)
- [OKX data analysis report](artifact/OKX_DATA_ANALYSIS.md)
- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/okx-data-collector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python helper code, JSON and CSV data examples, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical data helper writes OKX candle output as JSON and CSV when an output directory is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
