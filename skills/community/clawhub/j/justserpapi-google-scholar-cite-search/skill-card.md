## Description: <br>
Call GET /api/v1/google/scholar/cite/search for Google SERP Scholar Cite Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Google Scholar citation data, including export links, for a known Scholar result ID. It supports bibliography automation and citation workflows through the Just Serp API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Scholar citation lookup IDs and optional language settings are sent to Just Serp API. <br>
Mitigation: Use the skill only when that external API provider is approved for the citation lookup workflow and submitted identifiers are acceptable to share. <br>
Risk: The skill requires the JUST_SERP_API_KEY credential for authenticated API requests. <br>
Mitigation: Keep the API key out of chat messages, screenshots, logs, and committed files; pass it through the expected environment or command argument only when invoking the helper. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-scholar-cite-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; successful API calls return JSON citation data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a Google Scholar result ID supplied as the query parameter.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
