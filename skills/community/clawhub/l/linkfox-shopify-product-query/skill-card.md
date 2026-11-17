## Description:

Shopify商品查询 helps agents search and filter Shopify products by keyword or URL, price, weekly sales, listing date, Facebook ads, competition, supplier availability, and shipping country.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to research Shopify products for independent-store selection, dropshipping analysis, and competitive product comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox account login, API key generation, paid-plan ordering, and payment QR creation in addition to Shopify product lookup.

Mitigation: Require explicit user confirmation before login, API-key generation, package purchase, or payment QR creation.

Risk: API keys, SMS codes, and LINKFOX_* environment variables can expose account or billing access if entered into retained logs or untrusted environments.

Mitigation: Use trusted environments, avoid untrusted LINKFOX_* variables, do not paste secrets into retained transcripts, and prefer secure credential storage.

Risk: Product-query responses and cached results may be stored in local workspace files.

Mitigation: Run the skill in a trusted workspace and review or remove local linkfox output files when search results contain sensitive business research.

## Reference(s):

- [Shopify Product Query API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopify-product-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON command outputs and local JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product-query responses may be summarized for large result sets while the full JSON response is written locally.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
