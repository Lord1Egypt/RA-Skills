## Description: <br>
Aggregate liquidation pressure score across tracked perpetuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query a paid real-time crypto market signal before entering leveraged positions or monitoring systemic perpetual-futures risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize per-call x402 payments. <br>
Mitigation: Use a dedicated low-balance wallet, monitor charges, and avoid reusing a private key that controls important funds. <br>
Risk: The signal is paid at request time and may incur repeated charges during automated agent runs. <br>
Mitigation: Add call limits or human approval around automated invocations when integrating this skill into trading workflows. <br>


## Reference(s): <br>
- [Liquidation Pressure Signal](https://apexrunner.ai/signals/liquidation-pressure) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>
- [Liquidation Magnet Signal](https://apexrunner.ai/signals/liquidation-magnet) <br>
- [Crowded Trade Detector Signal](https://apexrunner.ai/signals/crowded-trade-detector) <br>
- [OI Divergence Signal](https://apexrunner.ai/signals/oi-divergence) <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/liquidation-pressure) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, JSON] <br>
**Output Format:** [Markdown with Python code blocks and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses x402 payment authorization with EVM_PRIVATE_KEY; signal responses include pressure_score, at_risk_usd, and level.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
