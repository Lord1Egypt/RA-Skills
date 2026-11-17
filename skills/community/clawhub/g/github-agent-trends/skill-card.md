## Description:

Generate formatted markdown or JSON leaderboards of agent-related GitHub repositories filtered by daily, weekly, or monthly activity and sorted by stars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for current GitHub leaderboards of agent-related open-source projects, with optional period, limit, token, and JSON output controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script contacts GitHub and may use a GITHUB_TOKEN environment value or --token argument.

Mitigation: Use a fine-grained, minimal GitHub token only when higher rate limits are needed, or run unauthenticated.

Risk: Results are based on GitHub Search API relevance and stars, not the official GitHub Trending page.

Mitigation: Present the output as a search-based leaderboard and review the generated repository list before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike47512/skills/github-agent-trends)
- [GitHub Search repositories API endpoint](https://api.github.com/search/repositories)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown leaderboard by default, or JSON array when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, or monthly periods, configurable result limits, and optional GitHub token use; default markdown output includes Chinese labels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
