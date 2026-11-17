## Description:

Helps agents manage Amazon Seller store authorization, including generating authorization links, listing authorized stores, checking authorization status, refreshing access tokens, and locally disconnecting store bindings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect Amazon Seller accounts to LinkFox, choose an authorized store, verify authorization health, and prepare sellerId plus region for downstream Amazon seller workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because it includes login, billing/payment, feedback reporting, sensitive local storage, and Amazon store authorization behavior.

Mitigation: Review the skill before installing, run only the intended authorization or store-management flow, and avoid onboarding or payment actions unless the user explicitly intends to use LinkFox account billing.

Risk: Gateway base URLs can be overridden with environment variables, which could send API keys or store authorization requests to an unintended endpoint.

Mitigation: Use trusted LinkFox endpoints and avoid custom gateway overrides unless the endpoint is controlled and expected.

Risk: API keys, seller identifiers, authorization status, and response files can be sensitive operational data.

Mitigation: Store API keys in a secret manager or protected environment, avoid exposing raw tokens, and clear local linkfox response files when they may contain store identifiers or authorization data.

Risk: Local disconnection only removes the current LinkFox member binding and does not revoke Amazon Seller Central authorization.

Mitigation: Tell users to revoke access in Amazon Seller Central when they need full OAuth authorization removal.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-auth)
- [API Reference](artifact/references/api.md)
- [Authorization Flow](artifact/references/authorization-flow.md)
- [Quick Start](artifact/references/quick-start.md)
- [Onboarding Guide](artifact/references/onboarding.md)
- [Script Usage Guide](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save complete JSON responses under a local linkfox session directory and summarize large responses; token-status helpers remove raw access and refresh tokens before display.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
