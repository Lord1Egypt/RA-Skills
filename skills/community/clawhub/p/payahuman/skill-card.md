## Description:

Pay a Human helps OpenClaw agents send Talentir payouts to creators by email or social media handle, retrieve payout and team information, and manage payout webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johanneskares](https://clawhub.ai/user/johanneskares)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to initiate and track Talentir creator payouts, inspect team details, and administer payout webhooks from an agent shell environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate high-impact payment actions and webhook changes through Talentir.

Mitigation: Require human confirmation for every recipient, amount, currency, and webhook target URL before executing commands.

Risk: The Talentir API key and returned webhook signing secrets are sensitive credentials.

Mitigation: Use a least-privilege API key, avoid unnecessary payout approval or webhook administration permissions, and store returned signing secrets securely.

## Reference(s):

- [Pay a Human on ClawHub](https://clawhub.ai/johanneskares/skills/payahuman)
- [Talentir API](https://www.talentir.com/api/v1)
- [Talentir Business Signup](https://www.talentir.com/start/business)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TALENTIR_API_KEY; payout requests may create financial transactions and webhook changes through Talentir.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
