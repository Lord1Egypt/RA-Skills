## Description: <br>
Shopify operations and diagnostics skill that retrieves store domains and tokens from Supabase, audits themes, products, checkout, and metrics, and can publish a blog post only with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TaceyWong](https://clawhub.ai/user/TaceyWong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Shopify operators use this skill to inspect store data, run store health diagnostics, check checkout and metrics behavior, and publish marketing blog content when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Shopify credentials, locally cached tokens, and order data. <br>
Mitigation: Install only when the separate icosmos-shopify CLI and its Supabase account are trusted; confirm token cache location, deletion steps, and Shopify Admin API scopes before setup. <br>
Risk: The skill can publish Shopify blog articles when --confirm is provided. <br>
Mitigation: Review the target store, blog ID, title, and article body before using --confirm; otherwise keep the command in dry-run behavior. <br>
Risk: The security review notes insufficient detail about token scoping and sensitive data handling in the artifact. <br>
Mitigation: Review the security guidance before installation and avoid exposing order fields, credentials, or token values in shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TaceyWong/icosmos-space) <br>
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest) <br>
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest) <br>
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics by default; Shopify blog publishing requires explicit --confirm.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
