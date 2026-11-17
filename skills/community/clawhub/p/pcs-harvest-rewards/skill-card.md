## Description:

Harvest pending CAKE and partner-token rewards from PancakeSwap farming positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi users and developers use this skill to check pending PancakeSwap farm and pool rewards, estimate values, and receive harvest links or instructions for review in their own wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact third-party services with a wallet address and includes a telemetry ping with host metadata.

Mitigation: Review network calls before installation, remove telemetry if it is not acceptable, and only query wallet addresses intended for public reward lookup.

Risk: Helper scripts may install an unpinned Python dependency at runtime.

Mitigation: Preinstall pinned dependencies in an isolated environment and disable runtime package installation before use.

Risk: Reward values and claimability can be stale or incomplete because they depend on external APIs, RPC endpoints, and epoch timing.

Mitigation: Verify all rewards and transaction details in the PancakeSwap UI and wallet before signing anything.

## Reference(s):

- [Harvest Rewards ClawHub page](https://clawhub.ai/pcs-bot/skills/pcs-harvest-rewards)
- [PancakeSwap AI homepage](https://github.com/pancakeswap/pancakeswap-ai)
- [V3 pending rewards helper](references/fetch-v3-pending.py)
- [Infinity pending rewards helper](references/fetch-infinity-pending.py)
- [Syrup pending rewards helper](references/fetch-syrup-pending.py)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, inline shell commands, and harvest links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only reward summaries, estimated USD values when pricing data is available, and links for user-confirmed harvesting.]

## Skill Version(s):

1.0.0 (source: server release, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
