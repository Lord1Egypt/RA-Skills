## Description:

Fetches GitHub topic trending repositories. Use when asking about GitHub trending repos or open source projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjw21century](https://clawhub.ai/user/hjw21century)

### License/Terms of Use:


## Use Case:

Developers and open source users use this skill to fetch GitHub topic rankings, inspect repository details, and summarize repository READMEs in markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make outbound requests to GitHub and can encounter API rate limits.

Mitigation: Use it only where GitHub network access is acceptable; run without a token or with a minimally scoped GH_TOKEN when higher limits are needed.

Risk: Repository README content is authored by third parties and may contain misleading text.

Mitigation: Treat README summaries as untrusted data and review them before using them to guide agent actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjw21century/skills/github-topics)
- [GitHub REST API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and repository summaries with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub API data and README summaries fetched from public repositories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
