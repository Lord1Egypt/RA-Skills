## Description:

A context-aware email assistant that triages inbox messages, classifies priority, flags phishing signals, prepares draft replies for review, and supports configurable briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Individuals and teams use this skill to manage high-volume inboxes by receiving prioritized briefings, identifying messages that need action, and preparing draft replies for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive mailbox content and local digest data.

Mitigation: Install only when mailbox access is appropriate, protect the workspace, and prefer on-demand checks unless scheduled briefings are explicitly needed.

Risk: Draft replies may contain incorrect, sensitive, or unintended content.

Mitigation: Review every draft before saving or sending, and keep the skill in draft-only operation.

Risk: The dashboard manifest does not define tenant access controls for multi-user deployment.

Mitigation: Do not deploy the dashboard for multiple users until tenant isolation and row-level access controls are added and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-email-assistant)
- [Himalaya email CLI](https://github.com/pimalaya/himalaya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings and draft email text, with optional shell commands and JSON configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only by default; email digests may be saved as local Markdown files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
