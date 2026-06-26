## Description: <br>
Calls the JustOneAPI Douban movie comments endpoint with a subject ID to retrieve ratings, snippets, and interaction counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Douban movie comment data from JustOneAPI for sentiment sampling, review monitoring, and lightweight analysis by subject ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends it as a query parameter, which may be captured by server logs, proxies, or debugging output. <br>
Mitigation: Use a scoped or easily rotated token, avoid sharing token values in chat or logs, and rotate the token if exposure is suspected. <br>
Risk: Using the skill sends requests and the provided token to JustOneAPI. <br>
Mitigation: Install and run the skill only if you trust JustOneAPI and the publisher account that released it. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douban-get-movie-comments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with a shell command example and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a subjectId; optional sort and page parameters refine the API request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
