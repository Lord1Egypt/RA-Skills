## Description: <br>
Call GET /api/douban/get-movie-reviews/v1 for Douban Movie Movie Reviews through JustOneAPI with subjectId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fetch Douban Movie review data for a specific subjectId through JustOneAPI. It supports review research and audience sentiment analysis by returning review titles, ratings, snippets, and related API output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A JustOneAPI token is required and may be exposed through command-line arguments, request URLs, logs, or shared systems. <br>
Mitigation: Use a limited or revocable token, avoid running the CLI where commands or URLs are logged, and rotate the token if exposure is suspected. <br>
Risk: The skill sends the token and requested Douban subject parameters to api.justoneapi.com. <br>
Mitigation: Use the skill only when the user is comfortable sending those credentials and request parameters to JustOneAPI. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douban-get-movie-reviews) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link) <br>
- [Douban Movie Movie Reviews Operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Douban subjectId; optional page and sort query parameters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
