## Description:

Twitter/X and meme evidence data via the 6551 API. Supports user profiles, tweet search, user tweets, follower events, deleted tweets, KOL followers, meme token evidence, and meme activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infra403](https://clawhub.ai/user/infra403)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to retrieve Twitter/X profiles, posts, follower activity, and meme-token evidence for research and monitoring workflows. It is suited to tasks that need data from the 6551 service and concise summaries of the returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add or remove Twitter monitoring entries, beyond data retrieval.

Mitigation: Before changing monitoring settings, confirm that the change is needed and check the target account and intended action.

Risk: The security scan had incomplete coverage because several local references could not be resolved.

Mitigation: Review the unresolved references and the skill behavior before relying on the scan result.

## Reference(s):

- [6551 API](https://ai.6551.io)
- [6551 API token setup](http://app.newsliquid.com/mcp)
- [ClawHub skill release](https://clawhub.ai/infra403/skills/opentwitter-mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Structured Twitter/X and meme activity data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected query and the data available from the service.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
