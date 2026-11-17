## Description:

ipeaky helps OpenClaw users store, list, test, and delete API keys through local workflows that avoid exposing full key values in chat history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christiancattaneo](https://clawhub.ai/user/christiancattaneo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use ipeaky to collect API keys through a local macOS secure input flow, store them in OpenClaw configuration, list masked keys, test provider access, and delete keys when no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling may expose or mishandle secrets in some scripts.

Mitigation: Review the skill before installation and use only test or restricted API keys until command-line secret handling, AppleScript input sanitization, and plaintext backup handling are resolved.

Risk: Stripe paid-tier scripts add payment-flow behavior that may not be appropriate for every installation.

Mitigation: Separate, review, or disable the paid-tier scripts unless the Stripe integration is intentionally deployed.

Risk: Stored keys can become available to other OpenClaw skills that request the same environment variable.

Mitigation: Use scoped or restricted keys and verify which installed skills declare matching environment variables before relying on shared key injection.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [Stripe Dashboard Products](https://dashboard.stripe.com/products)
- [Stripe Checkout Sessions API](https://api.stripe.com/v1/checkout/sessions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and masked status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked key prefixes and provider test results; must not include full secret values.]

## Skill Version(s):

3.2.0 (source: clawhub.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
