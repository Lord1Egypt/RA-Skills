## Description:

Webhook Receiver Pro provides agent guidance and Python code for receiving webhook events locally, logging events, filtering event types, retrying processing, verifying signatures, and dispatching handlers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to create or adapt a local Python webhook receiver for CI/CD, payment notification, monitoring alert, and chat event workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook events may be persisted with full headers or payload data, including tokens or personal data.

Mitigation: Redact sensitive headers and payload fields before logging, and restrict access to persisted webhook log files.

Risk: Webhook events can be logged or dispatched before required provider authentication is enforced.

Mitigation: Require provider signature verification before storing events or invoking handlers, and reject unsigned or invalid requests.

Risk: The broad activation trigger 'hook' can invoke the skill in unrelated contexts.

Mitigation: Remove or narrow the activation trigger so the skill only activates for explicit webhook receiver requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-webhook-receiver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code blocks and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include webhook receiver code, event handling examples, and security caveats.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter, hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
