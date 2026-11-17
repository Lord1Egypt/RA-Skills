## Description:

Query and manage marketing data across 40+ platforms, including Google Analytics, Google Ads, Facebook Ads, Instagram, Shopify, HubSpot, Klaviyo, TikTok, LinkedIn, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insightfulpipe](https://clawhub.ai/user/insightfulpipe)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts, operators, and developers use this skill to discover account and source identifiers, inspect platform action schemas, query marketing data, and run confirmed write operations across connected analytics, advertising, ecommerce, CRM, messaging, and SEO platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and invokes the third-party InsightfulPipe npm CLI package.

Mitigation: Confirm the npm package is trusted before installation, and prefer a reviewed pinned version or isolated environment when possible.

Risk: The skill uses INSIGHTFULPIPE_TOKEN to access connected marketing and business accounts.

Mitigation: Keep the token narrowly scoped and rotate or revoke it according to the connected account policies.

Risk: The skill can run write actions against connected platforms.

Mitigation: Approve write actions only after reviewing the target platform, account, and payload.

## Reference(s):

- [InsightfulPipe Homepage](https://insightfulpipe.com)
- [InsightfulPipe npm Package](https://www.npmjs.com/package/insightfulpipe)
- [ClawHub Skill Page](https://clawhub.ai/insightfulpipe/skills/insightfulpipe)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the insightfulpipe CLI and a pre-configured INSIGHTFULPIPE_TOKEN; write operations require user confirmation before running.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
