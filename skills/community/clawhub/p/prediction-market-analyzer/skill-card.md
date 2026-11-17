## Description:

Analyzes Polymarket and Kalshi prediction-market links or event identifiers and returns a localized security and liquidity risk brief from a third-party risk API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goplusbot](https://clawhub.ai/user/goplusbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess prediction-market events for liquidity, contract, and rule-related risks before acting on Polymarket or Kalshi market information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is flagged for review because it force-activates on supported market mentions and sends market identifiers to a third-party API.

Mitigation: Require explicit user confirmation before lookup and disclose the API recipient and fields sent.

Risk: The artifact includes behavior that disables HTTPS certificate and hostname verification for API calls.

Mitigation: Restore normal HTTPS verification before deployment.

Risk: Silent failure behavior can hide lookup failures during implicit triggers.

Mitigation: Remove silent failure handling or clearly report lookup status when a risk assessment is expected.

Risk: Market identifiers are interpolated into request URLs.

Mitigation: Validate and URL-encode identifiers before making requests.

## Reference(s):

- [Technical Specifications](references/technical_specs.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/goplusbot/skills/prediction-market-analyzer)
- [External Risk API](https://api.secwarex.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Localized Markdown risk brief with optional JSON-derived labels and risk levels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a Python script or direct HTTP request to retrieve third-party risk data for a parsed market identifier.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
