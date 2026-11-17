## Description:

Call GET /api/v1/google/scholar/cite/search for Google SERP Scholar Cite Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Google Scholar citation data and export links from Just Serp API for bibliography automation and citation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill passes the Just Serp API key through command-line arguments, where it may be exposed in local process listings or automation logs.

Mitigation: Use a version that reads JUST_SERP_API_KEY directly from the environment, avoid logging command lines, and rotate the key if exposure is suspected.

Risk: The skill sends lookup parameters to the Just Serp API service.

Mitigation: Review query values before execution and avoid sending sensitive or confidential citation lookup data.

## Reference(s):

- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link)
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_cite_search&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-scholar-cite-search)
- [Publisher profile](https://clawhub.ai/user/justserpapi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with raw JSON results when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and the query parameter for ScholarCiteSearch.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
