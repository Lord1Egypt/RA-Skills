## Description: <br>
Manage PerfexCRM from messaging apps with conversational CRUD access for customers, invoices, leads, tickets, projects, contracts, and other CRM resources through the PerfexCRM API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostasmm](https://clawhub.ai/user/kostasmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to let an agent retrieve, summarize, create, update, and delete PerfexCRM records through API calls from conversational channels such as WhatsApp, Telegram, Slack, or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad read and write access to sensitive CRM, customer, staff, and financial records. <br>
Mitigation: Use a dedicated least-privilege PerfexCRM API key, limit write and delete permissions to required resources, and start in a sandbox environment. <br>
Risk: Create, update, delete, ticket-reply, payment, staff, or customer-record actions can cause business-impacting changes. <br>
Mitigation: Require explicit human confirmation before executing those actions and review generated requests before sending them. <br>
Risk: Long-lived API keys can expose CRM data if leaked or over-scoped. <br>
Mitigation: Store keys as environment variables or managed secrets, rotate them regularly, and revoke keys that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kostasmm/perfexcrm-api) <br>
- [PerfexAPI homepage](https://perfexapi.com) <br>
- [PerfexAPI documentation](https://perfexapi.com/docs) <br>
- [PerfexCRM API and Webhooks module repository](https://github.com/sattip/perfexcrm-api-webhooks-module) <br>
- [PerfexAPI changelog](https://perfexapi.com/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PERFEXCRM_API_URL and PERFEXCRM_API_KEY; recommends pagination, response filtering, search-first access, and confirmation before destructive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
