## Description:

Fetches GitHub Trending repositories and returns Chinese daily or monthly Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxiaodong681-lab](https://clawhub.ai/user/lxiaodong681-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent for current GitHub Trending repository summaries by day or month, optionally filtered by programming language and result limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to GitHub Trending.

Mitigation: Review the network behavior before installation and run it only where outbound access to GitHub is acceptable.

Risk: The skill creates or overwrites local cache JSON files for daily and monthly results.

Mitigation: Install it in a workspace where those cache files are expected, and review cache contents if local persistence is a concern.

Risk: Generated summaries are Chinese by design.

Mitigation: Use this skill where Chinese Markdown output is desired or adapt the output formatting before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxiaodong681-lab/skills/github-trending-skill)
- [Project homepage](https://github.com/lxiaodong681-lab/github-trending-skill)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Chinese Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily or monthly summaries include repository name, description, language, total stars, and daily or monthly star growth.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
