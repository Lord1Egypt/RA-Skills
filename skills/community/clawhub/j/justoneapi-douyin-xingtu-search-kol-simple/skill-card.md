## Description: <br>
Call GET /api/douyin-xingtu/search-kol-simple/v1 for Douyin Creator Marketplace (Xingtu) KOL Keyword Search through JustOneAPI with keyword, page, and platformSource. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search Douyin Creator Marketplace (Xingtu) KOL data through JustOneAPI for creator sourcing and shortlist building. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upstream API uses the JustOneAPI token in the URL query string, which can expose credentials through logs, command traces, screenshots, or error output. <br>
Mitigation: Pass the token through JUST_ONE_API_TOKEN or the helper's token argument, avoid sharing full request URLs or command output that may contain the token, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-search-kol-simple) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON API response when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and query parameters keyword, page, and platformSource.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
