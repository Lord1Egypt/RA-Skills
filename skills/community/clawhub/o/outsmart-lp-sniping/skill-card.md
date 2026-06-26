## Description: <br>
Buy tokens at or near LP creation on Solana for sniping, bonding curve graduation, migration, new pool, LP-created, PumpFun graduation, LaunchLab, and first-buy scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outsmartchad](https://clawhub.ai/user/outsmartchad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare Solana LP sniping and follow-on sell or liquidity actions with the outsmart CLI. It is intended for newly created or migrating pools, not slow accumulation, established-token trading, or unresearched tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of a private key for irreversible Solana trades and liquidity actions. <br>
Mitigation: Use a dedicated low-balance wallet, never a main wallet, and require manual review before every buy, sell, pool creation, or liquidity transaction. <br>
Risk: LP sniping can expose users to rugs, late entries, MEV competition, and rapid losses. <br>
Mitigation: Verify every mint and pool address, keep position sizes conservative, set spend and slippage limits where available, and avoid increasing size to chase a missed entry. <br>
Risk: The skill depends on the outsmart CLI and mainnet endpoint configuration to perform sensitive trading actions. <br>
Mitigation: Confirm the installed CLI package and endpoint before use, and run commands only after reviewing the exact token, pool, amount, tip, and liquidity parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/outsmartchad/outsmart-lp-sniping) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the outsmart CLI plus PRIVATE_KEY and MAINNET_ENDPOINT environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
