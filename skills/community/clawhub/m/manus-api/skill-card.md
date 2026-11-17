## Description:

Guides agents in using the Manus API through Maton to manage tasks, projects, files, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to work with Manus tasks, projects, files, and webhooks through an authorized Maton connection, and to set up explicitly approved automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Manus accounts can expose sensitive task, file, and account data.

Mitigation: Confirm trust in Maton and Manus, use OAuth where possible, and limit access and shared data to the task at hand.

Risk: Writes or deletes can change or remove account resources.

Mitigation: Start with read-only calls and obtain explicit user approval before each write or delete.

Risk: Webhooks, triggers, and hosted functions can continue processing or forwarding data unattended.

Mitigation: Review the destination and scope, get approval before enabling automation, and remove it when no longer needed.

Risk: An exposed Maton API key could grant access to connected account data.

Mitigation: Prefer OAuth and never print, persist, or share MATON_API_KEY.

## Reference(s):

- [Manus API documentation](https://open.manus.im/docs/api-reference)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)
- [Manus skill release](https://clawhub.ai/byungkyu/skills/manus-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API call examples and setup steps for user-approved connections and automation.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
