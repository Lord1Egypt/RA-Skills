## Description:

Run Pine Script indicators from the command line using pinets-cli to execute, test, or analyze indicators, calculate technical analysis values, and fetch crypto market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alaa-eddine](https://clawhub.ai/user/alaa-eddine)

### License/Terms of Use:


## Use Case:

Developers and technical analysts use this skill to run Pine Script v5+ indicators through pinets-cli, inspect JSON plot outputs, and work with Binance or custom OHLCV candle data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unpinned npm/npx execution for pinets-cli.

Mitigation: Use a pinned, locally installed version with a lockfile or verified package source, and avoid global installation in shared environments.

Risk: The skill can fetch live market data and write output files.

Mitigation: Approve live market-data fetches and output paths explicitly before running commands.

## Reference(s):

- [PineTS CLI homepage](https://github.com/QuantForgeOrg/pinets-cli)
- [PineTS runtime](https://github.com/QuantForgeOrg/PineTS)
- [ClawHub skill page](https://clawhub.ai/alaa-eddine/skills/pinets)
- [Publisher profile](https://clawhub.ai/user/alaa-eddine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Pine Script examples, JSON examples, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described CLI output is structured JSON containing indicator metadata, plots, and optionally raw results and market data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
