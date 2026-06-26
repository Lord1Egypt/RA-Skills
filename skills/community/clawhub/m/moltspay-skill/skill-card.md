## Description: <br>
Pay for and use AI services through MoltsPay by discovering provider services, managing wallet status, and issuing payment commands across supported crypto chains or Alipay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaqing2023](https://clawhub.ai/user/yaqing2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent discover paid AI services, check MoltsPay wallet state, and prepare or run payment commands for service use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or use a local MoltsPay wallet that may hold funds. <br>
Mitigation: Install only when an agent-capable payment wallet is intended, review the wallet location, and keep balances low or use testnets. <br>
Risk: The skill can let an agent spend real funds through broad payment-related triggers. <br>
Mitigation: Require explicit user confirmation before funding wallets, changing limits, or paying for a service. <br>
Risk: Setup can install the MoltsPay CLI globally and initialize a wallet with default spending limits. <br>
Mitigation: Review the global npm install, provider URLs, and configured per-transaction and daily spending limits before use. <br>


## Reference(s): <br>
- [MoltsPay Skill on ClawHub](https://clawhub.ai/yaqing2023/moltspay-skill) <br>
- [MoltsPay Docs](https://moltspay.com/docs) <br>
- [MoltsPay Services](https://moltspay.com/services) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with command examples and concise status or payment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, chain choices, prices, spending limits, provider service tables, and generated service URLs when returned by a paid provider.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
