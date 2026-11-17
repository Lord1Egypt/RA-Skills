## Description:

Trade on Polymarket via split + CLOB execution. Browse markets, track positions with P&L, discover hedges via LLM. Polygon/Web3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woody2434](https://clawhub.ai/user/woody2434)

### License/Terms of Use:

Apache 2.0

## Use Case:

External developers and trading operators use this skill to browse Polymarket markets, manage a Polygon wallet, execute YES/NO trades, track positions and P&L, and discover possible hedges with LLM assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a raw EVM private key in the environment for trading.

Mitigation: Use a dedicated low-balance wallet, avoid storing keys in shell history or long-lived environment files, and inspect the scripts and dependencies before use.

Risk: The skill performs persistent on-chain approvals for Polymarket trading contracts.

Mitigation: Understand exactly what each approval permits before running approval commands and plan how to revoke approvals after trading.

Risk: Trading and hedge discovery can expose users to market, liquidity, CLOB execution, and LLM analysis errors.

Mitigation: Review proposed trades manually, keep balances small, verify liquidity and pricing independently, and treat hedge suggestions as decision support rather than guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woody2434/skills/polyclaw-2)
- [Publisher profile](https://clawhub.ai/user/woody2434)
- [Polymarket](https://polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, environment variable names, and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request structured JSON output for some market and hedge commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
