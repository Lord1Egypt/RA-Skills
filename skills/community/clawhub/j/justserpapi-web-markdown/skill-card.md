## Description:

Call GET /api/v1/web/markdown for Web Crawling Markdown through Just Serp API with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to crawl a supplied webpage URL through Just Serp API and receive readable Markdown for extraction, documentation workflows, or LLM input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to a third-party crawler.

Mitigation: Use only with URLs that are appropriate to disclose to Just Serp API; avoid private, internal, authenticated, or sensitive links.

Risk: The helper accepts the API key as a command-line argument.

Mitigation: Prefer execution patterns that read JUST_SERP_API_KEY directly from the environment and avoid exposing secrets in shell history, process listings, chat, screenshots, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-web-markdown)
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link)
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link)
- [Just Serp API base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with optional raw JSON response from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_SERP_API_KEY environment value and a target url parameter.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
