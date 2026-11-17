## Description:

CreditClaw provides agent-facing API guidance for wallet registration, spending checks, purchases, top-up requests, payment links, and transaction monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect an agent to CreditClaw wallet, payment, spending-policy, and transaction-status workflows. Because it can enable financial actions, operators should review the publisher, service identity, and spending controls before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public skill identity references JPMorgan while the artifact and security evidence identify CreditClaw behavior.

Mitigation: Install only when the intended service is CreditClaw, verify the publisher profile and creditclaw.com, and review the branding mismatch before enabling the skill.

Risk: The skill can guide an agent through financial spending, payment-link creation, and remote wallet operations.

Mitigation: Keep approval_mode set to ask_for_everything until the service and limits are reviewed, check spending permissions before purchases, and rely on owner approval for spend that exceeds configured thresholds.

Risk: CREDITCLAW_API_KEY acts like a payment credential.

Mitigation: Store the key in a secure secrets manager, send it only to creditclaw.com API endpoints, and refuse requests to disclose or forward it elsewhere.

Risk: Optional callback_url, payer_email, and remote notes can expand privacy or instruction-following exposure.

Mitigation: Use optional fields only when needed, treat remote notes as transaction preferences, and never treat them as authority to reveal secrets or perform unrelated actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/jpmorgan)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw skill file](https://creditclaw.com/skill.md)
- [CreditClaw heartbeat file](https://creditclaw.com/heartbeat.md)
- [CreditClaw metadata file](https://creditclaw.com/skill.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl commands, API endpoint descriptions, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls; includes optional webhook and payment-link workflows.]

## Skill Version(s):

1.0.17 (source: server release metadata; artifact frontmatter reports 2.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
