## Description:

OKX DeFi Invest helps agents discover OKX-aggregated DeFi products across chains and guide users through investing, withdrawing, claiming rewards, and reviewing APY, TVL, and liquidity data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to find OKX-aggregated DeFi yield, lending, borrowing, staking, and liquidity products, compare product details or trend charts, and prepare transaction steps for wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users toward signing high-impact DeFi transactions generated from calldata.

Mitigation: Before signing, verify the wallet address, chain, protocol, token, amount, spender approval, destination contract, fees, and expected asset changes in a trusted wallet or independent tool.

Risk: Opaque or unexpected calldata can result in unintended approvals, transfers, or position changes.

Mitigation: Do not sign calldata that cannot be decoded or that does not match the intended DeFi action.

Risk: Wallet addresses used with the skill may be financially identifying information.

Mitigation: Share wallet addresses only when needed and handle them as sensitive financial identifiers.

## Reference(s):

- [OKX DeFi CLI Command Reference](references/cli-reference.md)
- [OKX Web3 Homepage](https://web3.okx.com)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-defi-invest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command examples and structured transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet address resolution, product comparison tables, amount conversion guidance, calldata signing steps, and risk warnings.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
