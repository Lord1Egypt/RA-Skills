## Description:

Assembles a US B2B proposal from a scope sheet and a template, with scope, pricing, terms and signature blocks checked for gaps. Use when the user asks for b2b proposal template, proposal builder, sales proposal checklist. For US B2B sales teams that send written proposals to buyers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US B2B sales teams use this skill to assemble proposal drafts from scope, pricing, terms, and validity details, then identify missing fields and claims or commitments that need approval before the proposal is sent.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Unchecked input filenames can overwrite Markdown files outside the selected output folder in some directory layouts.

Mitigation: Validate filenames and enforce output-directory containment; use a fresh output folder.

Risk: The quickstart's Markdown input description does not match the renderer's CSV input, and the renderer may leave placeholders unfilled.

Mitigation: Confirm the input format matches the renderer and inspect the complete generated draft for missing fields before use.

Risk: The optional Windows toolkit is a separate, unsigned executable.

Mitigation: Review it separately, verify the published SHA-256 before running, and avoid elevated privileges unless necessary.

Risk: Proposal claims, legal terms, or commercial commitments may be inaccurate or unapproved.

Mitigation: Check claims against their sources and obtain deal-owner and legal approval before sending; never sign or send the proposal automatically.

## Reference(s):

- [Proposal Builder on ClawHub](https://clawhub.ai/rapidworker1/skills/proposal-builder)
- [Publisher profile](https://github.com/rapidworker1)
- [Proposal essentials](artifact/references/proposal-essentials.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown proposal draft with a scope table, terms block, and open-items checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft content for human review; do not send or sign without required approvals.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
