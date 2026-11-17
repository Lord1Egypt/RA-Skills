## Description:

Kaspa News lets an agent query public kaspa.news data for latest Kaspa news, core development updates, ecosystem launches, community discussion, videos, Reddit posts, and weekly pulse reports without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atl4so](https://clawhub.ai/user/atl4so)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch and present current Kaspa ecosystem updates from kaspa.news, including tweets, developer posts, videos, Reddit posts, and pulse reports. It is useful for concise news briefings and targeted social update retrieval about Kaspa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public network requests to kaspa.news and may present cached social or news content.

Mitigation: Use it when current Kaspa data from kaspa.news is desired, and review source links before relying on time-sensitive or market-relevant claims.

Risk: Broad trigger guidance could activate the skill for ambiguous mentions of kaspa.news or Kaspa updates.

Mitigation: Use explicit requests when you want the agent to fetch Kaspa news, and avoid ambiguous phrasing when retrieval is not intended.

## Reference(s):

- [Kaspa News Skill on ClawHub](https://clawhub.ai/atl4so/skills/kaspa-news)
- [kaspa.news public API](https://kaspa.news/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Plain text or Markdown, with optional JSON from script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, jq, Python requests, and internet access to kaspa.news public endpoints; no API keys or tokens are required.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
