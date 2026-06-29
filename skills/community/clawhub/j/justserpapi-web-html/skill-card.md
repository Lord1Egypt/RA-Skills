## Description: <br>
Call GET /api/v1/web/html for Web Crawling Html through Just Serp API with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch raw webpage HTML from public or authorized URLs through Just Serp API for scraping, metadata extraction, and page structure analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs are sent to Just Serp API and may reveal browsing intent or sensitive internal locations. <br>
Mitigation: Use the skill only with public or authorized URLs, and avoid sensitive or internal links unless policy permits sharing them with the provider. <br>
Risk: Returned raw HTML can contain private data copied from the target page. <br>
Mitigation: Inspect returned HTML before logging, sharing, or storing it, and redact private data when necessary. <br>
Risk: The skill requires a Just Serp API key. <br>
Mitigation: Pass the key through JUST_SERP_API_KEY or the helper's API-key argument and do not paste key values into chat, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-web-html) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link) <br>
- [OpenAPI operation summary](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a target url query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
