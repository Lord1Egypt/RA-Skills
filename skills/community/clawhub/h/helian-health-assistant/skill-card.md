## Description:

Helian Health Assistant guides users through health-check appointment booking, including hospital and package selection, identity and login steps, order creation, and payment through Helian Health and LianLian Pay services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuwang412](https://clawhub.ai/user/xuwang412)

### License/Terms of Use:

MIT-0

## Use Case:

External consumers use this agent to find health-check providers, compare packages and appointment slots, enter patient details, create a booking order, and complete payment. Developers can deploy it on supported agent platforms such as OpenClaw and Qoder for chat-based booking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle highly sensitive health, identity, authentication, and payment data, and security evidence reports that it may store patient, identity, and bank-card details in hidden plaintext files.

Mitigation: Do not use with real patient or bank-card data until local storage is removed or replaced with encrypted, consented, minimal-retention storage.

Risk: Security evidence reports that payment secrets may be printed in logs.

Mitigation: Redact payment credentials, tokens, bank-card details, and session identifiers from all user-visible output and logs before production use.

Risk: The security verdict is suspicious because the skill can book appointments and process payments.

Mitigation: Require human review before installation, limit deployment to approved environments, and verify each booking and payment action with the user before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuwang412/skills/helian-health-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown/plain text with tables, prompts, API-backed booking results, payment links, and setup snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health-check package details, appointment availability, login prompts, order status, and payment status]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
