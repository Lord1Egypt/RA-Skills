## Description:

Deprecated redirect for ibkr-options-assistant; agents should tell users to install the renamed skill instead of running this slug's scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexliu0130](https://clawhub.ai/user/alexliu0130)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this deprecated ClawHub release as a redirect notice for the renamed ibkr-options-assistant skill. The included toolkit evidence describes Interactive Brokers portfolio analysis, options analysis, JSON reporting, and an opt-in trading script, but this slug instructs agents not to run its scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated package still includes active Interactive Brokers account-analysis and trading scripts, including order cancellation and live order placement paths.

Mitigation: Do not install this deprecated slug as an operational skill; use the renamed package only after intentionally accepting broker-connected behavior.

Risk: Portfolio, account, P&L, Greeks, and Flex statement data may enter the agent context or output files.

Mitigation: Keep conversations and output files private, treat generated JSON like brokerage statements, and avoid sharing it with untrusted services.

Risk: trade.py cancellation and order commands can become real account actions when trading controls are enabled.

Mitigation: Keep IB Gateway in paper or read-only mode unless live trading is intended, leave trade.py safety gates closed by default, and treat cancellation/order commands as real broker actions.

Risk: Dependency or release drift could affect a live-account workflow.

Mitigation: Prefer pinned releases and locked dependency hashes before using the renamed package with a live account.

## Reference(s):

- [Greeks Primer](references/greeks_primer.md)
- [Options Book Summary](references/options_book_summary.md)
- [Options Strategy Library](references/strategies.md)
- [Trading Mode](references/trading.md)
- [Troubleshooting](references/troubleshooting.md)
- [Wheel Strategy](references/wheel_strategy.md)
- [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most included scripts are described as JSON emitters; the deprecated slug itself should produce guidance to install the renamed skill instead of executing scripts.]

## Skill Version(s):

0.2.4 (source: changelog, released 2026-05-14; release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
