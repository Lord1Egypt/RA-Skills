## Description:

Helps agents query Amazon SP-API Catalog Items through LinkFox by ASIN, keyword, identifier, or category to retrieve product details, summaries, images, and included catalog data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to look up Amazon catalog items for a selected seller account, region, and marketplace. It supports catalog research and store workflows that need item details, category nodes, summaries, images, or selected includedData fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account login, API-key creation, and billing recovery flows may expose SMS codes or API keys in shared environments.

Mitigation: Use a private terminal, avoid entering SMS codes in shared sessions, and do not persist API keys in shell profiles on shared machines.

Risk: Billing and order flows can present payment QR codes or payment URLs.

Mitigation: Verify the plan, amount, order identifier, and payment method before scanning a QR code or opening a payment URL.

Risk: Full catalog responses are stored locally under the workspace linkfox session directory.

Mitigation: Review the saved-file location before use and retain or delete response files according to the user's data-handling policy.

Risk: Repeated invalid or high-frequency SP-API calls can trigger temporary store-protection cooldowns.

Mitigation: Stop automatic retries on 400, 403, 404, or 429 style failures, follow retryAfter or blockedUntil when present, and correct parameters or authorization before retrying.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-catalog)
- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Amazon SP-API listCatalogCategories](https://developer-docs.amazon.com/sp-api/reference/listcatalogcategories)
- [Amazon SP-API searchCatalogItems](https://developer-docs.amazon.com/sp-api/reference/searchcatalogitems)
- [Amazon SP-API getCatalogItem](https://developer-docs.amazon.com/sp-api/reference/getcatalogitem)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses saved to local files, with stdout summaries for large responses and full inline JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are written under the current workspace linkfox session directory; the skill can also provide setup commands for LinkFox API-key configuration.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
