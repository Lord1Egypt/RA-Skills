## Description: <br>
Free Hedera analytics API for token prices, holder data, market caps, volume tracking, and CoinGecko bridge market lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to discover Hedera token analytics endpoints, issue public API calls, and build dashboards, alerts, research workflows, or trading-signal prototypes from live and historical token data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional ClawSwarm registration creates an external agent or wallet-related profile. <br>
Mitigation: Confirm the registration is intended and do not provide secrets, private keys, personal credentials, or wallet-sensitive data unless the service has been separately verified. <br>
Risk: The skill relies on public external crypto market-data APIs whose responses may change or be unavailable. <br>
Mitigation: Validate API responses before relying on them for dashboards, alerts, research, or trading-signal workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaflytok/hedera-data) <br>
- [onlyflies.buzz API base](https://onlyflies.buzz/api/v1) <br>
- [onlyflies.buzz Hedera analytics platform](https://onlyflies.buzz) <br>
- [ClawSwarm agent registration endpoint](https://onlyflies.buzz/clawswarm/api/v1/agents/register) <br>
- [CoinGecko bridge price endpoint](https://onlyflies.buzz/clawswarm/api/v1/coingecko/price/bitcoin,ethereum) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required for the documented public endpoints; optional ClawSwarm registration contacts an external service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
