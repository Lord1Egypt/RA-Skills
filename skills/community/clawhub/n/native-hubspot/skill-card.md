## Description: <br>
Query and manage HubSpot CRM data via the HubSpot API for contacts, companies, deals, tickets, and pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and CRM users use this skill to search, inspect, create, update, and associate HubSpot CRM records from an agent workflow using a private app token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change HubSpot CRM records using the user's HubSpot token. <br>
Mitigation: Use a dedicated least-privilege private app token, test in a sandbox or low-risk account first, and require explicit human approval before create, update, or associate commands run against production records. <br>


## Reference(s): <br>
- [Native HubSpot on ClawHub](https://clawhub.ai/codeninja23/native-hubspot) <br>
- [HubSpot CRM API endpoint](https://api.hubapi.com/crm/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, API calls] <br>
**Output Format:** [Terminal text tables, JSON API responses, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and HUBSPOT_TOKEN; write operations can create, update, or associate CRM records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
