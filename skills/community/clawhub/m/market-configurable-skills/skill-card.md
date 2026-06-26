## Description: <br>
Provides contract call guidance and best practices for GouGouBi configurable crypto price prediction market contracts, including market creation, trading, settlement, and ethers/web3 integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FranckStone](https://clawhub.ai/user/FranckStone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation authors use this skill to understand and prepare calls for creating GouGouBi prediction markets, buying YES/NO positions, swapping positions, resolving rounds, and redeeming settlements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated transaction guidance may be used for irreversible on-chain actions involving funds. <br>
Mitigation: Verify the network, contract address, wallet, token, amount, allowance, slippage, fee recipient, round, and native value before signing; prefer small test transactions and limited approvals. <br>
Risk: Contract call guidance can become unsafe if it is applied to the wrong deployment or an ABI that differs from the documented GouGouBi contracts. <br>
Mitigation: Compare proposed calls against the deployed contract ABI, product configuration, and current market addresses before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FranckStone/market-configurable-skills) <br>
- [Source skill file](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration guidance] <br>
**Output Format:** [Markdown with Solidity and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no commands are executed by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
