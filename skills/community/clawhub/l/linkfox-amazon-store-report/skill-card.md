## Description: <br>
Amazon Store Report helps agents request, poll, download, and decompress Amazon Seller and Vendor reports such as inventory, orders, sales traffic, FBA, finance, and Brand Analytics reports through an authorized LinkFox Amazon store connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, vendors, and agents use this skill to retrieve structured Amazon store reports for inventory, orders, sales, traffic, FBA, finance, returns, and Brand Analytics workflows after store authorization is handled by the dependency skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive seller, business, and customer report data. <br>
Mitigation: Confirm the seller, marketplace, date range, and report type before execution, and keep API keys, OAuth tokens, and report contents out of chats and logs. <br>
Risk: Downloaded reports may be exposed through the default short-lived localhost file server or left in temporary storage. <br>
Mitigation: Disable local HTTP serving for sensitive reports when possible, share only local paths with intended users, and delete temporary report files after use. <br>
Risk: Automatic feedback submissions could include private business or customer details if copied into feedback content. <br>
Mitigation: Review feedback content before submission and remove seller identifiers, customer data, credentials, and private report values. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-report) <br>
- [API Reference](references/api.md) <br>
- [Report Types](references/report-types.md) <br>
- [Report Request Schemas](references/report-requests/README.md) <br>
- [Amazon SP-API Report Type Values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) <br>
- [Amazon Selling Partner API Report Schemas](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report files, file URIs, and optional short-lived localhost download links for extracted report data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
