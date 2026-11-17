## Description:

Automatically search for low-competition GitHub bounty tasks with fewer than five comments and generate a report with details and estimated difficulty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bounty hunters use this skill to find less-crowded open GitHub issues labeled as bounties, sorted by comment count with basic difficulty estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running through an unpinned npx command can execute a package version that has not been reviewed.

Mitigation: Use a pinned package version or a reviewed local install path before running the tool.

Risk: The skill contacts GitHub's API and prints public issue results, so usage may be affected by network access and GitHub API rate limits.

Mitigation: Run it in an environment approved for external GitHub API calls and use authentication only when higher rate limits are needed.

Risk: Difficulty labels are heuristic estimates based on issue title keywords.

Mitigation: Review the linked issue details before selecting or prioritizing a bounty task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/santosparra651-arch/skills/github-bounty-hunter-v2)
- [GitHub Search API endpoint](https://api.github.com/search/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-text CLI report with issue titles, URLs, comment counts, and difficulty labels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default maximum comment count is five and can be changed with one CLI argument.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
