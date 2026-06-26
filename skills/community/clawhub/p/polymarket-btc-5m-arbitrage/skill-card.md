## Description: <br>
Polymarket BTC 5-minute high-frequency arbitrage bot for automated BTC up/down prediction market trading with optional SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whh110112](https://clawhub.ai/user/whh110112) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators can use this skill to configure and run a Polymarket BTC 5-minute market bot that scans active markets, analyzes order books, and reports arbitrage or wide-spread opportunities. It also includes optional SkillPay billing flows for paid access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill handles real-money trading and billing credentials without clearly bounded authority. <br>
Mitigation: Review and audit the code before installing, use test or limited-funds accounts first, require explicit confirmation for live trading or billing, and enforce strict spending limits. <br>
Risk: Sensitive Polymarket and SkillPay credentials are required for live operation. <br>
Mitigation: Provide credentials only through environment variables or a secure secret manager, remove or rotate any bundled SkillPay key before use, and never commit real private keys or API keys. <br>


## Reference(s): <br>
- [Polymarket API Reference](references/api-reference.md) <br>
- [BTC 5-minute Trading Strategy](references/trading-strategy.md) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash commands, Python scripts, and runtime log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Polymarket credentials for live use and may use SkillPay credentials when billing is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
