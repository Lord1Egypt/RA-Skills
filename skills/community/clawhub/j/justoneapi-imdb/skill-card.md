## Description:

Analyze IMDb workflows with JustOneAPI, including release expectation, extended details, top cast and crew, and base title information across 19 API-backed operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve IMDb-backed title, person, news, ranking, cast, review, and release information through JustOneAPI when the user can provide the required title ID, search term, category, or ranking filter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments, process telemetry, command history, or URL logs.

Mitigation: Use a dedicated low-privilege token where available, avoid sharing run logs or process listings, monitor token usage, and rotate the token if exposure is suspected.

Risk: Authenticated API calls can affect billing, quota, or account usage.

Mitigation: Review the token's account impact before installing and monitor usage after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown answer with selected API result fields and optional formatted JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and operation-specific parameters before making GET requests.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
