## Description: <br>
Google Merchant Center API integration with managed OAuth for reading, creating, updating, and deleting products, inventories, data sources, promotions, account settings, conversions, and reports in Google Shopping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to administer Google Merchant Center resources through Maton-managed OAuth. It supports Merchant Center catalog, inventory, promotion, account, reporting, notification, and conversion workflows, including write operations that require explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real changes to Merchant Center products, inventories, promotions, data sources, account settings, conversions, connections, and webhook subscriptions. <br>
Mitigation: Require explicit user approval with specific resource identifiers before any create, update, or delete operation. <br>
Risk: A request may target the wrong Merchant Center account or OAuth connection when multiple connections exist. <br>
Mitigation: Verify the account ID and Maton connection before changes, and include the intended Maton-Connection header when selecting a connection. <br>
Risk: MATON_API_KEY is a sensitive credential that can authorize access through Maton. <br>
Mitigation: Keep the key in an environment variable, avoid logging or sharing it, rotate it if exposed, and revoke unused Google Merchant connections. <br>
Risk: Merchant Center writes can affect live Google Shopping listings and business operations. <br>
Mitigation: Default to read-only checks first, retrieve the target resource for review, summarize the intended effect, and use least-privilege Google access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/google-merchant) <br>
- [Merchant API Overview](https://developers.google.com/merchant/api/overview) <br>
- [Merchant API Reference](https://developers.google.com/merchant/api/reference/rest) <br>
- [Products Guide](https://developers.google.com/merchant/api/guides/products/overview) <br>
- [Data Sources Guide](https://developers.google.com/merchant/api/guides/datasources) <br>
- [Reports Guide](https://developers.google.com/merchant/api/guides/reports) <br>
- [Product Data Specification](https://support.google.com/merchants/answer/7052112) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request examples and operational guidance; actual API responses depend on the user's Maton key, OAuth connection, Merchant Center account, and Google Merchant API permissions.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
