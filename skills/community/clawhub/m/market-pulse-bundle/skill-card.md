## Description: <br>
Provides real-time bundled market data: price tick, Fear & Greed index, and market regime for BTC in a single authenticated API call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to request a compact BTC market snapshot at the start of trading or decision workflows. The skill is intended for agents that can make paid x402-authenticated GET requests with a Base/USDC wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to use a spend-capable crypto private key for paid x402 requests without clear spending safeguards. <br>
Mitigation: Use a dedicated low-balance Base/USDC wallet, keep the private key out of logs and code, monitor charges, and avoid using a primary wallet or wallet with unrelated funds. <br>


## Reference(s): <br>
- [ClawHub Market Pulse Bundle](https://clawhub.ai/kynto2001-ctrl/skills/market-pulse-bundle) <br>
- [APEX Runner Market Pulse Bundle](https://apexrunner.ai/signals/market-pulse-bundle) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON data, Guidance] <br>
**Output Format:** [JSON API response with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and a funded Base/USDC wallet for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
