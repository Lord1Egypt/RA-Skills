## Description: <br>
Operate JobTread via its Pave API to create, read, update, and manage accounts, jobs, documents, tasks, locations, custom fields, and webhooks programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brokenwatch24](https://clawhub.ai/user/Brokenwatch24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to guide JobTread Pave API calls for customer, vendor, job, document, task, location, custom field, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A grant key can let an agent change live JobTread business records and create webhooks. <br>
Mitigation: Use the narrowest available grant, store it with restrictive permissions, and confirm every create, update, delete, webhook, or signed-document action before execution. <br>
Risk: Unattended automations can propagate incorrect changes or leave unnecessary webhooks active. <br>
Mitigation: Avoid unattended production automations and review or revoke webhooks and grants regularly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Brokenwatch24/jobtread-api) <br>
- [JobTread grants page](https://app.jobtread.com/grants) <br>
- [JobTread Pave API endpoint](https://api.jobtread.com/pave) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request payloads and automation patterns for a live JobTread workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
