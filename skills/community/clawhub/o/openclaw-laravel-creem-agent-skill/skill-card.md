## Description:

Creem payment store assistant that forwards store, payment, customer, transaction, product, heartbeat, checkout, and subscription requests to a local Laravel HTTP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romansh](https://clawhub.ai/user/romansh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw assistant to a local Laravel Creem Agent service for payment-store status, transactions, customers, subscriptions, products, monitoring checks, checkout creation, and subscription cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is documented as being embedded in a shell curl command for local HTTP calls.

Mitigation: Use a structured HTTP client or safely serialized JSON payload so user text cannot be interpreted as shell syntax.

Risk: Broad activation phrases may route unrelated status or payment-like prompts to the payment-store endpoint.

Mitigation: Narrow activation language to store-specific prompts and verify ambiguous prompts before calling the endpoint.

Risk: The skill can initiate state-changing payment actions such as checkout creation and subscription cancellation.

Mitigation: Require explicit user confirmation and exact resource identifiers before checkout creation or subscription cancellation.

Risk: The skill is intended for a local payment-store environment and depends on a trusted local Laravel service.

Mitigation: Install only in a trusted local demo or controlled payment-store environment with the Laravel endpoint running on the same machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romansh/skills/openclaw-laravel-creem-agent-skill)
- [Publisher profile](https://clawhub.ai/user/romansh)
- [Project homepage](https://github.com/nicepkg/laravel-creem-agent)
- [OpenClaw Telegram channel documentation](https://docs.openclaw.ai/channels/telegram)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text or Markdown relayed from a local JSON HTTP response, with shell command guidance for setup and verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For single endpoint calls, the skill relays the response field verbatim; for multi-step store questions, it may combine sequential endpoint responses into one concise answer.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
