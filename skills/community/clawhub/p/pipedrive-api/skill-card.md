## Description: <br>
Pipedrive API integration with managed OAuth for managing deals, persons, organizations, activities, and pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to inspect and manage Pipedrive CRM records through Maton-managed OAuth. It supports common sales workflows such as reading and updating deals, contacts, organizations, activities, pipelines, stages, notes, and users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and brokered OAuth access to Pipedrive CRM data. <br>
Mitigation: Keep MATON_API_KEY protected and install only when Maton is trusted to broker the connected Pipedrive account. <br>
Risk: Write-capable CRM operations can create, update, or delete deals, contacts, organizations, activities, notes, and OAuth connections. <br>
Mitigation: Require clear user confirmation before every create, update, or delete operation, including the target resource and intended effect. <br>
Risk: Multiple Pipedrive connections can route requests to the wrong account if no connection is specified. <br>
Mitigation: Use the intended Maton connection identifier when multiple accounts exist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/pipedrive-api) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Pipedrive API Overview](https://developers.pipedrive.com/docs/api/v1) <br>
- [Pipedrive Deals API](https://developers.pipedrive.com/docs/api/v1/Deals) <br>
- [Pipedrive Persons API](https://developers.pipedrive.com/docs/api/v1/Persons) <br>
- [Pipedrive Organizations API](https://developers.pipedrive.com/docs/api/v1/Organizations) <br>
- [Pipedrive Activities API](https://developers.pipedrive.com/docs/api/v1/Activities) <br>
- [Pipedrive Pipelines API](https://developers.pipedrive.com/docs/api/v1/Pipelines) <br>
- [Pipedrive Stages API](https://developers.pipedrive.com/docs/api/v1/Stages) <br>
- [Pipedrive Notes API](https://developers.pipedrive.com/docs/api/v1/Notes) <br>
- [Maton](https://maton.ai) <br>
- [Maton API gateway](https://api.maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with HTTP endpoint references and Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Maton-managed Pipedrive OAuth connection.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
