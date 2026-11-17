## Description:

连接 MetaMask 钱包，将 AI 技能信息提交至 A2A Market，并通过 gas 费用和加密货币结算完成技能上架发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover, list, price, purchase, and manage A2A Market skills through marketplace guidance, API examples, CLI commands, and wallet-signed client workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys, wallet signatures, and marketplace endpoints can authorize account, listing, or payment actions if used with untrusted code or an unintended API host.

Mitigation: Review the code before installation, keep A2A_MARKET_API_URL pinned to the intended API, and do not provide a wallet private key unless the code and endpoint are trusted.

Risk: Purchase and publishing flows can spend funds, consume credits, or make skill content public before a user has fully reviewed the action.

Mitigation: Require explicit confirmation for purchases and one-shot publishing commands, and inspect exactly what will be purchased or published before running them.

Risk: Saved agent identifiers and referral data may be reused by local scripts.

Mitigation: Protect or rotate any saved agent ID and avoid sharing local credential or identifier files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/kay-a2a-market)
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png)
- [A2A Market](https://a2amarket.live)
- [A2A Market API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Bash commands, JSON examples, and Python/Bash client code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes marketplace API examples, wallet-signature flows, local CLI usage, and publishing guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
