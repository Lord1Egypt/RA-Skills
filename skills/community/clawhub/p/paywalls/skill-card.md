## Description:

Creates and optimizes in-app paywalls, upgrade screens, upsell modals, and feature gates for free-to-paid conversion moments after users have experienced product value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

Product, growth, and UX teams use this skill to design and evaluate in-product upgrade moments such as feature gates, usage limits, trial-expiration screens, and upgrade modals. It helps frame timing, copy, layout, testing, and anti-pattern checks for converting free or lower-tier users while preserving trust.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personalized paywall experiments can involve analytics or targeting data.

Mitigation: Confirm consent or another lawful basis for analytics use, avoid sensitive attributes, and document targeting rules.

Risk: Local product-marketing context may contain confidential or regulated business information.

Mitigation: Review context files before use and keep recommendations within the intended product and data-handling boundaries.

Risk: Paywall optimization can drift into dark patterns or excessive prompts.

Mitigation: Keep dismiss options clear, cap prompt frequency, and review copy for pressure, guilt, or confusing opt-outs.

## Reference(s):

- [Paywall Experiment Ideas](references/experiments.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown prose with checklists, examples, and paywall copy recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local product-marketing context when available; produces recommendations rather than executable artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter metadata.version reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
