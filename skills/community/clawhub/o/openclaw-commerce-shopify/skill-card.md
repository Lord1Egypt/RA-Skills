## Description: <br>
Shopify store management through OpenClaw Commerce API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevKrutik](https://clawhub.ai/user/DevKrutik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Shopify merchants and operators use this skill to manage store orders, products, customers, collections, catalogs, and discounts through OpenClaw Commerce. It can read and change live store data when supplied with a valid OpenClaw Commerce API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change live Shopify store data through an API key. <br>
Mitigation: Use a dedicated, revocable, least-privilege API key; test on a non-production store first; and review proposed create, update, delete, email, payment, discount, or bulk actions before confirming. <br>
Risk: Store operations may expose customer, order, billing, tax, or credential data. <br>
Mitigation: Avoid sending or logging unnecessary sensitive store data and keep API keys out of transcripts and persistent logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DevKrutik/openclaw-commerce-shopify) <br>
- [OpenClaw Commerce](https://openclawcommerce.com) <br>
- [OpenClaw Commerce API](https://app.openclawcommerce.com/api/v1) <br>
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and GraphQL request templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_COMMERCE_API_KEY for authenticated OpenClaw Commerce requests.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
