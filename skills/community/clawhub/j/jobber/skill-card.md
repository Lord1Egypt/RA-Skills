## Description:

Connects an agent to Jobber through Maton to manage field-service clients, jobs, quotes, invoices, and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Field-service teams and their agents can look up Jobber records and, with user approval, create or update clients, jobs, quotes, and invoices. Users can also approve automations built around their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating or changing clients, jobs, or invoices can affect business and financial records.

Mitigation: Review the target, payload, and effect, and obtain explicit user approval before each write.

Risk: Automations and destinations can send matching events persistently or act on a schedule.

Mitigation: Review each function deploy, trigger, and destination separately; disclose what data flows and where before approval.

Risk: Connecting an account and handling customer data or credentials can expose sensitive information.

Mitigation: Authorize only the intended Jobber connection and necessary scopes; keep API keys and customer data out of destinations.

## Reference(s):

- [Jobber skill on ClawHub](https://clawhub.ai/byungkyu/skills/jobber)
- [Maton](https://maton.ai)
- [Jobber developer documentation](https://developer.getjobber.com/docs/)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Jobber results and proposed changes depend on the user's connected account and authorization.]

## Skill Version(s):

1.2.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
