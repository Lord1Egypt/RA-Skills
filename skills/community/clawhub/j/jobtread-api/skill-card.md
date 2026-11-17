## Description:

Operate JobTread through the Pave API to create, read, update, and manage accounts, jobs, documents, tasks, locations, custom fields, and webhooks programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brokenwatch24](https://clawhub.ai/user/brokenwatch24)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to automate JobTread workflows through API queries, including customer and vendor records, jobs, documents, tasks, locations, custom fields, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad live changes to JobTread business data.

Mitigation: Use the least-privilege grant available and test mutating queries on non-production data before operating on production records.

Risk: Grant keys and PDF token URLs can expose JobTread data if logged or shared.

Mitigation: Store grant keys in protected local files, avoid logging or sharing secrets and token URLs, and revoke or rotate grants when automation is no longer needed.

Risk: Webhooks may continue sending business events after the original automation task is complete.

Mitigation: Keep an inventory of created webhooks and disable or delete unused webhook subscriptions.

## Reference(s):

- [JobTread Agent ClawHub release](https://clawhub.ai/brokenwatch24/skills/jobtread-api)
- [JobTread grants](https://app.jobtread.com/grants)
- [JobTread Pave API endpoint](https://api.jobtread.com/pave)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API usage guidance and example requests; live effects depend on the user's JobTread grant permissions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
