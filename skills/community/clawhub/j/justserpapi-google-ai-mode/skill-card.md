## Description:

Call GET /api/v1/google/ai-mode for Google SERP Ai Mode through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call Just Serp API's Google AI Mode endpoint for a supplied search query and summarize generated answers, follow-up prompts, and cited links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys passed as command-line arguments can be exposed locally through shell history, process listings, or logs.

Mitigation: Prefer a version that reads JUST_SERP_API_KEY directly from the environment, and avoid pasting credential values into chat, screenshots, or logs.

Risk: Search queries and optional location fields are sent to Just Serp API.

Mitigation: Avoid sensitive queries or location values unless sharing them with the third-party API provider is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-ai-mode)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link)
- [Generated Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a Node.js runtime.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
