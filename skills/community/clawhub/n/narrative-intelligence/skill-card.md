## Description: <br>
AI-synthesised market narrative with directional bias score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to request a paid APEX Runner market narrative signal for macro context, directional bias, and narrative momentum checks before crypto trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet on Base with only the funds intended for signal purchases. <br>
Risk: Repeated invocations can incur per-call payment charges. <br>
Mitigation: Confirm the current per-call price and pricing tier before invoking the skill repeatedly. <br>
Risk: The signal provides crypto-market context that may be incomplete or unsuitable as sole trading guidance. <br>
Mitigation: Review the JSON response alongside independent risk controls before using it in trading workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/narrative-intelligence) <br>
- [APEX Runner Narrative Intelligence Signal](https://apexrunner.ai/signals/narrative-intelligence) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>
- [Related APEX Runner AI Narrative Signal](https://apexrunner.ai/signals/ai-narrative) <br>
- [Related APEX Runner Whale Sentiment Signal](https://apexrunner.ai/signals/whale-sentiment) <br>
- [Related APEX Runner Regime Signal](https://apexrunner.ai/signals/regime) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON response containing narrative, sentiment, confidence, timing, and market-context fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM private key for x402 payment authorization and may incur a per-call charge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
