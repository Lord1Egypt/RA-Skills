## Description: <br>
Provides real-time cross-asset price, volume, and spread snapshots across Kraken, Coinbase Advanced Trade, and Hyperliquid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch a paid real-time crypto market snapshot for dashboards, portfolio monitoring, and spread or volume checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent needs access to an EVM wallet private key to authorize paid market-data calls. <br>
Mitigation: Use a dedicated low-balance wallet and keep the private key out of chat, prompts, and logs. <br>
Risk: Repeated automatic calls can spend USDC. <br>
Mitigation: Confirm expected call volume before enabling the skill and monitor wallet spending. <br>


## Reference(s): <br>
- [Market Tick signal](https://apexrunner.ai/signals/market-tick) <br>
- [Market Tick pricing](https://apexrunner.ai/signals/my-pricing) <br>
- [BTC Price Tick signal](https://apexrunner.ai/signals/btc-price-tick) <br>
- [APEX Pulse signal](https://apexrunner.ai/signals/apex-pulse) <br>
- [Volume Analysis signal](https://apexrunner.ai/signals/volume-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON market-data snapshot with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM wallet private key for x402 payment authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
