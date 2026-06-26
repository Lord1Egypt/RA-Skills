## Description: <br>
Full HubSpot CRM automation - contacts, deals, companies, activities, and pipeline reports via the HubSpot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this skill to manage HubSpot CRM records from the command line, including contacts, deals, companies, activities, and pipeline reports. Developers and agents can use it to produce HubSpot API actions and JSON summaries for CRM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly change or delete live HubSpot CRM records. <br>
Mitigation: Use a dedicated least-privilege private app token, test commands on non-production records first, and require human review before update, association, stage-change, activity-log, or delete operations. <br>
Risk: The HubSpot private app token grants access according to its assigned scopes. <br>
Mitigation: Store the token only in the HUBSPOT_API_KEY environment variable, avoid broad write or delete scopes unless needed, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr3kstyle/hubspot-crm-skill) <br>
- [HubSpot API base endpoint](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration guidance] <br>
**Output Format:** [Markdown usage examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HUBSPOT_API_KEY environment variable and the Python requests package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
