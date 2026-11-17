## Description:

Call GET /api/v1/google/patents/details for Google SERP Patents Details through Just Serp API with patent_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's Google patent details endpoint for patent abstracts, claims, and legal status using a Google Patent ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing the Just Serp API key as a command-line argument can expose the secret locally.

Mitigation: Run only in environments where command lines are not captured in logs or visible to other local users, and prefer a helper version that reads JUST_SERP_API_KEY directly from the environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-patents-details)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link)
- [Just Serp API Base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with optional raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a patent_id parameter.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
