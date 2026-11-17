## Description:

Design the complete post-purchase customer experience from order confirmation through delivery and beyond, including transactional emails, shipping updates, unboxing moments, review solicitation, and repeat-purchase nudges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, CRM, lifecycle marketing, and retention teams use this skill to design post-purchase journeys that coordinate confirmation, shipping, unboxing, review, cross-sell, replenishment, and measurement touchpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS, email, tracking, and customer-data recommendations may create compliance or privacy exposure if implemented without legal and policy review.

Mitigation: Review SMS and email consent rules, privacy notices, customer-data minimization, review-platform and FTC policies, and UGC permission handling before operational use.

Risk: Tracking or QR-code URLs can expose sensitive order or customer identifiers if implemented with raw IDs.

Mitigation: Use privacy-preserving tokens or server-side lookup patterns instead of raw order IDs or customer IDs in URLs.

Risk: Review flows can become misleading if they suppress legitimate negative reviews or route customers away from transparent review processes.

Mitigation: Use negative-review handling to offer support while preserving authentic review collection and complying with platform and FTC policies.

## Reference(s):

- [Post-Purchase Flow Skill](artifact/SKILL.md)
- [Post-Purchase Flow Output Template](artifact/output-template.md)
- [Post-Purchase Email Timing Guide](artifact/email-timing-guide.md)
- [Unboxing Experience Design Guide](artifact/unboxing-design-guide.md)
- [Post-Purchase Flow Quality Checklist](artifact/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance, Analysis]

**Output Format:** [Markdown guidance, templates, journey maps, timing tables, checklists, and implementation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory workflow output; no executable behavior is included in the artifact.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
