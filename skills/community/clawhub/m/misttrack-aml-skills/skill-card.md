## Description:

Cryptocurrency address risk analysis, AML compliance checks, and on-chain transaction tracing using the MistTrack OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misttrack](https://clawhub.ai/user/misttrack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance analysts, and wallet-agent operators use this skill to check cryptocurrency addresses and transactions for AML risk, labels, behavior, counterparties, and multisig properties before investigation or transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional x402 pay-per-use path can sign and broadcast on-chain USDC payments from a local private key.

Mitigation: Prefer MISTTRACK_API_KEY mode; if x402 is necessary, use a dedicated low-balance wallet, pass the key only through a permission-restricted key file, and verify the endpoint before payment.

Risk: Unattended payments can occur if an operator supplies a key file and enables automatic payment behavior.

Mitigation: Avoid --auto and auto_pay=True in production agent pipelines; require explicit review for each payment.

Risk: Harness-level controls such as disable_model_calls may not be enforced by every agent platform.

Mitigation: Treat platform controls as advisory unless verified, and enforce payment approval and key-handling policy outside the skill runtime.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/misttrack/skills/misttrack-aml-skills)
- [MistTrack](https://misttrack.io/)
- [MistTrack documentation](https://docs.misttrack.io/)
- [MistTrack OpenAPI overview](https://docs.misttrack.io/openapi/overview)
- [MistTrack dashboard](https://dashboard.misttrack.io)
- [x402 protocol documentation](https://docs.cdp.coinbase.com/x402/welcome)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON or CSV script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only API-key mode is preferred; optional x402 payment mode can sign and broadcast blockchain payments when a key file is supplied.]

## Skill Version(s):

0.2.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
