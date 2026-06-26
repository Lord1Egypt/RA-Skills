## Description: <br>
Manage LP positions on Solana DEXes to earn swap fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outsmartchad](https://clawhub.ai/user/outsmartchad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan and run Solana liquidity-provider workflows, including DLMM and DAMM v2 pool checks, liquidity adds, fee claims, rebalancing, and exits. It is intended for on-chain LP farming rather than lending, staking, or centralized-exchange market making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a raw Solana wallet private key and an external CLI that can initiate irreversible financial transactions. <br>
Mitigation: Use a dedicated low-balance wallet, avoid exposing a main wallet private key, and manually review or simulate transactions before execution. <br>
Risk: Liquidity-provider positions can lose value through impermanent loss, out-of-range DLMM positions, fees, and volatile token behavior. <br>
Mitigation: Use conservative position sizing, keep gas reserves, prefer wider bins for DLMM, and review pool liquidity and token age before adding liquidity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/outsmartchad/outsmart-lp-farming) <br>
- [Project homepage](https://github.com/outsmartchad/outsmart-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require the outsmart CLI plus PRIVATE_KEY and MAINNET_ENDPOINT environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
