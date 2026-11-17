## Description:

Handle member/customer complaint workflows with a Linear-centered operating model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwqcode](https://clawhub.ai/user/qwqcode)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams use this skill to triage member complaint issues from Linear, separate issue facts from AI judgments, classify risk and intent, and draft structured internal analysis plus customer-facing replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted customer replies may imply refunds, compensation, exceptions, or timelines without approved policy support.

Mitigation: Review replies before sending and avoid final commitments unless the relevant policy or SOP is provided.

Risk: Complaint handling may involve legal threats, privacy concerns, chargebacks, public escalation, or other sensitive cases.

Mitigation: Escalate sensitive cases for human review and use the skill output as a structured draft rather than a final decision.

Risk: The default comment templates are Chinese and may not match every support team's workflow.

Mitigation: Confirm language and Linear write-back expectations before using the skill in production complaint handling.

## Reference(s):

- [Complaint Playbook](artifact/references/complaint-playbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown-style Linear comments and concise complaint summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured AI analysis comments, customer reply drafts, and complaint digest summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
