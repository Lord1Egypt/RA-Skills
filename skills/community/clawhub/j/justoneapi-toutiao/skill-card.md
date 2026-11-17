## Description:

Analyze Toutiao workflows with JustOneAPI, including article Details, user Profile, and app Keyword Search across 4 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Toutiao article details, user profiles, and keyword search results through authenticated JustOneAPI GET operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments or URL query strings.

Mitigation: Use a narrowly scoped or disposable token when available, avoid logging full commands or request URLs, and rotate the token if it may have appeared in process logs, shell history, or HTTP infrastructure logs.

Risk: The security verdict is suspicious because authenticated API requests depend on account-sensitive JustOneAPI credentials.

Mitigation: Review the skill before installation when the token has billing, quota, or account-sensitive access.

## Reference(s):

- [Toutiao API skill page](https://clawhub.ai/justoneapi/skills/justoneapi-toutiao)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and API-backed JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize decision-relevant response fields before raw JSON and should echo user-provided filters such as keyword, id, page, searchId, or userId.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
