## Description:

Price options, compute Greeks, and plot P&L diagrams with exercise analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to calculate Black-Scholes option prices, Greeks, implied volatility, payoff tables, breakeven points, option chains, and position P/L from terminal inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted calculator arguments can execute commands through unsafe Python heredoc interpolation.

Mitigation: Use only trusted numeric inputs until the interpolation is fixed, and review the script before installing or running it.

Risk: Price command inputs and results may be written to $HOME/.option-calculator/history.log.

Mitigation: Set OPTION_CALCULATOR_DIR to an appropriate directory or clear the history log when command history should not persist.

## Reference(s):

- [Option Calculator on ClawHub](https://clawhub.ai/xueyetianya/skills/option-calculator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bash and Python 3 standard library calculations; price commands may be logged under the configured option calculator data directory.]

## Skill Version(s):

2.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
