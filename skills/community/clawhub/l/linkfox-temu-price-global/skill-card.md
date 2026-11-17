## Description:

Temu全球站-定价 helps agents use LinkFox-mediated Temu Global pricing APIs for price orders, recommended prices, SKU supplier-price queries, and batch supplier-price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to query Temu Global pricing data, estimate or retrieve recommended supplier prices, inspect SKU supplier prices, and perform controlled supplier-price updates through LinkFox gateway scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags broad proxy, download, billing, and credential-storage powers around real seller credentials.

Mitigation: Use only in trusted environments, review the skill before installation, restrict access to credentials and token stores, and avoid exposing raw token values.

Risk: The skill can submit batch supplier-price changes and other actions that may affect seller operations.

Mitigation: Require explicit human confirmation and parameter review before price changes, billing/order actions, or repeated cost-incurring operations.

Risk: Gateway configuration and API keys control access to LinkFox-mediated Temu actions.

Mitigation: Verify gateway environment variables, scope API keys appropriately, and remove or rotate credentials when access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-price-global)
- [API reference](references/api.md)
- [Temu accessToken authorization](references/access-token.md)
- [Authorization flow](references/authorization-flow.md)
- [Onboarding and billing troubleshooting](references/onboarding.md)
- [Partner Global price catalog](references/partner-global-catalog.md)
- [Price API document index](references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a)
- [Temu Global OpenAPI router](https://openapi-b-global.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and saved JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may print small JSON responses directly, summarize larger responses, and save full API responses under a linkfox output directory.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
