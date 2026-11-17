## Description:

Call GET /api/v1/google/images/search for Google SERP Images Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API for Google Images search results, including image URLs and metadata for filtered image discovery, research, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented runner passes the Just Serp API key on the command line, which can expose the credential through local process listings or command logging.

Mitigation: Use a restricted API key where possible, avoid running the command in shared or heavily monitored environments, and rotate the key if exposure is suspected.

Risk: The API can return raw HTML when requested, and that content may be untrusted.

Mitigation: Treat returned HTML as untrusted content and sanitize or avoid rendering it directly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-images-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_images_search&utm_content=project_link)
- [OpenAPI Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summary with optional raw JSON and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Just Serp API key in JUST_SERP_API_KEY and a query parameter for imagesSearch.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
