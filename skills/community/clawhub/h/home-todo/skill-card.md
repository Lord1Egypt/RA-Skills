## Description:

Home Todo checks a local home todo file and appends reminders for incomplete tasks when the user sends Dashboard webchat messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberraccoonx](https://clawhub.ai/user/cyberraccoonx)

### License/Terms of Use:

MIT-0

## Use Case:

Individual ClawHub users use this skill to record home-related tasks and receive reminders when interacting through Dashboard webchat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Home todo reminders may be added to every Dashboard response.

Mitigation: Install only when this always-on reminder behavior is desired, and review generated responses before relying on them.

Risk: Home todo items may contain sensitive personal details stored in a local markdown file.

Mitigation: Avoid storing sensitive details and periodically review or delete ~/.openclaw/workspace/.home-todos.md.

Risk: Matching home todo statements from connected channels may be saved locally.

Mitigation: Review connected-channel usage and remove unwanted captured items from the local todo file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberraccoonx/skills/home-todo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reminder text appended to agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update ~/.openclaw/workspace/.home-todos.md for local todo tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
