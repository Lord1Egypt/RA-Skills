## Description:

Fetch top trending GitHub repositories today/this-week/this-month and summarize top 15 with stars, language, description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch and summarize recently created GitHub repositories ranked by stars, including language, star and fork counts, descriptions, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional GitHub token handling is unsafe enough to require review or patching before use.

Mitigation: Use unauthenticated mode, or patch the script to pass curl headers with an argument-safe Bash array and use only a short-lived, minimally scoped GitHub token.

## Reference(s):

- [GitHub Search Repositories API](https://api.github.com/search/repositories)
- [ClawHub skill page](https://clawhub.ai/brunovu20/skills/github-treding)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with repository summaries and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; optional GH_TOKEN increases GitHub API rate limits after token handling is patched.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
