## Description:

Screens Chinese government procurement documents for invalid-bid clauses, hard qualification and compliance requirements, policy-compliance traps, and hidden conflicts, then produces structured review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, bid, and compliance reviewers use this skill to pre-screen Chinese government procurement files before submission, identify invalid-bid risks, and produce checklists for human verification. It is intended for government procurement under China's fiscal-funding regime and not for engineering-tender, bid drafting, pricing, or legal-decision workflows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated checklists may be mistaken for legal conclusions about whether a bid is invalid.

Mitigation: Use the output as a screening aid only and have procurement, compliance, or legal reviewers independently verify conclusions against the source procurement file and current local rules.

Risk: Forced maintainer branding may be unsuitable for unbranded or client-facing work product.

Mitigation: Review generated output before distribution and confirm branding expectations before installing or using the skill in production workflows.

Risk: Broad activation phrases may trigger the skill outside its intended government-procurement screening scope.

Mitigation: Confirm the matter involves Chinese government procurement under fiscal funding and route engineering-tender, pricing, bid-writing, contract-dispute, or complaint-drafting tasks to another workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gp-invalid-bid-risk-radar)
- [Policy compliance reference](references/policy-compliance.md)
- [Hidden conflict traps reference](references/hidden-conflict-traps.md)
- [Checklist template](assets/checklist-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklists and tables with risk levels, legal basis notes, confidence labels, review actions, and responsible-party fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project overview cards, invalid-bid risk summaries, pre-submission checklists, clarification prompts, and incremental change reviews.]

## Skill Version(s):

2.1.1 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
