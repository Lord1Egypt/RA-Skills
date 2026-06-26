## Description: <br>
Audits Shopify store operations by syncing store domains and tokens from Supabase, diagnosing theme, product, checkout, and metrics issues, and publishing Shopify blog posts only with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TaceyWong](https://clawhub.ai/user/TaceyWong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Shopify operators and agent users use this skill to inspect store setup, products, checkout behavior, metrics, and content workflows, while keeping normal diagnostics read-only. Blog publishing is the only write operation and requires explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an unreviewed local CLI that handles account credentials, cached store tokens, and order data. <br>
Mitigation: Install only after trusting the publisher, verify the icosmos-shopify CLI separately, use least-privilege Shopify permissions, and confirm where tokens are cached and how to revoke them. <br>
Risk: Broad order retrieval can expose sensitive customer data. <br>
Mitigation: Avoid broad order exports, prefer narrow time windows, and rely on the documented behavior that sensitive fields are masked or omitted before sharing output. <br>
Risk: The blog publishing workflow can make public content changes to a Shopify store. <br>
Mitigation: Manually review the target store, blog ID, title, and body before using --confirm; without --confirm, the documented behavior is dry-run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TaceyWong/icosmos-shop) <br>
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest) <br>
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest) <br>
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics by default; blog publishing requires explicit --confirm. Sensitive token and order fields are expected to be masked or omitted.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
