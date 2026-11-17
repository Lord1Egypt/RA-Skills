## Description:

Negotiate on behalf of your principal with hard limits, graduated autonomy, and mandatory human approval for commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees and external users can use this skill to have an agent draft and manage negotiation messages within explicit hard limits, approval thresholds, and category-specific tactics. It is intended for buying, selling, peer-to-peer marketplace, and professional negotiations where the principal confirms limits before any commitment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Negotiation templates or messages could expose a user's private floor, ceiling, walk-away point, urgency, salary, or other leverage.

Mitigation: Review and edit templates before use, and keep the skill in draft-only or approval-required modes unless specific limits have been set.

Risk: Hidden Negotiation Profile examples could be mistaken for confirmed user preferences.

Mitigation: Treat profile entries as placeholders, and confirm preferences before storing or acting on them.

## Reference(s):

- [Buying Negotiations](artifact/buying.md)
- [Selling Negotiations](artifact/selling.md)
- [P2P Marketplace Negotiations](artifact/p2p.md)
- [Professional Negotiations](artifact/professional.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text negotiation drafts, questions, logs, and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit principal limits and approval thresholds before negotiation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
