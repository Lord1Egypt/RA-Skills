## Description:

Searches public Douyin videos, image posts, users, creator posts, comments, and hot rankings to support content research, competitor analysis, opinion review, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content strategists, analysts, and developers use this skill to collect public Douyin search results, creator posts, comments, and hot rankings for topic selection, competitor monitoring, opinion analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may cause Douyin public-data collection when user intent is ambiguous.

Mitigation: Invoke the skill only after confirming Douyin-related research intent, target scope, and result limits.

Risk: GUAIKEI_API_TOKEN is sensitive, and the implementation sends it in query strings while some token-error paths can display acquisition or contact guidance.

Mitigation: Use dedicated low-privilege tokens, avoid shared logs or terminals, inspect runtime output before trusted deployment, and remove contact or marketing text from authentication failures.

Risk: Result files are automatically retained under logs/ and may include public profile, post, comment, engagement, and location-label fields.

Mitigation: Store logs in a controlled workspace, delete them when analysis is complete, and avoid collecting or redistributing data beyond the permitted internal research use.

Risk: The skill depends on public Douyin data and an external Guaikei API, so availability, result completeness, and permitted use can vary.

Mitigation: Treat outputs as research signals, validate important findings against source pages, and ensure collection complies with applicable platform terms and laws.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trend-radar)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search input schema](assets/search_cli_req.schema.json)
- [Search output schema](assets/search_cli_resp.schema.json)
- [Post input schema](assets/post_cli_req.schema.json)
- [Post output schema](assets/post_cli_resp.schema.json)
- [Comment input schema](assets/comment_cli_req.schema.json)
- [Comment output schema](assets/comment_cli_resp.schema.json)
- [Hot ranking output schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance, files]

**Output Format:** [JSON stdout with saved JSON log files and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and GUAIKEI_API_TOKEN; public Douyin collection is capped at 10000 results per request.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, changelog, constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
