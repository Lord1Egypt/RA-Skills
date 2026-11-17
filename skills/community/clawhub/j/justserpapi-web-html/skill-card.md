## Description:

Call GET /api/v1/web/html for Web Crawling Html through Just Serp API with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to crawl a specified webpage through Just Serp API and retrieve HTML data for scraping, metadata extraction, or page-structure analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested URL is sent to Just Serp API under the user's API key.

Mitigation: Use only URLs that may be shared with that provider, and avoid localhost, internal systems, secret-bearing URLs, or sensitive page contents.

Risk: API credentials are required to call the endpoint.

Mitigation: Pass the key through the required environment variable or command argument and avoid exposing key values in chat, screenshots, or logs.

## Reference(s):

- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-web-html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Just Serp API key and a user-provided URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
