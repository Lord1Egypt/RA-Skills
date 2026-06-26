## Description: <br>
HubSpot CRM API integration with managed OAuth for contacts, companies, deals, pipelines, tickets, products, line items, marketing emails, and workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, support, and operations teams use this skill to inspect and manage HubSpot CRM data through agent-mediated HubSpot API calls. It supports read workflows plus confirmed write workflows for records such as contacts, companies, deals, tickets, campaigns, workflows, properties, quotes, tasks, notes, imports, and associations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access and sensitive credentials for a connected HubSpot account. <br>
Mitigation: Install only when the publisher and displayed files are trusted, and verify that the requested account access matches the intended HubSpot workflow. <br>
Risk: The skill can create, update, archive, delete, import, and associate HubSpot CRM records. <br>
Mitigation: Preview and explicitly confirm write or destructive operations before execution, especially batch, delete, archive, GDPR deletion, and workflow actions. <br>
Risk: HubSpot actions operate within the permissions of the connected user account. <br>
Mitigation: Use a HubSpot account with the minimum permissions needed for the task and review high-impact changes before approving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/hubspot-ops) <br>
- [HubSpot API Documentation](https://developers.hubspot.com/docs/overview) <br>
- [HubSpot CRM Contacts API Reference](https://developers.hubspot.com/docs/api/crm/contacts) <br>
- [HubSpot CRM Deals API Reference](https://developers.hubspot.com/docs/api/crm/deals) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected HubSpot account through ClawLink OAuth; write operations should be previewed and explicitly confirmed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
