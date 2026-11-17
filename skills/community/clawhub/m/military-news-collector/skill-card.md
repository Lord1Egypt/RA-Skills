## Description:

Collects global military news, ranks items by importance, and produces Chinese summaries with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgywayy](https://clawhub.ai/user/zgywayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can use this skill to ask an agent for current military-news roundups across conflicts, weapons systems, exercises, defense policy, geopolitics, and war updates. The skill guides the agent to cross-check public sources and return an importance-ranked Chinese summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Military news and conflict reporting can include incomplete, rapidly changing, or propaganda-influenced claims.

Mitigation: Use the skill's cross-verification guidance, prefer authoritative public sources, keep source links visible, and distinguish factual reporting from analysis.

Risk: Current-events collection requires repeated public web searches and page fetches.

Mitigation: Run it only in environments where public web access is acceptable and avoid providing local data or credentials.

## Reference(s):

- [Recommended Military News Sources](artifact/references/sources.md)
- [ClawHub skill release page](https://clawhub.ai/zgywayy/skills/military-news-collector)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown news roundup with ranked items, source links, star ratings, and search coverage statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 15-25 deduplicated news items sorted by assessed importance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
