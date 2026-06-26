## Description: <br>
Audit, plan, and safely optimize Shopify image alt text for product media, collection featured images, article featured images, and article inline images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvsao](https://clawhub.ai/user/lvsao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Shopify merchants and operators use this skill to inventory image alt text, generate concise improvement candidates, review proposed changes in batches, and apply approved Shopify Admin updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a global self-update before each run, which can change installed agent instructions before the user reviews the active version. <br>
Mitigation: Verify the installed version and helper files before granting Shopify credentials or approving write actions. <br>
Risk: The workflow requires sensitive Shopify credentials and can write alt text through Shopify Admin APIs. <br>
Mitigation: Use least-privilege Shopify access, never expose tokens in public files, preview proposed changes, and execute writes only after explicit approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvsao/optimize-shopify-alt-text) <br>
- [Shopify Admin GraphQL products query](https://shopify.dev/docs/api/admin-graphql/latest/queries/products) <br>
- [Shopify Admin GraphQL files query](https://shopify.dev/docs/api/admin-graphql/latest/queries/files) <br>
- [Shopify Admin GraphQL fileUpdate mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fileUpdate) <br>
- [Shopify Admin GraphQL collectionUpdate mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/collectionUpdate) <br>
- [Shopify Admin GraphQL articles query](https://shopify.dev/docs/api/admin-graphql/latest/queries/articles) <br>
- [Shopify Admin GraphQL articleUpdate mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleUpdate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with command snippets and JSON apply plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable alt text candidates and applies changes only after explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
