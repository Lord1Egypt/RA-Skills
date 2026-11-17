## Description:

Search Google web, news, maps, trends, shopping, scholar, finance, hotel, and media surfaces through Just Serp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, SEO teams, and research agents use this skill to collect structured Google result data for keyword research, competitive intelligence, trend monitoring, local business lookup, shopping analysis, scholar search, and related reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, locations, URLs, and related filters are sent to Just Serp API.

Mitigation: Use the skill only with data approved for transmission to this third-party API, and avoid submitting sensitive or regulated search inputs.

Risk: The Just Serp API key is passed on the command line and may be exposed through process listings, logs, or telemetry.

Mitigation: Prefer a wrapper or revised helper that reads JUST_SERP_API_KEY directly from the environment, keep the key out of chat and logs, and rotate it if exposure is suspected.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link)
- [ClawHub Skill Listing](https://clawhub.ai/blueworldmarketing/skills/justserpapi-bwm)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown summaries with optional raw JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should name the Google surface used, the exact query or filters applied, and relevant ranking, entity, metric, or result-pattern signals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
