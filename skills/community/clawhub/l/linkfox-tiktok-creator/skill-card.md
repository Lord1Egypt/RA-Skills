## Description:

Provides LinkFox-proxied TikTok Shop creator data queries and shoppable-video operations, including creator profiles, shop and showcase products, content pre-checks, posting, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and commerce operators use this skill to query TikTok Shop creator profile, shop product, and showcase product data, then guide supported shoppable-video pre-check, posting, and status workflows after a creator access token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle creator access tokens, LinkFox API keys, and SMS login data.

Mitigation: Use a dedicated environment, mask tokens in user-facing output, and remove shell-profile API keys when they are no longer needed.

Risk: The onboarding flow can create paid plan orders and render payment information.

Mitigation: Confirm billing intent, plan selection, and payment method explicitly before running order commands.

Risk: Supported workflows may publish public shoppable videos or submit content for pre-check.

Mitigation: Confirm publishing actions, target products, titles, and media inputs before invoking posting or pre-check calls.

Risk: Complete API responses and cache entries may be written to local files.

Mitigation: Clean up local response and cache files after use, especially when responses may contain creator or account data.

Risk: The artifact describes automatic external feedback reporting for mismatches or quality issues.

Mitigation: Avoid including secrets, creator tokens, personal data, or unnecessary business data in feedback reports.

## Reference(s):

- [TikTok Creator API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-creator)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses, with full responses saved as local JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses are printed inline; larger responses are summarized and saved locally. The proxy script uses a 24-hour local cache for repeated parameter sets.]

## Skill Version(s):

1.0.6 (source: server release evidence, released 2026-08-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
