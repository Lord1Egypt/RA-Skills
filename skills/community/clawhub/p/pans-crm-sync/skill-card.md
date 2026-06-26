## Description: <br>
Pans Crm Sync helps agents work with Salesforce and HubSpot CRM data for AI compute sales, including customer synchronization, pipeline updates, CRM reports, and conflict handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM operators, sales teams, and developers use this skill to synchronize customer data between Salesforce and HubSpot, query contact records, update pipeline status, and export CRM results as JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Salesforce and HubSpot credentials. <br>
Mitigation: Use least-privilege CRM credentials, prefer sandbox environments for initial testing, and avoid production write scopes until sync and update behavior is verified. <br>
Risk: CRM query and sync output can contain sensitive customer data. <br>
Mitigation: Treat terminal output and exported JSON files as sensitive data, store them only in approved locations, and remove them when no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Command-line output and optional JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRM credentials in environment variables and may process sensitive customer data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
