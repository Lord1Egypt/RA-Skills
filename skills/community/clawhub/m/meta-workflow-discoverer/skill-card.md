## Description:

AI-powered workflow automation discoverer that observes user patterns, identifies repetitive tasks, automatically generates executable automation workflows, and learns from history to create time-saving automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to identify repeated work patterns from task history, generate candidate workflows, and create scheduled, event-based, or manual automations for recurring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently profiles user activity and task history.

Mitigation: Use it only for non-sensitive workflows unless users give explicit consent and storage is scoped, protected, and retention-limited.

Risk: Conversation or skill-usage hooks can capture sensitive workflow context.

Mitigation: Avoid enabling hooks without clear notice, consent, and limits on what data is recorded.

Risk: Cross-user learning can expose or blend workflow patterns across users.

Mitigation: Disable cross-user learning unless strong isolation, anonymization, and governance approval are in place.

Risk: Generated automations may perform unintended work if enabled without review.

Mitigation: Review discovered workflows before automation, start with simple workflows, and monitor results before broad use.

Risk: Installation dependencies may be broader than the current implementation requires.

Mitigation: Remove unused dependencies or pin required packages before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/meta-workflow-discoverer)
- [Publisher profile](https://clawhub.ai/user/jason-aka-chen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples, plus structured workflow and automation dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill records task history and returns discovered workflows, trigger suggestions, automation records, sequence analysis, and exported workflow data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
