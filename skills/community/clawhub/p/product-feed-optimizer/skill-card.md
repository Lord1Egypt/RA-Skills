## Description:

Audits and improves Shopping and Performance Max product feeds by triaging disapprovals, checking required attributes, rewriting product titles and descriptions, and structuring feed-driven asset or listing groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, ecommerce teams, and agent-assisted media buyers use this skill to prepare or repair product feed data before Shopping or Performance Max campaigns. It helps turn feed exports, diagnostics, and landing-page checks into a remediation package for disapprovals, title patterns, attribute gaps, price and availability mismatches, and catalog segmentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product feed exports, diagnostics, landing-page URLs, and claims or offers memory can contain sensitive catalog, pricing, and campaign information.

Mitigation: Share only the fields needed for the feed audit and review the generated remediation package before applying changes.

Risk: Incorrect price, availability, identifier, or claim wording can lead to disapprovals or misleading feed updates.

Mitigation: Validate proposed fixes against landing pages, Merchant Center diagnostics, and approved claims or offer records before publishing.

## Reference(s):

- [Product Feed Optimizer on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/product-feed-optimizer)
- [Metadata homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Feed Title Patterns](references/feed-title-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown remediation package with tables, rewritten feed fields, and handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-item diagnostics, missing-attribute flags, title and description rewrites, price and availability checks, and feed segment recommendations.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
