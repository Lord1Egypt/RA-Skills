## Description: <br>
Mailgun API integration with managed OAuth for sending, receiving, tracking, and managing email resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Mailgun through Maton-managed OAuth for sending messages and managing domains, routes, templates, mailing lists, suppressions, events, tracking settings, webhooks, and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and change Mailgun routing, webhook, tracking, and credential settings when given access. <br>
Mitigation: Confirm the exact domain, recipient, route destination, webhook URL, tracking setting, or credential change before approving any write operation. <br>
Risk: The MATON_API_KEY grants access through Maton to the connected Mailgun account. <br>
Mitigation: Install only when Maton is trusted for this account, store the key as a protected secret, and use the intended Maton connection when multiple connections exist. <br>


## Reference(s): <br>
- [ClawHub Mailgun Skill](https://clawhub.ai/byungkyu/mailgun-api) <br>
- [Maton](https://maton.ai) <br>
- [Mailgun API Documentation](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview) <br>
- [Mailgun API Reference](https://mailgun-docs.redoc.ly/docs/mailgun/api-reference/intro/) <br>
- [Mailgun Postman Collection](https://www.postman.com/mailgun/mailgun-s-public-workspace/documentation/ik8dl61/mailgun-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and a valid MATON_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
