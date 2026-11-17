## Description:

Guides residential HVAC contractors, energy raters, home-performance auditors, and code officials through a draft ACCA Manual J 8th Edition block and room-by-room load calculation with Manual D CFM targets and a Manual S handoff for licensed-designer review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External HVAC contractors, energy raters, home-performance auditors, code officials, and design-build teams use this skill to draft or review residential Manual J load calculations before equipment selection, duct design, permits, rebates, or equipment purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A draft load report could be mistaken for a stamped or permit-ready HVAC design deliverable.

Mitigation: Keep the draft status and responsible-designer review block in outputs, and require review before permit submission, rebate filing, or equipment purchase.

Risk: Incorrect U-values, infiltration rates, leakage rates, or design conditions can produce misleading heating and cooling loads.

Mitigation: Require a source for every key input, log unknowns as measurement or assumption required, and avoid fabricating missing values.

Risk: Downstream equipment or duct choices could be made from advisory calculations without qualified sizing review.

Mitigation: Emit Manual S and Manual D handoff information only; do not select equipment, size ducts, pick register types, or stamp drawings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/manual-j-residential-load-calc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured draft Markdown load-calculation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumption logs, unresolved-information lists, Manual S and Manual D handoff blocks, and responsible-designer review language.]

## Skill Version(s):

0.1.1 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
