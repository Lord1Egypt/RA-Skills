## Description:

Plans PancakeSwap yield farming, CAKE staking, LP staking, unstaking, and reward-harvesting workflows by comparing APR data and producing PancakeSwap UI deep links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT

## Use Case:

External DeFi users and agents use this skill to compare PancakeSwap farms and Syrup Pools, plan staking or reward-harvesting actions, and open PancakeSwap deep links for wallet review and confirmation. The skill is planning-oriented and does not execute transactions by itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill mandates a telemetry ping before workflow use.

Mitigation: Disable or require explicit user approval for the ping before installation or execution.

Risk: Bundled local scripts and runtime dependency installation can execute unreviewed code.

Mitigation: Review the bundled Python and Node scripts, pin or preinstall dependencies, and run them only in a controlled environment.

Risk: Transaction-capable cast command examples could be misused for mainnet actions.

Mitigation: Prefer PancakeSwap UI deep links for mainnet and require explicit approval plus wallet-safe key handling for any CLI transaction.

Risk: APR, pool, and reward data come from external APIs and chain RPCs and may be stale or misleading.

Mitigation: Treat APR output as untrusted financial data and verify final rates and transaction details in the PancakeSwap UI before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pcs-bot/skills/pcs-farming-planner)
- [PancakeSwap AI Repository](https://github.com/pancakeswap/pancakeswap-ai)
- [PancakeSwap App](https://pancakeswap.finance/)
- [fetch-farms.py](references/fetch-farms.py)
- [fetch-syrup-pools.py](references/fetch-syrup-pools.py)
- [fetch-solana.cjs](references/fetch-solana.cjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, PancakeSwap deep links, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [APR and pool data are fetched from external APIs or chain RPCs and should be treated as time-sensitive.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
