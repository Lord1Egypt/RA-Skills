## Description: <br>
Queries EHunt Shopify store data through LinkFox to filter independent Shopify stores by store name or domain, country, store age, product count, ad count, monthly visits, monthly orders, and social follower metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find and compare Shopify stores and competitors by commercial signals such as traffic, orders, ads, products, country, and social presence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends Shopify search and filter terms to LinkFox. <br>
Mitigation: Use only in environments where sharing those query terms with LinkFox is acceptable and keep the API key in an environment variable rather than committed files. <br>
Risk: Large-response helper files may contain business-sensitive data or contact information. <br>
Mitigation: Write persisted responses to a temporary directory outside a git working tree, avoid committing them, and delete them after use. <br>


## Reference(s): <br>
- [EHunt Shopify Store Query API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-shopify-store-query) <br>
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist large API responses to local files and project selected fields for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
