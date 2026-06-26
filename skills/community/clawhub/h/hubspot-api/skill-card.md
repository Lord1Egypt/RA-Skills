## Description: <br>
HubSpot CRM API integration with managed OAuth for managing contacts, companies, deals, and associations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to work with HubSpot CRM through Maton-managed OAuth, including listing, searching, creating, updating, deleting, and associating CRM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY and uses Maton-managed OAuth for HubSpot access. <br>
Mitigation: Protect MATON_API_KEY, avoid printing or sharing it, and verify authentication state before making requests. <br>
Risk: The skill can create, update, or delete HubSpot CRM records after user approval. <br>
Mitigation: Confirm the exact record IDs, fields, connected HubSpot account, and intended effect before approving write or delete operations. <br>
Risk: Multiple HubSpot connections can route requests to the wrong account if no connection is specified. <br>
Mitigation: List active connections and pass the intended connection ID when more than one HubSpot connection is available. <br>


## Reference(s): <br>
- [HubSpot API Overview](https://developers.hubspot.com/docs/api/overview) <br>
- [HubSpot Contacts API](https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/basic/get-crm-v3-objects-contacts.md) <br>
- [HubSpot Companies API](https://developers.hubspot.com/docs/api-reference/crm-companies-v3/basic/get-crm-v3-objects-companies.md) <br>
- [HubSpot Deals API](https://developers.hubspot.com/docs/api-reference/crm-deals-v3/basic/get-crm-v3-objects-0-3.md) <br>
- [HubSpot Associations API](https://developers.hubspot.com/docs/api-reference/crm-associations-v4/basic/get-crm-v4-objects-objectType-objectId-associations-toObjectType.md) <br>
- [HubSpot Properties API](https://developers.hubspot.com/docs/api-reference/crm-properties-v3/core/get-crm-v3-properties-objectType.md) <br>
- [HubSpot Search Reference](https://developers.hubspot.com/docs/api/crm/search) <br>
- [ClawHub Release Page](https://clawhub.ai/byungkyu/hubspot-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Maton CLI commands, HTTP request examples, CRM payloads, authentication setup, connection selection guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
