## Description:

Call GET /api/v1/google/scholar/author for Google SERP Scholar Author through Just Serp API with author_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Google Scholar author profile data, publications, citation metrics, and research interests from the Just Serp API when given a Google Scholar author_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Scholar author IDs and query parameters are sent to the Just Serp API service.

Mitigation: Confirm the user trusts Just Serp API for the submitted lookup data before calling the endpoint.

Risk: The Just Serp API key could be exposed if pasted into chat, screenshots, or logs.

Mitigation: Keep JUST_SERP_API_KEY in the environment and pass it through the helper argument rather than sharing the key value.

## Reference(s):

- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link)
- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-scholar-author)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary followed by raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and author_id; optional query parameters include citation_id, language, results, sort, and view_op.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
