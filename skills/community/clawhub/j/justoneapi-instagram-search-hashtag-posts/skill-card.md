## Description: <br>
Call GET /api/instagram/search-hashtag-posts/v1 for Instagram Hashtag Posts Search through JustOneAPI with hashtag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query JustOneAPI for public Instagram hashtag posts, then summarize captions, author profiles, publish times, and pagination results for hashtag monitoring or competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends the token with API requests. <br>
Mitigation: Use a limited-scope token where available, keep token values out of chat, logs, screenshots, and shared URLs, and rotate the token if exposed. <br>
Risk: Hashtag searches and returned public Instagram content may reveal sensitive research interests or monitoring targets. <br>
Mitigation: Use the skill only for lawful, user-directed public-content research and avoid sharing command output when it exposes sensitive queries or results. <br>
Risk: API results depend on JustOneAPI availability, authorization, and Instagram data returned by the backend. <br>
Mitigation: Check backend error payloads and operation IDs before acting on results, and verify important findings against an authoritative source when used for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-instagram-search-hashtag-posts) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_hashtag_posts&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON results or JSON error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, JUST_ONE_API_TOKEN, a hashtag query, and optional endCursor pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
