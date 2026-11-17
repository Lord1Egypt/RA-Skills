## Description:

Provides Chinese and English GitHub Trending-style repository lists, language filters, and open-source update summaries, with static sample trend data in this release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers and open-source observers use this skill to ask an agent for GitHub Trending-style project lists by timeframe or programming language. The current release should be treated as sample trend output unless the publisher updates it to fetch live GitHub data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat static sample repository rankings and star counts as current GitHub Trending results.

Mitigation: Label outputs as sample data and verify trends against live GitHub Trending or GitHub API data before using them for decisions.

Risk: The skill description implies live trend monitoring while the release evidence says the current output is locally contained sample data.

Mitigation: Review the skill before installation and require a publisher update or clear demo/mock labeling before presenting the output as live data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/github-trending-cn)
- [Publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [Markdown-style trend list or JSON object containing repository entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language and result-limit filtering in the bundled script; values are static sample data in this release.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
