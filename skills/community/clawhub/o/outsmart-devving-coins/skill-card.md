## Description: <br>
Launch tokens on Solana launchpads for requests about creating a token, devving a coin, launching a meme, PumpFun, LaunchLab, Jupiter Studio, DBC, bonding curves, or token deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outsmartchad](https://clawhub.ai/user/outsmartchad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to plan and run Solana token launches through launchpads such as PumpFun, Jupiter Studio, Raydium LaunchLab, and Meteora DBC. It is not intended for buying existing tokens or providing liquidity to existing pools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to launch tokens and perform liquidity actions with wallet-signing authority through an external CLI. <br>
Mitigation: Use a fresh low-balance wallet, never use a primary wallet private key, and manually approve every transaction amount, fee, token detail, pool, and liquidity action. <br>
Risk: Execution depends on the external outsmart npm package and required wallet/network environment variables. <br>
Mitigation: Verify and pin the outsmart npm package before use, and provide PRIVATE_KEY and MAINNET_ENDPOINT only in an environment intended for this launch workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/outsmartchad/outsmart-devving-coins) <br>
- [Publisher profile](https://clawhub.ai/user/outsmartchad) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and launchpad guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the outsmart CLI plus PRIVATE_KEY and MAINNET_ENDPOINT environment variables when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
