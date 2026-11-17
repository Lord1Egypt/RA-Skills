## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns AI-synthesised market narrative with directional bias score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents that consume paid crypto market signals use this skill to retrieve an AI-synthesized market narrative and directional bias as context for market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example signs paid x402 requests with an EVM private key, so a misconfigured request or exposed key could authorize unintended payments.

Mitigation: Keep the key in a secret store, use a wallet funded only for intended calls, and retain the x402 max_amount cap.

## Reference(s):

- [Narrative Intelligence signal endpoint](https://apexrunner.ai/signals/narrative-intelligence)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/narrative-intelligence)
- [Whale Sentiment signal](https://apexrunner.ai/signals/whale-sentiment)
- [Regime signal](https://apexrunner.ai/signals/regime)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON market signal response with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 request on Base using USDC; requires an EVM wallet private key.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
