## Description: <br>
Call GET /api/douban/get-movie-review-detail/v1 for Douban Movie Review Details through JustOneAPI with reviewId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch detailed Douban movie review data by reviewId through JustOneAPI, including review metadata, content fields, and engagement signals for archiving or detailed opinion analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and may appear in URLs, logs, shell history, screenshots, proxies, or error reports. <br>
Mitigation: Use a limited-scope token when available, avoid sharing request URLs or command output, and rotate the token if exposure is suspected. <br>
Risk: The skill sends requests to a third-party API service operated by JustOneAPI. <br>
Mitigation: Install and run it only when you trust JustOneAPI with the API token and the requested Douban review lookup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douban-get-movie-review-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_review_detail&utm_content=project_link) <br>
- [Douban Movie Review Details operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when results are returned] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a JUST_ONE_API_TOKEN; the non-token lookup parameter is reviewId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
