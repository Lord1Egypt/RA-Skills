## Description: <br>
Giveaway Skills provides a call guide and ethers.js examples for interacting with a specific BSC mainnet giveaway contract, including creation, claiming, whitelist management, and expired withdrawal flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FranckStone](https://clawhub.ai/user/FranckStone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prepare scripts, frontends, or agent workflows that call the deployed giveaway contract on BSC mainnet and understand its parameters, restrictions, and transaction requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may lead to real BSC mainnet transactions that spend assets, approve token allowances, incur gas, or become irreversible after wallet confirmation. <br>
Mitigation: Verify chain ID, contract address, ABI/source, token addresses, giveaway amounts, fees, expiration times, and allowance scope before signing any transaction. <br>
Risk: Using stale or mismatched contract details can produce incorrect calls against the deployed giveaway contract. <br>
Mitigation: Confirm the deployed contract address and ABI/source against trusted project sources before wiring scripts, frontends, or agent workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FranckStone/giveaway-skills) <br>
- [BSC public RPC endpoint](https://bsc-dataseed.binance.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript/ethers.js code snippets and ABI fragments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain transaction guidance that requires user review before signing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
