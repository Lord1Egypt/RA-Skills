## Description:

Connects an agent to JotForm through Maton to create forms, manage submissions, and retrieve form data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to inspect JotForm forms and submissions, create or update forms, and manage approved JotForm workflows through a connected Maton account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton to JotForm grants access to account data within the authorized scope.

Mitigation: Connect only with the user's approval and select only the scopes needed for the task.

Risk: Writes, deletions, webhooks, triggers, destinations, and hosted functions can change data or keep forwarding future submissions.

Mitigation: Review the exact action and obtain explicit approval before enabling or executing it.

Risk: Form responses and credentials may contain sensitive information.

Mitigation: Share only requested response fields and avoid logging raw responses or credentials.

## Reference(s):

- [JotForm skill on ClawHub](https://clawhub.ai/byungkyu/skills/jotform)
- [JotForm API documentation](https://api.jotform.com/docs/)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with commands, code examples, and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-authorized form and submission data; requires a Maton account and network access.]

## Skill Version(s):

1.2.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
