## Description:

Discovers fast-growing GitHub repositories before they appear on the official Trending page by querying GitHub Search and ranking repositories by stars per day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humor200](https://clawhub.ai/user/humor200)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical researchers use this skill to find newly created or recently active GitHub repositories that are gaining stars quickly, then review the ranked results for emerging projects worth investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes unauthenticated requests to GitHub and can be constrained by public API rate limits.

Mitigation: Expect limited request volume by default and avoid adding a personal GitHub token unless its storage and transmission are understood.

Risk: Repository stars can be artificially inflated, and repositories with sparse metadata may be spam or mirrors.

Mitigation: Review high-ranked repositories manually and cross-check promising results with additional public signals before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/humor200/skills/github-rising-stars)
- [GitHub repository search API endpoint](https://api.github.com/search/repositories)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown table or JSON array of ranked public GitHub repositories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include repository rank, stars-per-day rate, star count, age, language, repository name, URL, description, and topics when JSON output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
