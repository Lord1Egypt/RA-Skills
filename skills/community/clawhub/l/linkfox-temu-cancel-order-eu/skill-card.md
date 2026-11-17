## Description:

Temu Europe cancellation skill for buyer after-sales cancellations and seller appeal or out-of-stock cancellation workflows through LinkFox and Temu Partner EU APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers and support operators use this skill to list buyer cancellation requests, agree to cancellations, submit seller cancellation appeals, submit out-of-stock cancellations, and check cancellation results for European site orders.

### Deployment Geography for Use:

Europe

## Known Risks and Mitigations:

Risk: The security review reports suspicious behavior because the skill combines Temu cancellation support with broader proxy, payment, and credential-storage behavior.

Mitigation: Install only if LinkFox is trusted and Temu cancellation through its gateway is required.

Risk: Endpoint override variables and broad proxy behavior can route requests outside the intended Temu EU cancellation workflow.

Mitigation: Avoid endpoint override environment variables and do not invoke arbitrary proxy types or non-EU sites.

Risk: LinkFox and Temu tokens may be exposed through shared workspaces, logs, or local token-store files.

Mitigation: Keep tokens out of shared workspaces and logs, and restrict permissions on LinkFox output and token-store files.

Risk: The onboarding flow can initiate payment or credit purchase actions.

Mitigation: Use payment and onboarding commands only when the user explicitly intends to buy LinkFox credits.

## Reference(s):

- [Skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-cancel-order-eu)
- [API reference](references/api.md)
- [Partner EU cancel order catalog](references/partner-eu-catalog.md)
- [API documentation index](references/apis/README.md)
- [Temu access token guide](references/access-token.md)
- [Authorization flow](references/authorization-flow.md)
- [Onboarding and billing guidance](references/onboarding.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9)
- [Temu EU OpenAPI router](https://openapi-b-eu.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, API calls, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses may be printed inline; larger responses are summarized after the full JSON response is saved.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
