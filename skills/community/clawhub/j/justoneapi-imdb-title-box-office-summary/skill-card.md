## Description:

Call GET /api/imdb/title-box-office-summary/v1 for IMDb Box Office Summary through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve IMDb title box-office summary data from JustOneAPI for revenue tracking and title comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token that may have billing impact, broad account access, or a long lifetime.

Mitigation: Use a narrowly scoped token when available, rotate it if exposed, and avoid sharing token values in chat, screenshots, or logs.

Risk: The token is passed through a command-line argument and sent to JustOneAPI in the request URL.

Mitigation: Run the skill only in trusted environments and avoid collecting command histories, process listings, or request URLs that may include credentials.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_box_office_summary&utm_content=project_link)
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_box_office_summary&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-box-office-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and an IMDb title id.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
