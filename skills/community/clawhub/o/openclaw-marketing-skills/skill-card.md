## Description:

A collection of 33 marketing skills for OpenClaw agents covering CRO, copywriting, SEO, paid ads, email, analytics, growth, sales enablement, and go-to-market strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill pack to give OpenClaw agents reusable marketing workflows for positioning, conversion optimization, copy, SEO, paid acquisition, analytics, lifecycle email, retention, and sales enablement. Developers may also use it to generate implementation-oriented guidance such as tracking plans, schema markup, experiment plans, and configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pack includes guidance for high-impact marketing and revenue operations such as ad campaigns, CRM workflows, billing-related lifecycle actions, email outreach, crawler access decisions, and voice-cloning workflows.

Mitigation: Require explicit user confirmation before taking any campaign, CRM, billing, email, crawler-access, or voice-cloning action, and review outputs before applying them to live accounts or customer data.

Risk: Some optional examples execute mutable third-party code through git clone, make, or npx.

Mitigation: Pin versions, inspect the code first, and run those examples only in a disposable sandbox.

Risk: Installing the pack in environments with ad accounts, CRM or billing access, API keys, or private customer data can increase exposure if agent actions are not constrained.

Mitigation: Review the skill before installation, limit tool permissions to the minimum needed, and keep sensitive credentials and private customer data out of prompts unless required.

## Reference(s):

- [OpenClaw Marketing Skills on ClawHub](https://clawhub.ai/leoyeai/skills/openclaw-marketing-skills)
- [README](artifact/README.md)
- [ClawHub manifest](artifact/clawhub.yaml)
- [Product Marketing Context skill](artifact/skills/product-marketing-context/SKILL.md)
- [Analytics Tracking event library](artifact/skills/analytics-tracking/references/event-library.md)
- [GA4 implementation reference](artifact/skills/analytics-tracking/references/ga4-implementation.md)
- [A/B testing sample size guide](artifact/skills/ab-test-setup/references/sample-size-guide.md)
- [Paid ads platform setup checklists](artifact/skills/paid-ads/references/platform-setup-checklists.md)
- [Schema markup examples](artifact/skills/schema-markup/references/schema-examples.md)
- [MyClaw.ai](https://myclaw.ai)
- [Evan Miller A/B test sample size calculator](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Schema.org](https://schema.org)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured plans, checklists, copy drafts, code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a product marketing context Markdown file when the product-marketing-context skill is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
