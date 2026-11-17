## Description:

A local Node.js skill that checks copied low-value consumables and revolving materials ledger text for totals, roll-forward relationships, duplicate rows, blanks, and amortization overages, with source-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Cost accountants and warehouse staff use this skill during month-end inventory and expense closing, or before annual stocktaking, to reconcile low-value consumables and revolving materials ledgers. It performs the free-tier checks locally and reports only on evidence present in the supplied ledger text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release explicitly omits several ledger checks, so users may over-read a clean result as a full accounting review.

Mitigation: Review the reported checks_not_run list and use additional review or the complete product scope when omitted checks matter.

Risk: The checker operates on copied ledger text and cannot validate source documents, ERP records, tax treatment, or accounting policy choices.

Mitigation: Use it as a reconciliation aid only and have qualified staff confirm accounting judgments and source-document support.

Risk: The skill and outputs are Chinese-language and local Node-based, which may be unsuitable for teams that cannot review the prompts and findings accurately.

Mitigation: Install only where reviewers can understand the Chinese-language behavior and can inspect the local Node execution path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/low-value-consumables-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON when the --json option is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include check scope, omitted free-tier checks, severity counts, row counts, and whether execution was local.]

## Skill Version(s):

1.0.19 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
