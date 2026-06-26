## Description: <br>
Harvest pending CAKE and partner-token rewards from PancakeSwap farming positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External PancakeSwap users use this skill to check pending farming, Infinity, V3, and Syrup Pool rewards, then receive harvest instructions and links for wallet-confirmed claiming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local shell commands and helper scripts, including runtime Python dependency installation. <br>
Mitigation: Review commands before execution, prefer an isolated environment, and allow only the required binaries and domains for the reward check. <br>
Risk: The workflow contacts external PancakeSwap, RPC, and market-data services with the user's wallet address and sends a small system-metadata ping. <br>
Mitigation: Use only when sharing a public wallet address and basic system metadata with those services is acceptable under the user's policy. <br>
Risk: Reward amounts and USD estimates depend on third-party APIs and public RPC endpoints and may be incomplete, delayed, or unavailable. <br>
Mitigation: Treat results as estimates and confirm final rewards and transactions in the user's own wallet and the PancakeSwap interface. <br>


## Reference(s): <br>
- [PancakeSwap AI homepage](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [fetch-v3-pending.py](references/fetch-v3-pending.py) <br>
- [fetch-infinity-pending.py](references/fetch-infinity-pending.py) <br>
- [fetch-syrup-pending.py](references/fetch-syrup-pending.py) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown rewards summary tables with inline shell commands and harvest links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet-scoped reward estimates, USD conversions when pricing data is available, and links for user-confirmed claiming.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
