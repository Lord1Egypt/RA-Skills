## Description: <br>
Call GET /api/v1/google/finance/search for Google SERP Finance Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Just Serp API's Google Finance search endpoint for market summaries, company details, and related finance results from a required query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key and sends finance search queries to a third-party API. <br>
Mitigation: Install only when the publisher is trusted, provide the key through JUST_SERP_API_KEY, and avoid sharing key values in chat, screenshots, or logs. <br>
Risk: Returned finance data is third-party search/API output and may be incomplete, stale, or unsuitable for trading decisions. <br>
Mitigation: Treat results as informational search output and verify important finance information against authoritative sources before acting on it. <br>
Risk: The optional html parameter can include raw HTML from search results. <br>
Mitigation: Leave raw HTML disabled unless it is needed for the task and handle any returned HTML as untrusted content. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-finance-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; the html parameter can request raw HTML in addition to structured data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
