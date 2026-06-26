## Description: <br>
Icosmos helps agents operate and diagnose Shopify stores through read-only audits, content queries, checkout checks, metric analysis, and explicitly confirmed Shopify blog publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TaceyWong](https://clawhub.ai/user/TaceyWong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and commerce teams use this skill to inspect Shopify store content, diagnose product, theme, checkout, and metrics issues, and publish marketing blog posts only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopify API tokens and related credentials are stored locally and should be treated as sensitive. <br>
Mitigation: Use a dedicated least-privilege Shopify token, confirm where local cache files are stored, delete exposed cache data, and rotate the token if the machine or cache may have been accessed. <br>
Risk: The skill includes one write-capable workflow for publishing Shopify blog posts. <br>
Mitigation: Keep publishing behind the documented --confirm flag and review the target store, blog, title, and body file before execution. <br>


## Reference(s): <br>
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest) <br>
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest) <br>
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON-oriented output conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics are the default; Shopify blog publishing requires an explicit --confirm flag.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
