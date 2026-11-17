## Description:

Search Google web, news, maps, trends, shopping, scholar, finance, hotel, and media surfaces through Just Serp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to collect structured Google result data for web, news, maps, trends, shopping, scholar, finance, hotel, image, video, and related search workflows through Just Serp API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is passed through a command-line argument and may be captured by process listings, shell history, logs, or monitoring.

Mitigation: Prefer a version that reads JUST_SERP_API_KEY directly from the environment, avoid logging invocation commands, and rotate the key if exposure is possible.

Risk: Search terms, localization filters, public image URLs, and related identifiers are sent to Just Serp API.

Mitigation: Use only data appropriate for a third-party API, avoid precise location fields and private or signed URLs unless necessary, and minimize submitted parameters.

Risk: The security verdict requires review before installation.

Mitigation: Review the skill and scanner summary before deployment, then decide whether the third-party API and credential handling are acceptable for the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill selects from read-only GET operations and requires JUST_SERP_API_KEY for authenticated Just Serp API requests.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
