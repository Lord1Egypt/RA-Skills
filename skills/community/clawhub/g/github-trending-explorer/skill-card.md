## Description:

Fetches global GitHub Trending weekly or monthly lists and produces a Markdown overview with a separate detail report for each repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review global GitHub Trending repositories for a week or month. It gathers repository details and creates Chinese Markdown reports for discovery and follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rerunning the skill can delete saved reports for the current period before replacement reports are ready, including after retrieval errors.

Mitigation: Back up the current period's reports before rerunning; retain existing reports until replacement reports have been saved successfully.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [GitStock GitHub Trending API](https://gitstock.org/api/v1/github/trending?period=weekly)
- [Repository detail report template](artifact/references/repo-output_template.md)
- [Overview report template](artifact/references/overview-output_template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown report files: one overview and one detail file per repository]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly or monthly, full-site Trending only; daily lists and language filters are not supported. Reports are archived by period.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
