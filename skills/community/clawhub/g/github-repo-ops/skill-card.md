## Description:

GitHub repository operations and analysis. Use when working with GitHub repos: analyzing code, checking issues, reviewing PRs, tracking stars/releases, searching for repositories, or understanding repo structure. Provides structured access to GitHub API data without needing a GitHub token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blalf](https://clawhub.ai/user/blalf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze public GitHub repositories, triage issues, compare repositories, and search public code or repositories using GitHub API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is limited to public GitHub data and may make network requests to GitHub's public API.

Mitigation: Use it for public repositories only, review generated guidance before acting on it, and do not expect private repository access or account-changing actions.

Risk: Public GitHub API access can be rate limited, especially without authentication.

Mitigation: Plan analyses around public API rate limits and rerun requests later if GitHub throttles access.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown or structured text with GitHub API endpoint guidance and repository analysis templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public GitHub data only; unauthenticated API rate limits and public repository scope apply.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
