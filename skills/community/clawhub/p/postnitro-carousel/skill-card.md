## Description:

Generate professional social media carousel posts using the PostNitro.ai Embed API, including AI-powered content generation and manual content import for LinkedIn, Instagram, TikTok, and X carousels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammuneeb](https://clawhub.ai/user/iammuneeb)

### License/Terms of Use:


## Use Case:

Developers, marketers, and social media operators use this skill to create carousel posts from text, article URLs, X posts, or structured slide content through the PostNitro Embed API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Carousel prompts, article URLs, X URLs, slide copy, and public image URLs are sent to PostNitro.

Mitigation: Do not submit secrets, confidential drafts, or unauthorized media unless the user is permitted to share them with PostNitro.

Risk: The skill requires a PostNitro API key and may consume account credits.

Mitigation: Confirm required environment variables are set and disclose likely credit use before initiating generation or import requests.

Risk: Generated output depends on asynchronous PostNitro processing and external downloadable URLs.

Mitigation: Poll at the documented interval, check for completed status, and present returned download URLs without embedding credentials.

## Reference(s):

- [PostNitro Embed API Reference](references/api-reference.md)
- [PostNitro Carousel Skill Examples](examples/EXAMPLES.md)
- [PostNitro](https://postnitro.ai)
- [PostNitro Carousel Generator on ClawHub](https://clawhub.ai/iammuneeb/skills/postnitro-carousel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for asynchronous PostNitro workflows that return downloadable PNG image URLs or a PDF URL.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
