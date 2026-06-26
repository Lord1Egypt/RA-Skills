## Description: <br>
OpenDexter helps agents search, price-check, and pay for x402 APIs across Solana and EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[branchmanager69](https://clawhub.ai/user/branchmanager69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use OpenDexter to discover paid x402 marketplace APIs, preview prices, check wallet setup, and make authorized USDC API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 API calls can spend USDC from a configured wallet. <br>
Mitigation: Review the endpoint, price, chain, and wallet setup before any paid fetch; prefer a dedicated low-balance wallet or strict per-call spending limit. <br>
Risk: Marketplace endpoint quality and reliability can vary. <br>
Mitigation: Prefer verified endpoints and review quality score, seller, price, network, and call count before calling an endpoint. <br>


## Reference(s): <br>
- [OpenDexter ClawHub listing](https://clawhub.ai/branchmanager69/opendexter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown or structured tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include marketplace search results, x402 prices, chain options, wallet status, API response data, and payment receipts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
