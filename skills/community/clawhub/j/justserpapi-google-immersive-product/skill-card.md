## Description:

Call GET /api/v1/google/immersive/product for Google SERP Immersive Product through Just Serp API with page_token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's Google immersive product endpoint and retrieve product features, specifications, and seller information for product research and merchandising analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends page_token query parameters and the Just Serp API key to api.justserpapi.com.

Mitigation: Install and run it only for intended Just Serp API usage, and avoid submitting sensitive or unrelated tokens.

Risk: The helper accepts the API key through a --api-key command-line argument.

Mitigation: Pass the key from a protected environment variable, avoid exposing command lines in logs or screenshots, and prefer a release that reads secrets directly from a protected channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-immersive-product)
- [Publisher profile](https://clawhub.ai/user/justserpapi)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link)
- [Just Serp API base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Just Serp API key and a page_token query parameter.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
