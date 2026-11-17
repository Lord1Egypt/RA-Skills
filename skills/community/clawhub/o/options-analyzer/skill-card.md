## Description:

Options Analyzer helps agents fetch option chains, calculate Greeks, analyze implied volatility, evaluate option strategy payoff and break-even points, and recommend options strategies using yfinance data and Black-Scholes calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzema216](https://clawhub.ai/user/benzema216)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to perform educational options analysis, including option-chain lookup, Greeks calculation, IV comparison, payoff analysis, and strategy selection support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data requests may disclose ticker symbols to Yahoo Finance through yfinance.

Mitigation: Use the skill only when that data flow is acceptable and avoid entering sensitive proprietary watchlists in shared environments.

Risk: Options analysis and strategy rankings may be mistaken for personalized financial advice.

Mitigation: Treat outputs as educational calculations, verify market data and assumptions independently, and make trading decisions outside the skill.

Risk: Unreviewed or floating Python dependencies can change behavior over time.

Mitigation: Install and run the skill in an isolated Python environment with reviewed, pinned dependencies.

## Reference(s):

- [Options strategies guide](references/strategies.md)
- [Greeks guide](references/greeks_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON analysis with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on live Yahoo Finance data retrieved through yfinance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
