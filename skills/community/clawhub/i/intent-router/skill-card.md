## Description:

Classify text into custom intents with confidence scoring and entity extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daisuke134](https://clawhub.ai/user/daisuke134)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to classify messages against a custom intent list for routing, NLU workflows, and multi-agent orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends message text to an external service with limited privacy and safety guidance.

Mitigation: Use only text that is appropriate to share with the listed service, and avoid secrets, sensitive personal data, and regulated data.

Risk: The skill asks users to install and authenticate a global third-party payment CLI.

Mitigation: Confirm the npm package publisher, version, payment destination, amount, and token storage or revocation behavior before authenticating or paying; consider using an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daisuke134/skills/intent-router)
- [intent-router x402 endpoint](https://anicca-proxy-production.up.railway.app/api/x402/intent-router)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object with intent, confidence, reasoning, secondary intent, entities, and detected language fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input text is limited to 2000 characters, context is limited to 500 characters, and candidate intents are limited to 2-20 items.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
