## Description:

Searches GitHub for recently created repositories with more than 5,000 stars and reports the highest-starred candidate not already in local history, widening the search window when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to discover a recently created, highly starred GitHub repository and receive a concise summary of its purpose, problem, and approach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a saved GitHub token from ~/.openclaw/.env even when GITHUB_TOKEN is unset.

Mitigation: Remove that credential-file fallback or block the skill's access to the file before use. If authentication is needed, supply a token limited to public-repository reads.

Risk: The single 100-result search page can omit eligible repositories from consideration, especially when previously shown repositories occupy results.

Mitigation: Treat the report as discovery from the returned results; adjust the star threshold or date window when broader coverage is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengzuo613/skills/github-latest-hot-repo-explorer)
- [GitHub repository search API endpoint](https://api.github.com/search/repositories)
- [GitHub repository README API endpoint](https://api.github.com/repos/{owner}/{repo}/readme)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown repository summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports one eligible repository per run and saves successful reports and shown-repository history locally.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
