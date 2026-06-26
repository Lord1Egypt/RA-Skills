## Description: <br>
Execute triangular arbitrage on Base network via KyberSwap for finding arbitrage opportunities, calculating optimal swap paths, executing multi-hop trades, and managing gas and slippage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DeFi operators use this skill to identify and evaluate triangular arbitrage paths on Base through KyberSwap. It can guide quote checks, profit calculations, and multi-hop swap execution with gas, slippage, price impact, and token safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct live on-chain swaps that may move real funds. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit confirmation before any transaction, and prefer read-only quote or simulation mode unless live trading is intentional. <br>
Risk: Trades on the wrong network or against unexpected token contracts can cause loss or failed transactions. <br>
Mitigation: Verify the Base network, router, factory, and token addresses before execution, and avoid tokens that fail the stated ownership and honeypot checks. <br>
Risk: Slippage, gas costs, or price impact can erase expected arbitrage profit. <br>
Mitigation: Calculate amountOutMin, gas cost, and price impact before execution, and only proceed when expected profit remains positive after those costs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HarleysCodes/kyberswap-arbitrage) <br>
- [Publisher Profile](https://clawhub.ai/user/HarleysCodes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with TypeScript snippets and transaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quote calculations, swap paths, contract addresses, and transaction safety checks; live transactions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
