## Description: <br>
Converts plain English automation requests into complete, deployable n8n workflow JSON with setup and testing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[di5cip1e](https://clawhub.ai/user/di5cip1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business automation builders use this skill to turn process descriptions into import-ready n8n workflows for lead capture, CRM sync, invoice follow-ups, social posting, support automation, and data routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflows can move data between systems, expose webhook endpoints, run schedules, send emails or public posts, or execute Function/Code nodes if imported without review. <br>
Mitigation: Review each workflow before enabling it, check data destinations and credential scopes, require webhook authentication, inspect Function/Code nodes, and test with sample data first. <br>
Risk: Generated workflow JSON may not match a user's exact n8n environment, credentials, or integration permissions. <br>
Mitigation: Validate required accounts, node availability, credentials, schedules, error paths, and sample inputs in a non-production workflow before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/di5cip1e/n8n-workflow-builder) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with import-ready n8n workflow JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow descriptions, prerequisites, credential notes, setup instructions, testing steps, and an embedded signature comment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
