## Description:

Call GET /api/v1/google/autocomplete for Google SERP Autocomplete through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to request Google autocomplete suggestions through Just Serp API for keyword expansion, search intent research, and localized query discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Just Serp API key can be exposed through process command lines when passed with --api-key.

Mitigation: Use the skill only in environments where process arguments are not logged or visible to untrusted users; prefer a release that reads JUST_SERP_API_KEY directly from the environment and rotate keys after exposure.

Risk: Requests consume Just Serp API credits or quota.

Mitigation: Confirm query, country, and language parameters before execution and monitor API usage for billing or quota impact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-autocomplete)
- [Just Serp API Publisher Profile](https://clawhub.ai/user/justserpapi)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Short Markdown summary followed by raw JSON from the Just Serp API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the autocomplete operation with required query and optional country and language parameters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
