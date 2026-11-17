## Description:

Horizon SDK helps agents work with prediction-market trading workflows, including market discovery, positions, orders, risk controls, wallet analytics, quantitative analytics, simulations, arbitrage, and portfolio tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesusmanuelrg](https://clawhub.ai/user/jesusmanuelrg)

### License/Terms of Use:


## Use Case:

Developers, analysts, and trading operators use this skill to let an agent inspect prediction-market portfolios, discover markets, run quantitative analysis, and prepare or execute trading and risk-management commands through the Horizon SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit or cancel real prediction-market orders.

Mitigation: Use paper trading by default and require human confirmation for every order, cancellation, arbitrage, and risk-control action.

Risk: The skill uses HORIZON_API_KEY for authenticated trading authority.

Mitigation: Restrict API-key permissions and provide the key only in environments intended for Horizon SDK trading.

Risk: The skill can start HTTPS data feeds from user-provided URLs.

Mitigation: Avoid untrusted feed URLs and prefer reviewed, pinned SDK versions before live trading.

## Reference(s):

- [ClawHub documentation](https://docs.openclaw.ai/tools/clawhub)
- [ClawHub skill page](https://clawhub.ai/jesusmanuelrg/skills/horizon-trader)
- [Publisher profile](https://clawhub.ai/user/jesusmanuelrg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands that return JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require HORIZON_API_KEY for authenticated Horizon SDK actions; all CLI command output is JSON.]

## Skill Version(s):

0.5.5 (source: server release evidence; artifact frontmatter reports 0.4.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
