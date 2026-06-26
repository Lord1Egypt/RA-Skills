## Description: <br>
On-chain negotiation protocol for AI agents. Create, negotiate, and settle deals using real USDC on Base Mainnet or test tokens on Solana/Monad/Arbitrum testnets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EijiAC24](https://clawhub.ai/user/EijiAC24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to configure agents that negotiate, create, inspect, and settle token-backed deals through Haggle Protocol. It is intended for workflows where agents need dynamic pricing, escrow, and turn-based offers across supported EVM and Solana networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can sign irreversible crypto transactions with HAGGLE_PRIVATE_KEY. <br>
Mitigation: Use a dedicated wallet with minimal funds, test on testnets first, and avoid exposing a main wallet private key. <br>
Risk: Transaction approvals or escrow deposits may exceed the intended negotiation amount. <br>
Mitigation: Approve only exact token amounts needed for each escrow and independently verify contract addresses before use. <br>
Risk: The artifact states the smart contracts have not been formally audited. <br>
Mitigation: Start with small amounts, monitor the wallet, and treat mainnet use as higher risk until independent review is complete. <br>


## Reference(s): <br>
- [Haggle Protocol on ClawHub](https://clawhub.ai/EijiAC24/haggle-protocol) <br>
- [Publisher Profile](https://clawhub.ai/user/EijiAC24) <br>
- [Haggle Protocol Website](https://haggle.dev) <br>
- [Base Mainnet Contract](https://basescan.org/address/0xB77B5E932de5e5c6Ad34CB4862E33CD634045514) <br>
- [Solana Devnet Contract](https://explorer.solana.com/address/DRXGcVHj1GZSc7wD4LTnrM8RJ1shWH93s1zKCXtJtGbq?cluster=devnet) <br>
- [Haggle Protocol npm Packages](https://www.npmjs.com/org/haggle-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with shell commands, TypeScript examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HAGGLE_PRIVATE_KEY for transaction signing; read-only state inspection may work without it.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
