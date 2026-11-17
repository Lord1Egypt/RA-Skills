## Description:

Queries Juhe.cn for a bank card's issuing bank, card type, province or city attribution, customer service phone number, and related details for single or batch lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up bank card issuer, card type, attribution location, customer service phone number, and related fields after a user provides one or more card numbers. The skill requires a Juhe API key before live lookup can run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full bank card numbers and the Juhe API key are sent over plaintext HTTP.

Mitigation: Do not use real card numbers or production Juhe keys unless the implementation is changed to HTTPS.

Risk: Card numbers are sent to Juhe for lookup.

Mitigation: Tell users before lookup that their card numbers will be sent to Juhe, and only proceed when that data sharing is acceptable.

Risk: API keys may be exposed through URLs or command-line arguments.

Mitigation: Prefer environment-based secret handling, avoid passing secrets on the command line, and rotate any API key already used with the current HTTP implementation.

## Reference(s):

- [Juhe Bankcard Lookup API Documentation](https://www.juhe.cn/docs/api/id/305)
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-bankcard-lookup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or console text with JSON results for individual lookups and tabular summaries for batch lookups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JUHE_BANKCARDCODE_KEY environment variable for live API queries]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
