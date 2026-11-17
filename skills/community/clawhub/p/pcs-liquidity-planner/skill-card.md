## Description:

Plans PancakeSwap liquidity provision by gathering user intent, verifying tokens, assessing pool metrics, recommending price ranges and fee tiers, and generating a PancakeSwap deep link for user review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and DeFi operators use this skill to plan PancakeSwap liquidity positions across supported chains without writing code. It helps compare pool types, fees, yield signals, and impermanent-loss risk before producing a PancakeSwap link for final user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious because the skill requests broad local code execution for a DeFi planning workflow.

Mitigation: Run it only in a restricted sandbox and avoid mounting wallets, private keys, credentials, or unrelated workspace files.

Risk: The skill depends on a non-bundled workspace-relative script for pool discovery.

Mitigation: Confirm the expected script exists in the target workspace and review it before allowing execution.

Risk: The skill automatically contacts pancakeswap.ai with host details during initialization.

Mitigation: Review the network ping behavior before installation and disable or block it if host telemetry is not acceptable.

Risk: Incorrect chain IDs, token addresses, or PancakeSwap URLs can lead users toward unsafe liquidity actions.

Mitigation: Verify every chain, token address, pool, and PancakeSwap URL before using any generated link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pcs-bot/skills/pcs-liquidity-planner)
- [PancakeSwap AI Repository](https://github.com/pancakeswap/pancakeswap-ai)
- [PancakeSwap App](https://pancakeswap.finance/)
- [Data Providers Reference](artifact/references/data-providers.md)
- [Position Types Reference](artifact/references/position-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command snippets and PancakeSwap deep link URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance and review links only; it does not execute blockchain transactions.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
