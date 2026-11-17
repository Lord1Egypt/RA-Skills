## Description:

GitHub market recon when the user asks for AI money trends, hot niches, competitor signals, or "找风口/赚钱方向调研", especially when sources are restricted to GitHub only or a previous research run was interrupted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianxing475](https://clawhub.ai/user/xianxing475)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce GitHub-only market reconnaissance reports on AI monetization trends, hot niches, competitor signals, and opportunity areas. It is useful when the user needs claims tied to GitHub or GitHub API evidence rather than general web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes GitHub and GitHub API requests, which can encounter rate limits or incomplete fetches.

Mitigation: Keep sources scoped to GitHub, use capped batches, switch to GitHub HTML search on rate-limit signals, and disclose throttling or missing data in the report.

Risk: Large reconnaissance jobs may use scoped subagents to parallelize research.

Mitigation: Embed the same GitHub-only constraints in subagent tasks, avoid file access for subagents, and review output for recovered or lost data after interruptions.

Risk: GitHub popularity signals can be mistaken for proof of revenue.

Mitigation: Frame stars, velocity, and repository activity as demand signals only, and include the caveat that GitHub heat does not prove revenue.

## Reference(s):

- [Proven URL Sets for GitHub Recon](references/url-sets.md)
- [ClawHub Skill Page](https://clawhub.ai/xianxing475/skills/market-recon)
- [Third-Party Publisher Profile](https://clawhub.ai/user/xianxing475)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evidence-linked trend report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cite fetched GitHub or GitHub API sources, disclose rate-limit or interruption recovery events, and avoid writing user files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
