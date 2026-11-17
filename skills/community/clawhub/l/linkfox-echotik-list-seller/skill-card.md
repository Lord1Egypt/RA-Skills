## Description:

Searches and analyzes TikTok Shop seller data across supported marketplaces, returning store-level sales, GMV, audience, rating, category, fulfillment, and content metrics for discovery and benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and commerce analysts use this skill to find and compare TikTok Shop stores by marketplace, category, GMV, sales trend, listing date, store origin, and sales channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox receives seller-search queries and may receive feedback content.

Mitigation: Install only if this data sharing is acceptable, avoid submitting sensitive business details in queries or feedback, and review LinkFox endpoint configuration before use.

Risk: Credential, account, and payment onboarding flows can expose API keys or trigger paid credit purchases.

Mitigation: Obtain and store API keys through a secure external process, verify plan and payment details before using onboarding commands, and use payment flows only when explicitly intended.

Risk: Saved LinkFox response and cache files may contain sensitive seller research or competitive analysis data.

Mitigation: Treat generated LinkFox data directories as sensitive business records and restrict retention, sharing, and repository commits accordingly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-seller)
- [EchoTik-TikTok店铺列表 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON responses, saved JSON files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a LinkFox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
