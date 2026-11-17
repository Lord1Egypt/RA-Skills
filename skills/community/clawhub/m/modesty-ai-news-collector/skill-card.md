## Description:

Collects AI news from newsletters, communities, product announcements, research, funding, open-source, and policy sources, then ranks items by observed heat and returns Chinese summaries with original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for recent AI news, product launches, research updates, funding events, open-source project momentum, and policy developments. It is designed for Chinese-language briefings sorted by heat with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on live public web search and source fetching, so results can be incomplete, stale, paywalled, or skewed by search ranking.

Mitigation: Review cited source links, confirm high-impact claims against primary or multiple reputable sources, and note inaccessible paid sources explicitly.

Risk: The workflow targets Chinese summaries by default, which may not match every user's expected output language.

Mitigation: Ask the agent for another output language when needed and verify translated summaries against the original sources.

Risk: The artifact links to an external setup guide outside ClawHub.

Mitigation: Review the external setup-guide page before following any installation or configuration steps.

## Reference(s):

- [Recommended AI News Sources](references/sources.md)
- [Complete setup guide](https://skillboss.co/skill.md)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-ai-news-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news briefing in Chinese with ranked sections and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected to include 15-25 news items, search-count metadata, covered search dimensions, and update time when sufficient evidence is gathered.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
