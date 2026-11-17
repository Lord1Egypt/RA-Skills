## Description:

Direct MyAnimeList lookup tool. Bypasses Jikan/API issues by using MAL's internal endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zun43d](https://clawhub.ai/user/zun43d)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to look up anime, manga, seasonal charts, top airing anime, and public MyAnimeList user lists from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query MyAnimeList internal endpoints rather than an official API, so lookup behavior can change if MyAnimeList changes those endpoints.

Mitigation: Review generated commands before execution and verify important results against MyAnimeList when endpoint behavior changes.

Risk: The skill performs disclosed network lookups to retrieve anime, manga, chart, and user-list data.

Mitigation: Use it only where outbound requests to MyAnimeList are acceptable under the deployment environment's network and data policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zun43d/skills/mal-lookup)
- [Publisher profile](https://clawhub.ai/user/zun43d)
- [MyAnimeList](https://myanimelist.net/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, grep, and awk; performs network lookups against MyAnimeList endpoints.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
