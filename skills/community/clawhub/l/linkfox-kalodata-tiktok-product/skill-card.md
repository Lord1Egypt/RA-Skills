## Description:

Searches Kalodata-powered TikTok Shop product leaderboards and retrieves detailed product metrics by productId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to browse TikTok Shop product leaderboards and inspect a selected product's sales, price, revenue, commission, category, shop, and engagement metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes account, billing, and feedback workflows in addition to product lookup behavior.

Mitigation: Review those workflows before installation and confirm any paid order manually.

Risk: API keys, endpoint overrides, and phone verification codes can affect account access and billing.

Mitigation: Use a dedicated API key, verify LINKFOX_* endpoint environment variables, and avoid sharing phone verification codes through the agent unless necessary.

Risk: Product lookup responses and cache files are persisted locally under a linkfox session directory.

Mitigation: Delete local linkfox output and cache files when they are no longer needed.

## Reference(s):

- [Kalodata TikTok Product API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-kalodata-tiktok-product)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON API results and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under a local linkfox session directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
