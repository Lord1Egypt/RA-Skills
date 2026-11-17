## Description:

Analyze Douban Movie workflows with JustOneAPI, including movie Reviews, review Details, and subject Details across 6 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Douban movie and TV subject details, reviews, comments, and recent hot title data through JustOneAPI for research, catalog enrichment, and sentiment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is supplied through command-line arguments and added to API URL query parameters, which can expose it through shell history, process listings, logs, or captured request URLs.

Mitigation: Use a narrowly scoped token when available, avoid recording full commands or request URLs, keep logs private, and rotate the token if exposure is suspected.

Risk: Douban subject IDs, review IDs, and query filters are sent to api.justoneapi.com with each request.

Mitigation: Use the skill only when sending those identifiers to JustOneAPI is acceptable for the task and data-handling environment.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douban)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answer with optional JSON API payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and Douban subject or review identifiers for most operations.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
