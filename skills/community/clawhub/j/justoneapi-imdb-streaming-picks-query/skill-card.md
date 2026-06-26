## Description: <br>
Call GET /api/imdb/streaming-picks-query/v1 for IMDb Streaming Picks through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve IMDb streaming-pick data through JustOneAPI for content discovery, watchlist research, and localized streaming recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent in the request URL and could be exposed through logs, shared command output, or copied URLs. <br>
Mitigation: Use a low-scope or revocable token where possible, avoid sharing request URLs or logs, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on live responses from an external JustOneAPI endpoint. <br>
Mitigation: Review returned data and backend error payloads before using results in user-facing recommendations or automated workflows. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with JSON response data and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the streamingPicksQuery operation and supports the optional languageCountry query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
