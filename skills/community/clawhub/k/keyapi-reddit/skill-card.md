## Description:

Analyze Reddit posts, comments, users, subreddits, feeds, rules, settings, and search signals through live KeyAPI REST workflows guided by official KeyAPI docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn natural-language Reddit research requests into docs-verified KeyAPI workflows for retrieving, comparing, and reporting on Reddit posts, comments, users, subreddits, feeds, and search trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses KeyAPI for live Reddit requests and requires a bearer token that may be stored in a local shell profile.

Mitigation: Use a session-only KEYAPI_TOKEN or a dedicated secret manager when possible, avoid passing real tokens on the command line, and review shell-profile setup before installing.

Risk: Live API workflows can send request bodies or selected local file contents to KeyAPI.

Mitigation: Review request bodies and local files before execution, and limit request scope to the user's approved Reddit analysis task.

## Reference(s):

- [KeyAPI Docs Index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Reddit Docs](https://docs.keyapi.ai/en/reddit/)
- [KeyAPI Authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [ClawHub Skill Page](https://clawhub.ai/xyzzero/skills/keyapi-reddit)
- [Global Rules](references/global-rules.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Reddit Rules](references/reddit-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with command examples, API result summaries, JSON previews, and optional saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live Reddit requests require a KeyAPI bearer token; large responses may be summarized unless saved to an output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
