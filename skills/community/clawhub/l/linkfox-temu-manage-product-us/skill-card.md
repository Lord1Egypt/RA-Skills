## Description:

Provides LinkFox-gatewayed Temu US Manage Product API guidance and scripts for product lookup, SKU queries, listing edits, deletion, inventory changes, sale and pre-sale status, category checks, property templates, compliance edits, external identifiers, and video cover retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace operators use this skill to work with Temu US Partner Manage Product APIs through LinkFox, including reading product data and preparing controlled product, inventory, listing-status, and compliance changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform store-changing Temu product operations, including product deletion, inventory edits, sale-status changes, pre-sale status changes, and compliance edits.

Mitigation: Use only with accounts where those actions are acceptable and require explicit human confirmation before running commands that delete products or change stock, listing status, pre-sale settings, or compliance data.

Risk: Credential handling and local token persistence require care because the skill uses LinkFox API keys and Temu access tokens or store keys.

Mitigation: Avoid storing or printing raw tokens, restrict local token-store access, and prefer masked token listing when inspecting saved stores.

Risk: Gateway endpoint override environment variables could redirect requests away from the intended LinkFox gateway.

Mitigation: Avoid setting gateway override environment variables unless the target endpoint is explicitly trusted and reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-manage-product-us)
- [API reference](references/api.md)
- [Partner US Manage Product catalog](references/partner-us-catalog.md)
- [Per-interface API documentation](references/apis/README.md)
- [Temu accessToken authorization and storage](references/access-token.md)
- [Onboarding and account issues](references/onboarding.md)
- [Temu Partner US Manage Product documentation](https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, and saved JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under a local linkfox data directory and may print full or summarized JSON depending on response size and inline mode.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
