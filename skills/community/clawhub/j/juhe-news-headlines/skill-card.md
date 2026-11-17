## Description:

Queries Juhe news headlines and story details by category using the Juhe News Headlines API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve categorized news headline lists or article details from Juhe for user-facing news queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose the Juhe API key and returned news data because the authoritative security summary says requests use unencrypted HTTP and weaker key-handling options are documented.

Mitigation: Prefer JUHE_NEWS_KEY over command-line keys, do not commit scripts/.env, and update the endpoints to HTTPS if Juhe supports it before real use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-news-headlines)
- [Juhe News Headlines API documentation](https://www.juhe.cn/docs/api/id/235)
- [Juhe data platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, formatted text summaries, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_NEWS_KEY API key.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
