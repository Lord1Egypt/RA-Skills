## Description: <br>
Gumroad API integration with managed OAuth for accessing products, sales, subscribers, licenses, and webhooks for a digital storefront. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, storefront operators, and support teams use this skill to inspect and manage Gumroad storefront data, verify licenses, review sales and subscribers, and configure webhooks through a Maton-managed OAuth connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key and Gumroad OAuth connection can expose sensitive storefront data and account access. <br>
Mitigation: Keep MATON_API_KEY private, use only the intended Gumroad connection, and revoke or rotate credentials if they may have been exposed. <br>
Risk: Write operations can modify or delete products, offer codes, licenses, variants, custom fields, and webhooks. <br>
Mitigation: Before allowing create, update, disable, enable, decrement, or delete actions, confirm the exact target resource and intended effect with the user. <br>
Risk: When multiple Gumroad connections exist, requests can be sent to the wrong storefront. <br>
Mitigation: Set the Maton-Connection header for the intended connection whenever more than one Gumroad account is connected. <br>


## Reference(s): <br>
- [Gumroad API Overview](https://gumroad.com/api) <br>
- [Gumroad Create API Application](https://help.gumroad.com/article/280-create-application-api) <br>
- [Gumroad License Keys Help](https://help.gumroad.com/article/76-license-keys) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/gumroad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, shell command snippets, HTTP endpoints, and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Gumroad OAuth connection.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
