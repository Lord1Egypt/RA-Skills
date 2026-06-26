## Description: <br>
Manage Pipedrive CRM from OpenClaw using API v1, including people, organizations, deals, leads, activities, notes, pipelines, and custom endpoint actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external operators, and developers use this skill to perform day-to-day Pipedrive CRM operations from an agent workflow, including record lookup, create/update/delete actions, deal stage movement, activity logging, notes, and custom API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Pipedrive CRM mutation authority can create, update, delete, or move business records. <br>
Mitigation: Use the least-privileged Pipedrive token available and require explicit human confirmation before delete operations or raw mutating requests. <br>
Risk: Credential exposure or misrouting could give the agent access to sensitive CRM data. <br>
Mitigation: Do not print raw tokens, keep credentials in environment variables, and verify that the configured API base points only to Pipedrive. <br>


## Reference(s): <br>
- [Entity Playbooks](references/entity-playbooks.md) <br>
- [Pipedrive API v1 Notes](references/pipedrive-v1-notes.md) <br>
- [ClawHub release page](https://clawhub.ai/danielfoch/pipedrive-crm-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Pipedrive API calls through bundled Python helper scripts when credentials are configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
