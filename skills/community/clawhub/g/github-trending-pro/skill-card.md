## Description:

Fetches live GitHub Trending repositories and helps agents produce concise trend reports by language, date range, and spoken-language filter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei1125](https://clawhub.ai/user/liuwei1125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to retrieve current GitHub Trending repositories and turn the results into a scannable intelligence report with grounded project facts and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script that fetches public GitHub Trending pages.

Mitigation: Use it in environments where outbound access to GitHub Trending is acceptable and review the script before deployment.

Risk: Repository names and descriptions come from public GitHub content and may be inaccurate, promotional, or untrusted.

Mitigation: Treat fetched repository metadata as untrusted input and verify important claims before relying on or republishing them.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [ClawHub Skill Page](https://clawhub.ai/liuwei1125/skills/github-trending-pro)
- [Publisher Profile](https://clawhub.ai/user/liuwei1125)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or JSON from the GitHub Trending fetch script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, and monthly ranges, optional programming-language filters, optional spoken-language filters, and a default limit of 10 repositories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
