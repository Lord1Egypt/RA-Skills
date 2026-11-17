## Description:

Plans PancakeSwap token swaps by gathering swap intent, checking token and market data, and generating a pre-filled PancakeSwap deep link for user review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan token swaps on PancakeSwap, verify token details, assess liquidity and pricing warnings, and open a pre-filled swap URL for wallet-side review and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initialization step sends environment details to pancakeswap.ai before the swap-planning workflow.

Mitigation: Review, remove, or gate the initialization ping before deployment unless that telemetry is acceptable.

Risk: The workflow may open PancakeSwap URLs in a local browser.

Mitigation: Inspect generated URLs before opening them and allow browser launch only for https://pancakeswap.finance/swap links.

Risk: Swap plans can rely on external token and market data that may be incomplete, stale, or misleading for low-liquidity assets.

Mitigation: Verify token contracts on-chain, surface liquidity and price warnings, and require user confirmation before using a generated deep link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pcs-bot/skills/pcs-swap-planner)
- [Publisher Profile](https://clawhub.ai/user/pcs-bot)
- [PancakeSwap AI Repository](https://github.com/pancakeswap/pancakeswap-ai)
- [PancakeSwap Swap Interface](https://pancakeswap.finance/swap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with swap details, warnings, shell command examples, and a PancakeSwap deep link URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill plans swaps only; users review and confirm any transaction in their own wallet.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
