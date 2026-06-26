## Description: <br>
Full-stack Orca Whirlpool agent for read-only pool analytics and on-chain liquidity management, with wallet access required only for intentional write operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaizen-orca](https://clawhub.ai/user/kaizen-orca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Orca Whirlpool pools on Solana, compare LP ranges and yields, plan rebalances or exits, and generate transaction workflows for liquidity and swap operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intentional write operations can sign and submit real Solana transactions when the user supplies a wallet key. <br>
Mitigation: Use a small dedicated wallet, review the generated TypeScript and transaction plan, verify pool addresses, token mints, amounts, slippage, and position mints, and run only after explicit confirmation. <br>
Risk: Wallet credentials are sensitive and unnecessary for read-only analytics. <br>
Mitigation: Do not set KEYPAIR_PATH for read-only pool analytics, rebalance planning, or exit planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaizen-orca/orca-lp-analytics) <br>
- [Orca REST API](https://api.orca.so/v2/solana) <br>
- [Beachhouse pool stats API](https://stats-api.mainnet.orca.so) <br>
- [Snorkel swap quote API](https://pools-api.mainnet.orca.so) <br>
- [Solana mainnet RPC](https://api.mainnet-beta.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and transaction planning details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analytics do not require wallet credentials; intentional write operations require a Solana keypair path and explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
