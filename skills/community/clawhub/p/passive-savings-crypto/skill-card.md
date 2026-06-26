## Description: <br>
Put idle USDC to work earning yield for you or your agent's wallet. Funds grow automatically and move like regular USDC when you're ready. No protocol interactions, no special steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marvinmarnold](https://clawhub.ai/user/marvinmarnold) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto users use this skill to let an agent check sUSDC balances, deposit Linea USDC into yield-bearing sUSDC, and transfer funds through provided Node.js scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real blockchain transactions and move wallet funds on Linea mainnet. <br>
Mitigation: Use a dedicated low-balance Linea wallet and require manual confirmation before every deposit or transfer. <br>
Risk: The mint flow may grant persistent router spending authority for USDC. <br>
Mitigation: Verify contract addresses independently and revoke or avoid unlimited USDC allowance if persistent approval is not acceptable. <br>
Risk: RPC configuration affects where signed transactions and wallet queries are sent. <br>
Mitigation: Set RPC_URL to a trusted Linea endpoint and review the fallback RPC before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marvinmarnold/passive-savings-crypto) <br>
- [Project homepage](https://github.com/locker-labs/passive-savings-crypto) <br>
- [autoHODL SYT reference](https://hackmd.io/@locker/autohodl-syts) <br>
- [autoHODL on-chain stats](https://dune.com/locker_money/autohodl) <br>
- [Aave](https://aave.com) <br>
- [Linea](https://linea.build) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with wallet addresses, balances, transaction hashes, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_PRIVATE_KEY and RPC_URL; deposit and transfer actions submit irreversible Linea mainnet transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
