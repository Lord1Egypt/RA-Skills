## Description: <br>
Call GET /api/imdb/title-user-reviews-summary-query/v1 for IMDb User Reviews Summary through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up IMDb title user review summaries from JustOneAPI by IMDb title ID, with optional language and country preferences. It supports audience sentiment analysis by returning aggregated review content and counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a query parameter and could be exposed through shared URLs, screenshots, or logs. <br>
Mitigation: Use a scoped or replaceable token when available, avoid sharing request URLs or logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_user_reviews_summary_query&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_user_reviews_summary_query&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-user-reviews-summary-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested or returned by the helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an IMDb title id and a JustOneAPI token; languageCountry defaults to en_US.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
