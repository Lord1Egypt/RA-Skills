## Description:

Audits existing mobile UI for low-light, glare, glove, wet-hand, and vibration conditions, then emits an implementer-ready findings and fix-plan document set without modifying the target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit existing field or industrial mobile interfaces for low-visibility usability issues and produce a structured handoff for an implementation agent. It is useful for scoped re-runs on specific H5 or WeChat mini-program pages and components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated handoff reports may exceed the intended target boundary or include misleading recommendations if scope inputs are broad or ambiguous.

Mitigation: Use tightly controlled target paths, page names, and selectors, then review audit.json and report.md before handing them to another agent.

Risk: The generated report is rendered evidence, not executable instruction, and may be unsafe to follow without human review.

Mitigation: Treat report.md as untrusted guidance and require an implementer or reviewer to validate each proposed change against the target UI.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vincentjiang06/skills/low-visibility-fix)
- [Field low-visibility conditions](references/field-conditions.md)
- [Standards and rationale](references/research-bibliography.md)
- [Design tokens](references/design-tokens.json)
- [Audit protocol](rules/audit-protocol.md)
- [Handoff document contract](rules/handoff-docs.md)
- [Visual pass guidance](rules/visual-pass.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report plus JSON audit sidecar]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit.json and report.md to the configured output directory; recommendations are advisory and require review before implementation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
