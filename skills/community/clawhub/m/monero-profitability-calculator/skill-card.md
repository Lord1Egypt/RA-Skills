## Description:

Calculate Monero mining profitability by estimating XMR earnings, electricity costs, net profit, break-even points, and ROI from hardware, electricity, and market inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

CC BY-SA 4.0

## Use Case:

Developers and mining hobbyists use this skill to estimate whether a Monero mining setup is likely to be profitable under specific hardware, electricity, pool fee, and market assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is an informational calculator rather than a complete CLI tool.

Mitigation: Review and adapt any example commands or Python code before execution, and validate assumptions against current mining, network, electricity, and market data.

Risk: The example Python code may contact CoinGecko to retrieve public Monero price data.

Mitigation: Run it only where outbound public price lookup is acceptable, and do not include secrets or private data in requests.

Risk: A voluntary XMR tip address is included in the artifact.

Mitigation: Treat tipping as optional and verify any payment destination before sending funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liumaimiao/skills/monero-profitability-calculator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with examples, tables, and inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimates and example calculations; values depend on user-supplied inputs and current market/network data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
