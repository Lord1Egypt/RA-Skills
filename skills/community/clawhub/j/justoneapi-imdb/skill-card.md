## Description: <br>
Analyze IMDb workflows with JustOneAPI, including release Expectation, extended Details, and top Cast and Crew across 19 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query JustOneAPI IMDb endpoints for title details, release expectations, cast and crew, search, news, and related entertainment research. It is best when the user can provide an IMDb ID, search term, category, or language/country filter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IMDb lookup terms, IMDb IDs, filters, and the JustOneAPI token are sent to JustOneAPI, with the token included in the request URL. <br>
Mitigation: Use a revocable or low-scope token, avoid sensitive lookup terms where possible, and keep tokens out of chat messages, screenshots, and logs. <br>
Risk: API error responses may include backend payloads tied to the selected operation and request parameters. <br>
Mitigation: Review error payloads before sharing them outside the operating environment, especially when requests include private titles, filters, or credentials. <br>


## Reference(s): <br>
- [JustOneAPI IMDb API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link) <br>
- [ClawHub skill listing](https://clawhub.ai/justoneapi/justoneapi-imdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown answer with optional JSON payloads and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation IDs and JSON parameter objects; requires JUST_ONE_API_TOKEN for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
