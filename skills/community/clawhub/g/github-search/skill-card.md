## Description:

Searches and analyzes GitHub repositories with filters for keywords, language, stars, forks, and update date to support technical research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshengli](https://clawhub.ai/user/linshengli)

### License/Terms of Use:


## Use Case:

Developers and technical researchers use this skill to find, filter, and compare open source GitHub repositories in a technology area and produce report-ready summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted search terms, repository names, sort values, or order values may trigger shell command execution in the bundled GitHub API scripts.

Mitigation: Use only trusted inputs until the scripts replace shell-based curl execution with structured HTTP requests and strict allowlists.

Risk: An inherited GITHUB_TOKEN may be exposed if command injection is triggered.

Mitigation: Avoid setting GITHUB_TOKEN for this skill unless needed, and use a least-privilege token when authenticated GitHub API access is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshengli/skills/github-search)
- [GitHub Search API endpoint](https://api.github.com/search/repositories)
- [GitHub REST repositories endpoint](https://api.github.com/repos)

## Skill Output:

**Output Type(s):** [Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown tables, JSON, or CSV repository reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include repository statistics, language summaries, activity indicators, and links to GitHub repositories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
