## Description:

Fetch product info by payment link ID. Calls GStable API to get payment link details, returns product name, description, price, and supported payment tokens. Ideal for AI assistants parsing payment links and displaying product information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankscar](https://clawhub.ai/user/tankscar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through an AI assistant to inspect GStable payment links before payment. The skill accepts a link ID or payment URL, fetches product details, and helps the agent summarize products, prices, supported tokens, and networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment link IDs or full payment URLs are sent to the configured GStable API host.

Mitigation: Use the default GStable API host or a trusted GSTABLE_API_BASE_URL value, and avoid submitting links that should not be shared with that service.

Risk: The skill uses npm dependencies and has routine supply-chain exposure.

Mitigation: Run npm install from the skill directory, keep dependencies updated, and review dependency changes before deployment.

Risk: Direct npx shebang execution can depend on the local npm resolution environment.

Mitigation: Prefer npm run get-link after installation unless the npm resolution environment is trusted.

## Reference(s):

- [GStable Get Payment Link API documentation](https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/)
- [Payment Link Reader on ClawHub](https://clawhub.ai/tankscar/skills/payment-link-reader)

## Skill Output:

**Output Type(s):** [JSON, text, shell commands, guidance]

**Output Format:** [JSON from the payment-link lookup command, with guidance for a concise natural-language summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm install; GSTABLE_API_BASE_URL can override the default GStable API host.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
