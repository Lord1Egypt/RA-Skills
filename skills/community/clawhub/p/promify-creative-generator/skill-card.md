## Description:

Generate ad creatives, marketing images, and advertising visuals using the Promify API for Meta Ads, Facebook Ads, Instagram Ads, Google Ads, TikTok Ads, and other ad platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promify](https://clawhub.ai/user/promify)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to turn product URLs into generated advertising creatives, including image URLs, creative copy, and quota status. Developers may also use it to configure Promify API access for an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose the Promify API key by pasting it into chat.

Mitigation: Configure PROMIFY_API_KEY in the local OpenClaw settings file instead of sharing the key in conversation.

Risk: Fetched product details may be sent to Promify automatically.

Mitigation: Use only public or approved product URLs, and avoid private, unpublished, internal, or sensitive product pages.

Risk: Generated advertising creatives or copy may be inaccurate or unsuitable for a campaign.

Mitigation: Review the final image URL and creative copy before publishing or using the output in an ad platform.

## Reference(s):

- [Promify](https://promify.ai)
- [Promify API Key Setup](https://promify.ai/login?redirect=/&from=openclaw)
- [ClawHub Skill Page](https://clawhub.ai/promify/skills/promify-creative-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with product summaries, status messages, image URLs, creative copy, quota information, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PROMIFY_API_KEY, fetches product-page data, submits a Promify image task, and polls for completion for up to three minutes.]

## Skill Version(s):

1.0.9 (source: server release evidence, created 2026-04-21T12:25:42Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
