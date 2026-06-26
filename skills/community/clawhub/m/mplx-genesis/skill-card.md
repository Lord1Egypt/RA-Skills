## Description: <br>
Launch tokens on Solana using Metaplex Genesis protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockiosaurus](https://clawhub.ai/user/blockiosaurus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and token creators use this skill to configure and launch Solana tokens with Metaplex Genesis, including LaunchPool distribution, unlocked allocations, Raydium liquidity pool graduation, lifecycle checks, and wallet setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of a local wallet for costly, hard-to-reverse Solana token launch actions. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit review of the network, wallet address, token allocations, fees, metadata upload, and finalization step before signing any transaction. <br>
Risk: Genesis launch execution depends on a separate plugin that performs transactions. <br>
Mitigation: Install only when the Genesis plugin is trusted and intended for use, and verify plugin configuration before launch operations. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/blockiosaurus/mplx-genesis) <br>
- [Publisher profile](https://clawhub.ai/user/blockiosaurus) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown or text guidance with structured launch parameters and tool-call recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the separate Genesis plugin to execute Solana transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
