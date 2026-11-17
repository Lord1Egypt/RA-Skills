## Description:

Use when discovering and screening China-mainland AI recruitment candidates from accepted conference or journal papers, matching authors to multiple job descriptions, investigating public professional evidence, preparing individually approved outreach, or classifying recruitment email replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting operators and hiring teams use this skill to collect accepted publication evidence, identify China-mainland AI candidates, compare candidates with job requirements, prepare outreach drafts, and classify recruitment replies while keeping final decisions and sends under human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak approval binding could allow candidate, contact, or mail-related actions to proceed without reliably matching the exact content a human reviewed.

Mitigation: Fix or compensate for the approval-preview weakness before relying on message approvals, and require operators to verify the exact recipient, subject, body summary, draft link, and approval record before send-related actions.

Risk: Model-driven reply handling can suggest unsubscribe, not-interested, closure, or follow-up actions that change candidate or contact records.

Mitigation: Require human confirmation for model-derived unsubscribe, not-interested, follow-up, deletion, suppression, and closure actions, especially when the reply is ambiguous.

Risk: The workflow processes candidate evidence, regional recruiting filters, and recruitment email thread content that may create privacy, employment, or data-transfer obligations.

Mitigation: Confirm legal and privacy approval before production use, run with controlled local storage and limited network access, and approve sending candidate or email-thread content to DeepSeek before enabling that integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/debtvc2022/skills/hr-candidate-discovery-screening)
- [Data Sources](references/data-sources.md)
- [Screening Policy](references/screening-policy.md)
- [Outreach Guidelines](references/outreach-guidelines.md)
- [Reply Classification](references/reply-classification.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown instructions with inline shell commands, JSON workflow records, and email draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human-reviewed recruiting workflows with explicit approval gates before candidate advancement, outreach preparation, send authorization, and contact-status changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
