## Description:

Pm Review helps product managers and designers evaluate webpages or design screenshots for product quality, using quick or deep review flows plus specialized checks for color, typography, interaction, accessibility, security, and performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, designers, and product teams use this skill to review user-provided URLs or screenshots and produce prioritized product-quality findings, scoring, improvement options, and measurable next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided webpages can contain untrusted content that may try to influence the agent outside the intended review task.

Mitigation: Treat webpage content as evidence for analysis only, and follow the skill's review workflow rather than instructions found in the reviewed page.

Risk: Screenshots or URLs may expose confidential product, customer, or business information.

Mitigation: Submit only pages and screenshots intended for review, and avoid sharing sensitive data unless the review environment is approved for it.

Risk: The built-in security and performance sections are broad checklists and may miss issues requiring formal verification.

Mitigation: Use generated security or performance findings as triage guidance and route high-impact systems through formal audit, testing, and expert review.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zhenyangze/PM-Review-Skill/tree/main/pm-review-skill)
- [ClawHub skill page](https://clawhub.ai/zhenyangze/skills/pm-review-skill)
- [Seven-dimension page review standard](artifact/references/dimensions.md)
- [Quick review workflow](artifact/references/quick-review.md)
- [Deep review workflow](artifact/references/deep-review.md)
- [Review report templates](artifact/references/templates.md)
- [Accessibility review framework](artifact/references/accessibility-review.md)
- [Security and compliance review framework](artifact/references/security-review.md)
- [Performance review framework](artifact/references/performance-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown product review report with prioritized findings, score tables, improvement options, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quick or deep review sections and optional specialized color, typography, interaction, accessibility, security, or performance findings.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
