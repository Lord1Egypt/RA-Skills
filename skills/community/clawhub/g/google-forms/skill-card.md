## Description:

Helps agents create Google Forms, add questions, and retrieve form responses through a managed Google Forms connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using Google Forms can ask an agent to inspect forms and responses or, with approval, create forms and questions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OAuth permissions can expose more Google Forms data than the task requires.

Mitigation: Review requested scopes and prefer read-only access where possible.

Risk: Form edits and hosted automations can make changes without the user intending them.

Mitigation: Confirm each write, new connection, and automation before it runs.

Risk: Triggers and destinations can keep forwarding matching events after setup.

Mitigation: Review the destination and forwarding scope, and obtain explicit approval before enabling ongoing forwarding.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/byungkyu/skills/google-forms)
- [Maton homepage](https://maton.ai)
- [Google Forms API reference](https://developers.google.com/workspace/forms/api/reference/rest)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance with CLI examples and selected form data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Form data and changes depend on the connected account's permissions; write operations require user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
