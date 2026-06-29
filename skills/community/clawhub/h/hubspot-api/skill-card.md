## Description: <br>
HubSpot CRM API integration with managed OAuth for managing contacts, companies, deals, and associations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to read, create, update, search, and archive HubSpot CRM records through Maton-managed OAuth. It is suited for CRM maintenance, data synchronization, and workflow automation involving contacts, companies, deals, associations, and object properties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, archive, and delete HubSpot CRM records through a connected account. <br>
Mitigation: Confirm the target object, connection, and intended effect before every write or delete operation. <br>
Risk: A leaked MATON_API_KEY could allow unauthorized access through the Maton account. <br>
Mitigation: Store MATON_API_KEY as a secret, avoid printing it in logs or chat, and rotate it if exposure is suspected. <br>
Risk: Requests are mediated by Maton before reaching HubSpot. <br>
Mitigation: Install only when Maton is an acceptable intermediary and use scoped Maton or HubSpot connections where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/hubspot-api) <br>
- [HubSpot API Overview](https://developers.hubspot.com/docs/api/overview) <br>
- [HubSpot Contacts API](https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/basic/get-crm-v3-objects-contacts.md) <br>
- [HubSpot Companies API](https://developers.hubspot.com/docs/api-reference/crm-companies-v3/basic/get-crm-v3-objects-companies.md) <br>
- [HubSpot Deals API](https://developers.hubspot.com/docs/api-reference/crm-deals-v3/basic/get-crm-v3-objects-0-3.md) <br>
- [HubSpot Associations API](https://developers.hubspot.com/docs/api-reference/crm-associations-v4/basic/get-crm-v4-objects-objectType-objectId-associations-toObjectType.md) <br>
- [HubSpot CRM Search](https://developers.hubspot.com/docs/api/crm/search) <br>
- [API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for live HubSpot operations.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
