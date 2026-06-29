## Description: <br>
Live ATR-based position sizing recommendation for current volatility <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to request live ATR-based position sizing before opening positions and to apply consistent risk-per-trade guidance across supported crypto markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize paid wallet requests from an EVM wallet. <br>
Mitigation: Use a dedicated EVM wallet with limited USDC, verify the apexrunner.ai endpoint and current pricing before use, and avoid wallets that hold unrelated funds. <br>
Risk: Live position sizing recommendations may not match a user's account constraints, market conditions, or risk limits. <br>
Mitigation: Review the JSON output before use, compare it with independent risk rules, and avoid connecting the recommendation directly to unattended trade execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/live-atr-sizing) <br>
- [Live ATR Sizing Signal](https://apexrunner.ai/signals/live-atr-sizing) <br>
- [APEX Runner Pricing Tiers](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, JSON] <br>
**Output Format:** [Markdown guidance with Python example code and JSON API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 wallet authorization; the signal endpoint charges per call.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
