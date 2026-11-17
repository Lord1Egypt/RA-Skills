## Description:

Retrieves public Xiaohongshu/Rednote search results, note details, comments, and creator post lists as structured data for content research and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content operators, analysts, and developers use this skill to retrieve public Xiaohongshu/Rednote search, note, comment, and creator-post data for content planning, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Guaikei API token and query targets.

Mitigation: Install only if you trust Guaikei with those values, keep the token out of shared logs, and rotate the token if it is exposed.

Risk: Scraped results and execution logs may contain sensitive local research data.

Mitigation: Treat generated logs as sensitive, control workspace file permissions, and delete retained logs that are no longer needed.

Risk: The skill is intended for public Xiaohongshu/Rednote data and does not establish authorization for broader data use.

Mitigation: Use it only for public data within the user's authorization scope and avoid redistributing collected data in ways that violate applicable rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-scraper)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON and may write JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; results are limited to public Xiaohongshu/Rednote data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter, package.json, and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
