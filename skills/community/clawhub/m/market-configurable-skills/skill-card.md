## Description:

Call guide and best practices for the configurable crypto price prediction market contracts GouGouBiMarketConfigurable.sol and GouGouBiMarketConfigurableFactory.sol, including factory creation parameters, market configuration fields, core trading and settlement methods, and conventions for calling the contracts from scripts, frontends, or OpenClow workflows via ethers/web3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franckstone](https://clawhub.ai/user/franckstone)

### License/Terms of Use:


## Use Case:

Developers and automation authors use this skill to create and interact with configurable EVM crypto price prediction markets from scripts, dApps, or OpenClow workflows. It helps callers understand factory creation parameters, market configuration fields, read methods, trading calls, settlement, redemption, and ABI fragments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated write calls can submit real financial transactions against prediction market contracts.

Mitigation: Verify the network, contract address, token, amount, fee recipient, and slippage settings before signing; require explicit user confirmation for any transaction.

Risk: Examples for contract setup and trading can be unsafe if tried directly on a live network.

Mitigation: Prefer testnets for trials and treat example addresses, market addresses, and factory addresses as placeholders until supplied by trusted project configuration.

Risk: The security guidance notes a Chinese startTime/endTime wording issue that could affect oracle logic interpretation.

Mitigation: Correct and review the startTime/endTime wording before relying on that section for oracle timing or settlement behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franckstone/skills/market-configurable-skills)
- [Publisher profile](https://clawhub.ai/user/franckstone)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Solidity and TypeScript examples, ABI fragments, and contract-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers read and write contract calls, configuration fields, slippage parameters, fee settings, oracle timing, settlement flow, and redemption behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
