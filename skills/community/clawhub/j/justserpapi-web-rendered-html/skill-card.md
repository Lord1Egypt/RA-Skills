## Description: <br>
Call GET /api/v1/web/rendered-html for Web Crawling Rendered Html through Just Serp API with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request rendered HTML for a supplied webpage URL through the Just Serp API for scraping, metadata extraction, and page structure analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends target URLs to an external Just Serp API service and may return raw rendered HTML into the agent output. <br>
Mitigation: Use only authorized public or non-sensitive URLs, avoid authenticated pages, internal services, confidential documents, and URLs containing tokens, and review returned HTML before sharing or relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-web-rendered-html) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_rendered_html&utm_content=project_link) <br>
- [Just Serp API docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_rendered_html&utm_content=project_link) <br>
- [Operations reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a URL query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
