## Description: <br>
GoHighLevel Private Integration Token API integration with managed authentication for CRM, sales pipelines, calendars, conversations, payments, and marketing automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to connect an agent to Maton-managed GoHighLevel Private Integration Token connections, choose agency or sub-account scope, and prepare approved API requests for CRM, pipeline, calendar, conversation, payment, and workflow tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad CRM, customer, pipeline, calendar, conversation, payment, and workflow data through connected GoHighLevel accounts. <br>
Mitigation: Install only when Maton and the publisher are trusted, use least-privilege agency or sub-account tokens, and minimize sensitive reads. <br>
Risk: Using the wrong agency or sub-account connection can route requests to an unintended scope. <br>
Mitigation: Specify the intended Maton-Connection for each request and confirm whether the operation requires an agency token or a sub-account token. <br>
Risk: Create, update, and delete calls can change business records or remove data. <br>
Mitigation: Review the target resource and intended effect before approving every write or delete action. <br>
Risk: The MATON_API_KEY and GoHighLevel Private Integration Tokens grant sensitive account access. <br>
Mitigation: Keep credentials private, store them in environment variables or approved secret storage, and rotate or revoke them if exposed. <br>


## Reference(s): <br>
- [GoHighLevel API Documentation](https://highlevel.stoplight.io/docs/integrations/) <br>
- [GoHighLevel Marketplace Documentation](https://marketplace.gohighlevel.com/docs/) <br>
- [Private Integration Token Guide](https://marketplace.gohighlevel.com/docs/integrations/custom-token) <br>
- [GoHighLevel Skill on ClawHub](https://clawhub.ai/byungkyu/highlevel-api) <br>
- [Related API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON request and response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; write and delete operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
