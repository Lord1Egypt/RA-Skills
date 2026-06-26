## Description: <br>
Posts two-sided GTC limit orders on Polymarket CLOB, manages inventory skew and price drift, and estimates rebate-eligible volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to configure, dry-run, and optionally run Polymarket CLOB market-making with explicit market allowlists, spread controls, inventory skew limits, and order-management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket orders with financial loss exposure. <br>
Mitigation: Start in dry-run mode, use small quote sizes, monitor inventory and balances, and enable --live only for markets you have intentionally allowlisted. <br>
Risk: API keys and optional wallet secrets are sensitive credentials. <br>
Mitigation: Store SIMMER_API_KEY and any wallet private key in secure secret storage and avoid committing or logging them. <br>
Risk: Unsupported or near-resolution markets can make the quoted prices or risk controls unsuitable. <br>
Mitigation: Use binary markets with active volume, avoid unsupported market types, and cancel or stop quoting before resolution when needed. <br>
Risk: Unattended cron or automaton runs can continue trading after market conditions change. <br>
Mitigation: Treat every --live scheduled run as real unattended trading and pair it with explicit market limits, conservative sizing, and active status checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-clob-maker) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Risk disclaimer](artifact/DISCLAIMER.md) <br>
- [Polymarket example market import](https://polymarket.com/event/will-btc-hit-100k-by-eoy-2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment variables, Python snippets, and optional JSON automaton status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and market IDs; live mode places real orders only when explicitly enabled.] <br>

## Skill Version(s): <br>
0.9.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
