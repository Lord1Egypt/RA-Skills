## Description:

Builds email list segments from a user's own list, CRM, GA4, ecommerce, and consent exports, including behavioral audiences, RFM tiers, lifecycle stages, suppression lists, and measured or estimated segment sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to prepare who should receive an email before creative or lifecycle flows are designed. It turns owned audience exports into reusable segment definitions, suppression rules, aggregate counts, and a handoff summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads subscriber, consent, and suppression-related exports that may contain personal data.

Mitigation: Use aggregate descriptions, counts, hashes, or segment rules in outputs and avoid echoing raw email addresses, phone numbers, or member rows.

Risk: The optional ESP live sync path can mutate email-platform suppression state.

Mitigation: Use dry-run behavior for review first and only run live sync after verifying the affected contacts and confirming that the platform state should change.

Risk: Missing consent records can make a cohort unsafe to mail.

Mitigation: Treat missing consent evidence as NEEDS_INPUT and reconcile suppression decisions against the consent registry before using the segment for a send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/list-segment-builder)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown segment map with aggregate counts, NEEDS_INPUT flags, suppression guidance, and a handoff summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write aggregate segmentation notes under memory/email/list-segment-builder/ and promote reusable summary items; should avoid raw PII rows.]

## Skill Version(s):

19.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
