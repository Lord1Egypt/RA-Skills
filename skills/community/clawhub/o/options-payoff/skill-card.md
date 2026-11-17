## Description:

Generate an interactive options payoff curve chart with dynamic parameter controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[himself65](https://clawhub.ai/user/himself65)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn described or screenshotted options positions into interactive payoff visualizations, including expiry and theoretical P&L curves, live risk stats, and controls for strikes, premiums, volatility, DTE, and spot price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote install command is not pinned to a reviewed commit or immutable release.

Mitigation: Install only from a trusted, pinned version or reviewed commit.

Risk: Broker screenshots may contain account details unrelated to payoff visualization.

Mitigation: Redact unrelated account details before sharing screenshots with an agent.

Risk: The skill can infer missing trading inputs such as spot, premium, IV, DTE, multiplier, and strikes, which may make the chart misleading if defaults are wrong.

Mitigation: Verify all inferred values before relying on the chart for trading decisions.

Risk: Broad financial-screenshot activation rules may trigger the skill when an options payoff visualization is not intended.

Mitigation: Use the skill only when an options payoff visualization is explicitly desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/himself65/skills/options-payoff)
- [Options Strategy Payoff Formulas](references/strategies.md)
- [Black-Scholes JavaScript Implementation](references/bs_code.md)

## Skill Output:

**Output Type(s):** [code, markdown, guidance]

**Output Format:** [Interactive HTML widget with concise Markdown explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided or inferred options parameters to render dynamic payoff and theoretical P&L charts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
