## Description:

Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanjolnoring](https://clawhub.ai/user/nanjolnoring)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch current news from multiple public sources, filter by source or keyword, and produce concise Simplified Chinese news briefings with deeper analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package references executable and template files that are missing from the artifact.

Mitigation: Review the package before deployment and require the referenced script and template to be included before relying on the skill.

Risk: The skill may fetch article content from external sources for broad news requests.

Mitigation: Use it only in environments where outbound news retrieval is acceptable and review generated reports for source quality and accuracy.

Risk: The skill directs the agent to save full reports to disk without a clear opt-out.

Mitigation: Confirm the report storage location and provide user control over whether reports are saved.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nanjolnoring/skills/news-aggregator-skill-4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report presented in chat and saved as a timestamped Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are intended to be written under a reports/ directory; fetched items may include extracted article content when deep fetching is used.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
