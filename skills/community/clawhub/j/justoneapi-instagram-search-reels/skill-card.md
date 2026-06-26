## Description: <br>
Call GET /api/instagram/search-reels/v1 for Instagram Reels Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search Instagram Reels through JustOneAPI by keyword or hashtag and summarize returned post, caption, and author-profile data for trend or niche research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JUST_ONE_API_TOKEN is sent to api.justoneapi.com as a URL query parameter. <br>
Mitigation: Treat the token as sensitive, avoid sharing full request URLs or command output, and rotate the token if exposure is suspected. <br>
Risk: Search keywords, hashtags, and pagination tokens are sent to JustOneAPI. <br>
Mitigation: Use this skill only when the user is comfortable sending those lookup values to JustOneAPI. <br>
Risk: Backend errors may include payload details from the API provider. <br>
Mitigation: Review error output before sharing it and remove tokens, full URLs, or sensitive search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-instagram-search-reels) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; sends keyword and optional paginationToken as query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
