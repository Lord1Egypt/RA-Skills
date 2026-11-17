## Description:

Industry Compare helps agents compare multiple companies in the same industry, assess industry position, analyze competitive advantages, and generate informational investment suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance-oriented agents use this skill to compare peer companies, evaluate industry rankings, summarize competitive advantages, and prepare informational market-analysis output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment suggestions, rankings, or comparison metrics may be incomplete, stale, or unsuitable for a user's specific financial situation.

Mitigation: Treat outputs as informational only and verify market data, assumptions, and conclusions independently before making decisions.

Risk: The optional TUSHARE_TOKEN environment variable is a credential that may expose access to a third-party data service if mishandled.

Mitigation: Provide a Tushare token only when the intended skill behavior requires it and store, scope, and rotate the token according to local credential-management practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsoforever/skills/industry-compare)
- [Project homepage](https://aigogoai.com)
- [Industry analysis framework](https://aigogoai.com/knowledge/industry-analysis)
- [Porter's Five Forces model](https://aigogoai.com/knowledge/porter-five-forces)
- [Competitive advantage analysis](https://aigogoai.com/knowledge/competitive-advantage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus terminal text output from the comparison script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language finance comparison output; examples include industry rankings, valuation metrics, profitability metrics, growth metrics, and competitive advantage summaries.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
