## Description: <br>
HubSpot CRM and CMS API integration for contacts, companies, deals, owners, and content management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwall1](https://clawhub.ai/user/kwall1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and CRM administrators use this skill to query and manage HubSpot CRM and CMS resources from an agent-assisted command workflow. It helps with contacts, companies, deals, owners, associations, properties, pages, domains, and files when a HubSpot private app token is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A valid HubSpot private app token can allow the agent-assisted workflow to read or change HubSpot CRM data. <br>
Mitigation: Use a dedicated least-privilege token, avoid sharing it in prompts or logs, and review create, update, association, and owner-assignment commands before execution. <br>
Risk: Commands can affect production CRM records if run against a live HubSpot portal. <br>
Mitigation: Prefer a sandbox or test records during setup, and confirm target record IDs, emails, owner IDs, and payloads before running write operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kwall1/hubspot) <br>
- [HubSpot API Base](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and HUBSPOT_ACCESS_TOKEN for the documented shell workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
