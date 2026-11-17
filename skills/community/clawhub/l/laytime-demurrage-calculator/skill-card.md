## Description:

Converts voyage charter terms, Statement of Facts entries, and Notice of Readiness records into a draft laytime, demurrage, or despatch calculation packet for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External chartering managers, post-fixture operators, claims handlers, port agents, traders, and maritime counsel use this skill to draft a clause-by-clause laytime statement, NOR validity walkthrough, timesheet, computation worksheet, evidence index, disputed-period flags, and open-questions list before commercial or legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle confidential voyage, rate, party, and claims materials.

Mitigation: Limit inputs and outputs to information needed for the calculation, and avoid echoing commercially sensitive facts beyond what the draft packet requires.

Risk: A laytime, demurrage, or despatch computation may be relied on commercially or legally before review.

Mitigation: Keep outputs marked as drafts and require chartering, claims, or counsel review before relying on the calculation.

Risk: Privileged or unlawfully obtained counterparty material could be supplied as evidence.

Mitigation: Do not incorporate privileged or unlawfully obtained counterparty materials; ask the user to confirm the source before using questionable material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/laytime-demurrage-calculator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft laytime packet with tables, formulas, appendices, disputed-period flags, and an evidence index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts for chartering, operations, claims-team, and counsel review; the skill does not issue invoices, notices of claim, or legal pleadings.]

## Skill Version(s):

0.1.1 (source: server release evidence and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
