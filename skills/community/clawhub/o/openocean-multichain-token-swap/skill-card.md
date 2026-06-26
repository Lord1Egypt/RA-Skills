## Description: <br>
OpenOcean-skills is a skill package for interacting with the OpenOcean Aggregator API. Use it to get swap quotes, build swap transactions, execute swaps, and troubleshoot OpenOcean workflows across 40+ chains, including EVM, Solana, and Sui. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openocean-admin](https://clawhub.ai/user/openocean-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to quote, build, and optionally execute OpenOcean token swaps across supported EVM and non-EVM chains while troubleshooting API and transaction failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and execute irreversible token swaps, and the fast path can broadcast without a confirmation step. <br>
Mitigation: Prefer quote, build, and confirmed execution flows; reserve the fast path for trusted automation with small transaction limits, strict external controls, and accepted transaction risk. <br>
Risk: The security summary identifies unsafe shell command construction in the fast execution path. <br>
Mitigation: Fix the fast execution script to remove eval and validate transaction fields before use. <br>
Risk: The skill requires wallet access, RPC configuration, and transaction signing for execution flows. <br>
Mitigation: Protect wallet credentials, use hardware wallet or keystore flows where appropriate, verify chain and transaction fields, and test with small amounts before larger swaps. <br>


## Reference(s): <br>
- [OpenOcean homepage](https://openocean.finance) <br>
- [OpenOcean Aggregator API](https://apis.openocean.finance/) <br>
- [OpenOcean Swap API v4](https://apis.openocean.finance/developer/apis/swap-api/api-v4) <br>
- [Foundry](https://getfoundry.sh/) <br>
- [OpenOcean API reference](references/api-reference.md) <br>
- [OpenOcean token registry](references/token-registry.md) <br>
- [Basic quote example](skills/quote/references/basic-quote.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with structured JSON blocks and Foundry cast commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction calldata, router addresses, gas estimates, slippage settings, transaction hashes, and wallet execution guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
