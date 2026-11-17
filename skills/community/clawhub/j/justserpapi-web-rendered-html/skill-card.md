## Description:

Call GET /api/v1/web/rendered-html for Web Crawling Rendered Html through Just Serp API with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call Just Serp API's rendered HTML crawl endpoint for a supplied URL. The skill supports webpage crawling workflows such as scraping, metadata extraction, and page structure analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to a third-party crawling API.

Mitigation: Avoid private, internal, authenticated, or secret-bearing URLs unless sharing them with Just Serp API is approved.

Risk: The API key is passed through a command-line argument.

Mitigation: Prefer a release or wrapper that reads the key directly from a protected environment variable and avoid exposing command histories or process listings.

## Reference(s):

- [Just Serp API Project Site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_rendered_html&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_rendered_html&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-web-rendered-html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and endpoint-specific summaries, with raw JSON returned after the summary when the API call succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a url query parameter; reports backend error payloads when the API fails.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
